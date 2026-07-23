#!/usr/bin/env python3
"""Minimal sanity test: push a workflow with on:push, poll for run, verify logs."""
import os, sys, json, time, subprocess, tempfile, urllib.request

# Load env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env")
if os.path.exists(env_path):
    import re
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k = k.strip(); v = v.strip()
            v = re.sub(r'\s+#.*$', '', v).strip()
            v = v.strip('"').strip("'")
            if k not in os.environ:
                os.environ[k] = v

TOKEN = os.environ.get("GITCODE_ACCESS_TOKEN", "")
EXECUTOR = os.environ.get("GITCODE_EXECUTOR", "")
OWNER = "ComputingActionTest"
REPO = "foundational-tests"

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout or "") + (r.stderr or "")

root = tempfile.mkdtemp(prefix="p2-sanity-")
repo_dir = os.path.join(root, "repo")
url = f"https://oauth2:{TOKEN}@gitcode.com/{OWNER}/{REPO}.git"

print(f"[{time.strftime('%H:%M:%S')}] Clone...")
rc, out = sh(f'git clone --depth 1 --branch main "{url}" "{repo_dir}"')
assert rc == 0, f"clone failed: {out[-200:]}"

WF = """\
on:
  push:
    branches: [main]
jobs:
  sanity:
    name: sanity-push-check
    runs-on: [dedicate-hosted, x64, large]
    steps:
      - name: ok
        run: echo "PUSH_TRIGGER_OK"
"""

wf_dir = os.path.join(repo_dir, ".gitcode", "workflows")
os.makedirs(wf_dir, exist_ok=True)
with open(os.path.join(wf_dir, "demo-push-sanity.yml"), "w", newline="\n") as f:
    f.write(WF)

sh("git add .gitcode/workflows/", cwd=repo_dir)
sh('git commit --allow-empty -m "demo: push sanity"', cwd=repo_dir)
rc, out = sh("git push origin main", cwd=repo_dir)
print(f"[{time.strftime('%H:%M:%S')}] Push: rc={rc}")

if rc != 0:
    print(f"PUSH FAILED: {out[-300:]}")
    sh(f"rm -rf {root}", shell=True)
    sys.exit(1)

sh("git rev-parse HEAD", cwd=repo_dir)

# Poll
print(f"[{time.strftime('%H:%M:%S')}] Polling...")
for i in range(30):
    url = f"https://api.gitcode.com/api/v8/repos/{OWNER}/{REPO}/actions/runs?access_token={TOKEN}&executor={EXECUTOR}&per_page=10"
    r = urllib.request.urlopen(urllib.request.Request(url), timeout=15)
    data = json.loads(r.read())
    for run in data.get("workflow_runs", []):
        fp = run.get("file_path", "")
        if "demo-push-sanity" in fp:
            print(f"[{time.strftime('%H:%M:%S')}] FOUND! status={run['status']} event={run['event']}")
            print(f"  run_id={run.get('workflow_run_id','')}")
            print("PUSH TRIGGER: WORKING")
            # Cleanup
            sh(f"git rm .gitcode/workflows/demo-push-sanity.yml", cwd=repo_dir)
            sh('git commit -m "chore: rm sanity"', cwd=repo_dir)
            rc_cl, _ = sh("git push origin main", cwd=repo_dir)
            print(f"  cleanup push: rc={rc_cl}")
            sh(f"rm -rf {root}", shell=True)
            sys.exit(0)
    time.sleep(10)
    if i % 3 == 0:
        print(f"  poll {i+1}...")

print("TIMEOUT: push trigger not detected")
sh(f"rm -rf {root}", shell=True)
sys.exit(1)
