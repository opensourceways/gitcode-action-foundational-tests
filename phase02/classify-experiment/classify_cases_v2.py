#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classify_cases_v2.py — 完整分类：遍历每个 case 的 trigger + setup + fault_injection + assertions，
对照 Phase 02 执行器 + assertion_engine 能力进行可脚本化程度分类。

输出 3 级文件（同目录）：
  classification_v2_report.md    — 逐 case 明细 + 阻断项
  classification_v2.csv           — 表格
  classification_v2_detail.json   — JSON
"""

import yaml
import re
import json
import sys
from pathlib import Path
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════════
#  Phase 02 执行能力基线（workflow_runner.py TRIGGER_STATUS 节选）
# ═══════════════════════════════════════════════════════════════════

TRIGGER_SUPPORT = {
    "push":                 {"supported": True,  "reason": ""},
    "tag":                  {"supported": False, "reason": "tag 触发：需 git tag+push 并按 tag ref 匹配"},
    "manual":               {"supported": False, "reason": "manual 触发：需 workflow_dispatch API（待确认端点）"},
    "workflow_dispatch":    {"supported": False, "reason": "workflow_dispatch：需 dispatch API（待确认端点）"},
    "pr":                   {"supported": False, "reason": "pr 触发：需建分支+开 PR（待确认 PR API）"},
    "pull_request":         {"supported": False, "reason": "pull_request：需建分支+开 PR（待确认 PR API）"},
    "pull_request_target":  {"supported": False, "reason": "pull_request_target：同 PR + base 上下文语义"},
    "pull_request_comment": {"supported": False, "reason": "pull_request_comment：需 PR comment API（未实现）"},
    "fork_pr":              {"supported": False, "reason": "fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者"},
    "schedule":             {"supported": False, "reason": "schedule：cron 无法按需触发（基础设施限制）"},
}

# trigger.as 能力：untrusted_contributor 需第二账号
UNTRUSTED_AS_BLOCKER = "trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者"

# fault_injection 能力：当前脚本完全不处理
FAULT_INJECTION_BLOCKER = "fault_injection 非 null：当前执行器不支持故障注入（需 kill_runner / network_partition / concurrent_flood infra）"

# 未知 setup.repo_fixture 可能影响执行（需确认对应仓已配置好 secrets/variables）
KNOWN_FIXTURES = {"basic-ci", "clean", "with-secrets", "fork-target", "fork-source",
                  "environment-protected", "private-registry", "large-repo",
                  "runner-release", "badge-test"}
FIXTURE_UNKNOWN_BLOCKER = "setup.repo_fixture 未知：需确认测试仓是否已配置好 secrets/variables 等前置资源"

# assertion_engine 支持 kind
ENGINE_KINDS = {"status", "run_status", "value", "leak", "mask", "config_probe"}

TARGET_KIND_MAP = {
    "run_logs":    {"value", "leak", "mask", "config_probe"},
    "run_status":  {"status", "run_status"},
}

UNSUPPORTED_TARGETS = {
    "error_message", "run_ui", "badge_response", "runner_schedulable",
    "runner_scheduling", "step_summary", "artifacts", "documentation",
    "queue_ui", "pr_ui", "run_duration", "workflow_validation",
}

# rubric 值提取
_RE_EN_QUOTED = re.compile(r"'([^']+)'")
_RE_UPPER_IDENT = re.compile(r'\b([A-Z][A-Z0-9_]{2,}(?:_[A-Z0-9]+)*)\b')
_RE_PAREN_VALUE = re.compile(r'[（(]([^）)]+)[）)]')
_RE_SPECIFIC_WORD = re.compile(r'\b(?:含|包含|输出|出现|显示|返回|为|是否是?)\s*[：:]?\s*([A-Za-z_][A-Za-z0-9_.-]+)')


def extract_rubric_value(rubric: str) -> list[str]:
    candidates = []
    for m in _RE_EN_QUOTED.finditer(rubric):
        candidates.append(m.group(1))
    for m in _RE_UPPER_IDENT.finditer(rubric):
        val = m.group(1)
        if val not in candidates and not val.startswith("_") and len(val) >= 4:
            candidates.append(val)
    for m in _RE_PAREN_VALUE.finditer(rubric):
        inner = m.group(1).strip()
        if re.search(r'[A-Za-z0-9_]', inner):
            candidates.append(inner)
    for m in _RE_SPECIFIC_WORD.finditer(rubric):
        val = m.group(1)
        if val not in candidates and not val.startswith("_"):
            candidates.append(val)
    return list(dict.fromkeys(candidates))


# ═══════════════════════════════════════════════════════════════════
#  分类逻辑
# ═══════════════════════════════════════════════════════════════════

def classify_trigger(trigger: dict) -> dict:
    """分类 trigger 可执行性。"""
    event = trigger.get("event", "") if trigger else ""
    actor = trigger.get("as", "")
    params = trigger.get("params") or {}

    info = TRIGGER_SUPPORT.get(event)
    if info is None:
        info = {"supported": False, "reason": f"未知触发事件 '{event}'"}

    blockers = []
    if not info["supported"]:
        blockers.append(info["reason"])

    # untrusted_contributor
    if actor == "untrusted_contributor":
        blockers.append(UNTRUSTED_AS_BLOCKER)

    # trigger.params 不做硬阻断，但标出来
    param_keys = list(params.keys())

    return {
        "event": event,
        "actor": actor,
        "supported": info["supported"] and actor != "untrusted_contributor",
        "blockers": blockers,
        "param_keys": param_keys,
    }


def classify_setup(setup: dict) -> dict:
    """分类 setup 可执行性。"""
    fixture = setup.get("repo_fixture", "") if setup else ""
    secrets = setup.get("secrets", []) if setup else []
    variables = setup.get("variables", {}) if setup else {}

    blockers = []
    if fixture not in KNOWN_FIXTURES:
        blockers.append(f"未知 repo_fixture '{fixture}'，需确认测试仓前置资源")

    return {
        "fixture": fixture,
        "secrets": secrets,
        "variables": variables,
        "blockers": blockers,
        "has_secrets": bool(secrets),
        "has_variables": bool(variables and len(variables) > 0),
        "known_fixture": fixture in KNOWN_FIXTURES,
    }


def classify_fault(fault_injection) -> dict:
    if not fault_injection:
        return {"blocked": False, "blocker": ""}
    return {"blocked": True, "blocker": FAULT_INJECTION_BLOCKER,
            "detail": fault_injection}


def classify_assertion(a: dict) -> dict:
    a_type = a.get("type", "")
    target = a.get("target", "")
    eval_ = a.get("eval", "")
    rubric = a.get("rubric", "")
    has_secret = "must_not_contain_secret" in a
    has_equals = "equals" in a

    r = {
        "type": a_type, "target": target, "eval": eval_,
        "rubric_preview": rubric[:80] + "..." if len(rubric) > 80 else rubric,
        "mappable": False, "kind": None, "missing_fields": [],
        "rubric_values": [], "blocker": "", "is_llm": (eval_ == "llm_assisted"),
    }

    if eval_ == "llm_assisted":
        r["blocker"] = "eval=llm_assisted, 需要 LLM 判定"
        return r

    if target in UNSUPPORTED_TARGETS:
        r["blocker"] = f"target={target} 不在引擎支持范围内"
        return r

    if has_secret and target == "run_logs":
        r["mappable"] = True
        r["kind"] = "mask"
        r["missing_fields"] = [f"secret_value: {a['must_not_contain_secret']} 的实际可见明文"]
        return r

    if target == "run_status":
        r["mappable"] = True
        r["kind"] = "run_status" if has_equals else "status"
        return r

    if target == "run_logs" and eval_ in ("deterministic", "determistic"):
        vals = extract_rubric_value(rubric)
        r["rubric_values"] = vals
        if a_type == "positive":
            r["mappable"] = True; r["kind"] = "value"
            if not vals:
                r["missing_fields"] = ["无法从 rubric 提取具体 expect 值"]
        elif a_type == "negative":
            r["mappable"] = True; r["kind"] = "leak"
            if not vals:
                r["missing_fields"] = ["无法从 rubric 提取具体 forbidden 值"]
        elif a_type == "nonfunctional":
            r["mappable"] = True; r["kind"] = "value"
            r["missing_fields"] = ["nonfunctional 类型语义模糊"]
        return r

    r["blocker"] = f"组合 type={a_type} target={target} eval={eval_} 无法映射"
    return r


def classify_case(yaml_path: Path) -> dict:
    with open(yaml_path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    cid = doc.get("id", yaml_path.stem)

    # 各维度分类
    trig = classify_trigger(doc.get("trigger") or {})
    setup_ = classify_setup(doc.get("setup") or {})
    fault = classify_fault(doc.get("fault_injection"))
    assertions = doc.get("assertions", [])
    assert_details = [classify_assertion(a) for a in assertions] if assertions else []

    # 收集所有阻断项
    all_blockers = []
    all_blockers.extend(trig["blockers"])
    all_blockers.extend(setup_["blockers"])
    if fault["blocked"]:
        all_blockers.append(fault["blocker"])
    for d in assert_details:
        if d["blocker"]:
            all_blockers.append(d["blocker"])

    # 断言统计
    mappable_a = [d for d in assert_details if d["mappable"]]
    unmappable_a = [d for d in assert_details if not d["mappable"]]
    llm_a = [d for d in assert_details if d["is_llm"]]

    # ── 判定分类（规则清晰、不相互覆盖）──
    if not trig["supported"]:
        # trigger 不支持 → 无法启动执行 → not_scriptable
        classification = "not_scriptable"
    elif not assert_details:
        # trigger 支持但无断言 → not_scriptable
        classification = "not_scriptable"
    elif not unmappable_a and not fault["blocked"] and not setup_["blockers"]:
        # trigger 支持 + 全部断言可映射 + 无 fault/setup 阻断 → full
        classification = "full_scriptable"
    else:
        # trigger 支持，但有至少一个阻断（断言/fault/setup）：能跑但不完整
        classification = "partial_scriptable"

    return {
        "case_id": cid,
        "dimension": doc.get("dimension", ""),
        "priority": doc.get("priority", ""),
        "title": doc.get("title", ""),
        "classification": classification,
        "all_blockers": all_blockers,
        "trigger": trig,
        "setup": setup_,
        "fault_injection": fault,
        "assertions_total": len(assertions),
        "assertions_mappable": len(mappable_a),
        "assertions_unmappable": len(unmappable_a),
        "assertions_llm": len(llm_a),
        "assertions_detail": assert_details,
    }


def main():
    yaml_dir = Path(__file__).resolve().parents[2] / "phase01/runs/2026-07-21-02/cases/yaml"
    if not yaml_dir.exists():
        print(f"[ERROR] cases dir not found: {yaml_dir}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(__file__).resolve().parent
    yaml_files = sorted(yaml_dir.glob("*.yaml"))

    results = []
    stats = defaultdict(lambda: defaultdict(int))

    for yf in yaml_files:
        r = classify_case(yf)
        results.append(r)
        dim = r["dimension"] or "unknown"
        cls = r["classification"]
        stats[dim][cls] += 1
        stats["__total__"][cls] += 1

    # ── JSON ──
    json_path = out_dir / "classification_v2_detail.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"[OK] {json_path}")

    # ── Markdown ──
    md_path = out_dir / "classification_v2_report.md"
    lines = []
    lines.append("# Case 完整可脚本化分类报告 v2（含 trigger + setup + fault + 断言）")
    lines.append("")
    lines.append(f"- **数据源**: `phase01/runs/2026-07-21-02/cases/yaml/`")
    lines.append(f"- **总 case 数**: {len(yaml_files)}")
    lines.append("")

    # 总体统计
    lines.append("## 总体统计")
    lines.append("")
    lines.append("| 分类 | 数量 | 占比 | 含义 |")
    lines.append("|------|------|------|------|")
    desc = {
        "full_scriptable": "trigger 支持 + 全部断言可映射，无阻断项",
        "partial_scriptable": "trigger 支持，但存在部分断言/参数无法映射",
        "not_scriptable": "trigger 不支持，或全部内容无法映射",
    }
    for cls in ("full_scriptable", "partial_scriptable", "not_scriptable"):
        cnt = stats["__total__"].get(cls, 0)
        pct = f"{cnt / len(yaml_files) * 100:.1f}%" if yaml_files else "0%"
        lines.append(f"| {cls} | {cnt} | {pct} | {desc.get(cls, '')} |")
    lines.append("")

    # 按维度
    lines.append("## 按维度 × 分类交叉统计")
    lines.append("")
    dims = ["completeness", "compatibility", "reliability", "security", "usability"]
    lines.append("| 维度 | full_scriptable | partial_scriptable | not_scriptable | 合计 |")
    lines.append("|------|-----------------|--------------------|----------------|------|")
    for dim in dims:
        f = stats[dim].get("full_scriptable", 0)
        p = stats[dim].get("partial_scriptable", 0)
        n = stats[dim].get("not_scriptable", 0)
        lines.append(f"| {dim} | {f} | {p} | {n} | {f+p+n} |")
    lines.append("")

    # 阻断项汇总
    lines.append("## 阻断项汇总（按出现次数排序）")
    lines.append("")
    blocker_counts = defaultdict(int)
    for r in results:
        for b in r["all_blockers"]:
            blocker_counts[b] += 1
    for blocker, cnt in sorted(blocker_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- **{cnt}** 条: `{blocker}`")
    lines.append("")

    # trigger 事件统计
    lines.append("## Trigger 事件分布")
    lines.append("")
    event_counts = defaultdict(int)
    for r in results:
        ev = r["trigger"]["event"]
        event_counts[ev] += 1
    lines.append("| 事件 | 数量 | 支持 |")
    lines.append("|------|------|------|")
    for ev, cnt in sorted(event_counts.items(), key=lambda x: -x[1]):
        supported = TRIGGER_SUPPORT.get(ev, {}).get("supported", False)
        lines.append(f"| {ev} | {cnt} | {'✅' if supported else '❌'} |")
    lines.append("")

    # 逐 case 明细
    lines.append("## 逐 Case 明细")
    lines.append("")
    for r in results:
        icon = {"full_scriptable": "✓", "partial_scriptable": "◐", "not_scriptable": "✗"}
        lines.append(f"### {icon.get(r['classification'], '?')} {r['case_id']} — {r['classification']}")
        lines.append(f"- 维度: {r['dimension']} | 优先级: {r['priority']}")
        lines.append(f"- 断言: {r['assertions_mappable']}/{r['assertions_total']} 可映射, {r['assertions_unmappable']} 无法映射, {r['assertions_llm']} 需 LLM")
        lines.append(f"- Trigger: event={r['trigger']['event']}, as={r['trigger']['actor']}, supported={r['trigger']['supported']}")
        if r['trigger']['param_keys']:
            lines.append(f"- Trigger params: {r['trigger']['param_keys']}")
        if r['trigger']['blockers']:
            for b in r['trigger']['blockers']:
                lines.append(f"  - 🚫 trigger: {b}")
        lines.append(f"- Setup: fixture={r['setup']['fixture']}, secrets={r['setup']['secrets']}, vars={r['setup']['variables']}")
        if r['setup']['blockers']:
            for b in r['setup']['blockers']:
                lines.append(f"  - ⚠️ setup: {b}")
        if r['fault_injection']['blocked']:
            lines.append(f"  - 💥 fault_injection: {r['fault_injection']['blocker']}")
            lines.append(f"    detail: {r['fault_injection']['detail']}")

        # 每条断言
        for i, d in enumerate(r["assertions_detail"]):
            flag = "✅" if d["mappable"] else ("🤖" if d["is_llm"] else "❌")
            lines.append(f"  {flag} assert[{i}] type={d['type']} target={d['target']} eval={d['eval']}")
            if d["kind"]:
                lines.append(f"     → kind: `{d['kind']}`")
            if d["rubric_values"]:
                lines.append(f"     → 候选值: {d['rubric_values']}")
            if d["missing_fields"]:
                for mf in d["missing_fields"]:
                    lines.append(f"     ⚠️ 缺: {mf}")
            if d["blocker"]:
                lines.append(f"     🚫 {d['blocker']}")
        lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] {md_path}")

    # ── CSV ──
    csv_path = out_dir / "classification_v2.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("case_id,dimension,priority,classification,trigger_event,trigger_as,trigger_supported,"
                "fixture,fault_injection,assertions_total,assertions_mappable,assertions_unmappable,"
                "assertions_llm,blocker_count,blockers\n")
        for r in results:
            blockers_str = " | ".join(r["all_blockers"]).replace('"', "'")
            fault_str = json.dumps(r["fault_injection"]["detail"]) if r["fault_injection"]["blocked"] else "null"
            f.write(f'{r["case_id"]},{r["dimension"]},{r["priority"]},{r["classification"]},'
                    f'{r["trigger"]["event"]},{r["trigger"]["actor"]},{r["trigger"]["supported"]},'
                    f'{r["setup"]["fixture"]},{fault_str},'
                    f'{r["assertions_total"]},{r["assertions_mappable"]},{r["assertions_unmappable"]},'
                    f'{r["assertions_llm"]},{len(r["all_blockers"])},"{blockers_str}"\n')
    print(f"[OK] {csv_path}")


if __name__ == "__main__":
    main()
