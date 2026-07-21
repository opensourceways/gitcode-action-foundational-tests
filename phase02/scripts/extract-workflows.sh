#!/bin/bash
# extract-workflows.sh — 从 case YAML 中提取 workflow 字段并逐条校验
# Usage: ./extract-workflows.sh <cases-yaml-dir> [output-dir]
set -uo pipefail

CASES_DIR="${1:?Usage: $0 <cases-yaml-dir> [output-dir]}"
OUT_DIR="${2:-${PWD}/tmp}"

mkdir -p "$OUT_DIR"
VENV_PY="/tmp/phase02-venv/bin/python3"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VALIDATE_PY="${SCRIPT_DIR}/validate_workflow.py"
HARDCODED_WF_ID="b03a4b84cd784ddea00c5270eba62c7f"

: ${GITCODE_COOKIE:?请设置 GITCODE_COOKIE}
: ${GITCODE_OWNER:="ComputingActionTest"}
: ${GITCODE_REPO:="foundational-tests"}

_log()   { echo "[$(date +%H:%M:%S)] $*"; }
_err()   { echo "[$(date +%H:%M:%S)] ERROR: $*" >&2; }

# ── Fetch existing workflow list once ────────────────────
_log "Fetching workflow list from ${GITCODE_OWNER}/${GITCODE_REPO}..."
WF_MAP_JSON=$($VENV_PY -c "
import json, os, sys
sys.path.insert(0, '${SCRIPT_DIR}')
from validate_workflow import _get_workflow_list
wfs = _get_workflow_list('${GITCODE_OWNER}/${GITCODE_REPO}', '${GITCODE_COOKIE}', 'web-api.gitcode.com')
m = {}
for w in wfs:
    fp = w.get('file_path', '')
    wid = w.get('workflow_id', '')
    if fp and wid:
        m[fp.split('/')[-1]] = wid
print(json.dumps(m))
" 2>/dev/null || echo "{}")

_log "Found $(echo "$WF_MAP_JSON" | $VENV_PY -c 'import sys,json; print(len(json.load(sys.stdin)))') existing workflows"

# ── Extract + validate one by one ────────────────────────
TOTAL=0; PASS=0; FAIL=0

for case_file in "$CASES_DIR"/*.yaml; do
  [ -f "$case_file" ] || continue
  TOTAL=$((TOTAL + 1))
  case_id=$(basename "$case_file" .yaml)
  wf_name=$(echo "$case_id" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g').yml

  # Extract
  $VENV_PY -c "
import yaml
with open('${case_file}') as f:
    c = yaml.safe_load(f)
wf = c.get('workflow', '')
if wf:
    with open('${OUT_DIR}/${wf_name}', 'w') as out:
        out.write(wf)
" 2>/dev/null

  if [ ! -s "${OUT_DIR}/${wf_name}" ]; then
    _log "[$TOTAL] $case_id — SKIP (no workflow field)"
    continue
  fi

  # Resolve workflow_id
  wid=$(echo "$WF_MAP_JSON" | $VENV_PY -c "import sys,json; m=json.load(sys.stdin); print(m.get('${wf_name}', '${HARDCODED_WF_ID}'))" 2>/dev/null || echo "$HARDCODED_WF_ID")

  # Validate
  result=$($VENV_PY "$VALIDATE_PY" "${OUT_DIR}/${wf_name}" --workflow-id "$wid" --cookie "$GITCODE_COOKIE" 2>&1)
  rc=$?

  case $rc in
    0) PASS=$((PASS + 1)); _log "[$TOTAL] $case_id — VALID" ;;
    1) FAIL=$((FAIL + 1)); _log "[$TOTAL] $case_id — INVALID"
       echo "$result" | while IFS= read -r l; do _log "  $l"; done ;;
    *) FAIL=$((FAIL + 1)); _log "[$TOTAL] $case_id — ERROR (rc=$rc)"
       echo "$result" | while IFS= read -r l; do _log "  $l"; done ;;
  esac
done

_log ""
_log "═══════════════════════════════════════"
_log "Done: $TOTAL cases — $PASS valid, $FAIL invalid/error"
_log "═══════════════════════════════════════"
