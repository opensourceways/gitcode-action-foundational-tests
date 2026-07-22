#!/usr/bin/env python3
"""
Rewrite workflow `on:` triggers to `workflow_dispatch` for cases
that don't specifically test trigger behavior.

Cases that KEEP their original trigger:
  - Non-push triggers (pr, schedule, fork_pr, etc.) → testing that trigger
  - Push cases specifically testing push behavior:
    COMP-TRIGGER, COMP-FILTER, COMPAT-PATHS, COMPAT-RECURSIVE, REL-PUSH-DEDUP

All other push-trigger cases → workflow_dispatch (can be triggered via dispatch API).
"""

import re, yaml
from pathlib import Path

# Cases that should keep their original trigger (testing trigger behavior)
KEEP_ORIGINAL_TRIGGER = {
    # Explicitly testing push trigger behavior
    "COMP-TRIGGER-02-001",    # 验证各种 trigger 事件
    "COMP-FILTER-02-001",     # 验证 push 路径过滤
    "COMPAT-PATHS-02-001",    # 验证 push paths
    "COMPAT-RECURSIVE-02-001",# 验证递归 push 触发
    "REL-PUSH-DEDUP-02-001",  # 验证 push 去重
}

def should_keep_trigger(cid, trigger_event):
    """Return True if the case should keep its original trigger."""
    if cid in KEEP_ORIGINAL_TRIGGER:
        return True
    # Non-push triggers are typically testing that specific trigger mechanism
    if trigger_event != "push":
        return True
    # Push trigger but not in the keep list → can be dispatched
    return False


def replace_trigger_in_wf(wf_text):
    """Replace 'on:' block with 'on:\n  workflow_dispatch:'."""
    # The wf_text has already been through fix_workflow_yaml_advanced,
    # so 'on:' should be in mapping format already.
    # Replace the entire on: section (from "on:" to the next top-level key)
    lines = wf_text.split("\n")
    result = []
    in_on = False
    skip = False
    
    for i, line in enumerate(lines):
        if not in_on:
            if re.match(r'^on:\s*$', line) or re.match(r'^on:\s+', line):
                in_on = True
                result.append("on:")
                result.append("  workflow_dispatch:")
                # Already added, now skip remaining on: block lines
                skip = True
                continue
            result.append(line)
        else:
            # Check if we're still in the on: block
            # Lines with 2-space indent (matching on: block children) or comments
            if line.startswith("  ") and line.lstrip() and not line.strip().startswith("#"):
                if skip:
                    continue  # skip lines within old on: block
                result.append(line)
            elif line.strip() == "" and skip:
                continue  # skip blank lines after on: block
            else:
                # End of on: block
                in_on = False
                skip = False
                if line.strip():
                    result.append(line)
    
    return "\n".join(result)


def main():
    cases_dir = Path(__file__).resolve().parent / "2026-07-21-02/cases/yaml"

    changed = 0
    skipped = 0
    for yf in sorted(cases_dir.glob("*.yaml")):
        cid = yf.stem
        with open(yf) as f:
            content = f.read()
            doc = yaml.safe_load(content)

        trigger_event = (doc.get("trigger") or {}).get("event", "push")
        
        if should_keep_trigger(cid, trigger_event):
            skipped += 1
            continue

        # Replace trigger in the workflow field
        wf = doc.get("workflow", "")
        if not wf:
            continue

        new_wf = replace_trigger_in_wf(wf)
        if new_wf == wf:
            continue

        # Write back
        # Find workflow: | block and replace
        with open(yf) as f:
            raw = f.read()

        match = re.search(r'^workflow:\s*\|', raw, re.MULTILINE)
        if not match:
            continue

        start = match.start()
        rest = raw[start + len(match.group()):]
        end_match = re.search(r'\n^(?=[\w-]+:)', rest, re.MULTILINE)
        end = start + len(match.group()) + (end_match.start() + 1 if end_match else len(rest))

        indent = "  "
        new_block_lines = [match.group()]
        for line in new_wf.splitlines():
            new_block_lines.append(f"{indent}{line}")
        new_block = "\n".join(new_block_lines) + "\n"

        new_raw = raw[:start] + new_block + raw[end:]
        with open(yf, "w") as f:
            f.write(new_raw)
        changed += 1
        print(f"  {cid}: push → workflow_dispatch")

    print(f"\nDone: {changed} changed, {skipped} kept original trigger")


if __name__ == "__main__":
    main()
