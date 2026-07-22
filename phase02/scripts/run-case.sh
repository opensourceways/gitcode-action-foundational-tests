#!/bin/bash
# run-case.sh — Phase 02 最小闭环执行脚本
# Usage: ./run-case.sh <case-yaml-path> <run-id>
set -euo pipefail

CASE_YAML="${1:?Usage: $0 <case-yaml-path> <run-id>}"
RUN_ID="${2:?}"
: ${GITCODE_ACCESS_TOKEN:?请设置 GITCODE_ACCESS_TOKEN}
: ${GITCODE_EXECUTOR:?请设置 GITCODE_EXECUTOR（GitCode 用户名，v8 Actions API 必填）}
: ${GITCODE_API_BASE_URL:="https://api.gitcode.com"}
: ${GITCODE_OWNER:="ComputingActionTest"}
: ${GITCODE_REPO:="foundational-tests"}
: ${GITCODE_BRANCH:="main"}
: ${TIMEOUT_SECONDS:=600}
: ${POLL_INTERVAL:=10}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/../runs/${RUN_ID}/results"
mkdir -p "$RESULTS_DIR"
VENV_PY="/tmp/phase02-venv/bin/python3"

_log() { echo "[$(date +%H:%M:%S)] $*"; }

# ── 1. Extract case fields ──────────────────────────────
_log "Loading case: $(basename $CASE_YAML)"

ENV_FILE="/tmp/case-env.sh"
$VENV_PY << PYEOF > "$ENV_FILE"
import yaml, json, re

def _fix_runs_on(m):
    indent = m.group(1)
    labels = re.findall(r'-\s+(\S+)', m.group(2))
    return f'{indent}runs-on: [{", ".join(labels)}]\n'

with open('${CASE_YAML}') as f:
    c = yaml.safe_load(f)
print(f'export CASE_ID="{c["id"]}"')
print(f'export CASE_TITLE="{c["title"]}"')
print(f'export CASE_DIM="{c["dimension"]}"')
print(f'export CASE_PRI="{c["priority"]}"')
print(f'export CASE_INTENT="{c["intent_ref"]}"')
print(f'export CASE_RESET="{c["teardown"]["reset"]}"')
print(f'export TRIGGER_EVENT="{c["trigger"]["event"]}"')
wf = c.get('workflow', '') or ''

# Normalize workflow YAML: fix common Phase 01 output issues
# 1. "on:\n- push" or "on:\n  - push" (list) → "on:\n  push:\n  workflow_dispatch:" (GitCode compatible)
wf = re.sub(r'^on:\s*\n\s*-\s+(\w+)', r'on:\n  \1:\n  workflow_dispatch:', wf, flags=re.MULTILINE)
# 2. "runs-on:\n    - label1\n    - label2" (multi-line list) → "runs-on: [label1, label2]" (inline)
wf = re.sub(r'^(\s+)runs-on:\s*\n((?:\s+-\s+\S+\n?)+)', _fix_runs_on, wf, flags=re.MULTILINE)

print(f'export WORKFLOW_FILE="/tmp/workflow-case.yml"')
with open('/tmp/workflow-case.yml', 'w') as wf_f:
    wf_f.write(wf)
print(f'export ASSERTIONS_FILE=\"/tmp/case-assertions.json\"')
with open('/tmp/case-assertions.json', 'w') as af:
    json.dump(c.get("assertions", []), af, ensure_ascii=False)
PYEOF

source "$ENV_FILE"
_log "CASE: $CASE_ID — $CASE_TITLE ($CASE_DIM/$CASE_PRI)"
START_TIME=$(date +%s)

