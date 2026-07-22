#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classify_cases.py — 逐个遍历 Phase 01 case YAML，对照 Phase 02 assertion_engine 能力，
分类每个 case 的断言可脚本化程度。

输出：
  class: full_scriptable   — 所有断言均可映射到 assertion_engine 的已知 kind
  class: partial_scriptable — 至少一个断言可映射，但存在无法映射的断言
  class: not_scriptable     — 所有断言均无法映射

同时输出每个断言的映射详情，包括 rubric 中是否能提取出具体 value。
"""

import yaml
import re
import json
import sys
from pathlib import Path
from collections import defaultdict

# ── assertion_engine 支持的 kind ──────────────────────────────────────
# 来自 assertion_engine.py 第 15-26 行
ENGINE_KINDS = {"status", "run_status", "value", "leak", "mask", "config_probe"}

# target → 可映射的 engine kind(s)
TARGET_KIND_MAP = {
    "run_logs":    {"value", "leak", "mask", "config_probe"},
    "run_status":  {"status", "run_status"},
}

# 这些 target 当前 assertion_engine 完全不支持，需要新的 infra：
UNSUPPORTED_TARGETS = {
    "error_message", "run_ui", "badge_response", "runner_schedulable",
    "runner_scheduling", "step_summary", "artifacts", "documentation",
    "queue_ui", "pr_ui", "run_duration", "workflow_validation",
}

# ── rubric 内具体值提取 ──────────────────────────────────────────────

# 匹配：中文引号/括号内的值、大写_下划线_标识符、日志模式
_RE_CN_QUOTED = re.compile(r'[「『"]([^」』"]+)[」』"]')
_RE_EN_QUOTED = re.compile(r"'([^']+)'")
_RE_UPPER_IDENT = re.compile(r'\b([A-Z][A-Z0-9_]{2,}(?:_[A-Z0-9]+)*)\b')
_RE_PAREN_VALUE = re.compile(r'[（(]([^）)]+)[）)]')
_RE_SPECIFIC_WORD = re.compile(r'\b(?:含|包含|输出|出现|显示|返回|为|是否是?)\s*[：:]?\s*([A-Za-z_][A-Za-z0-9_.-]+)')


def extract_rubric_value(rubric: str) -> list[str]:
    """尝试从中文 rubric 中提取可用于日志搜索的具体值。"""
    candidates = []

    # 英文引号内的值
    for m in _RE_EN_QUOTED.finditer(rubric):
        candidates.append(m.group(1))

    # 大写_下划线_标识符（如 WORKFLOW_PARSED, ENV_SECRET_ACCESSED）
    for m in _RE_UPPER_IDENT.finditer(rubric):
        val = m.group(1)
        if val not in candidates and not val.startswith("_") and len(val) >= 4:
            candidates.append(val)

    # 中文括号内的值（如 输出 Hello）
    for m in _RE_PAREN_VALUE.finditer(rubric):
        inner = m.group(1).strip()
        # 过滤纯中文
        if re.search(r'[A-Za-z0-9_]', inner):
            candidates.append(inner)

    # "含/包含/输出/出现/显示" 后紧跟的具体词
    for m in _RE_SPECIFIC_WORD.finditer(rubric):
        val = m.group(1)
        if val not in candidates and not val.startswith("_"):
            candidates.append(val)

    return list(dict.fromkeys(candidates))  # 去重保序


# ── 单条断言分类 ──────────────────────────────────────────────────────

def classify_assertion(a: dict, case_id: str) -> dict:
    """
    返回单条断言的分类详情：
      mappable: bool          — 能否映射到 assertion_engine kind
      kind: str | None        — 映射到的 kind
      missing_fields: list    — 映射后缺失的关键字段（如 expect / forbidden）
      rubric_values: list     — 从 rubric 提取的候选值
      blocker: str            — 无法映射的原因
      is_llm: bool            — 是否需要 LLM
    """
    a_type = a.get("type", "")
    target = a.get("target", "")
    eval_ = a.get("eval", "")
    rubric = a.get("rubric", "")
    has_secret = "must_not_contain_secret" in a
    has_equals = "equals" in a

    result = {
        "type": a_type,
        "target": target,
        "eval": eval_,
        "rubric_preview": rubric[:80] + "..." if len(rubric) > 80 else rubric,
        "mappable": False,
        "kind": None,
        "missing_fields": [],
        "rubric_values": [],
        "blocker": "",
        "is_llm": (eval_ == "llm_assisted"),
    }

    # 1. LLM assisted — 无条件不可映射
    if eval_ == "llm_assisted":
        result["blocker"] = "eval=llm_assisted, 需要 LLM 判定"
        return result

    # 2. target 完全不在引擎支持范围
    if target in UNSUPPORTED_TARGETS:
        result["blocker"] = f"target={target} 不在引擎支持范围内（需新 infra）"
        return result

    # 3. must_not_contain_secret — 可映射为 mask
    if has_secret and target == "run_logs":
        secret_name = a["must_not_contain_secret"]
        result["mappable"] = True
        result["kind"] = "mask"
        result["missing_fields"] = [f"secret_value: {secret_name} 的实际可见明文"]
        return result

    # 4. run_status 映射
    if target == "run_status":
        if has_equals:
            result["mappable"] = True
            result["kind"] = "run_status"
            result["missing_fields"] = []  # a["equals"] 可直接用
            return result
        else:
            result["mappable"] = True
            result["kind"] = "status"
            # status kind 不需要额外字段
            return result

    # 5. run_logs 映射
    if target == "run_logs" and eval_ in ("deterministic", "determistic"):
        rubric_vals = extract_rubric_value(rubric)
        result["rubric_values"] = rubric_vals

        if a_type == "positive":
            result["mappable"] = True
            result["kind"] = "value"
            if rubric_vals:
                result["missing_fields"] = []  # 有候选值
            else:
                result["missing_fields"] = ["无法从 rubric 提取具体 expect 值，需手工标注"]
            return result

        if a_type == "negative":
            result["mappable"] = True
            result["kind"] = "leak"
            if rubric_vals:
                result["missing_fields"] = []  # 有候选 forbidden 值
            else:
                result["missing_fields"] = ["无法从 rubric 提取具体 forbidden 值，需手工标注"]
            return result

        if a_type == "nonfunctional":
            result["mappable"] = True
            result["kind"] = "value"  # 近似
            result["missing_fields"] = ["nonfunctional 类型语义模糊，需人工判定期望"]
            return result

    # 6. 无法归类
    result["blocker"] = f"组合 type={a_type} target={target} eval={eval_} 无法映射"
    return result


# ── 单 case 分类 ──────────────────────────────────────────────────────

def classify_case(yaml_path: Path) -> dict:
    with open(yaml_path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    case_id = doc.get("id", yaml_path.stem)
    assertions = doc.get("assertions", [])
    dimension = doc.get("dimension", "")
    priority = doc.get("priority", "")
    title = doc.get("title", "")

    if not assertions:
        return {
            "case_id": case_id,
            "dimension": dimension,
            "priority": priority,
            "title": title,
            "total_assertions": 0,
            "classification": "not_scriptable",
            "reason": "无断言",
            "assertions_detail": [],
            "mappable_count": 0,
            "unmappable_count": 0,
            "llm_count": 0,
        }

    details = [classify_assertion(a, case_id) for a in assertions]
    mappable = [d for d in details if d["mappable"]]
    unmappable = [d for d in details if not d["mappable"]]
    llm = [d for d in details if d["is_llm"]]

    # 有哪些 unmappable 的 blocker（去重）
    blockers = list(set(d["blocker"] for d in unmappable if d["blocker"]))

    if not unmappable:
        classification = "full_scriptable"
        reason = "全部断言可映射"
    elif not mappable:
        classification = "not_scriptable"
        reason = "; ".join(blockers) if blockers else "全部断言无法映射"
    else:
        classification = "partial_scriptable"
        reason = "; ".join(blockers) if blockers else "部分断言无法映射"

    return {
        "case_id": case_id,
        "dimension": dimension,
        "priority": priority,
        "title": title,
        "total_assertions": len(assertions),
        "classification": classification,
        "reason": reason,
        "assertions_detail": details,
        "mappable_count": len(mappable),
        "unmappable_count": len(unmappable),
        "llm_count": len(llm),
    }


# ── 主流程 ────────────────────────────────────────────────────────────

def main():
    yaml_dir = Path(__file__).resolve().parents[2] / "phase01/runs/2026-07-21-02/cases/yaml"
    if not yaml_dir.exists():
        print(f"[ERROR] cases dir not found: {yaml_dir}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(__file__).resolve().parent
    yaml_files = sorted(yaml_dir.glob("*.yaml"))

    results = []
    stats = defaultdict(lambda: defaultdict(int))  # stats[dim][class] = count

    for yf in yaml_files:
        r = classify_case(yf)
        results.append(r)
        dim = r["dimension"] or "unknown"
        cls = r["classification"]
        stats[dim][cls] += 1
        stats["__total__"][cls] += 1

    # ── 写入详细 JSON ──
    json_path = out_dir / "classification_detail.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"[OK] 详细分类结果 → {json_path}")

    # ── 写入摘要 Markdown ──
    md_path = out_dir / "classification_report.md"
    lines = []
    lines.append("# Case 可脚本化分类报告")
    lines.append("")
    lines.append(f"**数据源**: `phase01/runs/2026-07-21-02/cases/yaml/`")
    lines.append(f"**总 case 数**: {len(yaml_files)}")
    lines.append(f"**assertion_engine 支持 kind**: {', '.join(sorted(ENGINE_KINDS))}")
    lines.append("")

    # 总体统计
    lines.append("## 总体统计")
    lines.append("")
    lines.append("| 分类 | 数量 | 占比 |")
    lines.append("|------|------|------|")
    for cls in ("full_scriptable", "partial_scriptable", "not_scriptable"):
        cnt = stats["__total__"].get(cls, 0)
        pct = f"{cnt / len(yaml_files) * 100:.1f}%" if yaml_files else "0%"
        lines.append(f"| {cls} | {cnt} | {pct} |")
    lines.append("")

    # 按维度
    lines.append("## 按维度 × 分类交叉统计")
    lines.append("")
    dims = ["completeness", "compatibility", "reliability", "security", "usability"]
    header = "| 维度 | full_scriptable | partial_scriptable | not_scriptable | 合计 |"
    sep = "|------|-----------------|--------------------|----------------|------|"
    lines.append(header)
    lines.append(sep)
    for dim in dims:
        f = stats[dim].get("full_scriptable", 0)
        p = stats[dim].get("partial_scriptable", 0)
        n = stats[dim].get("not_scriptable", 0)
        total = f + p + n
        lines.append(f"| {dim} | {f} | {p} | {n} | {total} |")
    lines.append("")

    # unmappable 原因汇总
    lines.append("## 无法映射的断言原因汇总")
    lines.append("")
    blocker_counts = defaultdict(int)
    for r in results:
        for d in r["assertions_detail"]:
            if d["blocker"]:
                blocker_counts[d["blocker"]] += 1

    for blocker, cnt in sorted(blocker_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- **{cnt}** 条: `{blocker}`")
    lines.append("")

    # 按 case 明细
    lines.append("## 逐 Case 明细")
    lines.append("")
    for r in results:
        icon = {"full_scriptable": "✓", "partial_scriptable": "◐", "not_scriptable": "✗"}
        lines.append(f"### {icon.get(r['classification'], '?')} {r['case_id']} — {r['classification']}")
        lines.append(f"- 维度: {r['dimension']} | 优先级: {r['priority']}")
        lines.append(f"- 可映射断言: {r['mappable_count']} / 无法映射: {r['unmappable_count']} / 需 LLM: {r['llm_count']}")
        lines.append(f"- 原因: {r['reason']}")

        for i, d in enumerate(r["assertions_detail"]):
            status_flag = "✅" if d["mappable"] else ("🤖" if d["is_llm"] else "❌")
            lines.append(f"  {status_flag} 断言[{i}] type={d['type']} target={d['target']} eval={d['eval']}")
            if d["kind"]:
                lines.append(f"     映射 kind: `{d['kind']}`")
            if d["rubric_values"]:
                lines.append(f"     提取候选值: {d['rubric_values']}")
            if d["missing_fields"]:
                for mf in d["missing_fields"]:
                    lines.append(f"     ⚠️ 缺少: {mf}")
            if d["blocker"]:
                lines.append(f"     🚫 {d['blocker']}")
        lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] 分类报告 → {md_path}")

    # ── 写入 CSV ──
    csv_path = out_dir / "classification.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("case_id,dimension,priority,classification,total_assertions,mappable,unmappable,llm_assisted,reason\n")
        for r in results:
            f.write(f"{r['case_id']},{r['dimension']},{r['priority']},{r['classification']},"
                    f"{r['total_assertions']},{r['mappable_count']},{r['unmappable_count']},"
                    f"{r['llm_count']},\"{r['reason']}\"\n")
    print(f"[OK] CSV → {csv_path}")


if __name__ == "__main__":
    main()
