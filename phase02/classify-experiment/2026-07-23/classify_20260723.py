#!/usr/bin/env python3
"""Generate classification report for 2026-07-23 VALID cases."""
import yaml, sys, json
from pathlib import Path
from collections import defaultdict

YAML_DIR = Path(__file__).resolve().parent / "VALID"
OUT_DIR = Path(__file__).resolve().parent

TRIGGER_SCRIPTABLE = {"push"}        # API works + platform fires trigger
TRIGGER_API_READY  = {"pull_request", "pull_request_target", "fork_pr",
                      "issue_comment", "pull_request_comment"}
                                     # API calls verified, platform does NOT fire
TRIGGER_WORKAROUND = {"schedule"}    # Needs cron push + wait (non-deterministic)
TRIGGER_UNTESTED  = {"manual", "workflow_dispatch", "tag"}
                                     # Not yet tested via API

ENGINE_KINDS = {"status", "run_status", "value", "leak", "mask", "config_probe"}
KNOWN_FIXTURES = {"basic-ci", "clean", "default", "with-secrets", "fork-target", "fork-source",
                  "environment-protected", "private-registry", "large-repo",
                  "runner-release", "badge-test"}

CLASS_LABELS = {
    "scriptable": "push trigger + 全部断言可映射",
    "api_blocked": "API 调用可行，平台不触发 (非代码问题)",
    "untested": "API 尚未验证可行性",
    "fixture_gap": "trigger 可触发但缺 repo fixture",
    "fault_gap": "需故障注入基础设施",
    "assertion_gap": "trigger 可触发但断言需新 kind",
}

SORT_ORDER = {"scriptable": 0, "assertion_gap": 1, "fixture_gap": 2, "fault_gap": 3, "untested": 4, "api_blocked": 5}
ICON = {"scriptable": "✓", "assertion_gap": "⬜", "fixture_gap": "⬜", "fault_gap": "⬜", "untested": "❓", "api_blocked": "✗"}


