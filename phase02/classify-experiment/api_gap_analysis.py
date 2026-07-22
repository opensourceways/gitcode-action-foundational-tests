#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
api_gap_analysis.py — 将 v2 分类中的阻断项映射到 GitCode API 缺口。

对照 phase01/inputs/gitcode-api/api-reference.md 中已存在的 20 个 Actions API 端点，
分析每种阻断是否需要新 API、已有 API 但未实现、还是非 API 问题（infra/LLM/UI）。
"""

import json
from pathlib import Path
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════════
#  已知 GitCode API（来自 api-reference.md）
# ═══════════════════════════════════════════════════════════════════

EXISTING_ACTIONS_API = {
    "list_runs":           "GET  /api/v8/repos/:owner/:repo/actions/runs",
    "get_run":             "GET  /api/v8/repos/:owner/:repo/actions/runs/:run_id",
    "list_jobs":           "GET  /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs",
    "get_job":             "GET  /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs/:job_id",
    "download_log":        "GET  /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs/:job_id/download-log",
    "list_artifacts":      "GET  /api/v8/repos/:owner/:repo/actions/artifacts",
    "list_run_artifacts":  "GET  /api/v8/repos/:owner/:repo/actions/runs/:run_id/artifacts",
    "get_artifact":        "GET  /api/v8/repos/:owner/:repo/actions/artifacts/:artifact_id",
    "delete_artifact":     "DELETE /api/v8/repos/:owner/:repo/actions/artifacts/:artifact_id",
    "download_artifact":   "GET  /api/v8/repos/:owner/:repo/actions/artifacts/:artifact_id/:archive_format",
    "list_runners":         "GET  /api/v8/repos/:owner/:repo/actions/runners",
    "list_shared_runners":  "GET  /api/v8/repos/:owner/:repo/actions/runners/shared-runners",
    "list_runner_sets":     "GET  /api/v8/repos/:owner/:repo/actions/runner-sets",
    "list_shared_runner_sets": "GET /api/v8/repos/:owner/:repo/actions/shared-runner-sets",
    "list_runner_groups":   "GET  /api/v8/orgs/:org/actions/runner-groups",
    "get_runner_group":     "GET  /api/v8/orgs/:org/actions/runner-groups/:runner_group_id",
    "list_group_runners":   "GET  /api/v8/orgs/:org/actions/runner-groups/:runner_group_id/runners",
    "list_group_runner_sets": "GET /api/v8/orgs/:org/actions/runner-groups/:runner_group_id/runners/sets",
    "list_shared_namespaces": "GET /api/v8/orgs/:org/actions/runner-groups/:runner_group_id/shared-namespaces",
    "validate_workflow":    "POST /api/v2/projects/:project/actions/valid",  # from validate_workflow.py, not in api-reference
}

# 相邻 API（api-reference 末尾提及但未列出完整端点）
NEIGHBOR_API_HINTS = {
    "pr_list":   "GET  /api/v5/repos/:owner/:repo/pulls",
    "webhooks":  "GET  /api/v5/repos/:owner/:repo/hooks",
    "git_trees": "GET  /api/v5/repos/:owner/:repo/git/trees/:sha",
    "issues":    "POST /api/v5/repos/:owner/issues",
}

# ═══════════════════════════════════════════════════════════════════
#  阻断项 → API 缺口映射
# ═══════════════════════════════════════════════════════════════════

BLOCKER_API_MAP = {
    # ── trigger 相关 ──
    "fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者": {
        "category": "trigger",
        "needs_new_api": True,
        "missing_apis": [
            "POST /api/v5/repos/:owner/:repo/forks  — 创建 fork",
            "POST /api/v5/repos/:owner/:repo/pulls  — 从 fork 分支向目标仓开 PR",
            "需要第二 GitCode 账号的 OAuth token",
        ],
        "note": "api-reference 提及 v5 PR API 但未列出 POST 端点；fork API 未见任何文档。",
    },
    "trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者": {
        "category": "trigger",
        "needs_new_api": False,  # 非 API 问题，是账号/权限问题
        "missing_apis": [
            "需要第二 GitCode 账号（非 ComputingActionTest）+ OAuth token",
        ],
        "note": "即使 trigger 是 push，也需要以 untrusted 账号身份 push 到 fork 再开 PR。",
    },
    "manual 触发：需 workflow_dispatch API（待确认端点）": {
        "category": "trigger",
        "needs_new_api": True,
        "missing_apis": [
            "POST /api/v8/repos/:owner/:repo/actions/workflows/:workflow_id/dispatch",
            "— workflow_dispatch 端点未在 api-reference 中出现",
            "（run 列表过滤参数有 event=Manual，说明平台已支持 manual 触发；",
            "  dispatch API 需从 GitCode 侧确认端点路径、请求体格式）",
        ],
    },
    "pr 触发：需建分支+开 PR（待确认 PR API）": {
        "category": "trigger",
        "needs_new_api": True,
        "missing_apis": [
            "POST /api/v5/repos/:owner/:repo/pulls  — 创建 PR",
            "(api-reference 相邻 API 中提及 v5 pull requests，但未列出完整端点；需确认参数格式、PR 创建后 run 关联方式)",
        ],
    },
    "pull_request：需建分支+开 PR（待确认 PR API）": {
        "category": "trigger",
        "needs_new_api": True,
        "missing_apis": [],  # same as pr
        "note": "与 pr 触发相同，仅事件名不同。",
    },
    "pull_request_target：同 PR + base 上下文语义": {
        "category": "trigger",
        "needs_new_api": True,
        "missing_apis": [],  # same as pr
        "note": "除 PR 创建 API 外，还需验证 target 上下文中 secrets 对 fork 不可见。",
    },
    "pull_request_comment：需 PR comment API（未实现）": {
        "category": "trigger",
        "needs_new_api": True,
        "missing_apis": [
            "POST /api/v5/repos/:owner/:repo/pulls/:number/comments  — 向 PR 发 comment",
            "（api-reference 提及 v5 Issues 但未提及 PR comments 端点）",
        ],
    },
    "schedule：cron 无法按需触发（基础设施限制）": {
        "category": "trigger",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "非 API 问题。cron 由平台侧按 schedule 字段调度，无法从外部触发。"
                "可通过 push trigger + ATOMGIT_EVENT_NAME=schedule 环境变量变通测试。",
    },
    "tag 触发：需 git tag+push 并按 tag ref 匹配": {
        "category": "trigger",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "本批 case 无 tag 触发。如需支持：git CLI 操作即可（tag + push），"
                "无需额外 API。run 匹配需按 tag ref 过滤（现有 poll_run 只按 head_sha + file_path）。",
    },

    # ── fault_injection ──
    "fault_injection 非 null：当前执行器不支持故障注入（需 kill_runner / network_partition / concurrent_flood infra）": {
        "category": "fault_injection",
        "needs_new_api": True,
        "missing_apis": [
            "POST /api/v8/repos/:owner/:repo/actions/runs/:run_id/cancel — 取消运行（模拟 kill_runner）",
            "无标准 API 可模拟 network_partition（需 infra 层操作）",
            "无标准 API 可模拟 concurrent_flood（需大量并发 dispatch 调用）",
        ],
        "note": "api-reference 有 run cancel 概念（status=CANCELED），但无对应端点。"
                "concurrent_flood 可通过 workflow_dispatch API 批量触发实现。",
    },

    # ── 断言 target ──
    "target=badge_response 不在引擎支持范围内": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [
            "HTTP GET {badge_url} — 直接 curl 即可（非 GitCode API，是 badge CDN 端点）",
        ],
        "note": "只需 HTTP client 检查 SVG 内容。trigger.params 中有 badge_url_template。",
    },
    "target=run_ui 不在引擎支持范围内": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "非 API 问题。需要 Playwright 浏览器自动化检查 Web UI。",
    },
    "target=artifacts 不在引擎支持范围内": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "API 已有！`GET /api/v8/.../actions/artifacts` + download endpoint。"
                "只需在 assertion_engine 中添加 artifact 断言 kind。",
    },
    "target=step_summary 不在引擎支持范围内": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "Job detail API (`get_job`) 已返回 steps 详情。需扩展 assertion_engine 解析 step 级别数据。",
    },
    "target=run_duration 不在引擎支持范围内": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "Run detail API 已有 `start_time` / `end_time`。只需计算差值并判断。",
    },
    "target=runner_schedulable 不在引擎支持范围内": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "API 已有！`GET /api/v8/.../actions/runners` 可查 runner 状态。"
                "只需扩展 assertion_engine。",
    },
    "target=runner_scheduling 不在引擎支持范围内": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "同 runner_schedulable。",
    },
    "target=workflow_validation 不在引擎支持范围内": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "validate_workflow.py 已实现 `POST /api/v2/projects/:project/actions/valid`。"
                "只需集成到 assertion_engine。",
    },
    "target=pr_ui 不在引擎支持范围内": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "同 run_ui，需 Playwright。",
    },

    # ── 断言 eval ──
    "eval=llm_assisted, 需要 LLM 判定": {
        "category": "assertion",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "非 API 问题。需在 assertion_engine 中添加 LLM 辅助判定通道（如评估 error_message 可诊断性）。"
                "44 条此类断言中，27 条 target=error_message（可诊断性评估），其余分布在 run_logs/run_ui 等。",
    },

    # ── setup fixture ──
    "未知 repo_fixture": {
        "category": "setup",
        "needs_new_api": False,
        "missing_apis": [],
        "note": "非 API 问题。需预先创建测试仓并配置好 secrets/variables/branch_protection。",
    },
}


def main():
    v2_json = Path(__file__).resolve().parent / "classification_v2_detail.json"
    with open(v2_json, "r", encoding="utf-8") as f:
        cases = json.load(f)

    # ── 汇总每个 case 需要的缺失 API ──
    case_api_needs = {}  # case_id → list of missing APIs
    api_usage_count = defaultdict(int)  # missing_api → count of cases needing it

    for c in cases:
        cid = c["case_id"]
        needs = []
        for blocker in c["all_blockers"]:
            mapped = BLOCKER_API_MAP.get(blocker)
            if mapped is None:
                # 尝试前缀匹配
                for key, val in BLOCKER_API_MAP.items():
                    if blocker.startswith(key.split("：")[0]) or key.startswith(blocker.split("：")[0]):
                        mapped = val
                        break
            if mapped and mapped.get("needs_new_api"):
                for api in mapped.get("missing_apis", []):
                    needs.append(api)
                    api_usage_count[api] += 1
        if needs:
            case_api_needs[cid] = needs

    # ── 还需要但不在 Actions API 列表中的 ──
    lines = []
    lines.append("# Phase 02 所需但缺失的 API")
    lines.append("")
    lines.append(f"对照 `phase01/inputs/gitcode-api/api-reference.md`（20 个 Actions API + 4 个相邻 API hint），")
    lines.append(f"分析 {len(cases)} 个 case 的全部阻断项 → API 缺口。")
    lines.append("")

    # ── 结论摘要 ──
    lines.append("## 结论摘要：需要的新 API / 确认的端点")
    lines.append("")

    # 按类别分组
    lines.append("### 🔴 完全缺失的 API（api-reference 中无任何提及）")
    lines.append("")
    lines.append("| API | 用途 | 影响 case 数 |")
    lines.append("|-----|------|-------------|")
    for note in [
        ("`POST /api/v5/repos/:owner/:repo/forks`", "创建 fork", "13 (fork_pr trigger)"),
        ("`POST /api/v5/repos/:owner/:repo/pulls`", "创建 PR（pr/pull_request 触发）", "13 fork + 5 pr + 1 pull_request + 1 pull_request_target = 20"),
        ("`POST /api/v8/repos/:owner/:repo/actions/workflows/:workflow_id/dispatch`", "workflow_dispatch (manual 触发)", "5"),
        ("`POST /api/v5/repos/:owner/:repo/pulls/:number/comments`", "PR comment (pull_request_comment 触发)", "1"),
        ("`POST /api/v8/repos/:owner/:repo/actions/runs/:run_id/cancel`", "取消运行 (fault_injection kill_runner)", "2 (CHAOS cases)"),
    ]:
        lines.append(f"| {note[0]} | {note[1]} | {note[2]} |")
    lines.append("")

    lines.append("### 🟡 API 已存在但未集成到 assertion_engine")
    lines.append("")
    lines.append("| 已有 API | 当前用途 | 缺失的 assertion kind |")
    lines.append("|----------|----------|----------------------|")
    for note in [
        ("`GET .../actions/artifacts` + download", "只在 api-reference 中有，log_fetcher 未调用", "artifact 内容断言 (1 case)"),
        ("`GET .../actions/runners`", "只在 api-reference 中有，未集成", "runner_schedulable / runner_scheduling (3 cases)"),
        ("`POST /api/v2/.../actions/valid`", "validate_workflow.py 已实现，未入 assertion_engine", "workflow_validation (2 cases)"),
        ("`GET .../actions/runs/:id` (start_time/end_time)", "workflow_runner 已调用但不计算 duration", "run_duration (2 cases)"),
    ]:
        lines.append(f"| {note[0]} | {note[1]} | {note[2]} |")
    lines.append("")

    lines.append("### 🟢 非 API 问题（infra / 账号 / LLM / UI）")
    lines.append("")
    lines.append("| 阻断 | 数量 | 解决方式 |")
    lines.append("|------|------|---------|")
    for note in [
        ("`trigger.as=untrusted_contributor`", "17", "需第二 GitCode 账号 + OAuth token（非 API，是账号资源）"),
        ("`schedule` trigger", "5", "cron 无法按需触发；变通：push trigger + 手动设 ATOMGIT_EVENT_NAME=schedule"),
        ("`eval=llm_assisted`", "44", "需 LLM 集成到 assertion_engine（非 API）"),
        ("`target=run_ui / pr_ui`", "4", "需 Playwright 浏览器自动化（非 API）"),
        ("`target=badge_response`", "3", "HTTP GET badge URL，非 GitCode API，直接 curl 即可"),
        ("`fault_injection` / `network_partition` / `concurrent_flood`", "3+2", "需 infra 层能力（kill runner、断网、并发 flood）"),
        ("`setup.repo_fixture` 未知", "~18", "需预先创建配置好的测试仓"),
    ]:
        lines.append(f"| {note[0]} | {note[1]} | {note[2]} |")
    lines.append("")

    # ── 按 case 明细 ──
    lines.append("## 按 Case 明细：哪些 case 需要什么 API")
    lines.append("")

    # 按缺失 API 分组
    by_api = defaultdict(list)
    for cid, apis in case_api_needs.items():
        for api in apis:
            api_short = api.split("—")[0].strip()
            by_api[api_short].append(cid)

    for api_short in sorted(by_api.keys(), key=lambda k: -len(by_api[k])):
        cids = by_api[api_short]
        lines.append(f"### `{api_short}` ({len(cids)} cases)")
        lines.append("")
        for cid in sorted(cids):
            lines.append(f"- {cid}")
        lines.append("")

    out_path = Path(__file__).resolve().parent / "api_gap_analysis.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] {out_path}")


if __name__ == "__main__":
    main()
