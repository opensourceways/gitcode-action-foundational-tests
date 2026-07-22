#!/usr/bin/env python3
"""
batch_run_dispatch_v2.py — 批量部署 + dispatch + poll + collect 所有 dispatchable case。

用法:
  export GITCODE_ACCESS_TOKEN=xxx
  export GITCODE_COOKIE=xxx
  export GITCODE_EXECUTOR=ccijunk
  python3 batch_run_dispatch_v2.py <run-id> [--max N]
"""

import argparse, json, os, shutil, subprocess, sys, tempfile, time, zipfile
from datetime import datetime
from pathlib import Path
import io
import requests
import yaml

TOKEN = os.environ.get("GITCODE_ACCESS_TOKEN", "")
COOKIE = os.environ.get("GITCODE_COOKIE", "")
EXECUTOR = os.environ.get("GITCODE_EXECUTOR", "ccijunk")
OWNER = "ComputingActionTest"
REPO = "foundational-tests"
BRANCH = "main"
WEB_API = "https://web-api.gitcode.com"
API_V8 = "https://api.gitcode.com"
TIMEOUT = 600
POLL = 10


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def v2_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {COOKIE}",
        "Origin": "https://gitcode.com",
        "Referer": "https://gitcode.com/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "X-App-Channel": "gitcode-fe", "X-App-Version": "0",
        "X-Device-ID": "unknown", "X-Device-Type": "Linux", "X-Platform": "web",
        "Cookie": f"GITCODE_ACCESS_TOKEN={COOKIE}; GitCodeUserName={EXECUTOR}",
    }


# ── Deploy ────────────────────────────────────────────────────────

def deploy_one(case_id, wf_text):
    """git clone → write → commit → push。返回 file_path。"""
    fp = f".gitcode/workflows/{case_id.lower().replace('_', '-')}.yml"
    workdir = tempfile.mkdtemp(prefix="br-")
    repo_url = f"https://oauth2:{TOKEN}@gitcode.com/{OWNER}/{REPO}.git"
    subprocess.run(["git", "clone", repo_url, f"{workdir}/repo"],
                   capture_output=True, text=True, check=True)
    os.makedirs(f"{workdir}/repo/.gitcode/workflows", exist_ok=True)
    with open(f"{workdir}/repo/{fp}", "w") as f:
        f.write(wf_text)
        f.write(f"\n# deploy: {int(time.time())}\n")
    subprocess.run(["git", "add", fp], cwd=f"{workdir}/repo", capture_output=True, check=True)
    # commit may fail if nothing changed (files identical) — that's ok
    r = subprocess.run(["git", "commit", "-m", f"test: {case_id}"], cwd=f"{workdir}/repo",
                       capture_output=True, text=True)
    if r.returncode != 0 and "nothing to commit" not in r.stderr:
        shutil.rmtree(workdir, ignore_errors=True)
        raise RuntimeError(f"git commit failed: {r.stderr[:200]}")
    subprocess.run(["git", "push", "origin", BRANCH], cwd=f"{workdir}/repo",
                   capture_output=True, timeout=30, check=True)
    shutil.rmtree(workdir, ignore_errors=True)
    return fp


# ── Dispatch ───────────────────────────────────────────────────────

def find_workflow_id(fp):
    project = f"{OWNER}%2F{REPO}"
    r = requests.post(f"{WEB_API}/api/v2/projects/{project}/actions/workflows/list",
                      headers=v2_headers(), json={}, timeout=10)
    for w in r.json().get("content", []):
        if w.get("file_path") == fp:
            return w["workflow_id"]
    return None


def dispatch_one(wf_id, fp):
    project = f"{OWNER}%2F{REPO}"
    url = f"{WEB_API}/api/v2/projects/{project}/actions/workflows/{wf_id}/dispatch"
    payload = {"ref": BRANCH, "branch": BRANCH, "branch_commit_id": "",
               "repo_https_url": f"https://gitcode.com/{OWNER}/{REPO}.git",
               "file_path": fp, "inputs": {}}
    r = requests.post(url, headers=v2_headers(), json=payload, timeout=10)
    return r.status_code, r.json() if r.headers.get("Content-Type", "").startswith("application/json") else r.text


