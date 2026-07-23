#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_pr_trigger.py — 验证 pull_request 触发能否自动脚本化

用法:
    cd phase02/classify-experiment/demo
    python3 demo_pr_trigger.py

流程:
    1. clone 仓库（main 分支）
    2. 在 main 上写入 workflow YAML（on: pull_request）并 push —— 必须先存在于 base 分支
    3. 创建 feature 分支，做一个无意义变更（触发 PR 差异）
    4. push feature 分支
    5. 调用 POST /api/v5/repos/.../pulls 创建 PR
    6. 轮询 v8 actions/runs（不限分支），找 event=MR 且 file_path 匹配的 run
    7. 下载 job 日志
    8. 清理（关闭 PR，删除分支，删除 main 上的 demo workflow）
"""

import os, sys, json, time, shutil, subprocess, tempfile, urllib.request, urllib.error

# ── 配置（从 .env 文件读）─────────────────────────────────────────────
def load_env():
    """从项目根 .env 加载环境变量（不覆盖已有变量）。处理内联注释和引号。"""
    import re
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip()
                v = re.sub(r'\s+#.*$', '', v).strip()
                v = v.strip('"').strip("'")
                if k not in os.environ:
                    os.environ[k] = v

load_env()

OWNER      = os.environ.get("GITCODE_OWNER", "ComputingActionTest")
REPO       = os.environ.get("GITCODE_REPO", "foundational-tests")
BRANCH     = os.environ.get("GITCODE_BRANCH", "main")
TOKEN      = os.environ.get("GITCODE_ACCESS_TOKEN", "")
EXECUTOR   = os.environ.get("GITCODE_EXECUTOR", "")
API_BASE   = "https://api.gitcode.com"
TIMEOUT    = 180
POLL       = 10

# ── 测试用的 workflow YAML（只 on: pull_request，不会因 push main 而触发）─
DEMO_WORKFLOW = """\
on:
  pull_request:
    types:
      - open
      - update
      - reopen
    branches: [main]
jobs:
  demo:
    name: demo-pr-trigger-test
    runs-on: [dedicate-hosted, x64, large]
    steps:
      - name: echo event
        run: |
          echo "EVENT=${{ atomgit.event_name }}"
          echo "PR_NUMBER=${{ atomgit.event.pull_request.number }}"
          echo "SUCCESS"
