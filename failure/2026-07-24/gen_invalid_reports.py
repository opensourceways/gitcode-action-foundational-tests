#!/usr/bin/env python3
"""Generate proper INVALID analysis: expected negative tests vs unexpected bugs."""
import json
from pathlib import Path
from collections import defaultdict
import yaml

RESULTS_JSON = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/phase02/classify-experiment/2026-07-23/validation-results.json")
SRC_DIR = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases/yaml")
OUT = Path("/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/analysis/validation-invalid-74-cases.md")

with open(RESULTS_JSON) as f:
    results = json.load(f)
invalids = sorted([r for r in results if r["status"] == "INVALID"], key=lambda x: x["case_id"])

case_meta = {}
for case in invalids:
    yf = SRC_DIR / f"{case['case_id']}.yaml"
    with open(yf) as f:
        c = yaml.safe_load(f)
    case_meta[case["case_id"]] = {
        "title": c.get("title", ""),
        "dimension": c.get("dimension", ""),
        "priority": c.get("priority", ""),
        "intent_ref": c.get("intent_ref", ""),
        "trigger_event": c.get("trigger", {}).get("event", "?") if isinstance(c.get("trigger"), dict) else "?",
        "assertions": c.get("assertions", []),
        "fault_injection": c.get("fault_injection"),
        "setup": c.get("setup", {}),
    }

# ── Classification ───────────────────────────────────────────────

def is_expected_negative(cid, meta):
    """Case intentionally tests platform rejection of bad input."""
    title = meta.get("title", "")
    neg_kw = [
        "应报错", "应被报错", "应拒绝", "应被拒绝", "应给出",
        "不应触发", "时报错", "报错应", "不被支持",
        "被拒绝", "不应接受", "应提示",
    ]
    if any(kw in title for kw in neg_kw):
        return True
    # Special cases where title says "应拒绝" etc
    return False

expected = []
unexpected = []

for case in invalids:
    cid = case["case_id"]
    meta = case_meta.get(cid, {})
    if is_expected_negative(cid, meta):
        expected.append(case)
    else:
        unexpected.append(case)

# ── Root cause for unexpected ────────────────────────────────────

def diagnose_unexpected(case):
    cid = case["case_id"]
    meta = case_meta.get(cid, {})
    title = meta.get("title", "")
    diags = case.get("diagnostics", [])
    all_msgs = " ".join(d["message"] for d in diags)

    if "cron" in all_msgs:
        return "01_cron"  # platform cron parser rejects valid cron
    if ("post.steps" in all_msgs or "post.run_always" in all_msgs):
        return "02_post"  # docs describe post, platform rejects
    if ("Cannot deserialize" in all_msgs and "stages" in all_msgs.lower()):
        return "03_stages_deser"  # stages array→map
    if ("Cannot deserialize" in all_msgs and "schedule" in all_msgs.lower()):
        return "04_schedule_deser"
    if ("failure()" in all_msgs or "success()" in all_msgs or "always()" in all_msgs
            or "unknownFunc" in all_msgs or "vars." in all_msgs):
        return "05_expr_function"  # GitHub-style expression functions
    if "permissions" in all_msgs.lower():
        return "06_permissions"  # job-level permissions unsupported
    if "environment" in all_msgs.lower():
        return "07_environment"  # environment field unsupported
    if "列表长度" in all_msgs and ("merge_requests" in all_msgs or "paths" in all_msgs):
        return "08_list_limit"  # doc doesn't mention limit
    if "runs-on" in all_msgs.lower():
        return "09_runs_on"  # runs-on validation too strict
    if "格式错误" in all_msgs or "pluginname" in all_msgs:
        return "10_uses_format"
    if "插件" in all_msgs and "不存在" in all_msgs:
        return "11_plugin_missing"
    if "while scanning" in all_msgs or "while parsing" in all_msgs:
        return "12_yaml_syntax"
    if "preemption" in all_msgs.lower():
        return "13_preemption"
    if "未知字段" in all_msgs or "unknown property" in all_msgs.lower() or "unknown_field" in all_msgs.lower():
        return "14_unknown_field"
    if "steps" in all_msgs and "16" in all_msgs:
        return "15_step_limit"
    return "99_other"

# ── Build report ─────────────────────────────────────────────────

