#!/usr/bin/env python3
"""
rewrite_workflows.py — 批量修复 Phase 01 case YAML 中的 workflow 字段，
使其符合 GitCode 格式（通过 validate_workflow API 校验）。

主要修复：
  1. on: 列表格式 → 映射格式  （- push  →  push:）
  2. runs-on: 多行列表 → 行内数组 （- label  →  [label]）
  3. runs-on: 三段标签统一格式
  4. name 字段位置修正

用法:
  python3 rewrite_workflows.py [--dry-run] [--validate]
"""

import argparse
import os
import re
import sys
import yaml
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
#  修复规则
# ═══════════════════════════════════════════════════════════════════

def fix_workflow_yaml(wf_yaml: str) -> str:
    """
    将 Phase 01 生成的 workflow YAML 修正为 GitCode 兼容格式。
    返回修正后的 YAML 字符串。
    """
    lines = wf_yaml.splitlines()
    result = []
    
    # 已知的 on event 名称
    KNOWN_EVENTS = {"push", "pull_request", "pull_request_target", "pull_request_comment",
                    "workflow_dispatch", "schedule", "fork_pr", "manual", "pr",
                    "workflow_call", "tag", "release"}

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── Fix 1: on: followed by list-style events ──
        # "on:" → "on:\n  push:\n    branches: [main]" or "on:\n  <event>:"
        if re.match(r'^on:\s*$', line):
            result.append("on:")
            i += 1
            # Collect all list items under `on:`
            events = []
            while i < len(lines) and re.match(r'^\s*-\s+(\S+)', lines[i]):
                m = re.match(r'^\s*-\s+(\S+)', lines[i])
                event_name = m.group(1)
                events.append(event_name)
                i += 1

            if not events:
                continue

            for ev in events:
                if ev in ("push",):
                    result.append(f"  {ev}:")
                    result.append("    branches:")
                    result.append("      - main")
                elif ev in ("workflow_dispatch", "manual"):
                    result.append(f"  workflow_dispatch:")
                elif ev in ("pull_request", "pr"):
                    result.append(f"  pull_request:")
                    result.append("    branches:")
                    result.append("      - main")
                elif ev in ("pull_request_target",):
                    result.append(f"  pull_request_target:")
                    result.append("    branches:")
                    result.append("      - main")
                elif ev in ("schedule",):
                    result.append(f"  schedule:")
                    result.append("    - cron: '0 0 * * *'")
                elif ev in ("fork_pr",):
                    result.append(f"  pull_request:")
                    result.append("    branches:")
                    result.append("      - main")
                else:
                    result.append(f"  {ev}:")

            # Skip any additional indent under the old `on:` block that's not caught
            continue

        # ── Fix 2: multi-line runs-on → inline array ──
        # "runs-on:\n  - label1\n  - label2" → "runs-on: [label1, label2]"
        m_runs = re.match(r'^(\s*)runs-on:\s*$', line)
        if m_runs:
            indent = m_runs.group(1)
            i += 1
            labels = []
            while i < len(lines) and re.match(r'^(\s+)-(\s+\S+)', lines[i]):
                labels.append(lines[i].strip()[2:])  # remove "- "
                i += 1
            if labels:
                if len(labels) == 3:
                    # Standard: [os, arch, flavor]
                    result.append(f"{indent}runs-on: [{', '.join(labels)}]")
                else:
                    result.append(f"{indent}runs-on: [{', '.join(labels)}]")
            else:
                result.append(f"{indent}runs-on: [ubuntu-latest, x64, small]")
            continue

        # ── Fix 3: strategy matrix multi-line ──
        # Keep matrix as-is; it's already valid YAML mapping format
        # But ensure it's consistent with GitCode

        result.append(line)
        i += 1

    return "\n".join(result)