"""

CASE_ID = "DEMO-PR-01-001"
WF_FILENAME = f"{CASE_ID.lower()}.yml"
HEAD_BRANCH = f"demo/test-pr-{int(time.time()) % 100000}"


# ── helpers ───────────────────────────────────────────────────────────
def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def sh(cmd, cwd=None, check=False):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True,
                       text=True, encoding="utf-8")
    out = (r.stdout or "") + (r.stderr or "")
    if check and r.returncode != 0:
        raise RuntimeError(f"cmd failed (rc={r.returncode}): {cmd}\n{out[-300:]}")
    return r.returncode, out


def api_call(method, path, data=None, use_contributor=False):
    """调用 GitCode API。path 须以 /api/v5/ 或 /api/v8/ 开头。"""
    token = os.environ.get("CONTRIBUTOR_GITCODE_TOKEN") if use_contributor else TOKEN
    sep = "&" if "?" in path else "?"
    url = f"{API_BASE}{path}{sep}access_token={token}"
    if "/api/v8/" in path and EXECUTOR:
        url += f"&executor={EXECUTOR}"

    body_bytes = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body_bytes, method=method)
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp_text = r.read().decode("utf-8", errors="replace")
            code = r.getcode()
    except urllib.error.HTTPError as e:
        resp_text = e.read().decode("utf-8", errors="replace")
        code = e.code
    except Exception as e:
        return {"_error": str(e), "_code": 0}

    try:
        return json.loads(resp_text)
    except json.JSONDecodeError:
        return {"_raw": resp_text, "_code": code}


# ── main demo ─────────────────────────────────────────────────────────
def main():
    if not TOKEN:
        log("❌ 缺少 GITCODE_ACCESS_TOKEN，请检查 .env")
        return 1

    log(f"📦 目标: {OWNER}/{REPO}@{BRANCH}")
    log(f"🔑 token: {TOKEN[:8]}...  executor: {EXECUTOR}")

    # ── 1. Clone ─────────────────────────────────────────────────────
    log("── 步骤 1: clone 仓库（main 分支）──")
    root = tempfile.mkdtemp(prefix="demo-pr-")
    repo_dir = os.path.join(root, "repo")
    url = f"https://oauth2:{TOKEN}@gitcode.com/{OWNER}/{REPO}.git"
    rc, out = sh(f'git clone --depth 1 --branch {BRANCH} "{url}" "{repo_dir}"')
    if rc != 0:
        log(f"❌ clone 失败: {out[-300:]}")
        shutil.rmtree(root, ignore_errors=True)
        return 1
    log(f"   ✅ clone 完毕 → {repo_dir}")

    pr_number = None
    wf_pushed_to_main = False
    try:
        # ── 2. 在 main 上写入 workflow 并 push（PR 触发的前提！）───
        log("── 步骤 2: 在 main 上写入 workflow YAML ──")
        wf_dir = os.path.join(repo_dir, ".gitcode", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        wf_path = os.path.join(wf_dir, WF_FILENAME)
        with open(wf_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(DEMO_WORKFLOW)
        log(f"   ✅ 写入 {wf_path}（on: pull_request，不会因 push 触发）")

        sh(f"git add {wf_path}", cwd=repo_dir, check=True)
        rc_diff, _ = sh("git diff --cached --quiet", cwd=repo_dir)
        allow = "--allow-empty " if rc_diff == 0 else ""
        sh(f'git commit {allow}-m "demo: add PR trigger workflow"', cwd=repo_dir)
        rc, out = sh(f"git push origin {BRANCH}", cwd=repo_dir)
        if rc != 0:
            log(f"❌ push main 失败: {out[-300:]}")
            return 1
        # 验证 remote SHA
        rc_push_sha, push_sha = sh("git rev-parse HEAD", cwd=repo_dir)
        log(f"   ✅ workflow 已推送到 main，SHA={push_sha.strip()}")
        wf_pushed_to_main = True

        # 等待平台索引新的 workflow 文件
        log("   等待平台索引...")
        time.sleep(30)

        # ── 3. pull 同步后再创建 feature 分支 ──────────────────────────
        log(f"── 步骤 3: pull 同步 + 创建分支 {HEAD_BRANCH} ──")
        sh(f"git pull origin {BRANCH}", cwd=repo_dir)
        sh(f"git checkout -b {HEAD_BRANCH}", cwd=repo_dir, check=True)
        # 做一个无意义变更让 PR 有 diff
        dummy_path = os.path.join(repo_dir, "demo-pr-trigger-marker.txt")
        with open(dummy_path, "w") as f:
            f.write(f"demo PR trigger test at {time.ctime()}\n")
        sh(f"git add demo-pr-trigger-marker.txt", cwd=repo_dir)
        sh(f'git commit -m "demo: PR trigger — dummy change"', cwd=repo_dir)
        rc, out = sh(f"git push origin {HEAD_BRANCH}", cwd=repo_dir)
        if rc != 0:
            log(f"❌ push 分支失败: {out[-300:]}")
            return 1
        log(f"   ✅ 分支 {HEAD_BRANCH} 已 push")

        # ── 4. 创建 PR ───────────────────────────────────────────────
        log("── 步骤 4: 创建 PR ──")
        pr_resp = api_call(
            "POST",
            f"/api/v5/repos/{OWNER}/{REPO}/pulls",
            data={
                "title": f"[Demo] PR trigger test — {CASE_ID}",
                "head": HEAD_BRANCH,
                "base": BRANCH,
                "body": "自动化 demo：验证 pull_request 触发 workflow",
            },
        )
        log(f"   API 返回: {json.dumps(pr_resp, indent=2, ensure_ascii=False)[:500]}")

        if "_error" in pr_resp or pr_resp.get("_code", 200) >= 400:
            log(f"❌ 创建 PR 失败: {pr_resp}")
            return 1

        pr_number = pr_resp.get("number") or pr_resp.get("iid") or pr_resp.get("id")
        log(f"   ✅ PR #{pr_number} 已创建")
        base_sha = (pr_resp.get("base", {}) or {}).get("sha", "?")
        head_sha = (pr_resp.get("head", {}) or {}).get("sha", "?")
        log(f"   PR base.sha={base_sha[:12]}...  head.sha={head_sha[:12]}...")

        # ── 5. 轮询 workflow run ──────────────────────────────────────
        log("── 步骤 5: 轮询 MR-triggered run ──")
        run = None
        elapsed = 0
        TERMINAL = ("COMPLETED", "FAILED", "CANCELED", "IGNORED")
        while elapsed < TIMEOUT:
            resp = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=100&pull_request_id={pr_number}")
            runs_pr = resp.get("workflow_runs", []) if isinstance(resp, dict) else []

            for r in runs_pr:
                stat = r.get("status", "")
                rid = r.get("workflow_run_id", "")
                log(f"   ★ 命中 pull_request_id={pr_number}: run_id={rid} status={stat} "
                    f"event={r.get('event','?')} file={r.get('file_path','?')}")
                if stat in TERMINAL:
                    run = r
                    break

            # 后备：也扫一次所有 run 看有没有 MR 事件的
            if not run and elapsed % 30 == 0:
                resp_all = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=100")
                runs_all = resp_all.get("workflow_runs", []) if isinstance(resp_all, dict) else []
                for r in runs_all:
                    ev = r.get("event", "")
                    fp = r.get("file_path", "")
                    if ev != "Manual" or WF_FILENAME in fp:
                        log(f"   非 Manual run: event={ev} status={r.get('status')} file={fp}")

            if run:
                break
            time.sleep(POLL)
            elapsed += POLL
            if elapsed % 30 == 0:
                log(f"   ⌛ 已等 {elapsed}s...")

        if run is None:
            log(f"⚠️  超时 {TIMEOUT}s 未等到 MR-triggered run")
        else:
            # ── 6. 获取 job + 日志 ───────────────────────────────────
            run_id = run.get("workflow_run_id", "") or run.get("id", "")
            log("── 步骤 6: 获取 jobs + 日志 ──")
            jobs_resp = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{run_id}")
            stages = (jobs_resp.get("stages") or []) if isinstance(jobs_resp, dict) else []

            for stage in stages:
                for j in (stage.get("jobs") or []):
                    jid = j.get("id", "")
                    jname = j.get("name", "?")
                    jstatus = j.get("status", "?")
                    log(f"   job: id={jid} name={jname} status={jstatus}")

                    if jid:
                        log_resp = api_call("GET",
                            f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{run_id}/jobs/{jid}/download_log")
                        raw_text = log_resp.get("_raw", "") if isinstance(log_resp, dict) else str(log_resp)
                        log(f"   log body (first 800 chars):\n---\n{raw_text[:800]}\n---")

            log("")
            log("══════════════════════════════════════════")
            log(f"  result: run_status={run.get('status')}")
            log(f"  conclusion={run.get('conclusion', 'N/A')}")
            log(f"  run_id={run_id}   PR #{pr_number}")
            log("══════════════════════════════════════════")

    finally:
        # ── 7. 清理 ───────────────────────────────────────────────────
        log("── 步骤 7: 清理 ──")
        
        if pr_number:
            close_resp = api_call(
                "PATCH",
                f"/api/v5/repos/{OWNER}/{REPO}/pulls/{pr_number}",
                data={"state": "closed"},
            )
            log(f"   关闭 PR #{pr_number}: {'ok' if '_error' not in close_resp else close_resp.get('_error')}")

        if wf_pushed_to_main:
            # 删除 main 上的 demo workflow
            sh(f"git checkout {BRANCH}", cwd=repo_dir)
            rm_path = os.path.join(repo_dir, ".gitcode", "workflows", WF_FILENAME)
            if os.path.exists(rm_path):
                sh(f"git rm {rm_path}", cwd=repo_dir)
                sh(f'git commit -m "chore: remove demo workflow"', cwd=repo_dir)
                sh(f"git push origin {BRANCH}", cwd=repo_dir)
                log(f"   删除 main 上的 {WF_FILENAME}")

        # 删除远程 feature 分支
        sh(f"git push origin --delete {HEAD_BRANCH}", cwd=repo_dir)
        log(f"   删除远程分支 {HEAD_BRANCH}")

        shutil.rmtree(root, ignore_errors=True)
        log(f"   ✅ 清理完毕")

    return 0


if __name__ == "__main__":
    sys.exit(main())
