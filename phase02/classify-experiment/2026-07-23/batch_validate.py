#!/usr/bin/env python3
"""Batch validate case YAMLs via GitCode API and split into VALID/INVALID/SKIP."""
import base64, json, os, sys, shutil, time
from pathlib import Path

import requests
import yaml

DEFAULT_WF_ID = "b03a4b84cd784ddea00c5270eba62c7f"
API_HOST = "web-api.gitcode.com"
PROJECT = "ComputingActionTest/foundational-tests"

def load_env():
    env_path = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/.env")
    env = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                if "=" in line:
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def validate_one(file_content: str, cookie: str, workflow_id: str, file_path: str, session: requests.Session):
    encoded_project = PROJECT.replace("/", "%2F")
    url = f"https://{API_HOST}/api/v2/projects/{encoded_project}/actions/valid"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cookie}",
        "Origin": "https://gitcode.com",
        "Referer": "https://gitcode.com/",
        "User-Agent": "Mozilla/5.0",
        "X-App-Channel": "gitcode-fe",
        "X-App-Version": "0",
        "X-Device-ID": "unknown",
        "X-Device-Type": "Linux",
        "X-Platform": "web",
        "Cookie": f"GITCODE_ACCESS_TOKEN={cookie}; GitCodeUserName=ccijunk",
    }
    encoded_content = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")
    payload = {"workflow_id": workflow_id, "file_path": file_path, "file_content": encoded_content}
    try:
        resp = session.post(url, params={"workflow_id": workflow_id}, headers=headers, json=payload, timeout=15)
        if "application/json" in resp.headers.get("Content-Type", ""):
            return resp.json()
        return {"status_code": resp.status_code, "text": resp.text[:500]}
    except Exception as e:
        return {"error": str(e)}

def main():
    src_dir = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases/yaml")
    out_dir = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/phase02/classify-experiment/2026-07-23")
    valid_dir = out_dir / "VALID"
    invalid_dir = out_dir / "INVALID"
    skip_dir = out_dir / "SKIP"
    for d in [valid_dir, invalid_dir, skip_dir]:
        d.mkdir(parents=True, exist_ok=True)

    env = load_env()
    cookie = env.get("GITCODE_COOKIE", "")
    if not cookie:
        print("FATAL: GITCODE_COOKIE not found in .env"); sys.exit(1)

    session = requests.Session()
    results = []
    yaml_files = sorted(src_dir.glob("*.yaml"))

    for i, yf in enumerate(yaml_files):
        case_id = yf.stem
        with open(yf) as f:
            case = yaml.safe_load(f)
        wf_text = case.get("workflow", "")
        if not wf_text:
            results.append({"case_id": case_id, "valid": None, "status": "SKIP", "reason": "no workflow field"})
            # Copy to SKIP
            shutil.copy2(str(yf), str(skip_dir / yf.name))
            sys.stderr.write(f"[{i+1}/{len(yaml_files)}] {case_id} SKIP (no workflow)\n")
            continue

        wf_name = case_id.lower().replace("_", "-") + ".yml"
        file_path = f".gitcode/workflows/{wf_name}"

        resp = validate_one(wf_text, cookie, DEFAULT_WF_ID, file_path, session)
        valid = resp.get("valid")

        status = "VALID" if valid is True else ("INVALID" if valid is False else "ERROR")
        result = {"case_id": case_id, "valid": valid, "status": status}

        if valid is True:
            shutil.copy2(str(yf), str(valid_dir / yf.name))
            result["diagnostics"] = []
        elif valid is False:
            shutil.copy2(str(yf), str(invalid_dir / yf.name))
            diags = resp.get("diagnostics", [])
            result["diagnostics"] = [
                {"severity": d.get("severity", "?"), "message": d.get("message", ""),
                 "line": d.get("range", {}).get("start", {}).get("line", "?"),
                 "column": d.get("range", {}).get("start", {}).get("column", "?")}
                for d in diags
            ]
        else:
            result["raw"] = json.dumps(resp, ensure_ascii=False)[:500]

        results.append(result)
        n_diag = len(result.get("diagnostics", []))
        sys.stderr.write(f"[{i+1}/{len(yaml_files)}] {case_id} {status}" + (f" ({n_diag} diagnostics)" if n_diag else "") + "\n")
        time.sleep(0.15)  # Rate limit

    # Save raw results
    with open(out_dir / "validation-results.json", "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    valid_count = sum(1 for r in results if r["status"] == "VALID")
    invalid_count = sum(1 for r in results if r["status"] == "INVALID")
    skip_count = sum(1 for r in results if r["status"] == "SKIP")
    error_count = sum(1 for r in results if r["status"] == "ERROR")

    print(f"\nDone: {len(results)} cases → {valid_count} VALID, {invalid_count} INVALID, {skip_count} SKIP, {error_count} ERROR")
    print(f"Results: {out_dir / 'validation-results.json'}")

if __name__ == "__main__":
    main()
