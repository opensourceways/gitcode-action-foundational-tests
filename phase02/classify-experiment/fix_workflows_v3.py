#!/usr/bin/env python3
"""
fix_workflows_v3.py — Read validation log, classify errors, apply fixes per validate-guide.md

Error → fix mapping:
  empty_name       → add missing job/step name (#10)
  bare_if          → wrap in ${{ }} / add () (#5)
  dup_key          → remove duplicate name: (#2)
  stages_format    → convert stages[] to map
  concurrency      → fix empty/invalid/unknown concurrency values
  permissions_block→ remove whole permissions block (#7)
  illegal_name_chars→ replace [...] with (...) (#3)
  runson_single    → convert to inline array (#6)
  strategy_unknown → remove exclude/include
  environment/svc  → remove unknown blocks (negative tests → skip)

Usage:
  # Dry run: just show what would be fixed
  python fix_workflows_v3.py --dry-run
  
  # Apply fixes
  python fix_workflows_v3.py
"""

import re
import os
import sys
import copy
from collections import Counter


CASE_YAML_DIR = os.path.join(os.path.dirname(__file__), "2026-07-21-02-re", "cases", "yaml")
LOG_FILE = "/tmp/v11_full.log"

# Intentional negative test patterns — skip fixing these
INTENTIONAL_NEGATIVE = {
    "plugin_not_found": True,   # Tests for non-existent plugin
    "uses_format": True,        # Tests for invalid uses format
    "steps_unknown": True,      # Tests for unsupported steps in call
    "secrets_unknown": True,    # Tests for unsupported secrets in step
    "on_branches_limit": True,  # Tests for branch limit enforcement
    "on_types_illegal": True,   # Tests for invalid types
    "on_format": True,          # Tests for array format on:
    "container_image_empty": True, # Tests for empty container image
    "run_name_unknown": True,   # Tests for unsupported run-name
    "matrix_if": True,           # runner.os / matrix.os in if → compatibility test
}


def parse_validation_log():
    """Parse the validation log into case_id → [error_msg] mapping."""
    with open(LOG_FILE) as f:
        content = f.read()

    case_errors = {}
    current_case = None

    for line in content.split("\n"):
        m = re.search(r'\] \[(\d+)\] ([\w-]+) — (INVALID|ERROR)', line)
        if m:
            current_case = m.group(2)
            if current_case not in case_errors:
                case_errors[current_case] = []
            continue
        m = re.search(r'\[Error\] L\d+:C\d+ — (.+)', line)
        if m and current_case:
            msg = m.group(1).strip()
            case_errors[current_case].append(msg)
            continue

    return case_errors


def classify_error(msg):
    """Classify an error message into a fix category."""
    if "重复的键" in msg:
        return "dup_key"
    if "值不能为空" in msg and ".name" in msg:
        if "stages[" in msg or "post." in msg:
            return "empty_stage_name"
        return "empty_name"
    if "值不能为空" in msg and ".runs-on" in msg:
        return "empty_runson"
    if "值不能为空" in msg and ".steps" in msg:
        return "empty_steps"
    if "while parsing" in msg or "mapping values" in msg:
        return "yaml_parse"
    if "名称仅支持输入" in msg:
        return "illegal_name_chars"
    if "if表达式无法解析" in msg:
        if "runner.os" in msg or "matrix." in msg:
            return "matrix_if"  # compatibility test, skip
        return "bare_if"
    if "permissions" in msg and "unknown property" in msg:
        return "permissions_block"
    if ".environment" in msg and "unknown property" in msg:
        return "environment_unknown"
    if ".services" in msg and "unknown property" in msg:
        return "services_unknown"
    if "strategy" in msg and "unknown property" in msg:
        return "strategy_unknown"
    if "runs-on以单个字符串形式定义" in msg:
        return "runson_single"
    if "GitcodeStage" in msg or ("stages" in msg and "LinkedHashMap" in msg):
        return "stages_format"
    if "GitcodeNormalJob" in msg and "env" in msg:
        return "env_format"
    if "列表长度超出限制" in msg:
        return "on_branches_limit"
    if "列表中存在非法值" in msg:
        return "on_types_illegal"
    if ".uses: 格式错误" in msg:
        return "uses_format"
    if "插件" in msg and "不存在" in msg:
        return "plugin_not_found"
    if ".steps: unknown property" in msg:
        return "steps_unknown"
    if ".secrets: unknown property" in msg:
        return "secrets_unknown"
    if "GitcodeOn" in msg:
        return "on_format"
    if "container.image" in msg and "值不能为空" in msg:
        return "container_image_empty"
    if "run-name: unknown property" in msg:
        return "run_name_unknown"
    if "concurrency" in msg:
        return "concurrency"
    if "env" in msg and "String-argument" in msg:
        return "env_format"
    return "unknown"


