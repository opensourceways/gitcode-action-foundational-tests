#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_artifact_assertion.py — 验证 artifact_download 断言可行性

目标: SEC-ARTF-01-001 需要验证 fork PR 的 artifact 不可被主仓下载。
但由于平台不触发非 push 事件，这里先验证核心能力：
  1. push workflow 触发 → 上传 artifact → API 列出 → 下载 → 校验内容
  2. 展示如何映射到 assertion_engine 的判定格式

用法:
    cd phase02/classify-experiment/demo
    python3 demo_artifact_assertion.py
"""

import os, sys, json, re, time, shutil, subprocess, tempfile, urllib.request, zipfile, io

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

WF_FILENAME = "demo-artifact-assert.yml"
POLL   = 10
TIMEOUT = 300

# 上传 artifact 的 workflow（push 触发）
ARTIFACT_WF = """\
on:
  push:
    branches: [main]
jobs:
  upload-artifact:
    name: upload-test-artifact
    runs-on: [dedicate-hosted, x64, large]
    steps:
      - name: create file
        run: |
          echo "ARTIFACT_CONTENT_OK" > demo-artifact.txt
          echo "timestamp=$(date +%s)" >> demo-artifact.txt
      - name: upload
        uses: upload-artifact
        with:
          name: demo-artifact
          path: demo-artifact.txt
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
        return json.loads(r.read().decode("utf-8", errors="replace"))


def api_download_raw(path):
    """Download raw bytes (for artifact zip)."""
    sep = "&" if "?" in path else "?"
    url = f"https://api.gitcode.com{path}{sep}access_token={TOKEN}&executor={EXECUTOR}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    if not TOKEN:
        log("❌ 缺少 token")
        return 1

    log("=" * 60)
    log("ARTIFACT ASSERTION 可行性验证")
    log("=" * 60)
    root = tempfile.mkdtemp(prefix="demo-art-")
    repo_dir = os.path.join(root, "repo")

    try:
        # ── 1. Push artifact workflow to main ──
        log("── 1. Push workflow ──")
        url = f"https://oauth2:{TOKEN}@gitcode.com/{OWNER}/{REPO}.git"
        rc, out = sh(f'git clone --depth 1 --branch {BRANCH} "{url}" "{repo_dir}"')
        if rc != 0:
            log(f"❌ clone 失败: {out[-200:]}")
            return 1

        wf_dir = os.path.join(repo_dir, ".gitcode", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        with open(os.path.join(wf_dir, WF_FILENAME), "w", newline="\n") as f:
            f.write(ARTIFACT_WF)
        sh("git add .gitcode/workflows/", cwd=repo_dir)
        sh('git commit --allow-empty -m "demo: artifact assertion"', cwd=repo_dir)
        rc, out = sh(f"git push origin {BRANCH}", cwd=repo_dir)
        if rc:
            log(f"❌ push 失败: {out[-200:]}")
            return 1
        log("   ✅ 已推送")

        # ── 2. Poll for run ──
        log("── 2. 轮询 run ──")
        run_id = None
        t0 = time.time()
        while time.time() - t0 < TIMEOUT:
            data = api_get(f"/api/v8/repos/{OWNER}/{REPO}/actions/runs?per_page=50")
            for r in data.get("workflow_runs", []):
                if WF_FILENAME in (r.get("file_path") or ""):
                    s = r.get("status", "")
                    rid = r.get("workflow_run_id", "")
                    if s == "COMPLETED":
                        run_id = rid
                        log(f"   ✅ Run {run_id} = COMPLETED")
                        break
            if run_id:
                break
            time.sleep(POLL)

        if not run_id:
            log("❌ 超时未找到 COMPLETED run")
            return 1

        # ── 3. List artifacts for this run ──
        log("── 3. 列出 artifact ──")
        art_list = api_get(f"/api/v8/repos/{OWNER}/{REPO}/actions/runs/{run_id}/artifacts")
        artifacts = art_list.get("artifacts", []) if isinstance(art_list, dict) else art_list
        if not isinstance(artifacts, list):
            # Some APIs wrap differently
            artifacts = (art_list.get("data") or []) if isinstance(art_list, dict) else []
        log(f"   Found {len(artifacts)} artifacts:")
        for a in artifacts:
            log(f"     id={a.get('id')} name={a.get('name')} size={a.get('size_in_bytes')}")

        if not artifacts:
            log("⚠️  无 artifact（可能 upload-artifact action 不支持）")
            return 1

        # ── 4. Download artifact ──
        log("── 4. 下载 artifact ──")
        art = artifacts[0]
        art_id = art.get("id") or art.get("artifact_id")
        art_name = art.get("name", "?")

        # Try multiple download URL patterns
        downloaded = False
        for fmt in ["zip", "raw"]:
            try:
                raw = api_download_raw(
                    f"/api/v8/repos/{OWNER}/{REPO}/actions/artifacts/{art_id}/{fmt}")
                log(f"   Downloaded via /{fmt}: {len(raw)} bytes")
                if len(raw) > 100:
                    # Try to parse as zip
                    try:
                        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                            for name in zf.namelist():
                                content = zf.read(name).decode("utf-8", errors="replace")
                                log(f"   Zip entry '{name}': {content[:200]}")
                                if "ARTIFACT_CONTENT_OK" in content:
                                    log("   ✅ 校验通过: ARTIFACT_CONTENT_OK")
                                    downloaded = True
                    except zipfile.BadZipFile:
                        log(f"   Raw content: {raw[:200].decode('utf-8', errors='replace')}")
                        if b"ARTIFACT_CONTENT_OK" in raw:
                            log("   ✅ 校验通过: ARTIFACT_CONTENT_OK")
                            downloaded = True
                    break
            except Exception as e:
                log(f"   Download via /{fmt}: {e}")

        if downloaded:
            log("")
            log("=" * 60)
            log("✅ artifact_download 断言可行")
            log("   API: GET /api/v8/.../artifacts/:id/:format")
            log("   可用于: SEC-ARTF-01-001 (fork PR artifact 隔离)")
            log("")
            log("断言引擎映射:")
            log("  kind: artifact_download")
            log("  target: artifact_download")
            log("  equals: 404_or_permission_denied  (negative case: 主仓不应能下载)")
            log("  must_not_equal: success             (negative: 下载不应成功)")
            log("=" * 60)
        else:
            log("⚠️  下载格式待确认")

    finally:
        # Cleanup
        if os.path.isdir(repo_dir):
            wf = os.path.join(repo_dir, ".gitcode", "workflows", WF_FILENAME)
            if os.path.exists(wf):
                sh(f"git rm {wf}", cwd=repo_dir)
                sh('git commit -m "chore: rm artifact demo"', cwd=repo_dir)
                sh(f"git push origin {BRANCH}", cwd=repo_dir)
                log("   清理完毕")
        shutil.rmtree(root, ignore_errors=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