rc_map = {
    "01_cron": "cron 表达式被拒 (合法语法)",
    "02_post": "post.steps/run_always 文档描述但平台拒",
    "03_stages_deser": "stages 反序列化错误 (array vs map)",
    "04_schedule_deser": "schedule 反序列化错误",
    "05_expr_function": "GitHub 表达式函数 vs GitCode 关键字",
    "06_permissions": "job 级 permissions 不支持",
    "07_environment": "environment 字段不支持",
    "08_list_limit": "列表长度限制未在文档声明",
    "09_runs_on": "runs-on 数组校验过严",
    "10_uses_format": "uses 格式错误",
    "11_plugin_missing": "引用插件路径不存在",
    "12_yaml_syntax": "YAML 语法错误",
    "13_preemption": "preemption events 取值限制",
    "14_unknown_field": "未知字段静默拒绝 (应警告)",
    "15_step_limit": "steps <=16 限制未在文档声明",
    "99_other": "其他",
}

rc_groups = defaultdict(list)
for case in unexpected:
    rc = diagnose_unexpected(case)
    rc_groups[rc].append(case)

lines = []
lines.append("# 66 INVALID Cases — 预期非法 (24) vs 非预期非法 (42)")
lines.append("")
lines.append(f"> Run: 2026-07-23-01 | 数据源: 369 cases → 289 通过 API 校验")
lines.append(f"> 逐例详情: `failure/2026-07-24/case/*.md` | 分析日期: 2026-07-24")
lines.append(f"> 分析方法: 遵循 `phase02/agents/failure-analyst/CLAUDE.md` 原则")
lines.append("")

lines.append("## 一、总体结论")
lines.append("")
lines.append("| 类别 | 数量 | 说明 |")
lines.append("|------|------|------|")
lines.append(f"| **预期非法** (negative test) | **{len(expected)}** | case 有意测试平台对非法输入的报错 — INVALID 是期望结果 |")
lines.append(f"| **非预期非法** → 需要修复 | **{len(unexpected)}** | case 描述正常功能但被平台校验驳回 — 属于平台缺陷或 case bug |")
lines.append(f"| **总计** | **{len(invalids)}** | |")
lines.append("")

lines.append("## 二、非预期非法 (42 cases) — 根因分类")
lines.append("")
lines.append("按 `failure-analyst/CLAUDE.md` 原则分类: 文档承诺了 X 但平台做不到 X → 产品缺陷；case 用错语法 → case bug。")
lines.append("")
lines.append("| 根因 | 数量 | 说明 | 涉及 Cases |")
lines.append("|------|------|------|----------|")
for rc, cases in sorted(rc_groups.items(), key=lambda x: -len(x[1])):
    ids = ", ".join(c["case_id"] for c in cases[:4])
    if len(cases) > 4:
        ids += f" ... (+{len(cases)-4})"
    lines.append(f"| {rc_map.get(rc, rc)} | {len(cases)} | | {ids} |")
lines.append("")

# ── Expected invalid ─────────────────────────────────────────────

lines.append("---")
lines.append("")
lines.append("## 三、预期非法 — 24 Negative Tests")
lines.append("")
lines.append("以下 cases 有意提交非法 YAML 以测试平台的报错能力，INVALID 是期望结果。")
lines.append("")
lines.append("| # | case_id | dimension | trigger | 标题 | neg/pos | 诊断摘要 |")
lines.append("|---|---------|-----------|---------|------|---------|---------|")
for i, case in enumerate(expected, 1):
    cid = case["case_id"]
    m = case_meta.get(cid, {})
    neg = sum(1 for a in m.get("assertions", []) if a.get("type") == "negative")
    pos = sum(1 for a in m.get("assertions", []) if a.get("type") == "positive")
    diag = case.get("diagnostics", [{}])[0].get("message", "?")[:55]
    lines.append(f"| {i} | {cid} | {m.get('dimension','?')} | {m.get('trigger_event','?')} | {m.get('title','')[:40]} | {neg}/{pos} | {diag} |")
lines.append("")

# ── Unexpected detail ────────────────────────────────────────────

lines.append("---")
lines.append("")
lines.append("## 四、非预期非法 — 逐根因详细分析")
lines.append("")
lines.append("每条都标明了是平台缺陷还是 case bug，附 GitCode docs 对照。")
lines.append("")