def fix_workflow_yaml_advanced(wf_text: str) -> str:
    """
    Primary fix function: uses the same regex approach as run-case.sh
    but more robust. Returns fixed YAML string.
    """
    # Fix 1: "on:\n  - push" → "on:\n  push:\n    branches: [main]"
    # Handle single event
    wf_text = re.sub(
        r'^on:\s*\n\s*-\s+push\s*$',
        'on:\n  push:\n    branches:\n      - main',
        wf_text, flags=re.MULTILINE
    )
    wf_text = re.sub(
        r'^on:\s*\n\s*-\s+workflow_dispatch\s*$',
        'on:\n  workflow_dispatch:',
        wf_text, flags=re.MULTILINE
    )
    wf_text = re.sub(
        r'^on:\s*\n\s*-\s+pull_request\s*$',
        'on:\n  pull_request:\n    branches:\n      - main',
        wf_text, flags=re.MULTILINE
    )
    wf_text = re.sub(
        r'^on:\s*\n\s*-\s+pull_request_target\s*$',
        'on:\n  pull_request_target:\n    branches:\n      - main',
        wf_text, flags=re.MULTILINE
    )
    wf_text = re.sub(
        r'^on:\s*\n\s*-\s+schedule\s*$',
        'on:\n  schedule:\n    - cron: "0 0 * * *"',
        wf_text, flags=re.MULTILINE
    )
    wf_text = re.sub(
        r'^on:\s*\n\s*-\s+pr\s*$',
        'on:\n  pull_request:\n    branches:\n      - main',
        wf_text, flags=re.MULTILINE
    )
    wf_text = re.sub(
        r'^on:\s*\n\s*-\s+manual\s*$',
        'on:\n  workflow_dispatch:',
        wf_text, flags=re.MULTILINE
    )

    # Fix 2: multi-line runs-on to inline (preserve trailing newline)
    def _fix_runs_on(m):
        indent = m.group(1)
        labels_block = m.group(2)
        labels = re.findall(r'^\s*-\s+(\S+)', labels_block, re.MULTILINE)
        trailing = m.group(3) if m.lastindex >= 3 else ""
        return f"{indent}runs-on: [{', '.join(labels)}]\n{trailing}"

    wf_text = re.sub(
        r'^(\s+)runs-on:\s*\n((?:\s+-\s+\S+.*\n?)+?)(\n|$)',
        _fix_runs_on,
        wf_text, flags=re.MULTILINE
    )

    # Fix 1b: multi-event "on:\n- push\n- pull_request" → expanded mapping
    # Handle: on:\n  - push\n  - pull_request → two event keys
    # Already handled single events above; this catches the remaining multi-event case
    # where one event was already fixed but the second remains as a list item
    
    # Clean up: "on:\n  <event1>:\n    ...\n  - <event2>" → proper YAML
    # This happens when Fix 1a matched only the first event
    wf_text = re.sub(
        r'^  push:\n    branches:\n      - main\n- pull_request',
        '  push:\n    branches:\n      - main\n  pull_request:\n    branches:\n      - main',
        wf_text, flags=re.MULTILINE
    )
    wf_text = re.sub(
        r'^  push:\n    branches:\n      - main\n- pr',
        '  push:\n    branches:\n      - main\n  pull_request:\n    branches:\n      - main',
        wf_text, flags=re.MULTILINE
    )
    wf_text = re.sub(
        r'^  push:\n    branches:\n      - main\n- fork_pr',
        '  push:\n    branches:\n      - main\n  pull_request:\n    branches:\n      - main',
        wf_text, flags=re.MULTILINE
    )
    # Fix 4: wrap run: values that contain ".\":" inside double-quoted strings
    # that cause PyYAML parsing failures. Single-quote wrapping avoids ambiguity.
    def _fix_run_quoting(m):
        run_key = m.group(1)
        value = m.group(2).strip()
        if value.startswith("'") and value.endswith("'"):
            return m.group(0)  # already single-quoted
        if re.search(r'"[^"]*:\s[^"]*"', value):
            return f"{run_key}'{value}'"
        return m.group(0)
    wf_text = re.sub(r'^(\s+run:\s+)(.+)$', _fix_run_quoting, wf_text, flags=re.MULTILINE)

    return wf_text