# ─── YAML file I/O ───

def read_case_yaml(case_id):
    fpath = os.path.join(CASE_YAML_DIR, f"{case_id}.yaml")
    if not os.path.exists(fpath):
        return None
    with open(fpath) as f:
        return f.read()


def write_case_yaml(case_id, content):
    fpath = os.path.join(CASE_YAML_DIR, f"{case_id}.yaml")
    with open(fpath, "w") as f:
        f.write(content)


# ─── Fix functions ───

def fix_dup_key(lines):
    """Remove duplicate `name:` keys — same indent, same value, same parent block."""
    # Find all name: lines
    name_lines = []
    for i, line in enumerate(lines):
        m = re.match(r'^(\s*)name:\s+(.+)', line)
        if m:
            indent = len(m.group(1))
            val = m.group(2).strip()
            name_lines.append((i, indent, val))
    
    to_remove = set()
    # Check for same indent + same value within close range
    for idx, (i, indent, val) in enumerate(name_lines):
        for j in range(idx + 1, len(name_lines)):
            j_idx, j_indent, j_val = name_lines[j]
            if j_indent == indent and j_val == val and j_idx - i < 80:
                to_remove.add(j_idx)
                break
    
    # Also remove workflow-level `name: CASE-ID` that is clearly a duplicate artifact
    # Pattern: indent 0-2, value matches CASE-ID format, and there's content elsewhere
    for i, line in enumerate(lines):
        m = re.match(r'^\s{0,2}name:\s+([A-Z]+-[\w-]+-\d+)', line)
        if m and i not in to_remove:
            has_other_content = any(
                i2 != i and not re.match(r'^\s*$', lines[i2])
                for i2 in range(max(0,i-3), min(len(lines), i+3))
                if (i2 >= 0 and i2 < len(lines) and lines[i2] is not None)
            )
            is_near_jobs = any(
                re.match(r'^\s{2}jobs:', lines[k])
                for k in range(max(0,i-20), i)
            )
            if is_near_jobs:
                to_remove.add(i)
    
    new_lines = [l for idx, l in enumerate(lines) if idx not in to_remove]
    return new_lines, len(to_remove)


def fix_empty_name(lines):
    """
    Add missing `name:` to jobs and steps.
    - For each job without a name, add one derived from the job key.
    - For each step (- uses: / - run:) without a name, add a default name.
    """
    new_lines = []
    changed = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Match job key:   job-name:
        # Skip structural keys: on, jobs, steps, strategy, container, concurrency
        STRUCTURAL_KEYS = {"on", "jobs", "steps", "strategy", "container", "concurrency",
                          "env", "permissions", "inputs", "outputs", "secrets", "stages",
                          "needs", "runs-on", "if", "with", "credentials", "image",
                          "types", "branches", "branches-ignore", "workflow_dispatch",
                          "push", "pull_request", "pull_request_target", "merge_requests",
                          "pull_request_comment", "schedule", "workflow_call", "workflow_run",
                          "fork", "fork_pr", "matrix", "os", "node", "experimental",
                          "fail-fast", "max-parallel", "preemption", "post",
                          "enable", "events", "cancel-in-progress", "group"}
        jm = re.match(r'^(\s{2,})([\w-]+):\s*$', line)
        if jm and not line.strip().startswith("-"):
            job_key = jm.group(2)
            if job_key in STRUCTURAL_KEYS:
                i += 1
                continue
            indent = jm.group(1)
            job_content_indent = indent + "  "
            
            # Check if next lines have a name at job content indent
            has_name = False
            j = i + 1
            while j < len(lines):
                nl = lines[j]
                if re.match(rf'^{job_content_indent}name:', nl):
                    has_name = True
                    break
                if re.match(rf'^{indent}\S', nl) and not re.match(rf'^{job_content_indent}', nl):
                    break
                j += 1
            
            if not has_name:
                display_name = job_key.replace("-", " ").title()
                new_lines.append(f"{job_content_indent}name: {display_name}")
                changed += 1
        
        # Match step:    - uses: ...  or   - run: ...
        sm = re.match(r'^(\s{4,})-\s+(uses:|run:)', line)
        if sm:
            step_indent = sm.group(1)
            step_content_indent = step_indent + "  "
            step_type = sm.group(2)
            
            # Check if next lines have a name at step content indent
            has_name = False
            j = i + 1
            while j < len(lines):
                nl = lines[j]
                if re.match(rf'^{step_content_indent}name:', nl):
                    has_name = True
                    break
                if re.match(rf'^{step_indent}-\s+', nl):
                    break  # Next step starts
                if re.match(rf'^{step_indent[:-2]}\S', nl) and not re.match(rf'^{step_content_indent}', nl):
                    break  # Back to parent level
                j += 1
            
            if not has_name:
                if step_type == "uses:":
                    uses_val = re.sub(r'^uses:\s*', '', sm.group(0).replace(f"{step_indent}- ", "")).strip()
                    new_lines.append(f"{step_content_indent}name: Use {uses_val}")
                else:
                    new_lines.append(f"{step_content_indent}name: Run command")
                changed += 1
        
        i += 1
    
    return new_lines, changed


