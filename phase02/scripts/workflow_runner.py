#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workflow_runner.py — Phase 02 原生组件：部署 + 触发 + 采集（确定性、可复用）

实现 `phase02/scripts/workflow-runner.md` 规格。**只负责把 workflow 部署到测试仓、
触发、等待、采集证据**——不判 pass/fail（那是 assertion_engine 的职责，rules.md §1）。

设计立场（炼钢：吸收 execute_serial/logassert/masking 的实战经验，弃用一次性脚本）：
  1. 按 (head_sha AND file_path) **精确匹配 run**。共享仓一次 push 会触发所有
     `on:push` 的 workflow → 同 SHA 多个 run；只按 head_sha 会抓到别人的 run
     （run 03 的假红教训）。必须再按"我这次推的文件名"过滤。
  2. 日志正文走 v8 `download_log`(下划线，跟随 302 → zip)，仅需 OAuth token，
     封装在 log_fetcher.py。（早期误判 `download-log` 连字符"平台缺陷"是端点名错，已更正。）
  3. 只产出"执行层"结果。判定词以 `phase02/rules.md` §11 为准，本组件只输出：
     采集成功 → RunResult(status=平台终态)；触发无 run → NO_RUN；
     超时 → TIMEOUT；API/网络错误(重试后仍失败) → ENV_ERROR。

用法（一次 clone、多条复用）：
    import workflow_runner as wr
    cfg = wr.RunnerConfig(owner="ComputingActionTest", repo="bingo", branch="main")
    with wr.Workspace(cfg) as ws:
        rr = wr.run_case(ws, cfg, case_id="SEC-MASK-SECRET-H-001",
                         workflow_yaml="<GitCode 原生 workflow 正文>",
                         fetch_logs=True)
    # rr 交给 assertion_engine.evaluate(rr, assertions)

凭据：
    ~/.gitcode-token         git push + v8 OAuth（query token）
    ~/.gitcode-web-curl.txt  web-api 取日志（浏览器会话，见 WEB-LOG-CREDENTIALS.md）
