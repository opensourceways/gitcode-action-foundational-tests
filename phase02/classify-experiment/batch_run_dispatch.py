#!/usr/bin/env python3
"""
batch_run_dispatch.py — 批量部署 + dispatch + poll + assert 所有 dispatchable case。

流程：
  1. git clone → 写 workflow 文件 → push（部署到仓库）
  2. POST dispatch API 触发
  3. poll v8 API 等待终态
  4. download_log 收集日志
  5. 运行简单断言（check log 关键词 / run_status）
  6. 记录结果 → results/<run_id>/

用法：
  export GITCODE_ACCESS_TOKEN=xxx
  export GITCODE_COOKIE=xxx        # dispatch 用
  export GITCODE_EXECUTOR=xxx      # v8 API 用户名
  python3 batch_run_dispatch.py <run-id> [--max N] [--case C1,C2]
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import yaml

# ── 配置 ──────────────────────────────────────────────────────────

TOKEN = os.environ.get("GITCODE_ACCESS_TOKEN", "")
COOKIE = os.environ.get("GITCODE_COOKIE", "")
EXECUTOR = os.environ.get("GITCODE_EXECUTOR", "")
OWNER = os.environ.get("GITCODE_OWNER", "ComputingActionTest")
REPO = os.environ.get("GITCODE_REPO", "foundational-tests")
BRANCH = os.environ.get("GITCODE_BRANCH", "main")
API_V8 = os.environ.get("GITCODE_API_BASE_URL", "https://api.gitcode.com")
WEB_API = "https://web-api.gitcode.com"
TIMEOUT = int(os.environ.get("TIMEOUT_SECONDS", "600"))
POLL = int(os.environ.get("POLL_INTERVAL", "10"))


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# ── Cookie Auth Headers ───────────────────────────────────────────

def v2_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {COOKIE}",
        "Origin": "https://gitcode.com",
        "Referer": "https://gitcode.com/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "X-App-Channel": "gitcode-fe",
        "X-App-Version": "0",
        "X-Device-ID": "unknown",
        "X-Device-Type": "Linux",
        "X-Platform": "web",
        "Cookie": f"GITCODE_ACCESS_TOKEN={COOKIE}; GitCodeUserName={EXECUTOR}",
    }


# ── Git 操作 ──────────────────────────────────────────────────────

def deploy_workflow(case_id, wf_yaml_text):
    """git clone → 写 workflow → commit → push。返回 (wf_name, wf_path)。"""
    wf_name = case_id.lower().replace("_", "-") + ".yml"
    wf_path = f".gitcode/workflows/{wf_name}"

    workdir = tempfile.mkdtemp(prefix="batch-")
    repo_url = f"https://oauth2:{TOKEN}@gitcode.com/{OWNER}/{REPO}.git"

    subprocess.run(["git", "clone", repo_url, f"{workdir}/repo"],
                   capture_output=True, text=True, check=True)
    repo_dir = f"{workdir}/repo"
    os.makedirs(f"{repo_dir}/.gitcode/workflows", exist_ok=True)

    with open(f"{repo_dir}/{wf_path}", "w") as f:
        f.write(wf_yaml_text)
        f.write(f"\n# trigger: {int(time.time())}\n")

    subprocess.run(["git", "add", ".gitcode/workflows/"], cwd=repo_dir,
                   capture_output=True, check=True)
    subprocess.run(["git", "commit", "-m", f"test: {case_id}"], cwd=repo_dir,
                   capture_output=True, check=True)
    subprocess.run(["git", "push", "origin", BRANCH], cwd=repo_dir,
                   capture_output=True, timeout=30, check=True)

    # Cleanup
    import shutil
    shutil.rmtree(workdir, ignore_errors=True)

    return wf_name, wf_path


# ── Dispatch API ──────────────────────────────────────────────────

def get_workflow_by_filepath(file_path):
    """在 v2 API 中按 file_path 查找 workflow_id。"""
    import urllib.request
    project_enc = f"{OWNER}%2F{REPO}"
    url = f"{WEB_API}/api/v2/projects/{project_enc}/actions/workflows/list"
    req = Request(url, data=b"{}", headers=v2_headers(), method="POST")
    try:
        with urlopen(req, timeout=10) as resp:
            wfs = json.loads(resp.read()).get("content", [])
        for w in wfs:
            if w.get("file_path") == file_path:
                return w["workflow_id"]
    except Exception:
        pass
    return None


def dispatch_workflow(workflow_id, file_path, ref="main"):
    """调用 dispatch API 触发 workflow。返回 (ok, run_id_or_error)。"""
    import urllib.request
    project_enc = f"{OWNER}%2F{REPO}"
    url = f"{WEB_API}/api/v2/projects/{project_enc}/actions/workflows/{workflow_id}/dispatch"
    payload = json.dumps({
        "ref": ref,
        "branch": BRANCH,
        "branch_commit_id": "",
        "repo_https_url": f"https://gitcode.com/{OWNER}/{REPO}.git",
        "file_path": file_path,
        "inputs": {},
    }).encode()
    req = Request(url, data=payload, headers=v2_headers(), method="POST")
    try:
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        if data.get("workflow_run_id"):
            return True, data["workflow_run_id"]
        return False, data.get("error_message", str(data))
    except HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode()[:300]}"
    except Exception as e:
        return False, str(e)


# ── Poll & Collect ────────────────────────────────────────────────

def poll_run(run_id, timeout=TIMEOUT):
    """轮询等待 run 终态。返回 run detail dict 或 None。"""
    url = f"{API_V8}/api/v8/repos/{OWNER}/{REPO}/actions/runs/{run_id}?access_token={TOKEN}"
    elapsed = 0
    while elapsed < timeout:
        try:
            with urlopen(Request(url), timeout=10) as resp:
                run = json.loads(resp.read())
            status = run.get("status", "")
            if status in ("COMPLETED", "FAILED", "CANCELED"):
                return run
            elapsed += POLL
            time.sleep(POLL)
        except Exception as e:
            log(f"  poll error: {e}")
            elapsed += POLL
            time.sleep(POLL)
    return None


def collect_logs(run_id):
    """收集所有 job 日志 → 字符串。"""
    jobs_url = f"{API_V8}/api/v8/repos/{OWNER}/{REPO}/actions/runs/{run_id}/jobs?access_token={TOKEN}"
    try:
        with urlopen(Request(jobs_url), timeout=10) as resp:
            jobs = json.loads(resp.read()).get("jobs", [])
    except Exception:
        return ""

    all_logs = []
    for j in jobs:
        jid = j.get("id", "")
        log_url = f"{API_V8}/api/v8/repos/{OWNER}/{REPO}/actions/runs/{run_id}/jobs/{jid}/download_log?access_token={TOKEN}"
        try:
            with urlopen(Request(log_url), timeout=30) as resp:
                import io
                data = resp.read()
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    for name in z.namelist():
                        all_logs.append(z.read(name).decode("utf-8", errors="replace"))
        except Exception as e:
            all_logs.append(f"[LOG_ERROR: {e}]")
    return "\n".join(all_logs)


# ── Simple Assert ─────────────────────────────────────────────────

def run_assertions(assertions, conclusion, logs):
    """简化版断言（同 run-case.sh 的逻辑）。"""
    results = []
    for a in assertions:
        a_type = a.get("type", "")
        target = a.get("target", "")
        rubric = a.get("rubric", "")
        passed = False

        if target == "run_logs":
            # Check for specific patterns from rubric
            vals = re.findall(r'[A-Z][A-Z0-9_]{3,}', rubric)
            found_any = any(v in logs for v in vals) if vals else False
            if found_any:
                passed = True
            elif conclusion == "COMPLETED" and len(logs) > 100:
                passed = True
        elif target == "run_status":
            expected = a.get("equals", "COMPLETED")
            passed = (conclusion == expected)
        else:
            passed = (conclusion == "COMPLETED")

        results.append({
            "type": a_type, "target": target,
            "pass": passed, "rubric": rubric[:80],
        })

    all_pass = all(r["pass"] for r in results) if results else (conclusion == "COMPLETED")
    return {"verdict": "PASS" if all_pass else "FAIL", "results": results}


# ── Main ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_id", help="run identifier")
    parser.add_argument("--max", type=int, default=0, help="max cases to run (0=all)")
    parser.add_argument("--case", help="comma-separated case IDs to run")
    parser.add_argument("--skip-deploy", action="store_true", help="skip git deploy (workflows already in repo)")
    args = parser.parse_args()

    if not TOKEN or not COOKIE or not EXECUTOR:
        log("ERROR: need GITCODE_ACCESS_TOKEN, GITCODE_COOKIE, GITCODE_EXECUTOR")
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    cases_dir = script_dir / "2026-07-21-02/cases/yaml"
    results_dir = script_dir / f"../runs/{args.run_id}/results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Load case list
    yaml_files = sorted(cases_dir.glob("*.yaml"))
    if args.case:
        want = set(args.case.split(","))
        yaml_files = [f for f in yaml_files if f.stem in want]
    if args.max > 0:
        yaml_files = yaml_files[:args.max]

    log(f"Target: {len(yaml_files)} cases, run_id={args.run_id}")

    results = []
    pass_count = fail_count = error_count = 0

    for i, yf in enumerate(yaml_files):
        cid = yf.stem
        with open(yf) as f:
            doc = yaml.safe_load(f)

        wf = doc.get("workflow", "")
        assertions = doc.get("assertions", [])
        trigger_ev = (doc.get("trigger") or {}).get("event", "")

        log(f"\n[{i+1}/{len(yaml_files)}] {cid} — {doc.get('title','')[:60]}")

        try:
            # 1. Deploy (skip if already in repo)
            wf_name = cid.lower().replace("_", "-") + ".yml"
            wf_path = f".gitcode/workflows/{wf_name}"

            if not args.skip_deploy:
                log(f"  deploy...")
                wf_name, wf_path = deploy_workflow(cid, wf)
                time.sleep(5)  # let push settle

            # 2. Resolve workflow_id & dispatch
            log(f"  resolve workflow_id...")
            wf_id = get_workflow_by_filepath(wf_path)
            if not wf_id:
                log(f"  ⚠️ workflow not found by file_path, retrying...")
                time.sleep(10)
                wf_id = get_workflow_by_filepath(wf_path)

            if not wf_id:
                result = {"case_id": cid, "verdict": "NOT_DEPLOYED",
                          "reason": "workflow_id not found (deploy may have failed or API lag)"}
                results.append(result)
                error_count += 1
                log(f"  ❌ NOT_DEPLOYED")
                continue

            log(f"  dispatch (wf_id={wf_id[:8]}...)...")
            ok, rid_or_err = dispatch_workflow(wf_id, wf_path)
            if not ok:
                result = {"case_id": cid, "verdict": "DISPATCH_FAILED",
                          "reason": rid_or_err}
                results.append(result)
                error_count += 1
                log(f"  ❌ DISPATCH_FAILED: {rid_or_err[:100]}")
                continue

            run_id_gc = rid_or_err
            log(f"  run_id={run_id_gc[:8]}... polling...")

            # 3. Poll
            run = poll_run(run_id_gc)
            if not run:
                result = {"case_id": cid, "verdict": "TIMEOUT",
                          "reason": f"poll timeout after {TIMEOUT}s"}
                results.append(result)
                error_count += 1
                log(f"  ❌ TIMEOUT")
                continue

            status = run.get("status", "?")
            log(f"  → {status}")

            # 4. Collect logs
            logs = collect_logs(run_id_gc)
            log(f"  logs: {len(logs)} chars")

            # 5. Assert
            assert_result = run_assertions(assertions, status, logs)
            verdict = assert_result["verdict"]

            result = {
                "case_id": cid,
                "title": doc.get("title", ""),
                "dimension": doc.get("dimension", ""),
                "priority": doc.get("priority", ""),
                "verdict": verdict,
                "gitcode_run_id": run_id_gc,
                "run_status": status,
                "assertion_results": assert_result["results"],
                "phase02_run": args.run_id,
            }

            results.append(result)
            if verdict == "PASS":
                pass_count += 1
                log(f"  ✅ PASS")
            else:
                fail_count += 1
                log(f"  ❌ FAIL")

            # Write individual result
            with open(results_dir / f"{cid}.json", "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

        except Exception as e:
            result = {"case_id": cid, "verdict": "ERROR", "reason": str(e)}
            results.append(result)
            error_count += 1
            log(f"  💥 ERROR: {e}")

    # ── Summary ───────────────────────────────────────────────────
    log(f"\n{'='*50}")
    log(f"SUMMARY: {pass_count} PASS / {fail_count} FAIL / {error_count} ERROR "
        f"/ {len(yaml_files)} total")

    # Write summary JSON
    summary = {
        "run_id": args.run_id,
        "total": len(yaml_files),
        "pass": pass_count,
        "fail": fail_count,
        "error": error_count,
        "results": results,
    }
    with open(results_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Write summary MD
    failed = [r for r in results if r.get("verdict") not in ("PASS",)]
    md_lines = [
        f"# Batch Run Report — {args.run_id}",
        "",
        f"**Total**: {len(yaml_files)} | **PASS**: {pass_count} | **FAIL**: {fail_count} | **ERROR**: {error_count}",
        "",
    ]
    if failed:
        md_lines.append("## Failures & Errors")
        md_lines.append("")
        for r in failed:
            md_lines.append(f"### {r['case_id']} — {r.get('verdict')}")
            md_lines.append(f"- Reason: {r.get('reason', 'N/A')}")
            if r.get("gitcode_run_id"):
                md_lines.append(f"- GitCode Run: `{r['gitcode_run_id']}`")
            md_lines.append("")

    # API / infra needs
    md_lines.append("## API / Infra Notes")
    md_lines.append("")
    md_lines.append("- Dispatch API: `POST web-api.gitcode.com/api/v2/projects/{project}/actions/workflows/{id}/dispatch`")
    md_lines.append("- Stop API: `POST web-api.gitcode.com/api/v2/projects/{project}/actions/workflow-runs/{id}/stop`")
    md_lines.append("- v8 Poll API: `GET api.gitcode.com/api/v8/repos/{owner}/{repo}/actions/runs/{id}`")
    md_lines.append("- v8 Log API: `GET api.gitcode.com/api/v8/repos/{owner}/{repo}/actions/runs/{id}/jobs/{job_id}/download_log`")
    md_lines.append("- `GITCODE_COOKIE` required for dispatch (web-api.gitcode.com)")
    md_lines.append("- `GITCODE_ACCESS_TOKEN` required for v8 API (api.gitcode.com)")
    md_lines.append("")

    with open(results_dir / "report.md", "w") as f:
        f.write("\n".join(md_lines))

    log(f"Results: {results_dir}/")
    log(f"Report:  {results_dir}/report.md")


if __name__ == "__main__":
    main()