def fix_bare_if(lines):
    """
    Fix bare if: expressions:
    - if: always            → if: ${{ always() }}
    - if: ${{ always }}     → if: ${{ always() }}
    - if: ${{ matrix.os == 'ubuntu' }} → if: ${{ matrix.os == 'ubuntu' }}  (already valid)
    """
    new_lines = []
    changed = 0
    
    for line in lines:
        m = re.match(r'^(\s*)if:\s+(.+)$', line)
        if not m:
            new_lines.append(line)
            continue
        
        indent = m.group(1)
        val = m.group(2).strip()
        
        # Already properly wrapped: ${{ ... }}
        if val.startswith("${{") and val.endswith("}}"):
            inner = val[3:-2].strip()
            # Fix missing parentheses on bare keyword inside ${{ }}
            new_inner = re.sub(
                r'(?<!\${{)\b(always|success|failure|cancelled|failed)\b(?!\s*\(|}})',
                r'\1()',
                inner
            )
            if new_inner != inner:
                new_lines.append(f"{indent}if: ${{{{ {new_inner} }}}}")
                changed += 1
                continue
            new_lines.append(line)
            continue
        
        # Bare keyword without ${{ }}
        bare_map = {
            "always": "${{ always() }}",
            "success": "${{ success() }}",
            "failure": "${{ failure() }}",
            "cancelled": "${{ cancelled() }}",
            "failed": "${{ failure() }}",
        }
        if val.lower() in bare_map:
            new_lines.append(f"{indent}if: {bare_map[val.lower()]}")
            changed += 1
            continue
        
        # Complex expression — wrap in ${{ }}
        if any(kw in val.lower() for kw in ["matrix.", "runner.", "secrets.", "env.", "inputs."]):
            # If it looks like an expression, wrap
            if not val.startswith("${{"):
                new_lines.append(f"{indent}if: ${{{{ {val} }}}}")
                changed += 1
                continue
        
        new_lines.append(line)
    
    return new_lines, changed


def fix_illegal_name_chars(lines):
    """Replace unsupported characters in name values (both inline and multi-line)."""
    new_lines = []
    changed = 0
    for line in lines:
        # Match: "- name: value" (inline) or "  name: value" (multi-line)
        m = re.match(r'^(\s*(?:-\s+)?name:\s+)(.+)$', line)
        if m:
            prefix = m.group(1)
            val = m.group(2)
            new_val = val
            if "[" in val or "]" in val:
                new_val = new_val.replace("[", "(").replace("]", ")")
            new_val = new_val.replace("\u2014", "-").replace("\u2013", "-")
            for old, new in [("\u2018", "'"), ("\u2019", "'"), ("\u201c", '"'), ("\u201d", '"'),
                             ("\u2026", "..."), ("\u00a0", " ")]:
                new_val = new_val.replace(old, new)
            if new_val != val:
                new_lines.append(f"{prefix}{new_val}")
                changed += 1
                continue
        new_lines.append(line)
    return new_lines, changed