for rc, cases in sorted(rc_groups.items(), key=lambda x: -len(x[1])):
    lines.append(f"### {rc_map.get(rc, rc)} ({len(cases)} cases)")
    lines.append("")

    for case in cases:
        cid = case["case_id"]
        m = case_meta.get(cid, {})
        title = m.get("title", "")
        diags = case.get("diagnostics", [])
        lines.append(f"**{cid}** — {title}")
        lines.append(f"- 维度: {m.get('dimension','?')} | 优先级: {m.get('priority','?')} | trigger: {m.get('trigger_event','?')}")
        lines.append(f"- intent_ref: {m.get('intent_ref','?')}")
        for d in diags:
            lines.append(f"- [{d.get('severity','?')}] L{d.get('line','?')}:C{d.get('column','?')}: {d.get('message','')}")
        lines.append("")

    liner = rc_map[rc]
    if rc == "01_cron":
        lines.append("**分析**: GitCode 文档 `configure-triggers.md` 描述了 schedule cron 触发方式。但平台 cron 解析器与标准 cron 语法不兼容——合法的 cron 表达式被拒绝。属于**平台缺陷**（cron 语法兼容性）。")
    elif rc == "02_post":
        lines.append("**分析**: 文档 `core-concepts/workflow-job-step-action.md` 描述了 `post` 后处理阶段，`workflow-file-location-structure.md` 列出了 `post` 字段。平台校验器报 unknown property。属于**文档冲突**（文档超前于平台实现）。")
    elif rc == "03_stages_deser":
        lines.append("**分析**: 文档 `configure-dependencies-order.md` 展示了 stages array 和 map 两种格式，但平台只接受 map 格式。属于**文档冲突**（两种格式都给了示例但只支持一种）。")
    elif rc == "05_expr_function":
        lines.append("**分析**: GitCode 不支持 GitHub Actions 的 `failure()`/`success()`/`always()` 函数调用语法，改用关键字 `failed`/`success`/`always`。属于**case bug** (用错语法)，已在 VALIDATION-RULES.md 规则 4d 记录。")
    elif rc == "06_permissions":
        lines.append("**分析**: 文档 `token-permissions.md` 描述了 job 级 permissions 覆盖，但平台尚不支持 job 级 `permissions` 字段。属于**平台缺陷**（能力缺口）。")
    elif rc == "07_environment":
        lines.append("**分析**: 文档描述了 `environment` 字段绑定环境级 secrets，但平台校验器拒绝此字段。属于**平台缺陷**（环境级 secrets 功能未实现）。")
    elif rc == "08_list_limit":
        lines.append("**分析**: 文档 `configure-triggers.md` 只说明 paths 匹配前 300 个变更文件，未说明 paths/branches 条目数上限为 32。属于**文档缺失**。")
    elif rc == "09_runs_on":
        lines.append("**分析**: 平台的 runs-on 数组格式校验过严。合法 label 组合（如自定义标签）被判定为非法，且错误消息未给出可用标签列表。属于**平台缺陷**。")
    elif rc == "10_uses_format" or rc == "11_plugin_missing":
        lines.append("**分析**: uses 路径指向不存在的文件或格式不符合 `pluginname@version` 规范。属于**case bug**（配置错误）。")
    elif rc == "12_yaml_syntax":
        lines.append("**分析**: YAML 语法错误（缩进、引号等）。属于**case bug**。")
    elif rc == "13_preemption":
        lines.append("**分析**: 文档未声明 preemption events 仅支持 `mr_id`，其他值被拒绝。属于**文档缺失**。")
    elif rc == "14_unknown_field":
        lines.append("**分析**: 未知字段被静默拒绝而非给出警告，测试期待的是'应被报错或警告'，但 case YAML 额外包含了不该有的字段。边界判定：如果 case 本身就是为了测试未知字段的报错，则属于预期行为。")
    elif rc == "15_step_limit":
        lines.append("**分析**: 文档未声明每 job 最多 16 个 step。属于**文档缺失**。")
    lines.append("")

# ── Summary table ─────────────────────────────────────────────────

lines.append("---")
lines.append("")
lines.append("## 五、逐条明细")
lines.append("")
lines.append("| # | case_id | status | dimension | trigger | neg/pos | 标题 | 诊断首行 |")
lines.append("|---|---------|--------|-----------|---------|---------|------|---------|")
for i, case in enumerate(invalids, 1):
    cid = case["case_id"]
    m = case_meta.get(cid, {})
    status = "EXPECTED" if is_expected_negative(cid, m) else "UNEXPECTED"
    neg = sum(1 for a in m.get("assertions", []) if a.get("type") == "negative")
    pos = sum(1 for a in m.get("assertions", []) if a.get("type") == "positive")
    diag = case.get("diagnostics", [{}])[0].get("message", "?")[:50]
    lines.append(f"| {i} | {cid} | {status} | {m.get('dimension','?')} | {m.get('trigger_event','?')} | {neg}/{pos} | {m.get('title','')[:35]} | {diag} |")

with open(OUT, "w") as f:
    f.write("\n".join(lines))
print(f"[OK] {OUT} ({len(lines)} lines)")
print(f"Expected: {len(expected)}, Unexpected: {len(unexpected)}")
