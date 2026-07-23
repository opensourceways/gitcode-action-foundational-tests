#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_fork_pr.py — 验证 fork PR (on: pull_request) 能否自动触发 workflow

核心测试：
  1. Bot 将 workflow YAML 推到 upstream main（base 分支必须有 workflow）
  2. Contributor fork 仓库，做变更，push 分支
  3. Contributor 从 fork 创建跨仓库 PR → upstream
  4. Bot 在上游轮询 run
  5. 清理

用法:
    cd phase02/classify-experiment/demo
    python3 demo_fork_pr.py
"""

import os, sys, json, re, time, shutil, subprocess, tempfile, urllib.request, urllib.error

# ── 配置 ──────────────────────────────────────────────────────────────
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k, v = k.strip(), v.strip()
                v = re.sub(r'\s+#.*$', '', v).strip()
                v = v.strip('"').strip("'")
                if k not in os.environ:
                    os.environ[k] = v

load_env()

OWNER         = os.environ.get("GITCODE_OWNER", "ComputingActionTest")
REPO          = os.environ.get("GITCODE_REPO", "foundational-tests")
BRANCH        = os.environ.get("GITCODE_BRANCH", "main")
BOT_TOKEN     = os.environ.get("GITCODE_ACCESS_TOKEN", "")
CONTRIB_TOKEN = os.environ.get("CONTRIBUTOR_GITCODE_TOKEN", "")
EXECUTOR      = os.environ.get("GITCODE_EXECUTOR", "")
API_BASE      = "https://api.gitcode.com"

WF_FILENAME   = "demo-fork-pr-01-001.yml"
WF_FILEPATH   = f".gitcode/workflows/{WF_FILENAME}"
FEAT_BRANCH   = f"demo/fork-test-{int(time.time()) % 100000}"
TIMEOUT       = 240
POLL          = 10

# ── workflow (只 on: pull_request，推 main 不会触发 push) ────────────
DEMO_WORKFLOW = """\
on:
  pull_request:
    types:
      - open
      - update
      - reopen
    branches: [main]
jobs:
  fork-demo:
    name: fork-pr-trigger-test
    runs-on: [dedicate-hosted, x64, large]
    steps:
      - name: echo context
        run: |
          echo "FORK_PR_TEST_OK"
          echo "EVENT=${{ atomgit.event_name }}"
          echo "PR=${{ atomgit.event.pull_request.number }}"
          echo "HEAD_REF=${{ atomgit.event.pull_request.head.ref }}"
