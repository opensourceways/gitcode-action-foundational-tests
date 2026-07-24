#!/usr/bin/env python3
"""Generate INVALID/ERROR case analysis reports under failure/2026-07-24/."""
import json
from pathlib import Path
from collections import defaultdict, Counter

import yaml

RESULTS_JSON = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/phase02/classify-experiment/2026-07-23/validation-results.json")
SRC_DIR = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases/yaml")
OUT_DIR = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24")
CASE_DIR = OUT_DIR / "case"
ANALYSIS_DIR = OUT_DIR / "analysis"
for d in [CASE_DIR, ANALYSIS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

with open(RESULTS_JSON) as f:
    results = json.load(f)

invalids = [r for r in results if r["status"] == "INVALID"]
errors = [r for r in results if r["status"] == "ERROR"]

print(f"INVALID: {len(invalids)}, ERROR: {len(errors)}")

# Read case metadata
case_meta = {}
for case in invalids + errors:
    yf = SRC_DIR / f"{case['case_id']}.yaml"
    if yf.exists():
        with open(yf) as f:
            c = yaml.safe_load(f)
        case_meta[case["case_id"]] = {
            "title": c.get("title", ""),
            "dimension": c.get("dimension", ""),
            "priority": c.get("priority", ""),
            "intent_ref": c.get("intent_ref", ""),
            "trigger_event": c.get("trigger", {}).get("event", "?") if isinstance(c.get("trigger"), dict) else "?",
        }

# ── Per-case reports ──────────────────────────────────────────

def generate_case_report(case):
    cid = case["case_id"]
    meta = case_meta.get(cid, {})
    lines = []
    lines.append(f"## 校验失败 · {cid} · {meta.get('title', '')}")
    lines.append("")
    lines.append(f"**判定结果**: {case['status']}")
    lines.append("")

    if case["status"] == "INVALID":
        lines.append(f"**根因**: 平台 schema 校验不通过")
        diags = case.get("diagnostics", [])
        lines.append(f"**诊断信息** ({len(diags)} 条):")
        for d in diags:
            lines.append(f"  - [{d['severity']}] L{d['line']}:C{d['column']} — {d['message']}")
        lines.append("")
    elif case["status"] == "ERROR":
        lines.append(f"**根因**: API 调用失败 (WAF 拦截 / 网络错误)")
        lines.append(f"**响应**: {case.get('raw', 'N/A')[:300]}")
        lines.append("")

    if meta:
        lines.append(f"- 维度: {meta.get('dimension', '?')} | 优先级: {meta.get('priority', '?')}")
        lines.append(f"- intent_ref: {meta.get('intent_ref', '?')} | trigger: {meta.get('trigger_event', '?')}")
    lines.append("")

    md_path = CASE_DIR / f"{cid}.md"
    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    return md_path

for case in invalids + errors:
    generate_case_report(case)

# ── Error category analysis ────────────────────────────────────

error_categories = defaultdict(list)
for case in invalids:
    for d in case.get("diagnostics", []):
        msg = d["message"]
        # Categorize
        cat = "unknown"
        if "cron" in msg.lower():
            cat = "cron_expression"
        elif "concurrency" in msg.lower():
            cat = "concurrency"
        elif "Cannot deserialize" in msg:
            cat = "deserialization"
        elif "unknown property" in msg.lower() or "unknown_field" in msg.lower():
            cat = "unknown_property"
        elif "列表长度" in msg or "branches" in msg or "paths" in msg:
            cat = "list_length"
        elif "permissions" in msg.lower():
            cat = "permissions"
        elif "格式错误" in msg or "pluginname" in msg:
            cat = "plugin_format"
        elif "插件" in msg or "不存在" in msg:
            cat = "plugin_missing"
        elif "runs-on" in msg.lower():
            cat = "runs_on"
        elif "if表达式" in msg:
            cat = "if_expression"
        elif "列表中存在非法值" in msg:
            cat = "illegal_enum"
        elif "on.merge_requests" in msg:
            cat = "merge_requests"
        elif "post" in msg.lower():
            cat = "post_fields"
        elif "run-name" in msg:
            cat = "run_name"
        error_categories[cat].append(case["case_id"])

# ── Master analysis report ─────────────────────────────────────

def gen_master():
    lines = []
    lines.append(f"# {len(invalids) + len(errors)} 条校验失败/错误 · 分类归因 + 汇总分析")
    lines.append("")
    lines.append(f"> 数据源: `phase01/runs/2026-07-23-01/cases/yaml/` (369 cases)")
    lines.append(f"> 校验结果: 289 VALID, {len(invalids)} INVALID, 6 SKIP, {len(errors)} ERROR")
    lines.append(f"> 逐例详情: `failure/2026-07-24/case/*.md`")
    lines.append(f"> 分析日期: 2026-07-24")
    lines.append("")

    # Summary table
    lines.append("## 一、概览")
    lines.append("")
    lines.append(f"| 分类 | 数量 | 占比 |")
    lines.append(f"|------|------|------|")
    lines.append(f"| VALID | 289 | 78.3% |")
    lines.append(f"| INVALID | {len(invalids)} | {len(invalids)/3.69:.1f}% |")
    lines.append(f"| SKIP | 6 | 1.6% |")
    lines.append(f"| ERROR | {len(errors)} | {len(errors)/3.69:.1f}% |")
    lines.append("")

    # Error categories
    lines.append("## 二、INVALID 错误分类")
    lines.append("")
    lines.append(f"| 类别 | 涉及 Cases | 数量 |")
    lines.append(f"|------|----------|------|")

    cat_names = {
        "cron_expression": "cron 表达式",
        "concurrency": "concurrency 配置",
        "deserialization": "类型反序列化失败",
        "unknown_property": "未知字段",
        "list_length": "列表长度限制",
        "permissions": "permissions 不支持",
        "plugin_format": "插件名格式错误",
        "plugin_missing": "依赖插件不存在",
        "runs_on": "runs-on 格式",
        "if_expression": "if 表达式",
        "illegal_enum": "枚举值非法",
        "merge_requests": "merge_requests 配置",
        "post_fields": "post 字段不支持",
        "run_name": "run-name 不支持",
    }

    for cat, cases in sorted(error_categories.items(), key=lambda x: -len(x[1])):
        sample = ", ".join(sorted(cases)[:5])
        if len(cases) > 5:
            sample += f" ... (+{len(cases)-5})"
        name = cat_names.get(cat, cat)
        lines.append(f"| {name} | {sample} | {len(cases)} |")
    lines.append("")

    # ERROR cases
    lines.append("## 三、ERROR 案例 (8 条)")
    lines.append("")
    lines.append("以下 cases 在校验 API 调用时返回 HTTP 418 (WAF 拦截)，无法获取校验结果：")
    lines.append("")
    for case in errors:
        meta = case_meta.get(case["case_id"], {})
        lines.append(f"- **{case['case_id']}**: {meta.get('title', '')} (dim={meta.get('dimension', '?')}, trigger={meta.get('trigger_event', '?')})")
    lines.append("")

    # Dimension breakdown
    lines.append("## 四、按维度统计")
    lines.append("")
    dim_counter = Counter()
    for case in invalids + errors:
        meta = case_meta.get(case["case_id"], {})
        dim_counter[meta.get("dimension", "unknown")] += 1
    lines.append(f"| 维度 | 数量 |")
    lines.append(f"|------|------|")
    for dim, count in dim_counter.most_common():
        lines.append(f"| {dim} | {count} |")
    lines.append("")

    # Detailed table
    lines.append("## 五、逐条归因表")
    lines.append("")
    lines.append("| # | case_id | status | dimension | trigger | 根因 | 诊断摘要 |")
    lines.append("|---|---------|--------|-----------|---------|------|---------|")
    for i, case in enumerate(invalids + errors, 1):
        cid = case["case_id"]
        meta = case_meta.get(cid, {})
        status = case["status"]
        dim = meta.get("dimension", "?")
        trigger = meta.get("trigger_event", "?")

        if case["status"] == "INVALID":
            diags = case.get("diagnostics", [])
            first_msg = diags[0]["message"][:70] if diags else "?"
            # Find root cause category
            root_cause = "schema_violation"
            for d in diags:
                msg = d["message"]
                if "cron" in msg.lower():
                    root_cause = "cron_expression"
                    break
                elif "concurrency" in msg.lower():
                    root_cause = "concurrency"
                    break
                elif "Cannot deserialize" in msg:
                    root_cause = "deserialization"
                    break
                elif "unknown property" in msg.lower():
                    root_cause = "unknown_property"
                    break
                elif "permissions" in msg.lower():
                    root_cause = "permissions"
                    break
            lines.append(f"| {i} | {cid} | {status} | {dim} | {trigger} | {root_cause} | {first_msg} |")
        else:
            lines.append(f"| {i} | {cid} | {status} | {dim} | {trigger} | WAF_blocked | HTTP 418 |")
    lines.append("")

    # Recommendations
    lines.append("## 六、建议")
    lines.append("")
    lines.append("1. **WAF 拦截 (8 cases)**: HTTP 418 说明部分 YAML 被阿里云 WAF 拦截，可能触发 SQL/XSS 检测规则。建议：排查 YAML 内容中的特殊字符（如 `${}`、反引号、URI 编码样式字符串）")
    lines.append("2. **concurrency 配置 (6+ cases)**: 多个 case 因 concurrency.max < 1、exceed-action 为空、preemption events 非法值被拒。检查 docs 与平台实现的差异")
    lines.append("3. **cron 表达式 (7 cases)**: schedule cron 校验失败，可能是平台 cron 语法与标准有差异（如不允许缩减的星期/月份字段）")
    lines.append("4. **unknown property 类 (7+ cases)**: `post.steps`、`post.run_always`、`run-name`、`permissions.contents` 这些字段是否确为平台不支持，还是校验器滞后于平台实际能力")
    lines.append("5. **merge_requests (3 cases)**: branches+branches-ignore 长度限制 + types 枚举值差异（opened vs open），GitCode MR 事件与 GitHub PR 事件的字段映射不完整")
    lines.append("")

    md_path = ANALYSIS_DIR / "validation-invalid-74-cases.md"
    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    print(f"[OK] Master analysis: {md_path} ({len(lines)} lines)")

gen_master()

# Count per-case reports generated
case_reports = list(CASE_DIR.glob("COMP-*.md")) + list(CASE_DIR.glob("COMPAT-*.md")) + list(CASE_DIR.glob("REL-*.md")) + list(CASE_DIR.glob("SEC-*.md")) + list(CASE_DIR.glob("USE-*.md"))
# Only count those generated in this run
new_cases = {r["case_id"] for r in invalids + errors}
new_reports = [f for f in CASE_DIR.glob("*.md") if f.stem in new_cases]
print(f"Case reports: {len(new_reports)} (INVALID={len(invalids)} + ERROR={len(errors)})")