def poll_run(run_id):
    url = f"{API_V8}/api/v8/repos/{OWNER}/{REPO}/actions/runs/{run_id}?access_token={TOKEN}"
    for _ in range(TIMEOUT // POLL):
        time.sleep(POLL)
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                st = r.json().get("status", "")
                if st in ("COMPLETED", "FAILED", "CANCELED"):
                    return r.json()
        except Exception:
            pass
    return None


def collect_logs(run_id):
    jobs_url = f"{API_V8}/api/v8/repos/{OWNER}/{REPO}/actions/runs/{run_id}/jobs?access_token={TOKEN}"
    try:
        jobs = requests.get(jobs_url, timeout=10).json().get("jobs", [])
    except Exception:
        return ""
    all_logs = []
    for j in jobs:
        jid = j.get("id", "")
        log_url = f"{API_V8}/api/v8/repos/{OWNER}/{REPO}/actions/runs/{run_id}/jobs/{jid}/download_log?access_token={TOKEN}"
        try:
            r = requests.get(log_url, timeout=30)
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                for name in z.namelist():
                    all_logs.append(z.read(name).decode("utf-8", errors="replace"))
        except Exception as e:
            all_logs.append(f"[LOG_ERROR: {e}]")
    return "\n".join(all_logs)


def simple_assert(assertions, status, logs):
    results = []
    for a in assertions:
        a_type = a.get("type", "")
        target = a.get("target", "")
        rubric = a.get("rubric", "")
        passed = False
        if target == "run_logs":
            import re
            vals = re.findall(r'[A-Z][A-Z0-9_]{3,}', rubric)
            passed = any(v in logs for v in vals) if vals else (status == "COMPLETED" and len(logs) > 100)
        elif target == "run_status":
            expected = a.get("equals", "COMPLETED")
            passed = (status == expected)
        else:
            passed = (status == "COMPLETED")
        results.append({"type": a_type, "target": target, "pass": passed, "rubric": rubric[:80]})
    all_pass = all(r["pass"] for r in results) if results else (status == "COMPLETED")
    return {"verdict": "PASS" if all_pass else "FAIL", "results": results}


# ── Main ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_id")
    parser.add_argument("--max", type=int, default=0)
    parser.add_argument("--case")
    args = parser.parse_args()

    if not TOKEN or not COOKIE:
        log("ERROR: need GITCODE_ACCESS_TOKEN + GITCODE_COOKIE")
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    cases_dir = script_dir / "2026-07-21-02/cases/yaml"
    results_dir = script_dir / f"../runs/{args.run_id}/results"
    results_dir.mkdir(parents=True, exist_ok=True)

    yaml_files = sorted(cases_dir.glob("*.yaml"))
    if args.case:
        want = set(args.case.split(","))
        yaml_files = [f for f in yaml_files if f.stem in want]
    if args.max > 0:
        yaml_files = yaml_files[:args.max]

    log(f"Cases: {len(yaml_files)}  run: {args.run_id}")

    results = []
    verdict_counts = {"PASS": 0, "FAIL": 0, "DISPATCH_FAIL": 0, "DEPLOY_FAIL": 0, "TIMEOUT": 0, "NOT_FOUND": 0}

    for i, yf in enumerate(yaml_files):
        cid = yf.stem
        with open(yf) as f:
            doc = yaml.safe_load(f)
        wf = doc.get("workflow", "")
        if not wf:
            continue

        log(f"\n[{i+1}/{len(yaml_files)}] {cid}")

        try:
            # 1. Deploy
            fp = deploy_one(cid, wf)
            log(f"  deployed → {fp}")
            time.sleep(6)

            # 2. Find + dispatch
            wf_id = find_workflow_id(fp)
            if not wf_id:
                time.sleep(10)
                wf_id = find_workflow_id(fp)
            if not wf_id:
                results.append({"case_id": cid, "verdict": "NOT_FOUND", "reason": "workflow not in API after deploy"})
                verdict_counts["NOT_FOUND"] += 1
                continue

            code, resp = dispatch_one(wf_id, fp)
            if code != 200:
                reason = resp.get("error_message", str(resp)) if isinstance(resp, dict) else str(resp)[:300]
                results.append({"case_id": cid, "verdict": "DISPATCH_FAIL", "reason": reason})
                verdict_counts["DISPATCH_FAIL"] += 1
                log(f"  ❌ dispatch fail: {reason[:120]}")
                continue

            rid = resp.get("workflow_run_id", "")
            log(f"  run {rid[:12]}... polling")

            # 3. Poll
            run = poll_run(rid)
            status = run.get("status", "?") if run else "TIMEOUT"
            if not run:
                results.append({"case_id": cid, "verdict": "TIMEOUT"})
                verdict_counts["TIMEOUT"] += 1
                continue

            log(f"  → {status}")

            # 4. Collect logs + assert
            logs = collect_logs(rid)
            ar = simple_assert(doc.get("assertions", []), status, logs)
            verdict = ar["verdict"]

            result = {
                "case_id": cid, "title": doc.get("title", ""),
                "dimension": doc.get("dimension", ""), "priority": doc.get("priority", ""),
                "verdict": verdict, "gitcode_run_id": rid, "run_status": status,
                "assertion_results": ar["results"], "phase02_run": args.run_id,
            }
            results.append(result)
            verdict_counts[verdict] += 1
            log(f"  {'✅' if verdict == 'PASS' else '❌'} {verdict}")

            with open(results_dir / f"{cid}.json", "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

        except Exception as e:
            results.append({"case_id": cid, "verdict": "ERROR", "reason": str(e)})
            log(f"  💥 ERROR: {e}")

    # ── Report ──
    total = len(yaml_files)
    log(f"\n{'='*50}")
    log(f"DONE: {verdict_counts} / {total} total")

    summary = {
        "run_id": args.run_id, "total": total, "counts": verdict_counts, "results": results,
    }
    with open(results_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    failed = [r for r in results if r.get("verdict") not in ("PASS",)]
    md = [
        f"# Batch Run Report — {args.run_id}",
        f"**{total} cases** | PASS={verdict_counts['PASS']} FAIL={verdict_counts['FAIL']} "
        f"DISPATCH_FAIL={verdict_counts['DISPATCH_FAIL']} TIMEOUT={verdict_counts['TIMEOUT']} "
        f"NOT_FOUND={verdict_counts['NOT_FOUND']}",
        "",
    ]
    if failed:
        md.append("## Non-PASS cases")
        for r in failed:
            md.append(f"- **{r['case_id']}** — `{r.get('verdict')}`: {r.get('reason','')[:200]}")
            if r.get("gitcode_run_id"):
                md.append(f"  run: `{r['gitcode_run_id']}`")
        md.append("")
    md.append("## API Used")
    md.append("- `POST web-api.gitcode.com/api/v2/.../dispatch` — trigger workflow_dispatch")
    md.append("- `GET api.gitcode.com/api/v8/.../runs/{id}` — poll status")
    md.append("- `GET api.gitcode.com/api/v8/.../jobs/{id}/download_log` — collect logs")
    md.append("")

    with open(results_dir / "report.md", "w") as f:
        f.write("\n".join(md))

    log(f"Results → {results_dir}/")


if __name__ == "__main__":
    main()
