#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
api_gap_analysis_v2.py — 将 v2 分类阻断项映射到 GitCode API 缺口。

对照 api-reference.md 中已有的 20 个 Actions API，分析每种阻断类型
需要什么新 API / API 已存在未集成 / 非 API 问题。
"""

import json
from pathlib import Path
from collections import defaultdict

# ── 阻断 → API 缺口（结构化、一行一个） ────────────────────────────

BLOCKER_TO_GAP = {
    # trigger 类
    "fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者": (
        "need_new_api", "fork_pr",
        "POST /api/v5/repos/:owner/:repo/forks （创建 fork）",
        "POST /api/v5/repos/:owner/:repo/pulls （从 fork 分支向目标仓开 PR）",
        "第二 GitCode 账号的 OAuth token",
        "api-reference 未提及 fork API；v5 PR 只提示了 GET 端点",
    ),
    "trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者": (
        "need_account", "untrusted",
        "第二 GitCode 账号 + OAuth token（非 API 缺口，是账号资源）",
        "即使 trigger=push 也需以 untrusted 身份 push 到 fork → 开 PR",
    ),
    "manual 触发：需 workflow_dispatch API（待确认端点）": (
        "need_new_api", "manual",
        "POST /api/v8/repos/:owner/:repo/actions/workflows/:workflow_id/dispatch",
        "api-reference 的 run 过滤参数有 event=Manual，说明平台支持 manual 触发，dispatch 端点路径待确认",
    ),
    "pr 触发：需建分支+开 PR（待确认 PR API）": (
        "need_new_api", "pr",
        "POST /api/v5/repos/:owner/:repo/pulls （创建 PR）",
        "api-reference 相邻 API 提示 v5 pull requests 存在，但未列出 POST 端点",
    ),
    "pull_request：需建分支+开 PR（待确认 PR API）": (
        "need_new_api", "pull_request",
        "POST /api/v5/repos/:owner/:repo/pulls （创建 PR）",
        "同 pr 触发",
    ),
    "pull_request_target：同 PR + base 上下文语义": (
        "need_new_api", "pull_request_target",
        "POST /api/v5/repos/:owner/:repo/pulls （创建 PR）",
        "需额外验证 target 上下文中 fork PR 无法访问 secrets",
    ),
    "pull_request_comment：需 PR comment API（未实现）": (
        "need_new_api", "pull_request_comment",
        "POST /api/v5/repos/:owner/:repo/pulls/:number/comments （PR comment）",
        "api-reference 提及 v5 Issues 但未提及 PR comments",
    ),
    "schedule：cron 无法按需触发（基础设施限制）": (
        "not_api_problem", "schedule",
        "非 API 问题。cron 由平台按时调度，外部无法触发。变通：push trigger + ATOMGIT_EVENT_NAME=schedule",
    ),

    # fault_injection
    "fault_injection 非 null：当前执行器不支持故障注入（需 kill_runner / network_partition / concurrent_flood infra）": (
        "need_run_cancel", "fault_injection",
        "POST /api/v8/repos/:owner/:repo/actions/runs/:run_id/cancel （kill_runner 模拟）",
        "network_partition 需 infra 层操作（无标准 API）",
        "concurrent_flood 可用 workflow_dispatch API 批量触发模拟",
    ),

    # 断言 target — 非 API 或已有 API 未集成
    "target=badge_response 不在引擎支持范围内": (
        "not_api_problem", "badge",
        "非 GitCode API — HTTP GET badge URL 即可，直接用 curl/libcurl",
    ),
    "target=run_ui 不在引擎支持范围内": (
        "not_api_problem", "run_ui",
        "非 API 问题 — 需 Playwright 浏览器自动化检查 Web UI",
    ),
    "target=artifacts 不在引擎支持范围内": (
        "api_exists_unused", "artifacts",
        "GET /api/v8/.../actions/artifacts + download — API 已有，只需集成到 assertion_engine",
    ),
    "target=step_summary 不在引擎支持范围内": (
        "api_exists_unused", "step_summary",
        "GET /api/v8/.../actions/runs/:run_id/jobs/:job_id — Job detail 已有 steps 信息，只需扩展 assertion_engine",
    ),
    "target=run_duration 不在引擎支持范围内": (
        "api_exists_unused", "run_duration",
        "GET /api/v8/.../actions/runs/:run_id — 已有 start_time/end_time，只需计算差值",
    ),
    "target=runner_schedulable 不在引擎支持范围内": (
        "api_exists_unused", "runner_schedulable",
        "GET /api/v8/.../actions/runners — API 已有，只需检查 runner 在线状态",
    ),
    "target=runner_scheduling 不在引擎支持范围内": (
        "api_exists_unused", "runner_scheduling",
        "同 runner_schedulable — API 已有",
    ),
    "target=workflow_validation 不在引擎支持范围内": (
        "api_exists_unused", "workflow_validation",
        "POST /api/v2/projects/:project/actions/valid — validate_workflow.py 已实现",
    ),
    "target=pr_ui 不在引擎支持范围内": (
        "not_api_problem", "pr_ui",
        "同 run_ui — 需 Playwright",
    ),

    # 断言 eval
    "eval=llm_assisted, 需要 LLM 判定": (
        "not_api_problem", "llm_assisted",
        "非 API 问题 — 需 LLM 辅助判定通道集成到 assertion_engine",
        "44 条中 27 条 target=error_message（可诊断性评估），其余在 run_logs/run_ui 等",
    ),
}


def main():
    v2_json = Path(__file__).resolve().parent / "classification_v2_detail.json"
    with open(v2_json) as f:
        cases = json.load(f)

    # ── 收集所有唯一阻断项 ──
    all_blockers_set = set()
    for c in cases:
        for b in c["all_blockers"]:
            all_blockers_set.add(b)

    # ── 按类别分组 ──
    need_new_api = []       # 🔴 完全缺失
    api_exists_unused = []  # 🟡 已有未集成
    not_api_problem = []    # 🟢 非 API
    need_account = []       # 🔵 账号
    need_run_cancel = []    # 🔴 cancel API + infra
    unknown = []

    for blocker in sorted(all_blockers_set):
        gap = BLOCKER_TO_GAP.get(blocker)
        if gap is None:
            # 前缀匹配
            for key, val in BLOCKER_TO_GAP.items():
                if blocker.startswith(key.split("：")[0]) or key.startswith(blocker.split("：")[0]):
                    gap = val
                    break
        if gap is None:
            unknown.append(blocker)
        elif gap[0] == "need_new_api":
            need_new_api.append((blocker, gap))
        elif gap[0] == "api_exists_unused":
            api_exists_unused.append((blocker, gap))
        elif gap[0] == "not_api_problem":
            not_api_problem.append((blocker, gap))
        elif gap[0] == "need_account":
            need_account.append((blocker, gap))
        elif gap[0] == "need_run_cancel":
            need_run_cancel.append((blocker, gap))

    # 统计每个阻断影响的 case 数
    blocker_case_count = defaultdict(int)
    for c in cases:
        for b in c["all_blockers"]:
            blocker_case_count[b] += 1

    # ── 写报告 ──
    lines = []
    lines.append("# Phase 02 API 缺口分析")
    lines.append("")
    lines.append("对照 `phase01/inputs/gitcode-api/api-reference.md`（20 个 Actions API），分析全部阻断项的 API 缺口。")
    lines.append("")

    lines.append("## 总体")
    lines.append("")
    lines.append(f"- 总 case: {len(cases)}")
    lines.append(f"- 可直接跑 (full_scriptable): {sum(1 for c in cases if c['classification']=='full_scriptable')}")
    lines.append(f"- 部分可跑 (partial_scriptable): {sum(1 for c in cases if c['classification']=='partial_scriptable')}")
    lines.append(f"- 无法跑 (not_scriptable): {sum(1 for c in cases if c['classification']=='not_scriptable')}")
    lines.append("")

    # ── 🔴 完全缺失的 API ──
    lines.append("## 🔴 完全缺失的 API（api-reference 中无对应端点）")
    lines.append("")
    lines.append("| 阻断 | 影响 case | 缺失的 API |")
    lines.append("|------|----------|-----------|")

    seen_gaps = set()
    for blocker, gap in need_new_api:
        if gap[1] in seen_gaps:
            continue
        seen_gaps.add(gap[1])
        cnt = blocker_case_count.get(blocker, 0)
        # 同类阻断也加起来
        for b2, cnt2 in blocker_case_count.items():
            if b2 != blocker:
                g2 = BLOCKER_TO_GAP.get(b2)
                if g2 and g2[1] == gap[1]:
                    cnt += cnt2
        apis = [x for x in gap[2:] if x.startswith("POST") or x.startswith("GET") or x.startswith("DELETE") or x.startswith("PUT")]
        api_str = "<br>".join(apis)
        note = [x for x in gap[2:] if not (x.startswith("POST") or x.startswith("GET") or x.startswith("DELETE") or x.startswith("PUT"))]
        note_str = " ".join(note) if note else ""
        lines.append(f"| {gap[1]} | {cnt} | {api_str}<br><small>{note_str}</small> |")

    lines.append("")

    # ── 🟡 已有 API 未集成 ──
    lines.append("## 🟡 API 已存在但未集成到 assertion_engine / workflow_runner")
    lines.append("")
    lines.append("| 阻断 | 影响 case | 已有 API | 缺失的动作 |")
    lines.append("|------|----------|---------|-----------|")
    for blocker, gap in api_exists_unused:
        cnt = blocker_case_count.get(blocker, 0)
        apis = [x for x in gap[2:] if "GET" in x or "POST" in x or "DELETE" in x]
        notes = [x for x in gap[2:] if x not in apis]
        api_str = "<br>".join(apis)
        note_str = " ".join(notes)
        lines.append(f"| {gap[1]} | {cnt} | {api_str} | {note_str} |")
    lines.append("")

    # ── 🟢 非 API 问题 ──
    lines.append("## 🟢 非 API 问题")
    lines.append("")
    lines.append("| 阻断 | 影响 case | 解决方式 |")
    lines.append("|------|----------|---------|")
    for blocker, gap in not_api_problem + need_account:
        cnt = blocker_case_count.get(blocker, 0)
        note = " ".join(gap[2:])
        lines.append(f"| {gap[1]} | {cnt} | {note} |")
    lines.append("")

    # ── fault_injection 特例 ──
    lines.append("## 🔴 fault_injection 特例")
    lines.append("")
    lines.append("| 阻断 | 影响 case | 需要的能力 |")
    lines.append("|------|----------|-----------|")
    for blocker, gap in need_run_cancel:
        cnt = blocker_case_count.get(blocker, 0)
        note = " ".join(gap[2:])
        lines.append(f"| {gap[1]} | {cnt} | {note} |")
    lines.append("")

    # ── 未知 fixture ──
    lines.append("## ⚠️ 未知 repo_fixture")
    lines.append("")
    fixture_blockers = [b for b in all_blockers_set if "repo_fixture" in b]
    fixture_cases = defaultdict(list)
    for c in cases:
        for b in c["all_blockers"]:
            if "repo_fixture" in b:
                fixture_cases[b].append(c["case_id"])
    for b in sorted(fixture_blockers):
        lines.append(f"- **{b}**: {len(fixture_cases[b])} cases ({', '.join(fixture_cases[b][:5])}...)" if len(fixture_cases[b]) > 5 else f"- **{b}**: {len(fixture_cases[b])} cases ({', '.join(fixture_cases[b])})")
    lines.append("")
    lines.append("> 解决方式：在测试组织下预先创建对应 fixture 仓，配置好 secrets/variables/branch_protection。非 API 缺口。")

    # ── 汇总：要拿到 GitCode 侧去确认的端点 ──
    lines.append("## 📋 需要向 GitCode 侧确认/申请的端点清单")
    lines.append("")
    lines.append("| 优先级 | API 端点 | 方法 | 用途 | 影响 case 数 |")
    lines.append("|--------|---------|------|------|-------------|")
    todo = [
        ("P0", "/api/v5/repos/:owner/:repo/pulls", "POST", "创建 PR（解锁 20 case）", "20"),
        ("P0", "/api/v8/repos/:owner/:repo/actions/workflows/:workflow_id/dispatch", "POST", "workflow_dispatch（解锁 5 manual case + 故障注入 flood）", "5+5"),
        ("P1", "/api/v5/repos/:owner/:repo/forks", "POST", "创建 fork（解锁 13 fork_pr case）", "13"),
        ("P1", "/api/v8/repos/:owner/:repo/actions/runs/:run_id/cancel", "POST", "取消运行（调试 + 5 chaos case）", "5"),
        ("P2", "/api/v5/repos/:owner/:repo/pulls/:number/comments", "POST", "PR comment 触发（1 case）", "1"),
    ]
    for pri, endpoint, method, purpose, count in todo:
        lines.append(f"| {pri} | `{endpoint}` | {method} | {purpose} | {count} |")
    lines.append("")

    out_path = Path(__file__).resolve().parent / "api_gap_analysis_v2.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] {out_path}")


if __name__ == "__main__":
    main()