def fix_stages_format(lines):
    """
    Fix stages that are array format instead of map.
    Handles two indent styles:
      Style A (items same indent as stages):
        stages:
        - name: stage1
      Style B (items indented +2 from stages):
        stages:
          - name: stage1
    """
    for i, line in enumerate(lines):
        m = re.match(r'^(\s*)stages:\s*$', line)
        if not m:
            continue
        stages_indent = m.group(1)
        j = i + 1
        if j >= len(lines):
            continue
        
        # Detect which style
        item_indent = None
        if re.match(rf'^{stages_indent}-\s+name:', lines[j]):
            item_indent = stages_indent
        elif re.match(rf'^{stages_indent}  -\s+name:', lines[j]):
            item_indent = stages_indent + "  "
        else:
            continue
        
        # Collect stage definitions and remap indentation
        before = lines[:i]
        after = []
        k = i + 1
        indent_shift = 2  # add 2 spaces to children (stage name adds a level)
        
        while k < len(lines):
            if re.match(rf'^{item_indent}-\s+name:', lines[k]):
                nm = re.match(rf'^{item_indent}-\s+name:\s+(.+)', lines[k])
                stage_name = nm.group(1).strip() if nm else "default"
                after.append(f"{stages_indent}  {stage_name}:")
                k += 1
                
                # Process children until next - name: or end of stages
                while k < len(lines):
                    if re.match(rf'^{item_indent}-\s+name:', lines[k]):
                        break
                    if lines[k].strip() == "":
                        after.append("")
                        k += 1
                        continue
                    non_space = len(lines[k]) - len(lines[k].lstrip())
                    if non_space < len(stages_indent) + 1:
                        break  # Back to parent level
                    if non_space == len(stages_indent) and not re.match(rf'^{item_indent}-\s+', lines[k]):
                        break  # Non-item key at same level as stages
                    after.append("  " + lines[k])
                    k += 1
                continue
            
            # Not a stage item
            non_space = len(lines[k]) - len(lines[k].lstrip()) if lines[k].strip() else 999
            if non_space < len(stages_indent) + 1:
                break
            after.append(lines[k])
            k += 1
        
        after.extend(lines[k:])
        result = before + [f"{stages_indent}stages:"] + after
        return result, 1
    
    return lines, 0


def fix_permissions_block(lines):
    """Remove `permissions:` block entirely (#7)."""
    to_remove = set()
    in_perms = False
    perms_indent = None
    
    for i, line in enumerate(lines):
        m = re.match(r'^(\s*)permissions:', line)
        if m:
            to_remove.add(i)
            in_perms = True
            perms_indent = len(m.group(1))
            continue
        if in_perms:
            if re.match(r'^ {' + str(perms_indent + 1) + r',}\S', line):
                to_remove.add(i)
            else:
                in_perms = False
    
    new_lines = [l for i, l in enumerate(lines) if i not in to_remove]
    return new_lines, len(to_remove)


def fix_runson_single(lines):
    """Fix runs-on: single string or unsupported labels → inline array (#6)."""
    new_lines = []
    changed = 0
    VALID_SINGLE = {"default", "ubuntu-latest", "euler-latest"}
    for line in lines:
        m = re.match(r'^(\s*)runs-on:\s+(.+)$', line)
        if m:
            indent = m.group(1)
            val = m.group(2).strip()
            # Single string (not array)
            if not val.startswith("["):
                if val not in VALID_SINGLE:
                    new_lines.append(f"{indent}runs-on: [dedicate-hosted, x64, large]")
                    changed += 1
                    continue
            # Single-element array with unsupported label
            elif val.count(",") == 0:
                inner = val.strip("[]").strip()
                if inner in ("windows-latest", "macos-latest", "self-hosted", "ubuntu-24"):
                    new_lines.append(f"{indent}runs-on: [dedicate-hosted, x64, large]")
                    changed += 1
                    continue
        new_lines.append(line)
    return new_lines, changed


def fix_strategy_unknown(lines):
    """Remove unknown exclude/include blocks from strategy."""
    to_remove = set()
    in_exclude_include = False
    key_indent = None
    
    for i, line in enumerate(lines):
        m = re.match(r'^(\s*)(exclude|include):', line)
        if m:
            to_remove.add(i)
            in_exclude_include = True
            key_indent = len(m.group(1))
            continue
        if in_exclude_include:
            if re.match(r'^ {' + str(key_indent + 2) + r',}\S', line):
                to_remove.add(i)
            else:
                in_exclude_include = False
    
    new_lines = [l for i, l in enumerate(lines) if i not in to_remove]
    return new_lines, len(to_remove)