def classify_case(yf: Path) -> dict:
    with open(yf) as f:
        case = yaml.safe_load(f)

    cid = case.get("id", yf.stem)
    dim = case.get("dimension", "unknown")
    pri = case.get("priority", "?")
    title = case.get("title", "")
    trigger = case.get("trigger", {})
    event = trigger.get("event", "push")
    actor = trigger.get("as", "maintainer")
    setup = case.get("setup", {})
    fixture = setup.get("repo_fixture", "default")
    fi = case.get("fault_injection") or {}
    assertions = case.get("assertions", [])
    classified = "scriptable"
    all_blockers = []

    # Trigger analysis (post-demo: all API calls work, platform only fires push)
    if event in TRIGGER_SCRIPTABLE:
        trigger_ok = True
    elif event in TRIGGER_API_READY:
        trigger_ok = False
        all_blockers.append(f"trigger {event}: API works, platform does NOT fire trigger")
    elif event in TRIGGER_WORKAROUND:
        trigger_ok = False
        all_blockers.append(f"trigger {event}: needs cron push + wait (non-deterministic)")
    elif event in TRIGGER_UNTESTED:
        trigger_ok = False
        all_blockers.append(f"trigger {event}: API not yet tested")
    else:
        trigger_ok = False
        all_blockers.append(f"trigger {event}: unknown/unmapped trigger event")

    if actor == "untrusted_contributor" and trigger_ok:
        all_blockers.append("trigger.as=untrusted_contributor: needs second account token")

    # Setup analysis
    if fixture not in KNOWN_FIXTURES:
        all_blockers.append(f"unknown repo_fixture '{fixture}'")

    # Fault injection
    if fi and fi.get("action"):
        acts = fi.get("action", "")
        all_blockers.append(f"fault_injection.action={acts}")

    # Assertion analysis
    assertion_details = []
    assertions_mappable = 0
    assertions_llm = 0
    assertions_unmappable = 0

    for ai, a in enumerate(assertions):
        targets = a.get("target", a.get("targets", ""))
        if isinstance(targets, str):
            targets = [targets]
        evals = a.get("eval", a.get("evaluation", "deterministic"))
        if isinstance(evals, str):
            evals = [evals] * len(targets)

        for ti, t in enumerate(targets):
            ev = evals[min(ti, len(evals) - 1)] if evals else "deterministic"
            kind = None
            desc = ""

            if ev == "llm_assisted":
                kind = "llm"
                desc = "LLM辅助"
                assertions_llm += 1

            elif t in ("run_logs",):
                if a.get("contains"):
                    kind = "value"
                    desc = f"contains='{a['contains']}'"
                elif a.get("must_not_contain"):
                    kind = "leak"
                    desc = f"must_not_contain='{a['must_not_contain']}'"
                else:
                    kind = "value"
                    desc = "run_logs (implicit value)"
            elif t in ("run_status", "job_status", "step_status"):
                if a.get("equals"):
                    kind = "run_status"
                    desc = f"equals='{a['equals']}'"
                else:
                    kind = "status"
                    desc = "status check"
            elif t == "error_message":
                if ev == "llm_assisted":
                    kind = "llm"
                    desc = "error message LLM"
                    assertions_llm += 1
                else:
                    kind = None
                    desc = "error_message (unmappable)"
            elif t in ("run_ui", "pr_ui"):
                kind = "run_ui"
                desc = "needs Playwright"
            elif t in ("runner_schedulable", "runner_scheduling"):
                kind = "runner_schedulable"
                desc = "needs runner API assertion kind"
            elif t == "run_duration":
                kind = "run_duration"
                desc = "needs duration assertion kind"
            elif t == "step_summary":
                kind = "step_summary"
                desc = "needs step summary assertion kind"
            elif t == "workflow_validation":
                kind = "workflow_validation"
                desc = "needs workflow validation assertion kind"
            elif t in ("badge_response",):
                kind = "badge_response"
                desc = "needs badge HTTP assertion kind"
            elif t in ("artifacts", "artifact_available", "artifact_content", "artifact_download", "artifact_state"):
                kind = "artifacts"
                desc = "needs artifact assertion kind"
            elif t in ("cache_step", "cache_restore", "cache_pollution", "main_cache_content", "latest_cache_status", "oldest_cache_status"):
                kind = "cache"
                desc = "needs cache assertion kind"
            elif t in ("upload_status", "download_status", "download_content", "md5_match", "hash_match", "upload_time_seconds", "download_time_seconds"):
                kind = "artifact_ops"
                desc = "needs artifact operation assertion kind"
            elif t in ("workflow_parse", "workflow_discovery", "yaml_validation", "workflow_status"):
                kind = "workflow_validation"
                desc = "needs workflow validation kind"
            elif t in ("run_event", "run_created", "run_file_path", "run_step_result", "run_status_sequence"):
                kind = "run_detail"
                desc = "needs run detail assertion kind"
            elif t in ("rerun_result", "rerun_context", "rerun_request", "rerun_count"):
                kind = "rerun"
                desc = "needs rerun assertion kind"
            elif t in ("parent_status", "downstream_status", "job_a_status", "job_b_status",
                       "created_runs_count", "completed_jobs_count", "generated_jobs_count",
                       "max_concurrent_jobs", "cancelled_jobs_count", "completed_count"):
                kind = "job_status"
                desc = "needs job-level status assertion kind"
            elif t in ("log_integrity", "log_line_count", "log_order"):
                kind = "log_detail"
                desc = "needs log detail assertion kind"
            elif t in ("resource_ratio", "max_concurrent_jobs", "max_running_count", "queued_count", "total_duration_seconds"):
                kind = "resource_metric"
                desc = "needs resource metric assertion kind"
            elif t in ("http_200_ratio", "http_error_codes", "response_time_p95_seconds", "api_status"):
                kind = "http_metric"
                desc = "needs HTTP metric assertion kind"
            elif t in ("success_rate", "speedup_ratio", "restore_time_seconds", "job_duration_seconds",
                       "job_duration_minutes", "image_pull_time_seconds", "cleanup_step_status",
                       "heartbeat_interval_seconds", "scheduling_latency_seconds",
                       "queued_to_running_latency", "queued_to_running_minutes", "queued_delay_ratio",
                       "max_queued_to_running_seconds", "avg_queued_to_running_seconds",
                       "max_queued_time_seconds", "p95_latency_seconds", "p50_latency_seconds",
                       "startup_time_diff_seconds", "state_sequence", "idle_to_running_seconds",
                       "running_to_idle_seconds", "step_output_length"):
                kind = "metric"
                desc = "needs metric assertion kind"
            elif t in ("pod_count", "reachable_status", "unreachable_timeout_seconds"):
                kind = "infra"
                desc = "needs infra assertion kind"
            elif t in ("runner_label", "runner_spec"):
                kind = "runner_spec"
                desc = "needs runner spec assertion kind"
            elif t in ("cancel_queued_status", "cancel_running_status", "cancel_post_main_status", "cancel_stabilization_seconds"):
                kind = "cancel"
                desc = "needs cancel assertion kind"
            elif t in ("failure_attribution",):
                kind = "failure_attribution"
                desc = "needs failure attribution kind"
            elif t in ("platform_docs", "error_stack", "documentation"):
                kind = "doc"
                desc = "needs doc check kind"
            elif t in ("download_day90_status", "download_day91_status"):
                kind = "artifact_expiry"
                desc = "needs artifact expiry check kind"
            elif t == "step_summary_html":
                kind = "step_summary_html"
                desc = "needs HTML parse kind"
            else:
                kind = None
                desc = f"unmapped target='{t}'"

            assertion_details.append({
                "index": ai, "type": a.get("type", ""), "target": t, "eval": ev,
                "kind": kind, "desc": desc,
            })

            if kind and kind in ENGINE_KINDS:
                assertions_mappable += 1
            elif kind and kind not in ENGINE_KINDS:
                assertions_unmappable += 1
            elif not kind:
                assertions_unmappable += 1

    # Set classification (post-demo: all API calls proven, platform blocks non-push)
    if event in TRIGGER_UNTESTED:
        classified = "untested"
    elif event in TRIGGER_API_READY or event in TRIGGER_WORKAROUND:
        classified = "api_blocked"
    else:
        classified = "scriptable"
    # Fixture issues
    if any("unknown repo_fixture" in b for b in all_blockers):
        if classified == "scriptable":
            classified = "fixture_gap"
    # Fault injection
    if fi and fi.get("action") and classified == "scriptable":
        classified = "fault_gap"
    # Assertion issues
    if assertions_llm > 0 and assertions_mappable == 0 and classified == "scriptable":
        classified = "assertion_gap"
    if assertions_unmappable > 0 and assertions_mappable == 0 and classified == "scriptable":
        classified = "assertion_gap"

    return {
        "case_id": cid, "dimension": dim, "priority": pri, "title": title,
        "classification": classified, "all_blockers": all_blockers,
        "trigger_ok": trigger_ok, "assertions_mappable": assertions_mappable,
        "assertions_llm": assertions_llm, "assertions_unmappable": assertions_unmappable,
        "assertions_total": len(assertions),
        "assertion_details": assertion_details,
    }


