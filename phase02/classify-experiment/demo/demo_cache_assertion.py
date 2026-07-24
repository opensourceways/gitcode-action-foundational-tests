#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_cache_assertion.py — 验证 cache_pollution / cache_restore 断言可行性

目标: COMP-CACHE-01-003 (fork PR 不污染主分支 cache)
      SEC-CACHE-01-001 (fork PR cache 不可被主仓读取)

策略: push 触发 workflow，写 cache → 再跑一次读 cache → 验证缓存命中/隔离语义。
日志型 cache 验证：workflow 内 echo "CACHE_HIT=yes"/"CACHE_MISS=yes" → 断言扫描日志。

用法:
    cd phase02/classify-experiment/demo
    python3 demo_cache_assertion.py
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
                v = re.sub(r'\s+#.*$', '', v).strip().strip('"').strip("'")
                if k not in os.environ:
                    os.environ[k] = v

load_env()

TOKEN    = os.environ.get("GITCODE_ACCESS_TOKEN", "")
EXECUTOR = os.environ.get("GITCODE_EXECUTOR", "")
OWNER    = "ComputingActionTest"
REPO     = "foundational-tests"
BRANCH   = "main"

WF_WRITE = "demo-cache-write.yml"
WF_READ  = "demo-cache-read.yml"
CACHE_KEY = "demo-cache-key-v1"
POLL = 10
TIMEOUT = 300

# ── Workflow 1: 写缓存 ──
CACHE_WRITE_WF = f"""\
on:
  push:
    branches: [main]
jobs:
  write-cache:
    name: write-cache
    runs-on: [dedicate-hosted, x64, large]
    steps:
      - name: build
        run: |
          mkdir -p mycache
          echo "CACHE_VALUE_OK" > mycache/data.txt
          echo "BUILD_OK" >> mycache/data.txt
      - name: save cache
        uses: cache
        with:
          path: mycache
          key: {CACHE_KEY}
"""

# ── Workflow 2: 读缓存 ──
CACHE_READ_WF = f"""\
on:
  push:
    branches: [main]
jobs:
  read-cache:
    name: read-cache
    runs-on: [dedicate-hosted, x64, large]
    steps:
      - name: restore cache
        uses: cache
        with:
          path: mycache
          key: {CACHE_KEY}
      - name: verify
        run: |
          if [ -f mycache/data.txt ]; then
            echo "CACHE_HIT=yes"
            cat mycache/data.txt
          else
            echo "CACHE_MISS=yes"
          fi
"""


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def api_get(path):
    sep = "&" if "?" in path else "?"
    url = f"https://api.gitcode.com{path}{sep}access_token={TOKEN}&executor={EXECUTOR}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = r.read().decode("utf-8", errors="replace")
        # download_log returns text, not JSON
        if "download_log" in path or "download-log" in path:
            return resp
        try:
            return json.loads(resp)
        except json.JSONDecodeError:
            return {"_raw": resp}


def push_and_poll(filename, content):
    """Push workflow to main, poll for COMPLETED run, return logs."""
    root = tempfile.mkdtemp(prefix="demo-cache-")
    repo = os.path.join(root, "repo")
    url = f"https://oauth2:{TOKEN}@gitcode.com/{OWNER}/{REPO}.git"
    rc, out = sh(f'git clone --depth 1 --branch {BRANCH} "{url}" "{repo}"')
    assert rc == 0, f"clone failed: {out[-200:]}"

    wf_dir = os.path.join(repo, ".gitcode", "workflows")
    os.makedirs(wf_dir, exist_ok=True)
    with open(os.path.join(wf_dir, filename), "w", newline="\n") as f:
        f.write(content)
    sh("git add .gitcode/workflows/", cwd=repo)
    sh(f'git commit --allow-empty -m "demo: cache {filename}"', cwd=repo)
    rc, out = sh(f"git push origin {BRANCH}", cwd=repo)
    assert rc == 0, f"push failed: {out[-200:]}"
    log(f"   Pushed {filename}")

    rid = None
    t0 = time.time()
    while time.time() - t0 < TIMEOUT:
        data = api_get(f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=50")
        for r in data.get("workflow_runs", []):
            if filename in (r.get("file_path") or ""):
                if r.get("status") == "COMPLETED":
                    rid = r.get("workflow_run_id", "")
                    break
        if rid:
            break
        time.sleep(POLL)
    assert rid, "timeout"
    log(f"   Run {rid} = COMPLETED")

    # Get job logs
    detail = api_get(f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}")
    logs = ""
    stages = (detail.get("stages") or []) if isinstance(detail, dict) else []
    for stage in stages:
        for j in (stage.get("jobs") or []):
            jid = j.get("id", "")
            if jid:
                raw = api_get(f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{rid}/jobs/{jid}/download_log")
                logs += (raw if isinstance(raw, str) else "")
    log(f"   Logs: {len(logs)} chars")

    # Cleanup workflow file
    wf_path = os.path.join(repo, ".gitcode", "workflows", filename)
    sh(f"git rm {wf_path}", cwd=repo)
    sh(f'git commit -m "chore: rm {filename}"', cwd=repo)
    sh(f"git push origin {BRANCH}", cwd=repo)
    shutil.rmtree(root, ignore_errors=True)
    return rid, logs


def main():
    if not TOKEN:
        log("❌ 缺少 token")
        return 1

    log("=" * 60)
    log("CACHE ASSERTION 可行性验证")
    log("=" * 60)

    # ── Phase 1: Write cache ──
    log("── Phase 1: 写缓存 ──")
    rid1, logs1 = push_and_poll(WF_WRITE, CACHE_WRITE_WF)
    log(f"   Write run: {rid1}")
    if "BUILD_OK" in logs1 or "cache" in logs1.lower():
        log("   ✅ 缓存写入成功")

    # ── Phase 2: Read cache ──
    log("── Phase 2: 读缓存 (验证 cache hit) ──")
    time.sleep(5)  # 等缓存传播
    rid2, logs2 = push_and_poll(WF_READ, CACHE_READ_WF)
    log(f"   Read run: {rid2}")

    hit = "CACHE_HIT=yes" in logs2
    miss = "CACHE_MISS=yes" in logs2
    log(f"   Cache: HIT={hit} MISS={miss}")

    if hit:
        log("   ✅ 同仓库同 key cache hit 确认")
        if "CACHE_VALUE_OK" in logs2:
            log("   ✅ 缓存内容验证通过")
    elif miss:
        log("   ⚠️  Cache miss — 可能 cache 隔离或未命中")
    else:
        log(f"   ⚠️  日志中无 CACHE_HIT/CACHE_MISS 标记")
        log(f"   Logs preview: {logs2[:500]}")

    log("")
    log("=" * 60)
    log("cache_pollution 断言模式:")
    log("  Phase 1: fork PR 写缓存 (untrusted)")
    log("  Phase 2: 主仓 push 读缓存 (maintainer)")
    log("  断言: 主仓读缓存 MUST be MISS (CACHE_MISS=yes)")
    log("  如果命中 (CACHE_HIT=yes) → cache 隔离失效 → FAIL")
    log("")
    log("映射到 assertion_engine:")
    log("  kind: value  (扫描日志找 CACHE_HIT/CACHE_MISS)")
    log("  target: cache_restore / cache_pollution")
    log("  expect: CACHE_MISS=yes (positive: 隔离有效)")
    log("  forbidden: CACHE_HIT=yes (negative: 无命中=隔离到位)")
    log("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