"""


# ── helpers ───────────────────────────────────────────────────────────
def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True,
                       text=True, encoding="utf-8")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def api_call(method, path, data=None, use_contributor=False):
    """调用 GitCode API。"""
    token = CONTRIB_TOKEN if use_contributor else BOT_TOKEN
    sep = "&" if "?" in path else "?"
    url = f"{API_BASE}{path}{sep}access_token={token}"
    if not use_contributor and "/api/v8/" in path and EXECUTOR:
        url += f"&executor={EXECUTOR}"

    body_bytes = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body_bytes, method=method)
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"_error": f"HTTP {e.code}", "_raw": body[:500]}
    except Exception as e:
        return {"_error": str(e)}


def git_clone(owner, repo, token, branch, target_dir):
    url = f"https://oauth2:{token}@gitcode.com/{owner}/{repo}.git"
    rc, out = sh(f'git clone --depth 1 --branch {branch} "{url}" "{target_dir}"')
    if rc != 0:
        log(f"❌ clone {owner}/{repo} 失败: {out[-200:]}")
        return False
    return True


def main():
    if not BOT_TOKEN or not CONTRIB_TOKEN:
        log("❌ 缺少 token，请检查 .env (GITCODE_ACCESS_TOKEN + CONTRIBUTOR_GITCODE_TOKEN)")
        return 1

    log("=" * 60)
    log("FORK PR 触发测试")
    log(f"  Bot:         {OWNER}/{REPO}")
    log(f"  Contributor: (token={CONTRIB_TOKEN[:8]}...)")
    log("=" * 60)

    root = tempfile.mkdtemp(prefix="demo-fork-")
    upstream_dir = os.path.join(root, "upstream")
    fork_dir = os.path.join(root, "fork")

    wf_on_main = False
    fork_full_name = None
    pr_number = None
    # for deleting fork later
    fork_owner = None

    try:
        # ── 1. Bot 推 workflow 到 upstream main ───────────────────
        log("── 步骤 1: Bot 推送 workflow 到 upstream main ──")
        if not git_clone(OWNER, REPO, BOT_TOKEN, BRANCH, upstream_dir):
            return 1

        wf_dir = os.path.join(upstream_dir, ".gitcode", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        with open(os.path.join(wf_dir, WF_FILENAME), "w", encoding="utf-8", newline="\n") as f:
            f.write(DEMO_WORKFLOW)

        sh("git add .gitcode/workflows/", cwd=upstream_dir)
        sh(f'git commit --allow-empty -m "demo: fork PR test workflow"', cwd=upstream_dir)
        rc, out = sh(f"git push origin {BRANCH}", cwd=upstream_dir)
        if rc != 0:
            log(f"❌ 推送 upstream 失败: {out[-200:]}")
            return 1
        log(f"   ✅ Workflow 已推送到 upstream main")
        wf_on_main = True

        # 等平台索引
        log("   等待平台索引 workflow (30s)...")
        time.sleep(30)

        # ── 2. Contributor fork 仓库 ──────────────────────────────
        log("── 步骤 2: Contributor fork 仓库 ──")
        fork_resp = api_call("POST",
            f"/api/v5/repos/{OWNER}/{REPO}/forks",
            use_contributor=True)
        log(f"   fork API: {json.dumps(fork_resp, ensure_ascii=False)[:300]}")
        
        if "_error" in fork_resp or not fork_resp.get("full_name"):
            log(f"   ⚠️  fork 创建返回错误（可能已存在），用 bot token 查 forks 列表...")
            forks_list = api_call("GET",
                f"/api/v5/repos/{OWNER}/{REPO}/forks?per_page=20",
                use_contributor=False)  # bot token 查看所有 fork
            if isinstance(forks_list, list):
                for fk in forks_list:
                    owner_info = fk.get("owner") or fk.get("user") or fk.get("namespace") or {}
                    login = ""
                    if isinstance(owner_info, dict):
                        login = owner_info.get("login") or owner_info.get("username") or owner_info.get("path", "")
                    log(f"   ... fork: {fk.get('full_name')} owner={login}")
                    if login:
                        fork_full_name = fk.get("full_name")
                        fork_owner = login
                        break
            if not fork_full_name:
                # Last resort: try contributor's own repos
                log("   ... 尝试从 contributor repos 查找...")
                import urllib.request as _ur
                url = f"{API_BASE}/api/v5/user/repos?access_token={CONTRIB_TOKEN}&per_page=50"
                r = _ur.urlopen(_ur.Request(url), timeout=15)
                repos = json.loads(r.read().decode("utf-8"))
                for repo_obj in (repos if isinstance(repos, list) else []):
                    if repo_obj.get("name") == REPO or repo_obj.get("path") == REPO:
                        fork_full_name = repo_obj.get("full_name") or repo_obj.get("path")
                        ns = repo_obj.get("namespace") or repo_obj.get("owner") or {}
                        fork_owner = (ns if isinstance(ns, dict) else {}).get("path", "")
                        log(f"   ... found: {fork_full_name} owner={fork_owner}")
                        break
        else:
            fork_full_name = fork_resp.get("full_name")
            ns = fork_resp.get("namespace") or fork_resp.get("owner") or {}
            fork_owner = (ns if isinstance(ns, dict) else {}).get("path") or ns.get("login", "")

        if not fork_full_name:
            log("❌ 无法获取 fork 信息")
            return 1

        fork_parts = fork_full_name.split("/")
        fork_owner = fork_owner or fork_parts[0] if len(fork_parts) >= 2 else ""
        log(f"   ✅ Fork: {fork_full_name}  owner={fork_owner}")

        # ── 3. Clone fork（等 20s 让 fork 初始化）──
        log(f"── 步骤 3: 等待 fork 初始化 + clone ──")
        log("   等待 20s...")
        time.sleep(20)

        # retry clone up to 3 times
        cloned = False
        for attempt in range(3):
            if git_clone(fork_owner, REPO, CONTRIB_TOKEN, BRANCH, fork_dir):
                cloned = True
                break
            log(f"   clone 失败 (attempt {attempt+1}/3)，等 10s 重试...")
            time.sleep(10)
        if not cloned:
            return 1

        sh(f"git checkout -b {FEAT_BRANCH}", cwd=fork_dir)
        # 做一个无意义变更
        dummy = os.path.join(fork_dir, "fork-demo-trigger.txt")
        with open(dummy, "w") as f:
            f.write(f"fork PR demo at {time.ctime()}\n")
        sh(f"git add fork-demo-trigger.txt", cwd=fork_dir)
        sh(f'git commit -m "demo: fork PR trigger"', cwd=fork_dir)
        rc, out = sh(f"git push origin {FEAT_BRANCH}", cwd=fork_dir)
        if rc != 0:
            log(f"❌ push fork 分支失败: {out[-200:]}")
            return 1
        log(f"   ✅ Fork 分支 {FEAT_BRANCH} 已 push")

        # ── 4. 创建跨仓库 PR (fork → upstream) ───────────────────
        log("── 步骤 4: 创建跨仓库 PR ──")
        pr_resp = api_call("POST",
            f"/api/v5/repos/{OWNER}/{REPO}/pulls",
            data={
                "title": f"[Demo] Fork PR trigger test",
                "head": f"{fork_owner}:{FEAT_BRANCH}",
                "base": BRANCH,
                "body": "自动化 demo：验证 fork PR 触发 on: pull_request workflow",
            },
            use_contributor=True)
        log(f"   PR API: {json.dumps({k: pr_resp.get(k) for k in ['id','iid','number','state','title','head','base'] if k in pr_resp}, ensure_ascii=False, default=str)[:500]}")

        if "_error" in pr_resp:
            log(f"❌ 创建 PR 失败: {pr_resp}")
            # 如果 head 格式不对，尝试只用分支名
            log("   尝试只用分支名作为 head...")
            pr_resp = api_call("POST",
                f"/api/v5/repos/{OWNER}/{REPO}/pulls",
                data={
                    "title": f"[Demo] Fork PR trigger test v2",
                    "head": FEAT_BRANCH,
                    "base": BRANCH,
                    "body": "自动化 demo v2",
                },
                use_contributor=True)
            log(f"   PR API v2: {json.dumps({k: pr_resp.get(k) for k in ['id','iid','number','state','title'] if k in pr_resp}, ensure_ascii=False)[:300]}")

        if "_error" in pr_resp:
            return 1

        pr_number = pr_resp.get("number") or pr_resp.get("iid")
        pr_id = pr_resp.get("id")
        log(f"   ✅ PR #{pr_number} (api id={pr_id}) 已创建")

        # ── 5. Bot 轮询 workflow run ──────────────────────────────
        log("── 步骤 5: 轮询 workflow run ──")
        run = None
        TERMINAL = ("COMPLETED", "FAILED", "CANCELED", "IGNORED")
        t0 = time.time()

        while time.time() - t0 < TIMEOUT:
            # 按 pull_request_id 查
            resp = api_call("GET",
                f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=100&pull_request_id={pr_number}")
            runs = resp.get("workflow_runs", []) if isinstance(resp, dict) else []

            for r in runs:
                s = r.get("status", "")
                rid = r.get("workflow_run_id", "")
                if s in TERMINAL:
                    run = (r, rid)
                    break
                log(f"   PENDING: run_id={rid} status={s}")

            if run:
                break

            # 后备：扫所有 run 找 fork-demo 文件
            if not run and int(time.time() - t0) % 30 < POLL:
                all_runs = api_call("GET",
                    f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=100")
                for r in (all_runs.get("workflow_runs", []) if isinstance(all_runs, dict) else []):
                    if WF_FILENAME in (r.get("file_path") or ""):
                        s = r.get("status", "")
                        rid = r.get("workflow_run_id", "")
                        log(f"   ★ 文件匹配: run_id={rid} status={s}")
                        if s in TERMINAL:
                            run = (r, rid)
                            break

            if run:
                break

            elapsed = int(time.time() - t0)
            if elapsed % 30 < POLL:
                log(f"   ⌛ {elapsed}s...")
            time.sleep(POLL)

        if run is None:
            log(f"⚠️  超时 {TIMEOUT}s 未找到 run")
        else:
            r, rid = run
            log("")
            log("=" * 60)
            log(f"  ✅ FOUND: run_id={rid}")
            log(f"     status={r.get('status')}  event={r.get('event')}")
            log(f"     file={r.get('file_path')}")
            log("=" * 60)

            # 尝试拉日志
            jobs_resp = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}")
            stages = (jobs_resp.get("stages") or []) if isinstance(jobs_resp, dict) else []
            for stage in stages:
                for j in (stage.get("jobs") or []):
                    jid = j.get("id", "")
                    if jid:
                        log_resp = api_call("GET",
                            f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}/jobs/{jid}/download_log")
                        raw = log_resp.get("_raw", "") if isinstance(log_resp, dict) else str(log_resp)
                        if "FORK_PR_TEST_OK" in raw:
                            log(f"   ✅ 日志确认: FORK_PR_TEST_OK")
                        log(f"   log (first 500 chars):\n---\n{raw[:500]}\n---")

    finally:
        # ── 6. 清理 ───────────────────────────────────────────────────
        log("── 清理 ──")

        # 关闭 PR
        if pr_number:
            r = api_call("PATCH",
                f"/api/v5/repos/{OWNER}/{REPO}/pulls/{pr_number}",
                data={"state": "closed"},
                use_contributor=True)
            log(f"   关闭 PR #{pr_number}: {'ok' if '_error' not in r else r.get('_error')}")

        # 删除 fork 分支
        if fork_dir and os.path.isdir(fork_dir):
            sh(f"git checkout {BRANCH}", cwd=fork_dir)
            sh(f"git push origin --delete {FEAT_BRANCH}", cwd=fork_dir)
            log(f"   删除 fork 分支 {FEAT_BRANCH}")

        # 删除 upstream 上的 demo workflow
        if wf_on_main and os.path.isdir(upstream_dir):
            wf_path = os.path.join(upstream_dir, ".gitcode", "workflows", WF_FILENAME)
            if os.path.exists(wf_path):
                sh(f"git rm {wf_path}", cwd=upstream_dir)
                sh('git commit -m "chore: remove demo workflow"', cwd=upstream_dir)
                sh(f"git push origin {BRANCH}", cwd=upstream_dir)
                log(f"   删除 upstream 上的 {WF_FILENAME}")

        shutil.rmtree(root, ignore_errors=True)
        log(f"   ✅ 清理完毕")

    return 0


if __name__ == "__main__":
    sys.exit(main())
