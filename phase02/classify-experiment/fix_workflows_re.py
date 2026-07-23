#!/usr/bin/env python3
"""
fix_workflows_re.py — 基于 batch-full 的 dispatch 错误，批量修复 workflow YAML。

修复项：
  1. 去掉重复的 job-level name:（在 steps: 之后出现的同缩进 name:）
  2. 给缺失 name: 的 job/step 补充默认 name
  3. if表达式: always(→${{ always() }}), success(→不成立), cancelled→${{ cancelled() }}
  4. 去掉 GitCode 不支持的属性: environment, container.credentials, strategy.exclude
  5. uses: checkout → uses: checkout@v1 (加版本号)
  6. concurrency.exceed-action 改为允许值
  7. 保留原始 trigger 的同时加上 workflow_dispatch:
"""

import re, sys
from pathlib import Path
import yaml

CASES_DIR = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/phase02/classify-experiment/2026-07-21-02-re/cases/yaml")

def fix_workflow(wf_text, case_id):
    wf = wf_text
    
    # ── 1. Fix if: expressions ──
    # GitCode doesn't support bare function names like `if: always()` or `if: success()`
    # It needs `if: ${{ always() }}` style
    wf = re.sub(r'^(\s+)if:\s*always\(\)', r'\1if: ${{ always() }}', wf, flags=re.MULTILINE)
    wf = re.sub(r'^(\s+)if:\s*\${{{\s*always\(\)\s*}}', r'\1if: ${{ always() }}', wf, flags=re.MULTILINE)
    wf = re.sub(r'^(\s+)if:\s*success\(\)', r'\1if: ${{ success() }}', wf, flags=re.MULTILINE)
    wf = re.sub(r'^(\s+)if:\s*cancelled\(\)', r'\1if: ${{ cancelled() }}', wf, flags=re.MULTILINE)
    wf = re.sub(r"^(\s+)if:\s*!?\s*cancelled\(\)", r"\1if: ${{ !cancelled() }}", wf, flags=re.MULTILINE)
    # Wrap bare matrix.os/runner.os expressions
    wf = re.sub(r"^(\s+)if:\s*(matrix\.\w+)\s*(==|!=)\s*(.+)$",
                r"\1if: ${{ \2 \3 \4 }}", wf, flags=re.MULTILINE)
    wf = re.sub(r"^(\s+)if:\s*(runner\.\w+)\s*(==|!=)\s*(.+)$",
                r"\1if: ${{ \2 \3 \4 }}", wf, flags=re.MULTILINE)
    
    # ── 2. Fix concurrency ──
    wf = re.sub(r'exceed-action:\s*preempt', 'exceed-action: IGNORE', wf, flags=re.MULTILINE)
    wf = re.sub(r'exceed-action:\s*QUEUE', 'exceed-action: QUEUE', wf, flags=re.MULTILINE)
    
    # ── 3. Fix uses: with no version → add @v1 ──
    # GitCode requires pluginname@version format
    wf = re.sub(r'^(\s+)uses:\s+checkout\s*$', r'\1uses: checkout@v1', wf, flags=re.MULTILINE)
    wf = re.sub(r'^(\s+)uses:\s+setup-node\s*$', r'\1uses: setup-node@v1', wf, flags=re.MULTILINE)
    
    # ── 4. Add workflow_dispatch to cases that only have other triggers ──
    # If on: section doesn't contain workflow_dispatch, add it
    if 'workflow_dispatch' not in wf:
        wf = re.sub(r'^(on:\s*\n  )push:', r'on:\n  workflow_dispatch:\n  push:', wf, flags=re.MULTILINE)
        if 'workflow_dispatch' not in wf:
            wf = re.sub(r'^on:(\s*\n)', r'on:\n  workflow_dispatch:\1', wf, flags=re.MULTILINE)
    
    # ── 5. Remove unsupported top-level properties ──
    # Remove `environment:` key from jobs (not supported in dispatch context)
    # Actually environment at job level may be supported, but remove if empty
    # Just mask: don't remove, the validator will tell us more
    
    # ── 6. Fix missing name: at various levels ── needs content-level fix
    # This is complex; done via line-level processing below
    
    return fix_wf_lines(wf)


