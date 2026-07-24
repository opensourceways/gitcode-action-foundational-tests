#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_pull_request_target.py — 验证 `on: pull_request_target` 触发

流程同 fork PR 但 YAML 改用 `pull_request_target` 触发器。
pull_request_target 运行在 base 分支上下文、可访问 secrets。

用法:
    cd phase02/classify-experiment/demo
    python3 demo_pull_request_target.py
"""

import os, sys, json, re, time, shutil, subprocess, tempfile, urllib.request

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

TOKEN         = os.environ.get("GITCODE_ACCESS_TOKEN", "")
CONTRIB_TOKEN = os.environ.get("CONTRIBUTOR_GITCODE_TOKEN", "")
EXECUTOR      = os.environ.get("GITCODE_EXECUTOR", "")
OWNER         = "ComputingActionTest"
REPO          = "foundational-tests"
BRANCH        = "main"

WF_FILENAME   = "demo-pr-target.yml"
FEAT_BRANCH   = f"demo/pr-target-{int(time.time()) % 100000}"
POLL          = 10
TIMEOUT       = 300

PR_TARGET_WF = """\
on:
  pull_request_target:
    types:
      - open
      - update
      - reopen
    branches: [main]
jobs:
  target-demo:
    name: pr-target-trigger-test
    runs-on: [dedicate-hosted, x64, large]
    steps:
      - name: echo context
        run: |
          echo "PR_TARGET_TRIGGER_OK"
          echo "EVENT=${{ atomgit.event_name }}"
