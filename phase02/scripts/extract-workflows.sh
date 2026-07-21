#!/bin/bash
# extract-workflows.sh — 从 case YAML 中提取 workflow 字段到 tmp/
# Usage: ./extract-workflows.sh <cases-yaml-dir> [output-dir]
set -euo pipefail

CASES_DIR="${1:?Usage: $0 <cases-yaml-dir> [output-dir]}"
OUT_DIR="${2:-${PWD}/tmp}"

mkdir -p "$OUT_DIR"
VENV_PY="/tmp/phase02-venv/bin/python3"

COUNT=0
for case_file in "$CASES_DIR"/*.yaml; do
  [ -f "$case_file" ] || continue
  case_id=$(basename "$case_file" .yaml)
  wf_name=$(echo "$case_id" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g').yml

  $VENV_PY -c "
import yaml
with open('${case_file}') as f:
    c = yaml.safe_load(f)
wf = c.get('workflow', '')
if wf:
    with open('${OUT_DIR}/${wf_name}', 'w') as out:
        out.write(wf)
    print('OK')
else:
    print('SKIP: no workflow field')
" 2>&1

  COUNT=$((COUNT + 1))
done

echo ""
echo "Done: processed ${COUNT} cases, output in ${OUT_DIR}/"
ls "$OUT_DIR" | wc -l | xargs echo "  workflow files:"