# ── 1.5 Validate workflow YAML before deploy ─────────────
_log "Validating workflow YAML..."
VALIDATE_SCRIPT="${SCRIPT_DIR}/validate_workflow.py"
if [ -f "$VALIDATE_SCRIPT" ]; then
  # Resolve workflow_id by matching case filename pattern
  WF_BASENAME=$(echo "$CASE_ID" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g').yml
  WF_ID=$($VENV_PY -c "
import json, os, sys
sys.path.insert(0, os.path.dirname('${VALIDATE_SCRIPT}'))
from validate_workflow import _get_workflow_list, _load_env_file
env = _load_env_file()
cookie = env.get('GITCODE_COOKIE') or env.get('GITCODE_ACCESS_TOKEN')
wfs = _get_workflow_list('${GITCODE_OWNER}/${GITCODE_REPO}', cookie, 'web-api.gitcode.com')
target = '${WF_BASENAME}'
for w in wfs:
    if w.get('file_path','').endswith(target):
        print(w['workflow_id'])
        break
" 2>/dev/null || echo "")

  if [ -n "$WF_ID" ]; then
    VALIDATE_OUTPUT=$($VENV_PY "$VALIDATE_SCRIPT" "$WORKFLOW_FILE" --workflow-id "$WF_ID" 2>&1) || {
      _log "YAML VALIDATION FAILED:"
      echo "$VALIDATE_OUTPUT" | while IFS= read -r line; do _log "  $line"; done
      _log "Aborting — fix YAML before deploying."
      exit 1
    }
    _log "YAML validation: PASS"
  else
    _log "WARNING: No existing workflow_id for ${WF_BASENAME}, skipping validation"
  fi
else
  _log "WARNING: validate_workflow.py not found, skipping pre-deploy validation"
fi

# ── 2. Deploy workflow ──────────────────────────────────
_log "Deploying to ${GITCODE_OWNER}/${GITCODE_REPO}"

WORK_DIR=$(mktemp -d)
git clone "https://oauth2:${GITCODE_ACCESS_TOKEN}@gitcode.com/${GITCODE_OWNER}/${GITCODE_REPO}.git" "$WORK_DIR/repo" 2>&1 | tail -1
cd "$WORK_DIR/repo"

mkdir -p .gitcode/workflows
WF_NAME=$(echo "$CASE_ID" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g').yml
cp "$WORKFLOW_FILE" ".gitcode/workflows/${WF_NAME}"

# Always ensure a content change so push triggers a new workflow run.
# Append a timestamp comment to the workflow file.
echo "" >> ".gitcode/workflows/${WF_NAME}"
echo "# trigger: $(date +%s)" >> ".gitcode/workflows/${WF_NAME}"

git add .gitcode/workflows/
git commit -m "test: ${CASE_ID}"
git push origin "$GITCODE_BRANCH" 2>&1 | tail -1
_log "Pushed: .gitcode/workflows/${WF_NAME}"

# ── 3. Poll for run ─────────────────────────────────────
# Strategy: match by file_path — each run object contains the workflow file path.
# Filter runs API response for the exact workflow file we just pushed.
WF_PATH=".gitcode/workflows/${WF_NAME}"
_log "Polling for run of ${WF_PATH}..."
sleep 8

RUN_ID_GC=""
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT_SECONDS ]; do
  RESP=$(curl -sS "${GITCODE_API_BASE_URL}/api/v8/repos/${GITCODE_OWNER}/${GITCODE_REPO}/actions/runs?access_token=${GITCODE_ACCESS_TOKEN}&executor=${GITCODE_EXECUTOR}&per_page=10&branch=${GITCODE_BRANCH}")
  RUN_ID_GC=$(echo "$RESP" | python3 -c "
import sys, json
runs = json.load(sys.stdin).get('workflow_runs', [])
target = '${WF_PATH}'
for r in runs:
    if r.get('file_path', '') == target:
        print(r.get('workflow_run_id', ''))
        break
" 2>/dev/null || echo "")

  if [ -n "$RUN_ID_GC" ]; then
    DETAIL=$(curl -sS "${GITCODE_API_BASE_URL}/api/v8/repos/${GITCODE_OWNER}/${GITCODE_REPO}/actions/runs/${RUN_ID_GC}?access_token=${GITCODE_ACCESS_TOKEN}&executor=${GITCODE_EXECUTOR}")
    STATUS=$(echo "$DETAIL" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null || echo "")
    _log "Run #${RUN_ID_GC}: $STATUS ($((ELAPSED))s)"

    case "$STATUS" in
      COMPLETED|FAILED|CANCELED) break ;;
    esac
  fi

  sleep $POLL_INTERVAL
  ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

if [ -z "$RUN_ID_GC" ] || [ $ELAPSED -ge $TIMEOUT_SECONDS ]; then
  VERDICT="TIMEOUT"
  RUN_CONCLUSION="timeout"
  JOB_COUNT=0
  LOGS=""
  _log "TIMEOUT after ${TIMEOUT_SECONDS}s"
else
  RUN_CONCLUSION=$(echo "$DETAIL" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null || echo "?")

  # ── 4. Collect ────────────────────────────────────
  JOBS_RESP=$(curl -sS "${GITCODE_API_BASE_URL}/api/v8/repos/${GITCODE_OWNER}/${GITCODE_REPO}/actions/runs/${RUN_ID_GC}/jobs?access_token=${GITCODE_ACCESS_TOKEN}&executor=${GITCODE_EXECUTOR}")
  JOB_COUNT=$(echo "$JOBS_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); jobs=d.get('jobs',[]); print(len(jobs))" 2>/dev/null || echo "0")

  LOGS=""
  if [ "$JOB_COUNT" -gt 0 ]; then
    JOB_IDS=$(echo "$JOBS_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(','.join(str(j['id']) for j in d.get('jobs',[])))" 2>/dev/null)
    for jid in $(echo "$JOB_IDS" | tr ',' ' '); do
      JOB_LOG_ZIP="/tmp/job-${jid}-log.zip"
      curl -sS -L -o "$JOB_LOG_ZIP" "${GITCODE_API_BASE_URL}/api/v8/repos/${GITCODE_OWNER}/${GITCODE_REPO}/actions/runs/${RUN_ID_GC}/jobs/${jid}/download_log?access_token=${GITCODE_ACCESS_TOKEN}&executor=${GITCODE_EXECUTOR}" 2>/dev/null
      JOB_LOG=$($VENV_PY -c "
import zipfile
try:
    with zipfile.ZipFile('${JOB_LOG_ZIP}') as z:
        for name in z.namelist():
            print(z.read(name).decode('utf-8', errors='replace'))
except Exception as e:
    print(f'[LOG_ERROR: {e}]')
" 2>/dev/null || echo "")
      rm -f "$JOB_LOG_ZIP"
      LOGS="${LOGS}
=== JOB #${jid} ===
${JOB_LOG}"
    done
  fi
  _log "Collected ${JOB_COUNT} job(s), $(echo "$LOGS" | wc -l) log lines"

  # ── 5. Assert ─────────────────────────────────────
  LOGS_FILE="/tmp/case-logs-${CASE_ID}.txt"
  echo "$LOGS" > "$LOGS_FILE"
  ASSERT_RESULTS=$($VENV_PY << PYEOF
import json, sys
with open('${LOGS_FILE}', 'r') as f:
    logs = f.read()
conclusion = "${RUN_CONCLUSION}"
with open('${ASSERTIONS_FILE}', 'r') as f:
    assertions = json.load(f)

results = []
for a in assertions:
    atype = a.get('type', '')
    target = a.get('target', '')
    rubric = a.get('rubric', '')
    passed = False

    if target == 'run_logs':
        if 'step-value' in rubric:
            passed = 'step-value' in logs
        elif 'ATOMGIT_WORKSPACE' in rubric:
            passed = 'ATOMGIT_WORKSPACE' in logs and ('/home' in logs or '/runner' in logs)
        elif 'TEST_VAR' in rubric:
            passed = 'TEST_VAR' in logs
        else:
            passed = conclusion == 'COMPLETED' and len(logs) > 100
    elif target == 'run_status':
        expected = a.get('equals', 'COMPLETED')
        passed = (conclusion == expected)
    else:
        passed = conclusion == 'COMPLETED'

    results.append({'type': atype, 'target': target, 'pass': passed, 'rubric': rubric})

all_pass = all(r['pass'] for r in results)
print(json.dumps({'verdict': 'PASS' if all_pass else 'FAIL', 'results': results}, ensure_ascii=False))
PYEOF
)
  rm -f "$LOGS_FILE"
  VERDICT=$(echo "$ASSERT_RESULTS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('verdict','ERROR'))" 2>/dev/null || echo "ERROR")
  echo "$ASSERT_RESULTS" > /tmp/case-assert-results.json
fi

# ── 6. Write result ─────────────────────────────────────
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

$VENV_PY << PYEOF
import json
with open('/tmp/case-assert-results.json', 'r') as f:
    ar = json.load(f)
result = {
  'case_id': '${CASE_ID}',
  'title': '${CASE_TITLE}',
  'dimension': '${CASE_DIM}',
  'priority': '${CASE_PRI}',
  'intent_ref': '${CASE_INTENT}',
  'phase02_run': '${RUN_ID}',
  'start_time': ${START_TIME},
  'end_time': ${END_TIME},
  'duration_seconds': ${DURATION},
  'verdict': '${VERDICT}',
  'gitcode_run_id': '${RUN_ID_GC:-}',
  'run_conclusion': '${RUN_CONCLUSION:-}',
  'job_count': ${JOB_COUNT:-0},
  'assertion_results': ar.get('results', [])
}
with open('${RESULTS_DIR}/${CASE_ID}.json', 'w') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
PYEOF

# ── 7. Summary ──────────────────────────────────────────
_log ""
_log "═══════════════════════════════════════"
_log "RESULT: ${CASE_ID}"
_log "  Verdict: ${VERDICT}"
_log "  Duration: ${DURATION}s"
_log "  GitCode Run: #${RUN_ID_GC:-N/A}"
_log "  Result: ${RESULTS_DIR}/${CASE_ID}.json"
_log "═══════════════════════════════════════"

rm -rf "$WORK_DIR"
[ "$VERDICT" = "PASS" ]