"""


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def api_call(method, path, data=None, use_contributor=False):
    token = CONTRIB_TOKEN if use_contributor else TOKEN
    sep = "&" if "?" in path else "?"
    url = f"https://api.gitcode.com{path}{sep}access_token={token}"
    if not use_contributor and "/api/v8/" in path and EXECUTOR:
        url += f"&executor={EXECUTOR}"

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"_error": f"HTTP {e.code}", "_raw": body[:300]}
    except Exception as e:
        return {"_error": str(e)}


def git_clone(owner, repo, token, branch, target_dir):
    url = f"https://oauth2:{token}@gitcode.com/{owner}/{repo}.git"
    rc, out = sh(f'git clone --depth 1 --branch {branch} "{url}" "{target_dir}"')
    return rc == 0


def main():
    if not TOKEN or not CONTRIB_TOKEN:
        log("❌ 缺少 token")
        return 1

    log("=" * 60)
    log("PULL_REQUEST_TARGET 触发测试 (fork PR)")
    log("=" * 60)
    root = tempfile.mkdtemp(prefix="demo-pt-")
    upstream_dir = os.path.join(root, "upstream")
    fork_dir = os.path.join(root, "fork")
    pr_number = None

    try:
        # ── 1. Push workflow to main ──
        log("── 1. 推送 pull_request_target workflow 到 main ──")
        if not git_clone(OWNER, REPO, TOKEN, BRANCH, upstream_dir):
            return 1
        wf_dir = os.path.join(upstream_dir, ".gitcode", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        with open(os.path.join(wf_dir, WF_FILENAME), "w", newline="\n") as f:
            f.write(PR_TARGET_WF)
        sh("git add .gitcode/workflows/", cwd=upstream_dir)
        sh('git commit --allow-empty -m "demo: pull_request_target workflow"', cwd=upstream_dir)
        rc, out = sh(f"git push origin {BRANCH}", cwd=upstream_dir)
        if rc:
            log(f"❌ push 失败: {out[-200:]}")
            return 1
        log("   ✅ 已推送，等待索引 (30s)...")
        time.sleep(30)

        # ── 2. Find fork ──
        log("── 2. 查找 contributor fork ──")
        fork_full_name = None
        fork_owner = None
        forks = api_call("GET", f"/api/v5/repos/{OWNER}/{REPO}/forks?per_page=20")
        if isinstance(forks, list):
            for fk in forks:
                log(f"   ... {fk.get('full_name')}")
                if fk.get("full_name", "").startswith("teamfi"):
                    fork_full_name = fk.get("full_name")
                    ns = fk.get("owner") or fk.get("namespace") or {}
                    fork_owner = (ns if isinstance(ns, dict) else {}).get("login", "") or "teamfi"
                    break
        if not fork_full_name:
            log("❌ 找不到 fork，请手动创建: teamfi/foundational-tests")
            return 1
        log(f"   ✅ Fork: {fork_full_name}")

        # ── 3. Clone fork, create branch, push ──
        log(f"── 3. Clone fork + 创建 {FEAT_BRANCH} ──")
        time.sleep(10)  # wait for fork to be ready
        if not git_clone(fork_owner, REPO, CONTRIB_TOKEN, BRANCH, fork_dir):
            return 1
        sh(f"git checkout -b {FEAT_BRANCH}", cwd=fork_dir)
        with open(os.path.join(fork_dir, "pr-target-demo.txt"), "w") as f:
            f.write(f"test at {time.ctime()}\n")
        sh("git add pr-target-demo.txt", cwd=fork_dir)
        sh('git commit -m "demo: PR target trigger"', cwd=fork_dir)
        rc, out = sh(f"git push origin {FEAT_BRANCH}", cwd=fork_dir)
        if rc:
            log(f"❌ push 分支失败: {out[-200:]}")
            return 1
        log(f"   ✅ 已 push")

        # ── 4. Create cross-repo PR ──
        log("── 4. 创建 fork PR ──")
        pr_resp = api_call("POST",
            f"/api/v5/repos/{OWNER}/{REPO}/pulls",
            data={
                "title": "[Demo] pull_request_target test",
                "head": f"{fork_owner}:{FEAT_BRANCH}",
                "base": BRANCH,
                "body": "Testing on: pull_request_target trigger from fork PR",
            },
            use_contributor=True)
        log(f"   PR: {json.dumps({k:pr_resp.get(k) for k in ['id','iid','number','state'] if k in pr_resp}, ensure_ascii=False)}")
        if "_error" in pr_resp:
            log(f"❌ 创建 PR 失败: {pr_resp}")
            return 1
        pr_number = pr_resp.get("number") or pr_resp.get("iid")
        log(f"   ✅ PR #{pr_number}")

        # ── 5. Poll ──
        log("── 5. 轮询 run ──")
        t0 = time.time()
        while time.time() - t0 < TIMEOUT:
            data = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=100&pull_request_id={pr_number}")
            for r in data.get("workflow_runs", []):
                s = r.get("status", "")
                rid = r.get("workflow_run_id", "")
                log(f"   ★ FOUND: run_id={rid} status={s}")
                if s in ("COMPLETED", "FAILED", "CANCELED"):
                    log(f"   ✅ 终态！")
                    detail = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}")
                    stages = (detail.get("stages") or []) if isinstance(detail, dict) else []
                    for stage in stages:
                        for j in (stage.get("jobs") or []):
                            jid = j.get("id", "")
                            if jid:
                                lr = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}/jobs/{jid}/download_log")
                                raw = lr.get("_raw", "") if isinstance(lr, dict) else str(lr)
                                if "PR_TARGET_TRIGGER_OK" in raw:
                                    log("   ✅ 日志: PR_TARGET_TRIGGER_OK")
                                log(f"   log: {raw[:200]}")
                    log("   ✅ SUCCESS — pull_request_target 触发脚本化可行")
                    return 0
            elapsed = int(time.time() - t0)
            if elapsed % 30 < POLL and elapsed > 0:
                # 后备扫描
                all_runs = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=50")
                for r in (all_runs.get("workflow_runs", []) if isinstance(all_runs, dict) else []):
                    if WF_FILENAME in (r.get("file_path") or ""):
                        s = r.get("status", "")
                        log(f"   文件匹配: run_id={r.get('workflow_run_id')} status={s}")
                log(f"   ⌛ {elapsed}s...")
            time.sleep(POLL)

        log(f"⚠️  超时 {TIMEOUT}s 未找到 run")
        return 1

    finally:
        log("── 清理 ──")
        if pr_number:
            r = api_call("PATCH", f"/api/v5/repos/{OWNER}/{REPO}/pulls/{pr_number}",
                         data={"state": "closed"}, use_contributor=True)
            log(f"   关闭 PR #{pr_number}: {'ok' if '_error' not in r else r.get('_error')}")
        if os.path.isdir(fork_dir):
            sh(f"git checkout {BRANCH}", cwd=fork_dir)
            sh(f"git push origin --delete {FEAT_BRANCH}", cwd=fork_dir)
        if os.path.isdir(upstream_dir):
            wf = os.path.join(upstream_dir, ".gitcode", "workflows", WF_FILENAME)
            if os.path.exists(wf):
                sh(f"git rm {wf}", cwd=upstream_dir)
                sh('git commit -m "chore: rm pr_target demo"', cwd=upstream_dir)
                sh(f"git push origin {BRANCH}", cwd=upstream_dir)
                log("   清理完毕")
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