def fix_concurrency(lines):
    """Fix concurrency: add missing exceed-action/max, fix invalid values."""
    result = []
    changed = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        cm = re.match(r'^(\s*)concurrency:\s*$', line)
        if cm:
            indent = cm.group(1)
            child_indent = indent + "  "
            result.append(line)
            i += 1
            
            # Collect existing children
            child_keys = {}
            child_start = i
            while i < len(lines):
                nl = lines[i]
                if re.match(rf'^{child_indent}(\S+)', nl):
                    key_m = re.match(rf'^{child_indent}(\w[-\w]*):\s*(.*)', nl)
                    if key_m:
                        child_keys[key_m.group(1)] = (nl, key_m.group(2).strip())
                    result.append(nl)
                    i += 1
                elif nl.strip() == "":
                    result.append(nl)
                    i += 1
                else:
                    break
            
            # Add missing required fields
            if "exceed-action" not in child_keys:
                result.insert(-1 if result and result[-1].strip() == "" else len(result),
                              f"{child_indent}exceed-action: QUEUE")
                changed += 1
            elif not child_keys["exceed-action"][1]:
                # Empty value — fix it
                for ri in range(len(result)-1, -1, -1):
                    if re.match(rf'^{child_indent}exceed-action:\s*$', result[ri]):
                        result[ri] = f"{child_indent}exceed-action: QUEUE"
                        changed += 1
                        break
            elif child_keys["exceed-action"][1] not in ("QUEUE", "IGNORE"):
                for ri in range(len(result)-1, -1, -1):
                    if re.match(rf'^{child_indent}exceed-action:', result[ri]):
                        result[ri] = f"{child_indent}exceed-action: QUEUE"
                        changed += 1
                        break
            
            if "max" not in child_keys:
                result.insert(-1 if result and result[-1].strip() == "" else len(result),
                              f"{child_indent}max: 1")
                changed += 1
            else:
                max_val = child_keys["max"][1]
                try:
                    if int(max_val) < 1:
                        for ri in range(len(result)-1, -1, -1):
                            if re.match(rf'^{child_indent}max:', result[ri]):
                                result[ri] = f"{child_indent}max: 1"
                                changed += 1
                                break
                except ValueError:
                    pass
        else:
            result.append(line)
            i += 1
    
    return result, changed


def fix_environment_unknown(lines):
    """Remove unknown `environment:` block from job level."""
    to_remove = set()
    in_block = False
    block_indent = None
    for i, line in enumerate(lines):
        m = re.match(r'^(\s*)environment:', line)
        if m:
            to_remove.add(i)
            in_block = True
            block_indent = len(m.group(1))
            continue
        if in_block:
            if re.match(r'^ {' + str(block_indent + 1) + r',}\S', line):
                to_remove.add(i)
            else:
                in_block = False
    new_lines = [l for i, l in enumerate(lines) if i not in to_remove]
    return new_lines, len(to_remove)


def fix_services_unknown(lines):
    """Remove unknown services block."""
    to_remove = set()
    in_svc = False
    svc_indent = None
    for i, line in enumerate(lines):
        m = re.match(r'^(\s*)services:', line)
        if m:
            to_remove.add(i)
            in_svc = True
            svc_indent = len(m.group(1))
            continue
        if in_svc:
            if re.match(r'^ {' + str(svc_indent + 1) + r',}\S', line):
                to_remove.add(i)
            else:
                in_svc = False
    new_lines = [l for i, l in enumerate(lines) if i not in to_remove]
    return new_lines, len(to_remove)


def fix_env_format(lines):
    """Fix env: that's a string instead of a map."""
    new_lines = []
    changed = 0
    for line in lines:
        m = re.match(r'^(\s*)env:\s+(\S+)$', line)
        if m:
            # Single string value — remove or convert
            indent = m.group(1)
            val = m.group(2)
            new_lines.append(f"{indent}env:")  # empty map
            changed += 1
        else:
            new_lines.append(line)
    return new_lines, changed


