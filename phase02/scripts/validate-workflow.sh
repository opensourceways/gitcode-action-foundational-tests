#!/bin/bash
# validate-workflow.sh — 通过 GitCode v2 API 校验 workflow YAML 格式
# Usage:
#   ./validate-workflow.sh <yaml-file>                          # 自动匹配 workflow_id
#   ./validate-workflow.sh <yaml-file> <workflow-id>             # 指定 workflow_id
#   ./validate-workflow.sh <yaml-file> --new                     # 不关联已有 workflow
#   ./validate-workflow.sh --batch <dir>                         # 批量校验目录下所有 yaml
set -euo pipefail

YAML_FILE="${1:?Usage: $0 <yaml-file> [workflow-id|--new]  or  $0 --batch <dir>}"
ARG2="${2:-}"

: ${GITCODE_ACCESS_TOKEN:?请设置 GITCODE_ACCESS_TOKEN}
: ${GITCODE_EXECUTOR:="ccijunk"}
: ${GITCODE_OWNER:="ComputingActionTest"}
: ${GITCODE_REPO:="foundational-tests"}

API_BASE="https://web-api.gitcode.com"
PROJECT_ID="${GITCODE_OWNER}%2F${GITCODE_REPO}"
VENV_PY="/tmp/phase02-venv/bin/python3"

_log()   { echo "[$(date +%H:%M:%S)] $*"; }
_err()   { echo "[$(date +%H:%M:%S)] ERROR: $*" >&2; }

# ── Common curl headers ──────────────────────────────────
_curl() {
  curl -sS "$@" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${GITCODE_ACCESS_TOKEN}" \
    -H "Origin: https://gitcode.com" \
    -H "Referer: https://gitcode.com/" \
    -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
    -H "X-App-Channel: gitcode-fe" \
    -H "X-App-Version: 0" \
    -H "X-Device-ID: unknown" \
    -H "X-Device-Type: Linux" \
    -H "X-Platform: web" \
    -b "GITCODE_ACCESS_TOKEN=${GITCODE_ACCESS_TOKEN}; GitCodeUserName=${GITCODE_EXECUTOR}"
}

# ── Fetch workflow list from repo ─────────────────────────
_get_workflow_list() {
  _curl -X POST "${API_BASE}/api/v2/projects/${PROJECT_ID}/actions/workflows/list" \
    -d '{}' 2>&1
}

# ── Resolve workflow_id by filename match ─────────────────
_resolve_workflow_id() {
  local yaml_file="$1"
  local basename
  basename=$(basename "$yaml_file")

  local wf_list
  wf_list=$(_get_workflow_list)

  # Match by filename
  local wid
  wid=$(echo "$wf_list" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    target = '${basename}'
    for wf in data.get('content', []):
        fp = wf.get('file_path', '')
        if fp.endswith(target) or target in fp:
            print(wf.get('workflow_id', ''))
            break
except: pass
" 2>/dev/null || echo "")

  echo "$wid"
}

# ── Validate single YAML ──────────────────────────────────
_validate_one() {
  local yaml_file="$1"
  local workflow_id="${2:-}"

  if [ ! -f "$yaml_file" ]; then
    _err "File not found: $yaml_file"
    return 2
  fi

  local yaml_content
  yaml_content=$(cat "$yaml_file")

  # Encode content as base64 (GitCode v2 API expects base64 in JSON body)
  local body
  body=$(echo "$yaml_content" | base64 -w0)

  local url
  if [ -n "$workflow_id" ]; then
    url="${API_BASE}/api/v2/projects/${PROJECT_ID}/actions/valid?workflow_id=${workflow_id}"
  else
    url="${API_BASE}/api/v2/projects/${PROJECT_ID}/actions/valid"
  fi

  local response
  response=$(_curl -X POST "$url" -d "{\"content\":\"$body\"}" 2>&1)

  echo "$response" | $VENV_PY -c "
import sys, json

try:
    data = json.load(sys.stdin)
except Exception as e:
    print(f'PARSE_ERROR: {e}')
    sys.exit(2)

valid = data.get('valid', None)
diagnostics = data.get('diagnostics', [])
error_code = data.get('error_code', '')
error_msg = data.get('error_message', '')

if error_code:
    print(f'API_ERROR: {error_code} — {error_msg}')
    sys.exit(2)

if valid is True:
    print('VALID')
    sys.exit(0)
elif valid is False:
    msgs = []
    for d in diagnostics:
        sev = d.get('severity', '?')
        msg = d.get('message') or '(no detail)'
        rng = d.get('range', {})
        s = rng.get('start', {})
        msgs.append(f'[{sev}] L{s.get(\"line\",\"?\")}:C{s.get(\"column\",\"?\")} — {msg}')
    if msgs:
        print('INVALID: ' + '; '.join(msgs))
    else:
        print('INVALID: (no diagnostics from server)')
    sys.exit(1)
else:
    print(f'UNKNOWN: {json.dumps(data)}')
    sys.exit(2)
"
}

# ── Main ──────────────────────────────────────────────────
if [ "$YAML_FILE" = "--batch" ]; then
  # Batch mode: validate all YAML files in directory
  BATCH_DIR="${ARG2:?Usage: $0 --batch <directory>}"
  _log "Batch validating YAML files in: $BATCH_DIR"

  TOTAL=0; PASS=0; FAIL=0; ERR=0
  for f in "$BATCH_DIR"/*.yaml "$BATCH_DIR"/*.yml; do
    [ -f "$f" ] || continue
    TOTAL=$((TOTAL + 1))
    fname=$(basename "$f")

    wid=$(_resolve_workflow_id "$f")
    if [ -z "$wid" ]; then
      _log "[$TOTAL] $fname — SKIP (no workflow_id, use --new or deploy first)"
      ERR=$((ERR + 1))
      continue
    fi

    result=$(_validate_one "$f" "$wid")
    case $? in
      0) PASS=$((PASS + 1)); _log "[$TOTAL] $fname — $result" ;;
      1) FAIL=$((FAIL + 1)); _log "[$TOTAL] $fname — $result" ;;
      *) ERR=$((ERR + 1));  _log "[$TOTAL] $fname — $result" ;;
    esac
  done

  _log "Done: $TOTAL files — $PASS valid, $FAIL invalid, $ERR errors"
  [ "$FAIL" -eq 0 ] && [ "$ERR" -eq 0 ]

else
  # Single file mode
  WORKFLOW_ID=""

  if [ "$ARG2" = "--new" ]; then
    :
  elif [ -n "$ARG2" ]; then
    WORKFLOW_ID="$ARG2"
  else
    WORKFLOW_ID=$(_resolve_workflow_id "$YAML_FILE")
    if [ -z "$WORKFLOW_ID" ]; then
      _log "WARNING: No matching workflow_id found. Use --new or deploy first."
      _log "Trying without workflow_id..."
    fi
  fi

  _log "Validating: $(basename $YAML_FILE)"
  [ -n "$WORKFLOW_ID" ] && _log "  workflow_id: $WORKFLOW_ID"

  _validate_one "$YAML_FILE" "$WORKFLOW_ID"
fi
