#!/bin/bash
# validate-tmp-workflows.sh — 批量校验 tmp/ 目录下的 workflow YAML
# Usage: ./validate-tmp-workflows.sh [tmp-dir]
set -uo pipefail

TMP_DIR="${1:-${PWD}/tmp}"
VENV_PY="/tmp/phase02-venv/bin/python3"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VALIDATE_PY="${SCRIPT_DIR}/validate_workflow.py"
HARDCODED_WF_ID="b03a4b84cd784ddea00c5270eba62c7f"

: ${GITCODE_COOKIE:?请设置 GITCODE_COOKIE}
: ${GITCODE_OWNER:="ComputingActionTest"}
: ${GITCODE_REPO:="foundational-tests"}

_log()   { echo "[$(date +%H:%M:%S)] $*"; }
_err()   { echo "[$(date +%H:%M:%S)] ERROR: $*" >&2; }

if [ ! -f "$VALIDATE_PY" ]; then
  _err "validate_workflow.py not found at $VALIDATE_PY"
  exit 1
fi

if [ ! -d "$TMP_DIR" ]; then
  _err "tmp dir not found: $TMP_DIR"
  exit 1
fi

# ── Fetch existing workflow list, build filename→id map as JSON ──
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

# ── Validate each YAML ───────────────────────────────────
TOTAL=0; PASS=0; FAIL=0

for yml in "$TMP_DIR"/*.yml; do
  [ -f "$yml" ] || continue
  TOTAL=$((TOTAL + 1))
  fname=$(basename "$yml")

  wid=$(echo "$WF_MAP_JSON" | $VENV_PY -c "import sys,json; m=json.load(sys.stdin); print(m.get('${fname}', '${HARDCODED_WF_ID}'))" 2>/dev/null || echo "$HARDCODED_WF_ID")

  result=$($VENV_PY "$VALIDATE_PY" "$yml" --workflow-id "$wid" --cookie "$GITCODE_COOKIE" 2>&1)
  rc=$?

  case $rc in
    0) PASS=$((PASS + 1)); _log "[$TOTAL] $fname — VALID" ;;
    1) FAIL=$((FAIL + 1)); _log "[$TOTAL] $fname — INVALID"
       echo "$result" | while IFS= read -r l; do _log "  $l"; done ;;
    *) FAIL=$((FAIL + 1)); _log "[$TOTAL] $fname — ERROR (rc=$rc)"
       echo "$result" | while IFS= read -r l; do _log "  $l"; done ;;
  esac
done

_log ""
_log "═══════════════════════════════════════"
_log "Done: $TOTAL files — $PASS valid, $FAIL invalid/error"
_log "═══════════════════════════════════════"