def fix_empty_stage_name(lines):
    """Add missing name: to stages, post jobs, and their sub-jobs/steps."""
    new_lines = []
    changed = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        # Match: stages: or post:
        m = re.match(r'^(\s*)(stages|post):\s*$', line)
        if m:
            base_indent = m.group(1)
            key = m.group(2)
            i += 1
            
            # Process children: each stage/post block key at base+2 indent
            while i < len(lines):
                nl = lines[i]
                if nl.strip() == "":
                    new_lines.append(nl)
                    i += 1
                    continue
                non_space = len(nl) - len(nl.lstrip())
                if non_space <= len(base_indent):
                    break
                
                if non_space == len(base_indent) + 2:
                    # Stage name or post job key
                    sm = re.match(r'^\s{2,}([\w-]+):\s*$', nl)
                    if sm:
                        stage_key = sm.group(1)
                        content_indent = base_indent + "    "  # 4 spaces from stage level
                        new_lines.append(nl)
                        i += 1
                        
                        # Check if name exists immediately after
                        has_name = False
                        j = i
                        while j < len(lines) and (lines[j].strip() == "" or len(lines[j]) - len(lines[j].lstrip()) >= len(content_indent)):
                            if lines[j].strip() == "":
                                j += 1
                                continue
                            if re.match(r'^' + content_indent + r'name:', lines[j]):
                                has_name = True
                                break
                            if len(lines[j]) - len(lines[j].lstrip()) < len(content_indent):
                                break
                            j += 1
                        
                        if not has_name:
                            new_lines.append(f"{content_indent}name: {stage_key.replace('-', ' ').title()}")
                            changed += 1
                        
                        # Also handle jobs inside stage
                        while i < len(lines):
                            nl2 = lines[i]
                            if nl2.strip() == "":
                                new_lines.append(nl2)
                                i += 1
                                continue
                            ns2 = len(nl2) - len(nl2.lstrip())
                            if ns2 <= len(base_indent) + 2:
                                break
                            if ns2 == len(base_indent) + 4 and re.match(r'^\s+[\w-]+:\s*$', nl2):
                                # Job inside stage
                                job_content_indent = base_indent + "      "  # 6 spaces
                                new_lines.append(nl2)
                                i += 1
                                has_job_name = False
                                k = i
                                while k < len(lines) and (lines[k].strip() == "" or len(lines[k]) - len(lines[k].lstrip()) >= len(job_content_indent)):
                                    if lines[k].strip() == "":
                                        k += 1
                                        continue
                                    if re.match(r'^' + job_content_indent + r'name:', lines[k]):
                                        has_job_name = True
                                        break
                                    if len(lines[k]) - len(lines[k].lstrip()) < len(job_content_indent):
                                        break
                                    k += 1
                                if not has_job_name:
                                    jk = re.match(r'^\s+([\w-]+):\s*$', nl2)
                                    if jk:
                                        new_lines.append(f"{job_content_indent}name: {jk.group(1).replace('-', ' ').title()}")
                                        changed += 1
                            else:
                                new_lines.append(nl2)
                                i += 1
                        continue
                
                new_lines.append(nl)
                i += 1
            continue
        
        # Match: post.jobs key
        pm = re.match(r'^(\s{2,})post:\s*$', line)
        if pm:
            base_indent = pm.group(1)
            i += 1
            while i < len(lines):
                nl = lines[i]
                if nl.strip() == "":
                    new_lines.append(nl)
                    i += 1
                    continue
                ns = len(nl) - len(nl.lstrip())
                if ns <= len(base_indent):
                    break
                if ns == len(base_indent) + 2 and re.match(r'^\s+jobs:\s*$', nl):
                    jobs_content_indent = base_indent + "    "
                    new_lines.append(nl)
                    i += 1
                    # Process post jobs
                    while i < len(lines):
                        nl2 = lines[i]
                        if nl2.strip() == "":
                            new_lines.append(nl2)
                            i += 1
                            continue
                        ns2 = len(nl2) - len(nl2.lstrip())
                        if ns2 <= len(base_indent) + 2:
                            break
                        if ns2 >= len(base_indent) + 4 and re.match(r'^\s+[\w-]+:\s*$', nl2):
                            jc_indent = base_indent + "      "
                            new_lines.append(nl2)
                            i += 1
                            has_name = False
                            k = i
                            while k < len(lines):
                                if lines[k].strip() == "":
                                    k += 1
                                    continue
                                if re.match(r'^' + jc_indent + r'name:', lines[k]):
                                    has_name = True
                                    break
                                if len(lines[k]) - len(lines[k].lstrip()) < len(jc_indent):
                                    break
                                k += 1
                            if not has_name:
                                jk = re.match(r'^\s+([\w-]+):\s*$', nl2)
                                if jk:
                                    new_lines.append(f"{jc_indent}name: {jk.group(1).replace('-', ' ').title()}")
                                    changed += 1
                        else:
                            new_lines.append(nl2)
                            i += 1
                    continue
                new_lines.append(nl)
                i += 1
            continue

        i += 1

    return new_lines, changed


