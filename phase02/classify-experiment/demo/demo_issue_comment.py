#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_issue_comment.py — 验证 `on: issue_comment` 触发能否自动脚本化

流程:
  1. Bot 推 workflow (on: issue_comment) 到 upstream main
  2. Bot 创建一个 issue
  3. Contributor 在 issue 下发评论 → 触发 workflow
  4. Bot 轮询 run
  5. 清理

用法:
    cd phase02/classify-experiment/demo
    python3 demo_issue_comment.py
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

TOKEN       = os.environ.get("GITCODE_ACCESS_TOKEN", "")
CONTRIB_TOKEN = os.environ.get("CONTRIBUTOR_GITCODE_TOKEN", "")
EXECUTOR    = os.environ.get("GITCODE_EXECUTOR", "")
OWNER       = "ComputingActionTest"
REPO        = "foundational-tests"
BRANCH      = "main"

WF_FILENAME = "demo-issue-comment.yml"
POLL = 10
TIMEOUT = 300

ISSUE_COMMENT_WF = """\
on:
  issue_comment:
    types:
      - created
jobs:
  comment-demo:
    name: issue-comment-trigger-test
    runs-on: [dedicate-hosted, x64, large]
    steps:
      - name: echo
        run: echo "ISSUE_COMMENT_TRIGGER_OK"
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


def main():
    if not TOKEN or not CONTRIB_TOKEN:
        log("❌ 缺少 token")
        return 1

    log("=" * 60)
    log("ISSUE_COMMENT 触发测试")
    log("=" * 60)
    root = tempfile.mkdtemp(prefix="demo-ic-")
    repo_dir = os.path.join(root, "repo")
    issue_number = None

    try:
        # ── 1. 推 workflow 到 main ──
        log("── 1. 推送 workflow 到 main ──")
        url = f"https://oauth2:{TOKEN}@gitcode.com/{OWNER}/{REPO}.git"
        rc, out = sh(f'git clone --depth 1 --branch {BRANCH} "{url}" "{repo_dir}"')
        if rc != 0:
            log(f"❌ clone 失败: {out[-200:]}")
            return 1

        wf_dir = os.path.join(repo_dir, ".gitcode", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        with open(os.path.join(wf_dir, WF_FILENAME), "w", newline="\n") as f:
            f.write(ISSUE_COMMENT_WF)
        sh("git add .gitcode/workflows/", cwd=repo_dir)
        sh('git commit --allow-empty -m "demo: issue_comment workflow"', cwd=repo_dir)
        rc, out = sh(f"git push origin {BRANCH}", cwd=repo_dir)
        if rc != 0:
            log(f"❌ push 失败: {out[-200:]}")
            return 1
        log("   ✅ 已推送")
        log("   等待平台索引 (30s)...")
        time.sleep(30)

        # ── 2. Bot 创建 issue ──
        log("── 2. Bot 创建 issue ──")
        issue_resp = api_call("POST",
            f"/api/v5/repos/{OWNER}/{REPO}/issues",
            data={
                "title": "[Demo] issue_comment trigger test",
                "body": "Platform test: issue_comment should trigger workflow.",
            })
        log(f"   issue API: {json.dumps({k:issue_resp.get(k) for k in ['id','number','iid','title','state'] if k in issue_resp}, ensure_ascii=False)}")
        if "_error" in issue_resp:
            log(f"❌ 创建 issue 失败: {issue_resp}")
            return 1
        issue_number = issue_resp.get("number") or issue_resp.get("iid")
        issue_id = issue_resp.get("id")
        log(f"   ✅ Issue #{issue_number} (id={issue_id})")

        # ── 3. Contributor 发评论 ──
        log("── 3. Contributor 发评论 ──")
        comment_resp = api_call("POST",
            f"/api/v5/repos/{OWNER}/{REPO}/issues/{issue_number}/comments",
            data={"body": "test comment to trigger issue_comment workflow"},
            use_contributor=True)
        log(f"   comment API: {json.dumps({k:comment_resp.get(k) for k in ['id','body'] if k in comment_resp}, ensure_ascii=False)[:200]}")
        if "_error" in comment_resp:
            log(f"❌ 发评论失败: {comment_resp}")
            return 1
        log(f"   ✅ 评论已发布")

        # ── 4. 轮询 run ──
        log("── 4. 轮询 run ──")
        t0 = time.time()
        while time.time() - t0 < TIMEOUT:
            data = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=100")
            for r in data.get("workflow_runs", []):
                if WF_FILENAME in (r.get("file_path") or ""):
                    s = r.get("status", "")
                    rid = r.get("workflow_run_id", "")
                    log(f"   ★ FOUND: run_id={rid} status={s}")
                    if s in ("COMPLETED", "FAILED", "CANCELED"):
                        log("   ✅ 终态！")
                        detail = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}")
                        stages = (detail.get("stages") or []) if isinstance(detail, dict) else []
                        for stage in stages:
                            for j in (stage.get("jobs") or []):
                                jid = j.get("id", "")
                                if jid:
                                    lr = api_call("GET", f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}/jobs/{jid}/download_log")
                                    raw = lr.get("_raw", "") if isinstance(lr, dict) else str(lr)
                                    if "ISSUE_COMMENT_TRIGGER_OK" in raw:
                                        log("   ✅ 日志: ISSUE_COMMENT_TRIGGER_OK")
                                    log(f"   log: {raw[:200]}")
                        log("   ✅ SUCCESS — issue_comment 触发脚本化可行")
                        return 0
            elapsed = int(time.time() - t0)
            if elapsed % 30 < POLL and elapsed > 0:
                log(f"   ⌛ {elapsed}s...")
            time.sleep(POLL)

        log(f"⚠️  超时 {TIMEOUT}s 未找到 run")
        return 1

    finally:
        log("── 清理 ──")
        # Close issue
        if issue_number:
            r = api_call("PATCH", f"/api/v5/repos/{OWNER}/{REPO}/issues/{issue_number}",
                         data={"state": "closed"})
            log(f"   关闭 issue: {'ok' if '_error' not in r else r.get('_error')}")
        # Remove workflow
        if os.path.isdir(repo_dir):
            wf = os.path.join(repo_dir, ".gitcode", "workflows", WF_FILENAME)
            if os.path.exists(wf):
                sh(f"git rm {wf}", cwd=repo_dir)
                sh('git commit -m "chore: rm issue_comment demo"', cwd=repo_dir)
                sh(f"git push origin {BRANCH}", cwd=repo_dir)
                log("   清理完毕")
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
