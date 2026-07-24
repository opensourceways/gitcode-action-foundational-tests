#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_schedule.py — 验证 `on: schedule` cron 触发能否自动脚本化

策略: 推一个每分钟后触发的 cron (秒级粒度的最短间隔)，轮询等待 run。

用法:
    cd phase02/classify-experiment/demo
    python3 demo_schedule.py
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

TOKEN    = os.environ.get("GITCODE_ACCESS_TOKEN", "")
EXECUTOR = os.environ.get("GITCODE_EXECUTOR", "")
OWNER    = "ComputingActionTest"
REPO     = "foundational-tests"
BRANCH   = "main"

WF_FILENAME = "demo-schedule.yml"
POLL = 15
TIMEOUT = 600  # 10 min for cron to fire

SCHEDULE_WF = """\
on:
  schedule:
    - cron: "* * * * *"
jobs:
  cron-demo:
    name: schedule-cron-test
    runs-on: [dedicate-hosted, x64, large]
    steps:
      - name: echo
        run: echo "SCHEDULE_TRIGGER_OK"
"""

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout or "") + (r.stderr or "")

def api_get(path):
    sep = "&" if "?" in path else "?"
    url = f"https://api.gitcode.com{path}{sep}access_token={TOKEN}&executor={EXECUTOR}"
    r = urllib.request.urlopen(urllib.request.Request(url), timeout=15)
    return json.loads(r.read().decode("utf-8"))

def main():
    if not TOKEN:
        log("❌ 缺少 token")
        return 1

    log("=" * 60)
    log("SCHEDULE 触发测试")
    log("=" * 60)
    root = tempfile.mkdtemp(prefix="demo-sched-")
    repo_dir = os.path.join(root, "repo")

    try:
        url = f"https://oauth2:{TOKEN}@gitcode.com/{OWNER}/{REPO}.git"
        rc, out = sh(f'git clone --depth 1 --branch {BRANCH} "{url}" "{repo_dir}"')
        if rc != 0:
            log(f"❌ clone 失败: {out[-200:]}")
            return 1

        # Push schedule workflow
        wf_dir = os.path.join(repo_dir, ".gitcode", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        with open(os.path.join(wf_dir, WF_FILENAME), "w", newline="\n") as f:
            f.write(SCHEDULE_WF)

        sh("git add .gitcode/workflows/", cwd=repo_dir)
        sh('git commit --allow-empty -m "demo: schedule cron test"', cwd=repo_dir)
        rc, out = sh(f"git push origin {BRANCH}", cwd=repo_dir)
        if rc != 0:
            log(f"❌ push 失败: {out[-200:]}")
            return 1
        log("✅ Cron workflow 已推送到 main (* * * * *)")

        # Poll
        log(f"轮询 (最多 {TIMEOUT}s)...")
        t0 = time.time()
        while time.time() - t0 < TIMEOUT:
            data = api_get(f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=50")
            for r in data.get("workflow_runs", []):
                if WF_FILENAME in (r.get("file_path") or ""):
                    s = r.get("status", "")
                    rid = r.get("workflow_run_id", "")
                    log(f"  ★ FOUND: run_id={rid} status={s} event={r.get('event')}")
                    if s in ("COMPLETED", "FAILED", "CANCELED"):
                        log(f"  ✅ 终态！")
                        # Get logs
                        detail = api_get(f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}")
                        stages = (detail.get("stages") or []) if isinstance(detail, dict) else []
                        for stage in stages:
                            for j in (stage.get("jobs") or []):
                                jid = j.get("id", "")
                                if jid:
                                    log_resp = api_get(f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}/jobs/{jid}/download_log")
                                    raw = log_resp.get("_raw", "") if isinstance(log_resp, dict) else str(log_resp)
                                    if "SCHEDULE_TRIGGER_OK" in raw:
                                        log("  ✅ 日志确认: SCHEDULE_TRIGGER_OK")
                                    log(f"  log preview: {raw[:200]}")
                        return 0
            elapsed = int(time.time() - t0)
            if elapsed % 60 < POLL and elapsed > 0:
                log(f"  ⌛ {elapsed}s...")
            time.sleep(POLL)

        log(f"⚠️  超时 {TIMEOUT}s 未等到 schedule run")
        return 1

    finally:
        # Cleanup
        if os.path.isdir(repo_dir):
            wf_path = os.path.join(repo_dir, ".gitcode", "workflows", WF_FILENAME)
            if os.path.exists(wf_path):
                sh(f"git rm {wf_path}", cwd=repo_dir)
                sh('git commit -m "chore: rm schedule demo"', cwd=repo_dir)
                sh(f"git push origin {BRANCH}", cwd=repo_dir)
                log("  清理完成")
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