def fix_empty_runson(lines):
    """Add default runs-on for jobs inside stages that have empty runs-on."""
    new_lines = []
    changed = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        m = re.match(r'^(\s+)runs-on:\s*$', line)
        if m:
            new_lines.append(f"{m.group(1)}runs-on: [dedicate-hosted, x64, large]")
            changed += 1
        i += 1
    return new_lines, changed


def fix_empty_steps(lines):
    """Give empty steps a minimal default step."""
    new_lines = []
    changed = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\s+)steps:\s*$', line)
        if m:
            indent = m.group(1)
            new_lines.append(line)
            i += 1
            # Check if followed by actual step entries or just blank/next key
            has_steps = False
            j = i
            while j < len(lines):
                nl = lines[j]
                if nl.strip() == "":
                    j += 1
                    continue
                ns = len(nl) - len(nl.lstrip())
                if ns > len(indent):
                    has_steps = True
                    break
                else:
                    break
            if not has_steps:
                step_indent = indent + "  "
                new_lines.append(f"{step_indent}- name: Placeholder step")
                new_lines.append(f"{step_indent}  run: echo 'placeholder'")
                changed += 1
                continue
        else:
            new_lines.append(line)
        i += 1
    return new_lines, changed


def fix_yaml_parse(lines):
    """Fix YAML parse errors from broken matrix definitions (old generator bug).
    
    Pattern:
        os:
          name: Os
        - ubuntu
        - windows
    →  os:
        - ubuntu
        - windows
    """
    new_lines = []
    changed = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for: key:\n  name: <value>\n- <item>  (broken matrix parent)
        m = re.match(r'^(\s+)([\w-]+):\s*$', line)
        if m:
            key_indent = m.group(1)
            key_name = m.group(2)
            child_indent = key_indent + "  "
            
            # Check next non-blank line
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            
            if j < len(lines):
                next_line = lines[j]
                nm = re.match(r'^' + child_indent + r'name:\s+(.+)', next_line)
                if nm:
                    # Found pattern: key with name annotation
                    # Check if name line is followed by list items at lesser indent
                    k = j + 1
                    while k < len(lines) and lines[k].strip() == "":
                        k += 1
                    if k < len(lines):
                        after_name = lines[k]
                        after_indent = len(after_name) - len(after_name.lstrip())
                        if after_indent <= len(key_indent) and after_name.lstrip().startswith("- "):
                            # This is the broken pattern: name: inside key, then list at outer indent
                            # Solution: remove the name: line, promote list items as children of key
                            new_lines.append(line)  # keep the key:
                            i += 1
                            # Skip the name: line
                            while i < len(lines) and (lines[i].strip() == "" or re.match(r'^' + child_indent + r'name:', lines[i])):
                                i += 1
                            # Now add list items with +2 indent
                            while i < len(lines):
                                cl = lines[i]
                                if cl.strip() == "":
                                    new_lines.append(cl)
                                    i += 1
                                    continue
                                ci = len(cl) - len(cl.lstrip())
                                if ci > len(key_indent):
                                    # Already a child — keep as-is
                                    new_lines.append(cl)
                                    i += 1
                                elif ci <= len(key_indent) and cl.lstrip().startswith("- "):
                                    # List item at wrong indent — add 2 spaces
                                    new_lines.append("  " + cl)
                                    i += 1
                                    changed += 1
                                else:
                                    break  # End of list
                            changed += 1
                            continue
        
        new_lines.append(line)
        i += 1
    
    return new_lines, changed


# ─── Fix dispatcher ───

FIX_FUNCTIONS = {
    "dup_key": fix_dup_key,
    "empty_name": fix_empty_name,
    "empty_stage_name": fix_empty_stage_name,
    "empty_runson": fix_empty_runson,
    "empty_steps": fix_empty_steps,
    "bare_if": fix_bare_if,
    "illegal_name_chars": fix_illegal_name_chars,
    "stages_format": fix_stages_format,
    "permissions_block": fix_permissions_block,
    "runson_single": fix_runson_single,
    "strategy_unknown": fix_strategy_unknown,
    "concurrency": fix_concurrency,
    "environment_unknown": fix_environment_unknown,
    "services_unknown": fix_services_unknown,
    "env_format": fix_env_format,
    "yaml_parse": fix_yaml_parse,
}