"""
import os
import re
import json
import time
import shutil
import tempfile
import subprocess
import urllib.request
import urllib.error

import yaml

# log_fetcher 与本文件同目录（phase02/scripts/）
try:
    import log_fetcher
except ImportError:  # 允许从别处 import 时按路径补齐
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import log_fetcher  # noqa


# ── 配置 ──────────────────────────────────────────────────────────
class RunnerConfig:
    """执行器配置。默认对齐当前被测实例（bingo），可由环境变量覆盖。"""

    def __init__(self, owner=None, repo=None, branch=None,
                 api_base=None, token=None,
                 timeout=None, poll_interval=None, executor=None):
        self.owner = owner or os.environ.get("GITCODE_OWNER", "ComputingActionTest")
        self.repo = repo or os.environ.get("GITCODE_REPO", "bingo")
        self.branch = branch or os.environ.get("GITCODE_BRANCH", "main")
        self.api_base = (api_base or os.environ.get("GITCODE_API_BASE_URL",
                                                    "https://api.gitcode.com")).rstrip("/")
        self.token = token or self._load_token()
        self.timeout = int(timeout or os.environ.get("PHASE02_CASE_TIMEOUT", 300))
        self.poll_interval = int(poll_interval or os.environ.get("PHASE02_POLL_INTERVAL", 12))
        # ⚠️ 未验证点：run-case.sh 给每个 v8 调用附加 &executor=<用户名>，而经实测
        #    跑通的 execute_*.py 并不带此参数。默认不带；如平台要求可经环境变量启用。
        self.executor = executor or os.environ.get("GITCODE_EXECUTOR", "")

    @staticmethod
    def _load_token():
        path = os.path.expanduser(os.environ.get("GITCODE_TOKEN_FILE", "~/.gitcode-token"))
        if os.path.exists(path):
            return open(path, encoding="utf-8").read().strip()
        env = os.environ.get("GITCODE_ACCESS_TOKEN", "")
        if env:
            return env
        raise FileNotFoundError(
            "未找到 GitCode token：既无 ~/.gitcode-token 也无 GITCODE_ACCESS_TOKEN")


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ── HTTP（带重试；失败抛 ApiError → 上层落 ENV_ERROR）────────────────
class ApiError(RuntimeError):
    pass


def api_get(cfg, path, retries=2):
    """GET {api_base}/api/v8/repos/{owner}/{repo}{path}。重试 retries 次。"""
    base = f"{cfg.api_base}/api/v8/repos/{cfg.owner}/{cfg.repo}{path}"
    sep = "&" if "?" in base else "?"
    url = f"{base}{sep}access_token={cfg.token}"
    if cfg.executor:
        url += f"&executor={cfg.executor}"
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            # 4xx 不重试（token/资源问题），5xx 重试
            if 400 <= e.code < 500:
                raise ApiError(f"HTTP {e.code} on {path}")
            last = ApiError(f"HTTP {e.code} on {path}")
        except Exception as e:  # 网络/超时
            last = ApiError(f"{type(e).__name__}: {e} on {path}")
        if attempt < retries:
            time.sleep(2)
    raise last or ApiError(f"unknown error on {path}")


# ── git shell ─────────────────────────────────────────────────────
def _sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True,
                       text=True, encoding="utf-8")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


HERE = os.path.dirname(os.path.abspath(__file__))
PHASE02 = os.path.dirname(HERE)

# ── 工作区（持久化缓存，跨 batch 复用；首次 clone，后续 git pull）──
_CACHE_ROOT = os.path.join(PHASE02, ".cache", "repos")


class Workspace:
    """clone 一次测试仓到持久缓存目录，退出时保留以备下个 batch 复用。"""

    def __init__(self, cfg):
        self.cfg = cfg
        self.repo_dir = os.path.join(_CACHE_ROOT, cfg.owner, cfg.repo)

    def __enter__(self):
        url = (f"https://oauth2:{self.cfg.token}@gitcode.com/"
               f"{self.cfg.owner}/{self.cfg.repo}.git")
        if os.path.isdir(os.path.join(self.repo_dir, ".git")):
            # 缓存存在：拉取最新、强制对齐远程（抹掉上次 batch 的 teardown 残留）
            rc, out = _sh("git fetch --depth 1 origin", cwd=self.repo_dir)
            if rc == 0:
                _sh(f"git checkout -q {self.cfg.branch}", cwd=self.repo_dir)
                _sh(f"git reset --hard origin/{self.cfg.branch}", cwd=self.repo_dir)
            else:
                # fetch 失败则重新 clone
                shutil.rmtree(self.repo_dir, ignore_errors=True)
        if not os.path.isdir(os.path.join(self.repo_dir, ".git")):
            os.makedirs(os.path.dirname(self.repo_dir), exist_ok=True)
            rc, out = _sh(f'git clone --depth 1 "{url}" "{self.repo_dir}"')
            if rc != 0:
                raise ApiError(f"git clone 失败: {out[-200:]}")
        return self

    def __exit__(self, *exc):
        pass  # 持久化缓存，不删除


# ── 0. 预检（push 前本地校验，拦编译错误，零 API 依赖）─────────────
# GitCode step name 禁止字符（VALIDATION-RULES §3b）
_STEP_NAME_FORBIDDEN = set('[]|!>&#?*=<\'"@${}+')


def preflight_validate(workflow_yaml):
    """push 前本地校验编译产物是否为合法且合规的 GitCode workflow。

    返回 (ok: bool, errors: list[str])。ok=False → run_case 应判 COMPILE_ERROR，
    **不 push**（省一次真跑）。依据 phase01/schema/VALIDATION-RULES.md（平台实测 12 条）
    + PyYAML 语法解析。纯本地、零 API/凭据依赖。
    """
    errors = []

    # 1) YAML 语法（catch 例如 run 命令含 ": " 破坏 plain scalar 的错误）
    try:
        doc = yaml.safe_load(workflow_yaml)
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        loc = f"（第 {mark.line + 1} 行）" if mark else ""
        return False, [f"YAML 语法错误{loc}: {getattr(e, 'problem', e)}"]
    if not isinstance(doc, dict):
        return False, ["workflow 顶层不是映射"]

    # 2) on 触发器：YAML1.1 把 on 解析为 True；必须映射形式，不能列表（平台拒绝 §3.3）
    trigger = doc.get("on", doc.get(True))
    if trigger is None:
        errors.append("缺 on 触发器")
    elif isinstance(trigger, list):
        errors.append("on 用了列表形式（on: [push]），平台会拒绝；须用映射 on:\\n  push:\\n    branches: [...]")

    # 3) jobs
    jobs = doc.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        return False, errors + ["缺 jobs 或 jobs 非映射"]

    for jid, job in jobs.items():
        if not isinstance(job, dict):
            errors.append(f"job '{jid}' 非映射"); continue
        # 3a) job name 必填（§2）
        if not job.get("name"):
            errors.append(f"job '{jid}' 缺 name（平台报 name cannot be empty）")
        # 3b) runs-on 必须数组形式（§1）
        ro = job.get("runs-on")
        if not isinstance(ro, list):
            errors.append(f"job '{jid}' runs-on 须用数组格式 [ubuntu-latest, x64, small]，实得 {type(ro).__name__}")
        # 3c) steps ≤ 16（§5）+ 每 step 有 name 且无非法字符（§3）
        steps = job.get("steps") or []
        if len(steps) > 16:
            errors.append(f"job '{jid}' steps={len(steps)} 超过 16，须拆 job（§5）")
        for i, st in enumerate(steps):
            if not isinstance(st, dict):
                errors.append(f"job '{jid}' step[{i}] 非映射"); continue
            nm = st.get("name")
            if not nm:
                errors.append(f"job '{jid}' step[{i}] 缺 name（含 bare uses step）")
            else:
                bad = _STEP_NAME_FORBIDDEN & set(str(nm))
                if bad:
                    errors.append(f"job '{jid}' step name 含非法字符 {sorted(bad)}: {nm!r}")
                if len(str(nm)) > 128:
                    errors.append(f"job '{jid}' step name 超 128 字符")

    # 注：早期 VALIDATION-RULES §7 称 vars.* 上下文不支持——**已被实测推翻**
    # （run 03 的 vars.DUP + handoff 均真跑 PASS）。GitCode 支持 vars.* 引用仓库/组织变量，
    # 故此处**不再拦截** vars.*（曾误判合法 workflow 为 COMPILE_ERROR）。

    return (len(errors) == 0), errors


# ── 1. 部署（写 workflow、commit、push）→ (sha, wf_filename)────────
def deploy(ws, cfg, case_id, workflow_yaml):
    """把 workflow 正文写入 .gitcode/workflows/<case-id>.yml 并 push。

    返回 (head_sha, wf_filename)。push 失败返回 (None, wf_filename)。
    """
    wf_filename = case_id.lower().replace("_", "-") + ".yml"
    dst = os.path.join(ws.repo_dir, ".gitcode", "workflows", wf_filename)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(workflow_yaml)
    _sh("git add .gitcode/workflows/", cwd=ws.repo_dir)
    # 无变更时用 --allow-empty 强制触发一次
    rc_nodiff, _ = _sh("git diff --cached --quiet", cwd=ws.repo_dir)
    allow = "--allow-empty " if rc_nodiff == 0 else ""
    _sh(f'git commit {allow}-m "test: {case_id}"', cwd=ws.repo_dir)
    rc, out = _sh(f"git push origin {cfg.branch}", cwd=ws.repo_dir)
    if rc != 0:
        log(f"  push 失败: {out[-200:]}")
        return None, wf_filename
    rc, sha = _sh("git rev-parse HEAD", cwd=ws.repo_dir)
    return sha.strip(), wf_filename


# ── 2. 轮询（head_sha AND file_path 精确匹配）→ run dict | None ─────
_TERMINAL = ("COMPLETED", "FAILED", "CANCELED", "IGNORED")


def poll_run(cfg, sha, wf_filename):
    """轮询到"我这次推的那个 workflow 文件"的 run 抵达终态。

    ★ 必须 (head_sha == sha) AND (file_path 以 wf_filename 结尾) 双条件——
      否则会抓到同一次 push 触发的别的/历史 workflow 的 run（run 03 教训）。
    超时返回最后见到的 pending run（若有），否则 None。
    """
    elapsed, pending = 0, None
    while elapsed < cfg.timeout:
        d = api_get(cfg, f"/actions/runs?branch={cfg.branch}&per_page=30")
        runs = d.get("workflow_runs", []) if isinstance(d, dict) else []
        for r in runs:
            fp = r.get("file_path") or ""
            if r.get("head_sha") == sha and fp.endswith(wf_filename):
                if r.get("status") in _TERMINAL:
                    return r
                pending = r
        time.sleep(cfg.poll_interval)
        elapsed += cfg.poll_interval
    return pending


# ── 3. 采集 → RunResult ───────────────────────────────────────────
def collect(cfg, run, fetch_logs=False):
    """采集 run/job/step 状态（+可选日志正文）→ RunResult dict。

    job 元信息用 log_fetcher.list_jobs（以 run detail stages.jobs[].id 为准，
    比 /jobs 接口的 id 更可靠——后者某些场景返回空串，见 log_fetcher 说明）。
    日志用 log_fetcher.fetch_job_logs 走 v8 download_log(zip)，抓**原始正文
    （不含 step 名）**，供负向断言全文扫描而不被污染。仅需 OAuth token。
    """
    rid = run.get("workflow_run_id", "") or run.get("id", "")
    try:
        jobs_meta = log_fetcher.list_jobs(cfg.owner, cfg.repo, rid)
    except Exception as e:
        raise ApiError(f"list_jobs 失败: {e}")

    jobs, logs_parts = [], []
    for j in jobs_meta:
        steps = [{"name": s.get("name"), "status": s.get("status")}
                 for s in (j.get("steps") or []) if isinstance(s, dict)]
        jobs.append({"id": j.get("id"), "name": j.get("name"),
                     "status": j.get("status"), "steps": steps})
        if fetch_logs:
            try:
                logs_parts.append(
                    log_fetcher.fetch_job_logs(None, cfg.owner, cfg.repo, rid, j))
            except Exception as e:
                logs_parts.append(f"<log-fetch-error: {e}>")

    return {
        "status": run.get("status"),
        "gitcode_run_id": rid,
        "conclusion": run.get("conclusion") or run.get("status"),
        "event": run.get("event"),
        "head_sha": run.get("head_sha"),
        "jobs": jobs,
        "logs": "\n".join(logs_parts),
        "logs_available": bool(fetch_logs),
        "artifacts": [],  # v8 artifacts 采集按需补
    }


# ── 高层：一条用例 部署→轮询→采集 ─────────────────────────────────
# ── 触发适配器（确定性；把 trigger.event 翻译成对 GitCode 的操作）──────
# ★ 架构：所有"触发前置操作"（建 PR / 建 tag / dispatch）都是**确定性**的，归属本模块，
#   不交给任何 LLM agent（LLM 只做只读的检查/归因）。push 已实现；其余为可确定性实现的
#   扩展点——需先验证 GitCode 对应 API/语义，未实现前如实返回 unsupported 原因（→ INCONCLUSIVE）。
TRIGGER_STATUS = {
    "push":                 {"supported": True},
    "tag":                  {"supported": False,
                             "reason": "tag 触发：需 git tag+push 并按 tag ref 匹配 run（确定性，待验证 GitCode tag 触发语义）"},
    "manual":               {"supported": False,
                             "reason": "manual 触发：需调 GitCode workflow_dispatch API（待确认端点）"},
    "workflow_dispatch":    {"supported": False,
                             "reason": "workflow_dispatch：需 dispatch API（待确认端点）"},
    "pr":                   {"supported": False,
                             "reason": "pr 触发：需建分支+开 PR（确定性，待确认 PR 创建端点与 run 关联方式）"},
    "pull_request":         {"supported": False,
                             "reason": "pull_request 触发：需建分支+开 PR（待确认 PR API 与 run 关联）"},
    "pull_request_target":  {"supported": False,
                             "reason": "pull_request_target：同 PR，且需注意 base 上下文语义"},
    "fork_pr":              {"supported": False,
                             "reason": "fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者（基础设施依赖）"},
    "schedule":             {"supported": False,
                             "reason": "schedule：cron 无法按需触发（基础设施限制）"},
}


def trigger_supported(event):
    """返回 (supported: bool, reason: str)。未知事件视为不支持。"""
    info = TRIGGER_STATUS.get(event)
    if info is None:
        return False, f"未知触发事件 '{event}'"
    return info["supported"], info.get("reason", "")


def teardown(ws, cfg, wf_filename):
    """删除本次部署的 workflow 文件并 push（fixture 级清理，防仓库污染）。

    ★ 为什么需要：共享仓里每个 on:push 的 workflow 文件都会被后续任何 push 连带触发，
    不清理会越积越多、互相污染、淹没结果（曾积累 45 个遗留文件）。best-effort，失败不阻断。
    """
    path = f".gitcode/workflows/{wf_filename}"
    rc, _ = _sh(f"git rm -q {path}", cwd=ws.repo_dir)
    if rc != 0:
        return False
    _sh('git commit -q -m "chore: teardown test workflow"', cwd=ws.repo_dir)
    rc, out = _sh(f"git push origin {cfg.branch}", cwd=ws.repo_dir)
    if rc != 0:
        log(f"  teardown push 失败: {out[-150:]}")
    return rc == 0


def run_case(ws, cfg, case_id, workflow_yaml, fetch_logs=False, teardown_reset="fixture",
             trigger_event="push"):
    """执行单条用例的"执行层"链路。返回 RunResult（含执行层异常状态）。

    执行层状态（映射 rules.md §11 的执行类判定）：
      NO_RUN       触发后没等到对应 run
      TIMEOUT      轮询超时且从未见到终态
      ENV_ERROR    API/网络错误（重试后仍失败）
      INCONCLUSIVE 触发方式尚未实现（见 TRIGGER_STATUS）
      其余         平台终态（COMPLETED/FAILED/...），交 assertion_engine 判定

    trigger_event：触发方式；push 已实现，其余（见 TRIGGER_STATUS）未实现 → INCONCLUSIVE + 具体原因。
    teardown_reset：`fixture`/`full_instance` → 跑完删除本次 push 的 workflow 文件（防污染）；`none` → 保留。
    注：workflow 合法性应在 push 前经 preflight_validate 拦截。
    """
    t0 = time.time()
    wf_filename = None
    # 触发适配：非 push 事件目前未实现 → 如实返回具体原因（不糊弄）
    ok, reason = trigger_supported(trigger_event)
    if not ok:
        return _exec_result("INCONCLUSIVE", case_id, reason=reason, t0=t0)
    try:
        sha, wf_filename = deploy(ws, cfg, case_id, workflow_yaml)
        if not sha:
            return _exec_result("ENV_ERROR", case_id, reason="git push 失败", t0=t0)
        try:
            run = poll_run(cfg, sha, wf_filename)
            if run is None:
                return _exec_result("NO_RUN", case_id, head_sha=sha, t0=t0)
            if run.get("status") not in _TERMINAL:
                return _exec_result("TIMEOUT", case_id, head_sha=sha,
                                    gitcode_run_id=run.get("workflow_run_id", ""), t0=t0)
            rr = collect(cfg, run, fetch_logs=fetch_logs)
            rr["duration_seconds"] = round(time.time() - t0)
            # 平台终态 FAILED 但 0 job：极可能 workflow 被平台拒绝（SYNTAX_ERROR 类）。
            if rr.get("status") == "FAILED" and not rr.get("jobs"):
                rr["workflow_rejected"] = True
                rr["reason"] = "run FAILED 且 0 job：workflow 可能被平台拒绝（预检未覆盖的规则）"
            return rr
        finally:
            # 无论判定结果如何，清理本次 push 的文件（除非 reset=none）
            if wf_filename and teardown_reset != "none":
                try:
                    teardown(ws, cfg, wf_filename)
                except Exception as e:
                    log(f"  teardown 异常（忽略）: {e}")
    except ApiError as e:
        return _exec_result("ENV_ERROR", case_id, reason=str(e), t0=t0)


def _exec_result(status, case_id, reason="", head_sha="", gitcode_run_id="", t0=None):
    return {
        "status": status,
        "case_id": case_id,
        "gitcode_run_id": gitcode_run_id,
        "conclusion": status,
        "head_sha": head_sha,
        "jobs": [],
        "logs": "",
        "logs_available": False,
        "artifacts": [],
        "reason": reason,
        "duration_seconds": round(time.time() - t0) if t0 else 0,
    }


if __name__ == "__main__":
    # 自检：仅验证可 import 与配置装载，不触网。
    print("workflow_runner self-check: imports OK")
    try:
        cfg = RunnerConfig()
        print(f"  config: {cfg.owner}/{cfg.repo}@{cfg.branch} api={cfg.api_base} "
              f"executor={'set' if cfg.executor else '(none)'}")
    except Exception as e:
        print(f"  config load: {type(e).__name__}: {e}")