def generate_report(results, out_dir):
    stats = defaultdict(lambda: defaultdict(int))
    for r in results:
        stats[r['dimension']][r['classification']] += 1
        stats['__total__'][r['classification']] += 1

    total = len(results)

    lines = []
    lines.append("# Case 可脚本化分类报告 — 2026-07-23 VALID")
    lines.append("")
    lines.append(f"**数据源**: `phase02/classify-experiment/2026-07-23/VALID/` (平台校验通过的 cases)")
    lines.append(f"**分类规则**: `phase02/classify-experiment/quick-start.md` (基于 demo 实测)")
    lines.append("")
    lines.append("## 总体统计")
    lines.append("")
    lines.append(f"| 分类 | 数量 | 占比 | 含义 |")
    lines.append(f"|------|------|------|------|")
    for label, meaning in CLASS_LABELS.items():
        cnt = stats['__total__'].get(label, 0)
        lines.append(f"| `{label}` | **{cnt}** | {cnt/total*100:.1f}% | {meaning} |")
    lines.append("")

    dims = ['completeness', 'compatibility', 'reliability', 'security', 'usability']
    lines.append("## 按维度 × 分类")
    lines.append("")
    labels_order = list(CLASS_LABELS.keys())
    lines.append("| 维度 | " + " | ".join(labels_order) + " | 合计 |")
    lines.append("|------" + "|------" * len(labels_order) + "|------|")
    for dim in dims:
        cols = [str(stats[dim].get(l, 0)) for l in labels_order]
        lines.append(f"| {dim} | " + " | ".join(cols) + f" | {sum(int(c) for c in cols)} |")
    totals = [str(stats['__total__'].get(l, 0)) for l in labels_order]
    grand = sum(int(t) for t in totals)
    lines.append(f"| **合计** | " + " | **" + " | **".join(totals) + f"** | **{grand}** |")
    lines.append("")

    # Blocker summary
    blocker_cases = defaultdict(set)
    for r in results:
        for b in r['all_blockers']:
            blocker_cases[b].add(r['case_id'])

    lines.append("---")
    lines.append("")
    lines.append("## 阻断项汇总（按唯一 case 去重）")
    lines.append("")

    categories = {
        "Trigger 阻断": ["trigger", "trigger.as"],
        "New assertion kind 需要": [],
        "Fault injection": ["fault_injection"],
        "Repo fixture 未知": ["unknown repo_fixture"],
    }

    lines.append("### Trigger 层")
    lines.append("")
    lines.append("| 阻断 | Cases | 说明 |")
    lines.append("|------|-------|------|")
    for b, cases in sorted(blocker_cases.items(), key=lambda x: -len(x[1])):
        if "trigger" in b.lower():
            # 标注是否为 api_blocked
            note = ""
            if "API works, platform does NOT fire" in b:
                note = " (API 已打通，平台不触发)"
            elif "needs cron" in b:
                note = " (cron push + wait 可行)"
            elif "API not yet tested" in b:
                note = " (待 API 验证)"
            lines.append(f"| {b} | {len(cases)} |{note}")
    lines.append("")

    lines.append("### 断言层 — 需新 assertion kind")
    lines.append("")
    new_kind_cases = defaultdict(set)
    for r in results:
        for ad in r['assertion_details']:
            kind = ad.get('kind', '')
            if kind and kind not in ENGINE_KINDS and kind != "llm":
                new_kind_cases[kind].add(r['case_id'])

    lines.append("| 新 assertion kind | Cases | 示例 target |")
    lines.append("|------|-------|------|")
    for kind, cases in sorted(new_kind_cases.items(), key=lambda x: -len(x[1])):
        sample = ""
        for r in results:
            if r['case_id'] in cases:
                for ad in r['assertion_details']:
                    if ad.get('kind') == kind:
                        sample = ad.get('target', '')
                        break
                if sample:
                    break
        lines.append(f"| `{kind}` | {len(cases)} | `{sample}` |")
    lines.append("")

    lines.append("### 断言层 — LLM 辅助判定")
    llm_count = len([r for r in results if r['assertions_llm'] > 0])
    lines.append(f"- {llm_count} cases 包含 `eval=llm_assisted` 断言")
    lines.append("")

    lines.append("### 其他")
    lines.append("")
    lines.append("| 阻断 | Cases |")
    lines.append("|------|-------|")
    for b, cases in sorted(blocker_cases.items(), key=lambda x: -len(x[1])):
        if "trigger" not in b.lower() and "fault" not in b.lower() and "repo_fixture" not in b.lower():
            lines.append(f"| {b} | {len(cases)} |")
    lines.append("")

    # Per-case detail
    lines.append("---")
    lines.append("")
    lines.append("## 逐 Case 明细")
    lines.append("")

    for r in sorted(results, key=lambda x: (
        SORT_ORDER.get(x['classification'], 99),
        x['case_id'])):
        icon = ICON.get(r['classification'], "?")
        lines.append(f"### {icon} {r['case_id']} — {r['classification']}")
        lines.append(f"- 维度: {r['dimension']} | 优先级: {r['priority']}")
        lines.append(f"- 标题: {r['title']}")
        lines.append(f"- Trigger: {'OK' if r['trigger_ok'] else 'BLOCKED'}")
        lines.append(f"- 断言: {r['assertions_total']} total / {r['assertions_mappable']} mappable / {r['assertions_llm']} LLM / {r['assertions_unmappable']} unmappable")
        if r['all_blockers']:
            lines.append(f"- 阻断项:")
            for b in r['all_blockers']:
                lines.append(f"  - {b}")
        # Show assertion details
        for ad in r['assertion_details']:
            status = "✅" if (ad['kind'] and ad['kind'] in ENGINE_KINDS) else ("🤖" if ad['kind'] == 'llm' else "⬜" if ad['kind'] else "❌")
            lines.append(f"  {status} [{ad['index']}] type={ad['type']} target={ad['target']} eval={ad['eval']} → {ad['desc']}")
        lines.append("")

    md_path = out_dir / "classification_report.md"
    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    print(f"[OK] {md_path} ({len(lines)} lines)")
    return md_path


def main():
    import sys
    src = YAML_DIR
    yaml_files = sorted(src.glob("*.yaml"))
    print(f"Classifying {len(yaml_files)} cases from {src}...")
    results = [classify_case(yf) for yf in yaml_files]
    generate_report(results, OUT_DIR)


if __name__ == "__main__":
    main()