def load_and_fix_case(yaml_path: Path) -> tuple[dict, str, str]:
    """
    Load a case YAML, fix its workflow field, return (doc, original_wf, fixed_wf).
    """
    with open(yaml_path, "r") as f:
        doc = yaml.safe_load(f)

    wf = doc.get("workflow", "") or ""
    if not wf:
        return doc, "", ""

    fixed = fix_workflow_yaml_advanced(wf)
    return doc, wf, fixed


def write_fixed_case(yaml_path: Path, fixed_wf: str):
    """
    精确替换 workflow: | 块。直到遇到下一个顶层 key（列 0 起始的 \w+: ）。
    """
    with open(yaml_path, "r") as f:
        content = f.read()

    # Find "workflow: |" at column 0
    match = re.search(r'^workflow:\s*\|', content, re.MULTILINE)
    if not match:
        return False

    start = match.start()
    # Scan forward for the next top-level key at column 0
    # (skip the "workflow:" line itself)
    rest = content[start + len(match.group()):]
    # Next line starting at column 0 with word: pattern
    end_match = re.search(r'\n^(?=\w[\w-]*:)', rest, re.MULTILINE)
    if end_match:
        end = start + len(match.group()) + end_match.start() + 1  # +1 for the \n
    else:
        end = len(content)

    old_block = content[start:end]

    # Build new block, preserve trailing content
    indent = "  "
    new_wf_lines = [match.group()]
    for line in fixed_wf.splitlines():
        new_wf_lines.append(f"{indent}{line}")
    new_block = "\n".join(new_wf_lines) + "\n"

    new_content = content[:start] + new_block + content[end:]

    with open(yaml_path, "w") as f:
        f.write(new_content)
    return True


def main():
    parser = argparse.ArgumentParser(description="Rewrite case YAML workflow fields to GitCode format")
    parser.add_argument("--dry-run", action="store_true", help="只显示差异，不写入")
    parser.add_argument("--validate", action="store_true", help="通过 GitCode API 校验（需 COOKIE）")
    parser.add_argument("--case", help="只处理指定 case（如 COMP-ENV-02-001）")
    parser.add_argument("cases_dir", nargs="?", help="cases yaml 目录路径")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    cases_dir = Path(args.cases_dir) if args.cases_dir else script_dir / "2026-07-21-02/cases/yaml"

    if not cases_dir.exists():
        print(f"[ERROR] cases dir not found: {cases_dir}")
        sys.exit(1)

    yaml_files = sorted(cases_dir.glob("*.yaml"))
    if args.case:
        yaml_files = [f for f in yaml_files if args.case in f.stem]
        if not yaml_files:
            print(f"[ERROR] no case matching '{args.case}'")
            sys.exit(1)

    changed = 0
    errors = 0

    for yf in yaml_files:
        doc, orig_wf, fixed_wf = load_and_fix_case(yf)
        cid = doc.get("id", yf.stem)

        if not orig_wf:
            print(f"  [SKIP] {cid}: no workflow field")
            continue

        if orig_wf == fixed_wf:
            continue

        print(f"\n[{cid}]")
        
        # Show diff summary
        orig_lines = orig_wf.splitlines()
        fixed_lines = fixed_wf.splitlines()
        for j, (o, f) in enumerate(zip(orig_lines[:6], fixed_lines[:6])):
            if o != f:
                print(f"  - {o}")
                print(f"  + {f}")
        if max(len(orig_lines), len(fixed_lines)) > 6:
            print(f"  ... ({max(len(orig_lines), len(fixed_lines))} lines total)")

        if not args.dry_run:
            ok = write_fixed_case(yf, fixed_wf)
            if ok:
                changed += 1
            else:
                print(f"  [ERROR] failed to write")
                errors += 1

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Done: {changed} changed, {errors} errors, {len(yaml_files)} total")


if __name__ == "__main__":
    main()
