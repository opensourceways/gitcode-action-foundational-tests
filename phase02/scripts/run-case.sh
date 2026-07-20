#!/bin/bash
# run-case.sh — Phase 02 最小闭环执行脚本
# Usage: ./run-case.sh <case-yaml-path> <run-id>
set -euo pipefail

CASE_YAML="${1:?Usage: $0 <case-yaml-path> <run-id>}"
RUN_ID="${2:?}"
: ${GITCODE_ACCESS_TOKEN:?请设置 GITCODE_ACCESS_TOKEN}
: ${GITCODE_API_BASE_URL:="https://api.gitcode.com"}
: ${GITCODE_OWNER:="ComputingActionTest"}
: ${GITCODE_REPO:="foundational-tests"}
: ${GITCODE_BRANCH:="main"}
: ${TIMEOUT_SECONDS:=600}
: ${POLL_INTERVAL:=10}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/../runs/${RUN_ID}/results"
mkdir -p "$RESULTS_DIR"
VENV_PY="source /tmp/phase02-venv/bin/activate && python3"

_log() { echo "[$(date +%H:%M:%S)] $*"; }

# ── 1. Extract case fields ──────────────────────────────
_log "Loading case: $(basename $CASE_YAML)"

ENV_FILE="/tmp/case-env.sh"
$VENV_PY << PYEOF > "$ENV_FILE"
import yaml, json
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
print(f'export WORKFLOW_FILE="/tmp/workflow-case.yml"')
with open('/tmp/workflow-case.yml', 'w') as wf_f:
    wf_f.write(wf)
print(f'export ASSERTIONS_JSON=\'{json.dumps(c.get("assertions", []), ensure_ascii=False)}\'')
PYEOF

source "$ENV_FILE"
_log "CASE: $CASE_ID — $CASE_TITLE ($CASE_DIM/$CASE_PRI)"
START_TIME=$(date +%s)

# ── 2. Deploy workflow ──────────────────────────────────
_log "Deploying to ${GITCODE_OWNER}/${GITCODE_REPO}"

WORK_DIR=$(mktemp -d)
git clone "https://oauth2:${GITCODE_ACCESS_TOKEN}@gitcode.com/${GITCODE_OWNER}/${GITCODE_REPO}.git" "$WORK_DIR/repo" 2>&1 | tail -1
cd "$WORK_DIR/repo"

mkdir -p .gitcode/workflows
WF_NAME=$(echo "$CASE_ID" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g').yml
cp "$WORKFLOW_FILE" ".gitcode/workflows/${WF_NAME}"

if git diff --quiet && git diff --cached --quiet; then
  _log "No changes, re-triggering with empty commit"
  git add .gitcode/workflows/
  git commit --allow-empty -m "test: re-run ${CASE_ID}"
else
  git add .gitcode/workflows/
  git commit -m "test: ${CASE_ID}"
fi
git push origin "$GITCODE_BRANCH" 2>&1 | tail -1
_log "Pushed: .gitcode/workflows/${WF_NAME}"

# ── 3. Poll for run ─────────────────────────────────────
_log "Polling for run completion..."
sleep 8

RUN_ID_GC=""
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT_SECONDS ]; do
  RESP=$(curl -sS "${GITCODE_API_BASE_URL}/api/v8/repos/${GITCODE_OWNER}/${GITCODE_REPO}/actions/runs?access_token=${GITCODE_ACCESS_TOKEN}&per_page=3&branch=${GITCODE_BRANCH}")
  RUN_ID_GC=$(echo "$RESP" | python3 -c "import sys,json; runs=json.load(sys.stdin).get('workflow_runs',[]); print(runs[0]['id'] if runs else '')" 2>/dev/null || echo "")

  if [ -n "$RUN_ID_GC" ]; then
    DETAIL=$(curl -sS "${GITCODE_API_BASE_URL}/api/v8/repos/${GITCODE_OWNER}/${GITCODE_REPO}/actions/runs/${RUN_ID_GC}?access_token=${GITCODE_ACCESS_TOKEN}")
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
  RUN_CONCLUSION=$(echo "$DETAIL" | python3 -c "import sys,json; print(json.load(sys.stdin).get('conclusion',''))" 2>/dev/null || echo "?")

  # ── 4. Collect ────────────────────────────────────
  JOBS_RESP=$(curl -sS "${GITCODE_API_BASE_URL}/api/v8/repos/${GITCODE_OWNER}/${GITCODE_REPO}/actions/runs/${RUN_ID_GC}/jobs?access_token=${GITCODE_ACCESS_TOKEN}")
  JOB_COUNT=$(echo "$JOBS_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d) if isinstance(d,list) else 0)" 2>/dev/null || echo "0")

  LOGS=""
  if [ "$JOB_COUNT" -gt 0 ]; then
    JOB_IDS=$(echo "$JOBS_RESP" | python3 -c "import sys,json; print(','.join(str(j['id']) for j in json.load(sys.stdin)))" 2>/dev/null)
    for jid in $(echo "$JOB_IDS" | tr ',' ' '); do
      JOB_LOG=$(curl -sS "${GITCODE_API_BASE_URL}/api/v8/repos/${GITCODE_OWNER}/${GITCODE_REPO}/actions/runs/${RUN_ID_GC}/jobs/${jid}/download-log?access_token=${GITCODE_ACCESS_TOKEN}" 2>/dev/null || echo "")
      LOGS="${LOGS}
=== JOB #${jid} ===
${JOB_LOG}"
    done
  fi
  _log "Collected ${JOB_COUNT} job(s), $(echo "$LOGS" | wc -l) log lines"

  # ── 5. Assert ─────────────────────────────────────
  ASSERT_RESULTS=$($VENV_PY << PYEOF
import json, sys
logs = """${LOGS}"""
conclusion = "${RUN_CONCLUSION}"
assertions = json.loads('${ASSERTIONS_JSON}')

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
            passed = conclusion == 'success' and len(logs) > 100
    elif target == 'run_status':
        expected = a.get('equals', 'success')
        passed = (conclusion == expected)
    else:
        passed = conclusion == 'success'

    results.append({'type': atype, 'target': target, 'pass': passed, 'rubric': rubric})

all_pass = all(r['pass'] for r in results)
print(json.dumps({'verdict': 'PASS' if all_pass else 'FAIL', 'results': results}, ensure_ascii=False))
PYEOF
)
  VERDICT=$(echo "$ASSERT_RESULTS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('verdict','ERROR'))" 2>/dev/null || echo "ERROR")
fi

# ── 6. Write result ─────────────────────────────────────
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

$VENV_PY << PYEOF
import json
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
  'assertion_results': json.loads('''${ASSERT_RESULTS:-{"results":[]}}''')['results']
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