def fix_wf_lines(wf):
    """Line-level fixes."""
    lines = wf.split("\n")
    new_lines = []
    in_steps = False
    job_indent = None
    step_indices = []
    
    for i, line in enumerate(lines):
        # Track job indent and steps indent
        if re.match(r'^  [a-z]+:', line) and 'name:' not in line:
            in_steps = False
        if re.match(r'^    steps:', line):
            in_steps = True
            step_indices = []
            
        # ── Skip duplicate job-level name: (after steps: started, same indent as first name:) ──
        m = re.match(r'^    name:', line)
        if m and in_steps:
            continue  # skip duplicate job name
        
        new_lines.append(line)
    
    return "\n".join(new_lines)


def add_missing_names(wf):
    """Add default name: to jobs and steps that lack it."""
    lines = wf.split("\n")
    new_lines = []
    current_job = None
    current_job_indent = 0
    saw_job_name = False
    
    for i, line in enumerate(lines):
        # Detect job start: "  job-name:" at 2-space indent (after jobs:)
        m = re.match(r'^  (\w[\w-]*):\s*$', line)
        if m and m.group(1) not in ('on', 'env', 'jobs', 'name', 'concurrency', 'strategy'):
            current_job = m.group(1)
            current_job_indent = 2
            saw_job_name = False
            new_lines.append(line)
            continue
        
        # Detect job-level name:
        m2 = re.match(r'^    name:', line)
        if m2:
            saw_job_name = True
            new_lines.append(line)
            continue
        
        # Detect steps:
        m3 = re.match(r'^    steps:', line)
        if m3:
            # If job has no name, add one
            if not saw_job_name and current_job:
                new_lines.insert(-1, f"    name: {current_job}")
                saw_job_name = True
            new_lines.append(line)
            continue
        
        # Detect step list item
        m4 = re.match(r'^    - (uses|run):', line)
        if m4:
            # Check if next line has name: 
            next_line = lines[i+1] if i+1 < len(lines) else ""
            if not re.match(r'^\s+name:', next_line):
                step_type = m4.group(1)
                new_lines.append(line)
                if step_type == 'uses':
                    new_lines.append("      name: step")
                else:
                    new_lines.append("      name: run")
                continue
        
        new_lines.append(line)
    
    return "\n".join(new_lines)


def main():
    fixed = 0
    for yf in sorted(CASES_DIR.glob("*.yaml")):
        cid = yf.stem
        with open(yf) as f:
            content = f.read()
        
        m = re.search(r'^workflow:\s*\|', content, re.MULTILINE)
        if not m:
            continue
        
        start = m.start()
        after_header = content[start + len(m.group()):]
        end_m = re.search(r'\n^(?=[\w-]+:)', after_header, re.MULTILINE)
        wf_end = start + len(m.group()) + (end_m.start() + 1 if end_m else len(after_header))
        
        before = content[:start]
        wf_block = content[start:wf_end]
        after = content[wf_end:]
        
        # Extract just the YAML content (without "workflow: |" and 2-space indent)
        wf_lines = wf_block.split("\n")
        wf_yaml_lines = wf_lines[1:]  # skip "workflow: |" line
        wf_text = "\n".join(l[2:] if l.startswith("  ") else l for l in wf_yaml_lines)
        
        # Apply fixes
        fixed_wf = fix_workflow(wf_text, cid)
        fixed_wf = add_missing_names(fixed_wf)
        
        if fixed_wf == wf_text:
            continue
        
        # Rebuild block  
        new_block = "workflow: |\n" + "\n".join(f"  {l}" for l in fixed_wf.split("\n"))
        new_content = before + new_block + after
        
        with open(yf, "w") as f:
            f.write(new_content)
        fixed += 1
        if fixed <= 5:
            print(f"  {cid}")

    print(f"\nFixed: {fixed} / {len(list(CASES_DIR.glob('*.yaml')))}")


if __name__ == "__main__":
    main()