WORKFLOW_START_RE = re.compile(r'workflow:\s*\|\n')
END_MARKER_RE = re.compile(r'\n((?:trigger|fault_injection|assertions|teardown):)')

def extract_workflow_text(case_content):
    """Extract workflow YAML string from case YAML. Returns (text, end_marker)."""
    m = WORKFLOW_START_RE.search(case_content)
    if not m:
        return None, None
    start = m.end()
    rest = case_content[start:]
    em = END_MARKER_RE.search(rest)
    if not em:
        # Try end of file
        wf_text = rest.strip()
        return wf_text, ""
    wf_text = rest[:em.start()]
    end_marker = em.group(1)
    return wf_text, end_marker


def replace_workflow_text(case_content, new_wf_text, end_marker):
    """Replace the workflow block in the case YAML, preserving the end marker."""
    m = WORKFLOW_START_RE.search(case_content)
    if not m:
        return case_content
    rest = case_content[m.end():]
    em = END_MARKER_RE.search(rest)
    if not em:
        return case_content
    old_wf = rest[:em.start()]
    old_block = f"workflow: |\n{old_wf}\n{end_marker}"
    new_block = f"workflow: |\n{new_wf_text}\n{end_marker}"
    return case_content.replace(old_block, new_block, 1)


def apply_fixes_to_case(case_id, error_categories, dry_run=False):
    """Apply all needed fixes to one case."""
    content = read_case_yaml(case_id)
    if not content:
        return False, "File not found"

    wf_text, end_marker = extract_workflow_text(content)
    if wf_text is None:
        return False, "Could not extract workflow"

    lines = wf_text.split("\n")
    total_changed = 0
    fix_log = []

    for cat in sorted(set(error_categories)):
        if cat in INTENTIONAL_NEGATIVE:
            fix_log.append(f"  [skip-intentional] {cat}")
            continue
        if cat not in FIX_FUNCTIONS:
            fix_log.append(f"  [skip-unknown] {cat}")
            continue

        fix_func = FIX_FUNCTIONS[cat]
        new_lines, count = fix_func(lines)
        if count > 0:
            lines = new_lines
            total_changed += count
            fix_log.append(f"  [{cat}] {count} change(s)")
        else:
            fix_log.append(f"  [{cat}] no change needed")

    if total_changed == 0:
        return False, "\n".join(fix_log)

    if not dry_run:
        new_wf_text = "\n".join(lines)
        new_content = replace_workflow_text(content, new_wf_text, end_marker)
        write_case_yaml(case_id, new_content)

    return True, f"{total_changed} total changes\n" + "\n".join(fix_log)


def main():
    dry_run = "--dry-run" in sys.argv

    print("Parsing validation log...")
    case_errors = parse_validation_log()
    print(f"Found {len(case_errors)} cases with errors")

    # Classify errors per case
    case_categories = {}
    all_cats = Counter()
    for case_id, errors in case_errors.items():
        cats = [classify_error(e) for e in errors]
        case_categories[case_id] = cats
        for c in cats:
            all_cats[c] += 1

    print(f"\nError categories: {dict(all_cats.most_common())}\n")

    fixed = 0
    failed = 0
    skipped_intentional = 0

    for case_id in sorted(case_categories.keys()):
        cats = case_categories[case_id]
        intentional = [c for c in cats if c in INTENTIONAL_NEGATIVE]
        actionable = [c for c in cats if c not in INTENTIONAL_NEGATIVE and c in FIX_FUNCTIONS]
        unknown = [c for c in cats if c not in INTENTIONAL_NEGATIVE and c not in FIX_FUNCTIONS]

        if not actionable:
            skipped_intentional += 1
            continue

        print(f"[{case_id}] {len(cats)} errs: {dict(Counter(cats))}")
        success, msg = apply_fixes_to_case(case_id, cats, dry_run=dry_run)
        if success:
            print(f"  FIXED — {msg}")
            fixed += 1
        else:
            print(f"  SKIP — {msg}")
            failed += 1

    print(f"\n=== SUMMARY ===")
    print(f"  Fixed: {fixed}")
    print(f"  Could not fix: {failed}")
    print(f"  Intentional/Skipped: {skipped_intentional}")
    if dry_run:
        print(f"  (DRY RUN — no files modified)")


if __name__ == "__main__":
    main()
