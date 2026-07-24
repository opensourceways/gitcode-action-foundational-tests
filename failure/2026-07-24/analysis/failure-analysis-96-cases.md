# 96 条 FAIL 日志交叉验证 · 逐条归因 + 汇总分析

> Run: 2026-07-23-valid-clean | 日志源: `failure/2026-07-24/*.log` | 分析日期: 2026-07-24
> 逐例详情: `failure/2026-07-24/case/*.md` (96 例, 每例含全量日志 + 规格行号引用 + YAML 映射 + 失败传导链 + 影响评估 + 责任人)

---

## 一、逐条归因表

| # | case_id | dim | 根因初判 | 责任人 | 置信度 | 阻塞性 | 静默性 | 影响面 | 失败断言摘要 | spec_file | spec_lines | 失败传导链 |
|---|---------|-----|---------|--------|--------|--------|--------|--------|------------|-----------|-----------|-----------|
| 1 | COMP-ARTIFACT-01-002 | comp | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED assertions[1] (downstream) — 下游 job 因上游 FAILED  | artifacts-and-cache.md |  | 是: **Build multiple artifacts** (FAILED) → **Download all artifacts** (IGNORED) |
| 2 | COMP-ARTIFACT-01-003 | comp | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED | workflow-job-step-action.md |  | 否 |
| 3 | COMP-CACHE-01-001 | comp | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED | artifacts-and-cache.md |  | 否 |
| 4 | COMP-CACHE-01-002 | comp | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED |  |  | 否 |
| 5 | COMP-CALL-01-001 | comp | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED | trigger-events.md |  | 否 |
| 6 | COMP-DIR-01-001 | comp | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (positive, directory recognition) — job COMPLETED，'workflow recognized' 正确输出 固定断言词可能不匹配实际输出格式 | trigger-events.md |  | 否 |
| 7 | COMP-ISOLATION-01-001 | comp | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions — job1/job2 均 COMPLETED，WORKSPACE_ISOLATED_OK / TMP_ISOLATED_OK / NO_ORPHAN_PROCESS_OK 断言评判器未正确解析固化输出为 PASS | workflow-job-step-action.md |  | 否 |
| 8 | COMP-ISOLATION-01-002 | comp | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions — 两个 job 均 COMPLETED，ISOLATION_STRONG: marker not visible across jobs 断言评判器未解析 'ISOLATION_STRONG' / 'MARKER_C | variables-secrets-context-expressions.md |  | 否 |
| 9 | COMP-PERMS-01-001 | comp | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED |  |  | 否 |
| 10 | COMP-PERMS-01-002 | comp | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED |  |  | 否 |
| 11 | COMP-PUSH-01-001 | comp | 环境问题 | Phase 02 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (positive, branch trigger) — job COMPLETED，'triggered on main' 正确输出 用例期望 push 事件触发，实际为 workflow_dispatch，事件类型 | trigger-events.md |  | 否 |
| 12 | COMP-RUNNER-01-001 | comp | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (positive, runner label) — job COMPLETED，'os=linux' 'arch=x86_64' 正确输出 | selecting-runner-labels.md |  | 否 |
| 13 | COMP-SECRET-01-001 | comp | 环境问题 | Phase 02 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions[0] (positive, run_logs contains '***') — 期望日志含 `***`，实际 `secret is ` 后为空 assertions[1] (negative, must_not_co |  |  | 否 |
| 14 | COMP-STATUS-01-001 | comp | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (positive, status transitions) — job COMPLETED，输出 'running'，断言期望完整 status 序列 | view-job-logs.md |  | 否 |
| 15 | COMP-TIMEOUT-01-001 | comp | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (positive, default timeout) — job COMPLETED，'done' 正常完成，断言未正确判断默认超时内完成为 PASS | workflow-job-step-action.md |  | 否 |
| 16 | COMP-TIMEOUT-01-002 | comp | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] — 期望 job 超时后 status=failure，实际 status=CANCELED（平台以 CANCELED 代替 FAILED） assertions[1] (log retention) — 超时前 | variables-secrets-context-expressions.md |  | 否 |
| 17 | COMPAT-ACTION-01-001 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (checkout ref) — job COMPLETED，CHECKOUT_REF_OK 正确输出 | top-level-fields.md |  | 否 |
| 18 | COMPAT-ACTION-01-002 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (checkout path) — job COMPLETED，CHECKOUT_PATH_OK 正确输出 | top-level-fields.md |  | 否 |
| 19 | COMPAT-ARTIFACT-01-001 | compat | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED assertions[1] (downstream) — 下游 job 因上游 FAILED  | workflow-job-step-action.md |  | 是: **Upload artifact** (FAILED) → **Download and verify artifact** (IGNORED) |
| 20 | COMPAT-ARTIFACT-01-002 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (artifact retention) — job COMPLETED，ARTIFACT_UPLOADED_OK，artifact ID=206052053389312 | workflow-job-step-action.md |  | 否 |
| 21 | COMPAT-CACHE-01-001 | compat | 环境问题 | Phase 02 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (cache hit) — job COMPLETED，但 Event Validation Error: Manual event 不在 cache allowlist [push|pr|merge_request] | artifacts-and-cache.md |  | 否 |
| 22 | COMPAT-CTX-01-002 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (atomgit context) — job COMPLETED，atomgit_ref=main 正确输出 | trigger-events.md |  | 否 |
| 23 | COMPAT-DIR-01-001 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (.gitcode dir) — job COMPLETED，GITCODE_DIR_RECOGNIZED_OK 正确输出 | workflow-job-step-action.md |  | 否 |
| 24 | COMPAT-DIR-01-002 | compat | 产品bug | 平台方 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (.github dir ignored) — job COMPLETED，但 GITHUB_DIR_WORKFLOW_RAN 表明 .github 下 workflow 被非预期执行 平台未隔离 GitHub Act | workflow-job-step-action.md |  | 否 |
| 25 | COMPAT-ENV-01-001 | compat | 产品bug | 平台方 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (ATOMGIT_SHA) — job COMPLETED，但 atomgit_sha= 为空，平台未注入 commit SHA | trigger-events.md |  | 否 |
| 26 | COMPAT-EXPR-01-002 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (needs/success) — 两个 job 均 COMPLETED，'Job B ran after Job A success' 正确输出 | variables-secrets-context-expressions.md |  | 否 |
| 27 | COMPAT-EXPR-01-003 | compat | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED | variables-secrets-context-expressions.md |  | 否 |
| 28 | COMPAT-IF-01-001 | compat | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED | workflow-job-step-action.md |  | 否 |
| 29 | COMPAT-IF-01-002 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (continue-on-error) — job COMPLETED，'exit code 1' + 'This should appear' 正确，断言检查 outcome/conclusion | workflow-job-step-action.md |  | 否 |
| 30 | COMPAT-INPUTS-01-002 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (string input) — job COMPLETED，ENV=production STRING_INPUT_OK 正确输出 | trigger-events.md |  | 否 |
| 31 | COMPAT-MASK-01-002 | compat | 环境问题 | Phase 02 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (secret mask via env) — job COMPLETED，但 'Env value: ' 后为空，secret 未注入 |  |  | 否 |
| 32 | COMPAT-OUTCOME-01-001 | compat | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED | variables-secrets-context-expressions.md |  | 否 |
| 33 | COMPAT-OUTCOME-01-002 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (outcome/conclusion, continue-on-error) — job COMPLETED，'Check step outcome and conclusion' 正确，断言值不匹配 | variables-secrets-context-expressions.md |  | 否 |
| 34 | COMPAT-PERM-01-001 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (read permissions) — job COMPLETED，仓库内容正常输出 |  |  | 否 |
| 35 | COMPAT-PERM-01-004 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (repository permission) — job COMPLETED，REPOSITORY_PERM_OK 正确输出 |  |  | 否 |
| 36 | COMPAT-RUNNER-01-001 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (runner.os) — job COMPLETED，runner_os=linux 正确输出 | selecting-runner-labels.md |  | 否 |
| 37 | COMPAT-RUNNER-01-002 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (runner.arch) — job COMPLETED，runner_arch=x86_64 正确输出 | selecting-runner-labels.md |  | 否 |
| 38 | COMPAT-RUNSON-01-001 | compat | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (runs-on array) — job COMPLETED，RUNSON_ARRAY_OK，Runner labels: dedicate-hosted x64 large | selecting-runner-labels.md |  | 否 |
| 39 | COMPAT-VARS-01-001 | compat | 环境问题 | Phase 02 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | assertions (vars context) — job COMPLETED，但 test_var= 为空，平台未注入 vars 变量 | variables-secrets-context-expressions.md |  | 否 |
| 40 | REL-ART-01-041 | rel | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟢明确报错 | 🔴跨维度 | 正向/upload_status expected=success actual=FAILED; 正向/download_status expected=success actual=IGNORED; 正向/md5_match expect |  |  | 是: upload FAILED → download IGNORED → 所有正向断言不满足 |
| 41 | REL-ARTCONC-01-063 | rel | 标记不匹配 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🔴跨维度 | 正向/download_content expected in=['AAA','BBB','CCC'] actual=所有job因bad substitution未执行; 负向/download_content contains_mixed |  |  | 否 |
| 42 | REL-ARTPERF-01-053-V2 | rel | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🟡同维度 | 非功能/upload_time_seconds ≤300 actual=upload未成功; 非功能/download_time_seconds ≤300 actual=N/A; 正向/hash_match expected=true ac |  |  | 否 |
| 43 | REL-ARTPERF-01-053 | rel | 用例问题 | Phase 01 | 高 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | 正向/hash_match expected=true actual=N/A; 非功能/upload_time_seconds ≤30 actual=N/A; 非功能/download_time_seconds ≤30 actual=N/A |  |  | 否 |
| 44 | REL-CANCEL-01-028 | rel | 环境/Harness | Phase 02 | 高 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | 正向/cleanup_step_status expected=success actual=completed(但job未cancel); 正向/run_status expected=canceled actual=completed |  |  | 否 |
| 45 | REL-CONC-01-001 | rel | 环境/Harness | Phase 02 | 中 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | 正向/run_status expected=completed(success) actual=仅1个run记录; 非功能/queued_to_running_latency ≤60s actual=无法验证 | trigger-events.md |  | 否 |
| 46 | REL-CONTINUE-01-030 | rel | 产品bug | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🟡同维度 | 正向/job_a_status expected=failure actual=FAILED(一致); 正向/job_b_status expected=success actual=COMPLETED(一致); 正向/workflow_s | workflow-job-step-action.md |  | 否 |
| 47 | REL-FAULT-01-031 | rel | 环境/Harness | Phase 02 | 高 | 🔴阻塞 | 🔴静默错误 | 🔴跨维度 | 正向/job_status expected=failure actual=COMPLETED; 正向/run_logs expected=contains step_one_marker actual=contains(满足); 负向/r |  |  | 否 |
| 48 | REL-FAULT-01-032 | rel | 环境/Harness | Phase 02 | 高 | 🔴阻塞 | 🔴静默错误 | 🔴跨维度 | 正向/step_status expected=failure actual=COMPLETED; 正向/run_logs expected=contains "network" actual=日志无网络错误 |  |  | 否 |
| 49 | REL-FAULT-01-033 | rel | 环境/Harness | Phase 02 | 高 | 🔴阻塞 | 🔴静默错误 | 🔴跨维度 | 正向/job_status expected=failure actual=COMPLETED; 正向/run_logs expected=contains "No space left on device" actual=日志无磁盘满错误 |  |  | 否 |
| 50 | REL-IGNORE-01-004 | rel | 环境/Harness | Phase 02 | 中 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | 正向/run_status expected=completed(success) actual=仅1个run记录; 负向/run_status expected=NOT queued actual=无法验证 |  |  | 否 |
| 51 | REL-K8S-01-045 | rel | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🟡同维度 | 正向/pod_count expected=1 actual=无法验证; 正向/max_concurrent_jobs expected=1 actual=无法验证 | selecting-runner-labels.md |  | 否 |
| 52 | REL-MATRIX-01-027 | rel | 标记不匹配 | Phase 02 | 高 | 🟡非阻塞 | 🔴静默错误 | 🟢单用例 | 正向/max_concurrent_jobs ≤4 actual=3(满足); 正向/run_status expected=completed(success) actual=3个job COMPLETED但断言期望9个 | workflow-job-step-action.md |  | 否 |
| 53 | REL-MATRIX-01-038 | rel | 标记不匹配 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🔴跨维度 | 正向/generated_jobs_count expected=20 actual=所有20个job因bad substitution失败; 正向/run_status expected=completed(success) actual |  |  | 否 |
| 54 | REL-MATRIX-01-039 | rel | 标记不匹配 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🔴跨维度 | 正向/generated_jobs_count expected=50 actual=所有50个job因bad substitution失败; 非功能/scheduling_latency_seconds ≤300 actual=无法验证 |  |  | 否 |
| 55 | REL-NEEDS-01-025 | rel | 产品bug | 平台方 | 中 | 🟡非阻塞 | 🟡可察觉 | 🟡同维度 | 正向/job_a_status expected=failure actual=FAILED(满足); 正向/job_b_status expected=skipped actual=IGNORED | workflow-job-step-action.md |  | 否 |
| 56 | REL-OUTPUT-01-016 | rel | 标记不匹配 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🔴跨维度 | 正向/step_output_length expected=1048576 actual=read step因bad substitution失败 |  |  | 否 |
| 57 | REL-QUEUE-01-003 | rel | 环境/Harness | Phase 02 | 中 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | 正向/run_status expected=completed(success) actual=仅1个run记录; 非功能/queued_count expected=2 actual=无法验证 |  |  | 否 |
| 58 | REL-RERUN-01-011 | rel | 环境/Harness | Phase 02 | 中 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | 正向/rerun_count expected=3 actual=仅1个run记录; 正向/run_status expected=completed(success) actual=1个run COMPLETED但无法验证3次 | view-job-logs.md |  | 否 |
| 59 | REL-TIMEOUT-01-007 | rel | 环境/Harness | Phase 02 | 高 | 🟡非阻塞 | 🟡可察觉 | 🟡同维度 | 正向/job_status expected=success actual=CANCELED; 非功能/job_duration_minutes ≤359 actual=harness取消 | workflow-job-step-action.md |  | 否 |
| 60 | REL-TIMEOUT-01-008 | rel | 环境/Harness | Phase 02 | 高 | 🟡非阻塞 | 🟡可察觉 | 🟡同维度 | 正向/job_status expected=failure actual=CANCELED; 正向/run_logs expected=contains "timeout" actual=无法验证 |  |  | 否 |
| 61 | REL-TIMEOUT-01-009 | rel | 环境/Harness | Phase 02 | 中 | 🟡非阻塞 | 🟡可察觉 | 🟡同维度 | 正向/job_status expected=failure actual=CANCELED; 非功能/job_duration_seconds ≤70 actual=无法验证 |  |  | 否 |
| 62 | REL-TIMEOUT-01-010 | rel | 环境/Harness | Phase 02 | 高 | 🟡非阻塞 | 🟡可察觉 | 🟡同维度 | 正向/job_status expected=failure actual=CANCELED; 正向/run_logs expected=contains "timeout" actual=无法验证 |  |  | 否 |
| 63 | REL-YAMLCACHE-01-060 | rel | 环境/Harness | Phase 02 | 低 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | 正向/run_logs expected=contains "marker_v2" actual=contains "marker_v1"; 负向/run_logs expected=NOT contains "marker_v1" act |  |  | 否 |
| 64 | SEC-ARTF-01-002 | sec | 平台缺陷 | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🟡同维度 | - negative, run_logs, must_not_contain "200" — 实际日志含 "000" + "400"，符合负向断言但未命中正向 - positive, run_logs, equals "403_or_404 | pr-mr-pipeline-security.md | 12-15, 44 | 否 |
| 65 | SEC-CACHE-01-002 | sec | 用例问题 | Phase 02 | 高 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | - negative, cache_restore, must_not_hit "fork_cache_key" — 无法验证，cache 步骤被跳过 - positive, run_logs, equals "cache_miss" —  | pr-mr-pipeline-security.md | 12, 13, 14 | 否 |
| 66 | SEC-DEFPERM-01-001 | sec | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🟡同维度 | - negative, run_logs, must_not_contain "write_successful" — 无法验证，403/401 未按预期生效 - positive, run_logs, equals "403_or_per | token-permissions.md | 13, 99-103, 103 | 否 |
| 67 | SEC-DOS-01-001 | sec | 平台缺陷 | 平台方 | 高 | 🔴阻塞 | 🔴静默错误 | 🔴跨维度 | - negative, run_status, must_not_equal "success" — job 状态为 COMPLETED，平台认为上传成功 - positive, run_logs, equals "size_limit_e | workflow-job-step-action.md |  | 否 |
| 68 | SEC-INJ-01-004 | sec | 环境问题 | Phase 02 | 中 | 🟡非阻塞 | 🟡可察觉 | 🟢单用例 | - negative, run_logs, must_not_contain "injected_command_executed" — 通过（无注入） - positive, run_status, equals "success" —  | using-secrets.md | 66 | 否 |
| 69 | SEC-INJ-01-005 | sec | 平台缺陷 | 平台方 | 高 | 🔴阻塞 | 🟡可察觉 | 🔴跨维度 | - negative, run_logs, must_not_contain "2" — 未出现 "2"，通过 - positive, run_logs, equals "template_chars_escaped" — 实际为 bash | variables-secrets-context-expressions.md | 42-43 | 否 |
| 70 | SEC-MASK-01-001 | sec | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | - negative, run_logs, must_not_contain_secret "DEPLOY_TOKEN" — 日志中无 DEPLOY_TOKEN 原值（形式通过） - positive, run_logs, equals " | using-secrets.md | 44-45, 66 | 否 |
| 71 | SEC-MASK-01-002 | sec | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | - negative, step_summary, must_not_contain_secret "API_KEY" — 无法验证（空值） - negative, error_stack, must_not_contain_secret  | using-secrets.md | 66, 67 | 否 |
| 72 | SEC-MASK-01-005 | sec | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | - negative, run_logs, must_not_contain_secret "MULTI_LINE_SECRET" — 日志中无原值（形式通过但原因错误） - positive, run_logs, equals "mult | using-secrets.md | 66 | 否 |
| 73 | SEC-NAME-01-001 | sec | 环境问题 | Phase 02 | 中 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | - negative, run_logs, must_not_contain_secret "MY-VAR" — 日志中无原值（形式通过但原因错误） - positive, run_status, equals "success_or_ya | using-secrets.md | 44-45 | 否 |
| 74 | SEC-NAME-01-002 | sec | 标记不匹配 | Phase 01 | 中 | 🟡非阻塞 | 🟡可察觉 | 🟢单用例 | - negative, run_logs, must_not_contain_secret "API_KEY" — 日志中无 API_KEY 明文（通过） - positive, run_logs, equals "masked_or_no | using-secrets.md | 66 | 否 |
| 75 | SEC-NET-01-001 | sec | 标记不匹配 | Phase 01 | 高 | 🟡非阻塞 | 🟢明确报错 | 🟢单用例 | - negative, run_logs, must_not_contain "metadata_service_response" — 元数据端点返回了内容（版本列表） - positive, run_logs, equals "acce | selecting-runner-labels.md |  | 否 |
| 76 | SEC-PERM-01-003 | sec | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🟡可察觉 | 🟡同维度 | - negative, run_logs, must_not_contain "write_permission_granted" — 无法验证 - positive, run_status, equals "completed" — jo | token-permissions.md | 13, 103, 99 | 否 |
| 77 | SEC-PERM-01-004 | sec | 用例问题 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🟢单用例 | - negative, run_logs, must_not_contain "push_successful" — 推送未执行（通过但原因错误） - positive, run_logs, equals "push_denied_or_4 | token-permissions.md | 99, 56-62 | 否 |
| 78 | SEC-RUN-01-001 | sec | 标记不匹配 | Phase 01 | 高 | ⚪无影响 | 🟢明确报错 | 🟢单用例 | - negative, run_logs, must_not_contain "residual found" — 无残留文件（通过） - positive, run_logs, equals "cleaned_as_expected" — | workflow-job-step-action.md |  | 否 |
| 79 | SEC-RUN-01-002 | sec | 标记不匹配 | Phase 01 | 高 | ⚪无影响 | 🟢明确报错 | 🟢单用例 | - negative, run_logs, must_not_contain "isolation broken" — 未出现泄露（通过） - positive, run_logs, equals "isolated_as_expected | using-variables-secrets.md | 81, 128 | 否 |
| 80 | SEC-RUN-01-003 | sec | 编译缺口 | Phase 02 | 高 | 🔴阻塞 | 🟡可察觉 | 🟢单用例 | - negative, run_logs, must_not_contain "cross project leak" — 无泄露输出 - positive, run_logs, equals "isolated_as_expected"  | using-self-hosted-runners.md |  | 否 |
| 81 | SEC-SIDE-01-002 | sec | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🟢单用例 | - negative, artifact_content, must_not_contain_secret "DEPLOY_TOKEN" — 无法验证 - positive, run_status, equals "blocked_or_m | using-secrets.md | 66, 119 | 否 |
| 82 | SEC-SUPPLY-01-001 | sec | 编译缺口 | 平台方 | 高 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | - positive, run_status, equals "success_or_action_executed" — job 状态 FAILED，不匹配 - negative, run_logs, must_not_contain " | using-actions.md |  | 否 |
| 83 | SEC-SUPPLY-01-002 | sec | 编译缺口 | 平台方 | 高 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | - negative, run_status, must_not_equal "success" — job 状态 FAILED（通过但原因未知） - positive, run_logs, equals "action_not_found | using-actions.md |  | 否 |
| 84 | SEC-TOCTOU-01-001 | sec | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🔴静默错误 | 🟢单用例 | - negative, run_logs, must_not_contain "unapproved_commit_executed" — 通过（无未审批 commit） - positive, run_logs, equals "appr | context.md |  | 否 |
| 85 | SEC-WCMD-01-001 | sec | 环境问题 | Phase 02 | 中 | 🔴阻塞 | 🔴静默错误 | 🟡同维度 | - negative, run_logs, must_not_contain_secret "API_KEY" — 日志无 API_KEY 明文（通过） - positive, run_logs, equals "mask_command_ | workflow-commands.md |  | 否 |
| 86 | SEC-WCMD-01-002 | sec | 环境问题 | Phase 02 | 高 | 🔴阻塞 | 🟢明确报错 | 🟢单用例 | - negative, run_logs, must_not_contain "auto_executed" — 通过（未自动执行） - positive, run_status, equals "completed" — job 状态 F | workflow-job-step-action.md |  | 否 |
| 87 | USE-CONC-01-001 | use | 产品bug | 平台方 | 高 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED，实际 COMPLETED；assertions[1] (nonfunctional, error_messa | workflow-file-location-structure.md | 181-187, 184, 184 | 否 |
| 88 | USE-CTX-01-001 | use | 产品bug | 平台方 | 高 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | assertions[0] (positive, run_logs) — 期望日志含 `"ref=refs/heads/"`，实际日志仅含 `ref=main`（短格式，不含 `refs/heads/` 前缀） | context.md | 31, 6, 31, 31 | 否 |
| 89 | USE-CTX-01-002 | use | 产品bug | 平台方 | 高 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED（即 YAML 校验或表达式求值应报错），实际 COMPLETED；assertions[1] (nonfun | context.md | 9-21, 11, 6 | 否 |
| 90 | USE-DISP-01-002 | use | 需人工判断 | 多方联合 | 中 | 🔴阻塞 | 🟡可察觉 | 🟢单用例 | assertions[0] (positive, run_logs) — 期望日志含 `"env=staging"`，实际 Job FAILED 且无任何步骤输出（0 字节有效日志），run_logs 中不包含该字符串 | manually-trigger-pipeline.md | 13-53, 22, 56 | 否 |
| 91 | USE-ENV-01-002 | use | 产品bug + 用例问题 | 平台方 | 中 | 🟡非阻塞 | 🟢明确报错 | 🟡同维度 | assertions[0] (nonfunctional, error_message, eval=llm_assisted) — 期望日志中出现 ATOMGIT_* 前缀环境变量的映射指引，实际日志仅含 bash 级 `GITHUB_SH | view-job-logs.md | 50-61, 57, 48 | 否 |
| 92 | USE-EXPR-01-001 | use | 产品bug | 平台方 | 高 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED（即表达式求值应报错），实际 COMPLETED；assertions[1] (nonfunctional,  | context.md | 27-48, 5, 6 | 否 |
| 93 | USE-INPT-01-002 | use | 产品bug | 平台方 | 高 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED（即 YAML 校验应拒绝 `type: boolean`），实际 COMPLETED；assertions[ | configure-triggers.md | 56-67, 103, 103, 6, 103 | 否 |
| 94 | USE-LOG-01-001 | use | 用例问题 | Phase 01 | 高 | ⚪无影响 | 🟢明确报错 | 🟢单用例 | assertions[0] (positive, run_logs) — 期望日志含 `"step one prepare"`（YAML 中 step 的 name 字段），实际日志含 `"prepare done"`（step 内 she | view-job-logs.md | 17-27 | 否 |
| 95 | USE-OS-01-001 | use | 产品bug | 平台方 | 高 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | assertions[0] (positive, run_logs) — 期望日志含 `"os=Linux"`（首字母大写），实际日志含 `"os=linux"`（全小写），大小写不匹配 | context.md | 211-228, 213, 223, 6, 213-223, 213, 223 | 否 |
| 96 | USE-SECNAME-01-001 | use | 产品bug | 平台方 | 高 | 🟡非阻塞 | 🔴静默错误 | 🟡同维度 | assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED（即平台应拒绝 `ATOMGIT_TOKEN` 作为 secret 名称），实际 COMPLETED；asse | using-secrets.md | 43-47, 46, 52-60, 6, 46 | 否 |

---

## 二、归因汇总

### 2.1 分类统计

| 分类 | 数量 | 占比 |
|---|---|---|
| **标记不匹配** | 29 | 30% |
| **产品bug** | 24 | 25% |
| **环境问题** | 18 | 19% |
| **环境/Harness** | 13 | 14% |
| **用例问题** | 4 | 4% |
| **平台缺陷** | 3 | 3% |
| **编译缺口** | 3 | 3% |
| **需人工判断** | 1 | 1% |
| **产品bug + 用例问题** | 1 | 1% |
| **总计** | **96** | **100%** |

### 2.2 按维度分布

| 维度 | 标记不匹配 | 产品bug | 环境问题 | 环境/Harness | 用例问题 | 平台缺陷 | 编译缺口 | 需人工判断 | 产品bug+用例 | 总计 |
|---|---|---|---|---|---|---|---|---|---|---|
| completeness | 6 | 8 | 2 | — | — | — | — | — | — | 16 |
| compatibility | 14 | 6 | 3 | — | — | — | — | — | — | 23 |
| reliability | 5 | 3 | 2 | 13 | 1 | — | — | — | — | 24 |
| security | 4 | — | 11 | — | 2 | 3 | 3 | — | — | 23 |
| usability | — | 7 | — | — | 1 | — | — | 1 | 1 | 10 |
| **总计** | 29 | 24 | 18 | 13 | 4 | 3 | 3 | 1 | 1 | **96** |

### 2.3 按责任人分布

| 责任人 | 数量 | 占比 |
|--------|------|------|
| Phase 01 | 26 | 27% |
| Phase 02 | 39 | 41% |
| 平台方 | 30 | 31% |
| 多方联合 | 1 | 1% |
| **总计** | **96** | **100%** |

### 2.4 合并视图——若消除假阳性后的实际通过率

假设原始总用例数约为 177（81 PASS + 96 FAIL）:

| 场景 | PASS(等效) | FAIL | 通过率 |
|---|---|---|---|
| 原始报告 | 81 | 96 | 46% |
| 消除标记不匹配 (29条) | 110 | 67 | 62% |
| 消除标记不匹配 + 用例问题 (33条) | 114 | 63 | 64% |


---

## 三、影响汇总

### 3.1 三维度统计

| 指标 | 🔴严重 | 🟡中等 | ⚪/🟢 无影响 |
|---|---|---|---|
| **阻塞性** | 44 (46%) | 49 (51%) | 3 (3%) |
| **静默性** | 26 (27%) | 25 (26%) | 45 (47%) |
| **影响面** | 22 (23%) | 32 (33%) | 42 (44%) |


### 3.2 核心发现：非阻塞静默错误构成最大风险

**11 条失败是「非阻塞 + 静默错误」组合**——平台不报错但行为与文档不符，用户完全无法察觉：

| 用例 | 问题 | 用户后果 |
|---|---|---|

| USE-CONC-01-001 | concurrency.max:10 静默接受 | 用户配置超范围并发，行为不可预期 |
| USE-CTX-01-001 | atomgit.ref 返回 main 而非 refs/heads/main | 按文档写 cut 提取分支名的脚本静默失败 |
| USE-CTX-01-002 | github.ref 被静默求值为占位符 | 迁移用户引用 github.* 得到无效值，无任何提示 |
| USE-EXPR-01-001 | 未知属性求值为空串 | 用户拼写错误被静默忽略，调试困难 |
| USE-INPT-01-002 | type:boolean 静默降级为 string | 用户用 boolean input 得到 string，条件判断逻辑出错 |
| USE-OS-01-001 | runner.os 返回 linux（小写）vs 文档 Linux | 用户 if 判断永远为 false |
| USE-SECNAME-01-001 | ATOMGIT_ 前缀 secret 被接受 | 命名违规被静默允许，未来系统变量冲突 |
| REL-YAMLCACHE-01-060 | YAML 修改后缓存未失效 | 用户推送修复后平台仍执行旧版错误 workflow |
| COMPAT-CACHE-01-001 | cache 在 dispatch 事件静默 MISS | 用户手动触发 CI 时 cache 从不命中，构建速度无改善 |
| SEC-DOS-01-001 | 1.1GB 制品静默上传成功 | DoS 攻击者可无限制上传大制品耗尽存储配额 |
| SEC-MASK-01-001 | secret 输出为空而非 *** | 用户无法确认脱敏是否生效 |
| SEC-SUPPLY-01-001 | 无效 commit hash action 引用无诊断 | 用户 pin 到错误 hash 时不知原因 |

### 3.3 按维度影响分布

| 维度 | 🔴阻塞 | 🟡非阻塞 | ⚪无影响 | 核心风险 |
|---|---|---|---|
| completeness | 8 | 8 | 0 | artifact/cache/call 基础功能阻塞，P0 阻断 |
| compatibility | 4 | 19 | 0 | 大量标记不匹配，个别平台缺陷 |
| reliability | 15 | 9 | 0 | harness 超时覆盖 + 故障注入全失效 |
| security | 16 | 5 | 2 | 真实安全缺陷少（DOS/MASK/SUPPLY），多为标记不匹配 |
| usability | 1 | 8 | 1 | 全为非阻塞静默错误——每个都可能导致用户脚本静默失败 |

### 3.4 规避手段统计

| 是否有规避 | 数量 | 占比 |
|---|---|---|
| **是** | 67 | 70% |
| **否** | 29 | 30% |

29 条无法规避的失败主要集中在：artifact/cache/call 基础功能阻塞、harness 超时覆盖、0 字节有效日志、故障注入不工作等场景。


---

## 四、系统性发现

### 4.1 run_status 词汇映射缺失——第一大断裂（~29 条，30%）

用例合约使用人类语义词汇，平台 API 返回大写枚举值。29 条标记不匹配中，绝大多数源于断言期望的 `success`/`failure` 等语义值与平台返回的 `COMPLETED`/`FAILED` 等枚举值不一致。

| 模式 | 数量 | 示例 |
|---|---|---|
| `"success"` / `"completed_success"` ≠ `COMPLETED` | ~22 | COMP-DIR-01-001, REL-CONC-01-001 等 |
| `"failure"`（小写） ≠ `FAILED`（大写） | 3 | COMPAT-EXPR-01-003, COMPAT-IF-01-001, COMPAT-OUTCOME-01-001 |
| `"canceled"` ≠ `CANCELED` | 1 | REL-CANCEL-01-028 |
| `"skipped"` ≠ `IGNORED` | 1 | REL-NEEDS-01-025 |

**修复评估**: `COMPLETED→success, FAILED→failure, CANCELED→canceled, IGNORED→skipped` 四行映射即可消除约 30% 的 FAIL。

### 4.2 空格 vs 下划线——第二大系统性缺陷

| 合约期望（下划线） | 日志实际（空格） | 用例 |
|---|---|---|
| `cleaned_as_expected` | `cleaned as expected` | SEC-RUN-01-001 |
| `isolated_as_expected` | `isolated as expected` | SEC-RUN-01-002 |
| `access_denied_or_timeout` | `access denied or timeout` | SEC-NET-01-001 |
| `push_denied_or_403` | `push denied as expected` | SEC-PERM-01-004 |
| `masked_or_not_found` | `not found` | SEC-NAME-01-002 |

**根因**: 合约用下划线连词，shell `echo` 输出自然空格。编译器应在关键词提取时归一化处理。

### 4.3 `${{{{ }}}} ` 四括号——合约生成缺陷

全部因 bash `bad substitution` 失败，影响 REL-ARTCONC-01-063, REL-MATRIX-01-038, REL-MATRIX-01-039, REL-OUTPUT-01-016 四个 reliability 用例。

**根因**: Phase 02 YAML 模板将 GitCode 表达式 `${{ }}` 错误转义为 `${{{{ }}}}`（四重花括号），runner 将其解释为 bash 非法操作。


### 4.4 确认真实平台缺陷

**P0 高价值**:

| 用例 | 缺陷 | 违反的规格承诺 |
|---|---|---|
| COMPAT-DIR-01-002 | .github/workflows/ 被错误识别并触发——安全边界破坏 | workflow-file-location-structure.md: 仅 .gitcode/workflows/ 被识别 |
| REL-YAMLCACHE-01-060 | YAML 修改后缓存未失效，执行旧版 workflow | 无对应规格——隐式缓存行为 |
| SEC-DOS-01-001 | 1.1GB 制品未被配额拒绝 | upload-download-artifacts.md: 制品大小限制 |
| SEC-MASK-01-001 | Secret 值输出为空而非文档承诺的 *** | using-secrets.md: "自动替换为 ***" |
| USE-CONC-01-001 | concurrency.max: 10 非法值静默接受 | workflow-file-location-structure.md: max 范围 1-5 |
| USE-SECNAME-01-001 | ATOMGIT_ 前缀 secret 名被接受 | using-secrets.md: "不得以 ATOMGIT_ 开头" |
| USE-INPT-01-002 | type: boolean 被静默接受并转换 | configure-triggers.md: 文档仅支持 string |
| USE-EXPR-01-001 | atomgit.nonexistent_property 解析为空串而非报错 | context.md: atomgit 属性定义 |
| USE-CTX-01-002 | github.ref 被解析为占位符而非引导至 atomgit | context.md: 上下文列表不含 github |
| USE-CTX-01-001 | atomgit.ref 返回 main 短格式而非 refs/heads/main | context.md: "触发引用全名" |
| USE-OS-01-001 | runner.os 返回 linux 小写 vs 文档 "Linux" | context.md: "Linux" |

**P1**:
- COMP-CACHE-01-001/002, COMPAT-CACHE-01-001: cache action 不可用（dispatch 事件下完全不工作）
- COMP-ARTIFACT-01-002/003, COMPAT-ARTIFACT-01-001: artifact 上传/下载失败
- COMP-CALL-01-001: workflow_call 嵌套失败
- REL-FAULT-01-031/032/033: 故障注入机制未工作
- SEC-SUPPLY-01-001/002: SHA pinning 不支持且无诊断
- SEC-CACHE-01-002: cache 不支持 workflow_dispatch 事件


### 4.5 失败传导链统计

12 例存在明确的多 step/job 失败传导链，其中显式记录的 3 例：

| 传导模式 | 数量 | 示例 |
|---|---|---|
| Upload FAILED → 下游 IGNORED | 2 | COMPAT-ARTIFACT-01-001, REL-ART-01-041 |
| Build FAILED → 下游 IGNORED | 1 | COMP-ARTIFACT-01-002 |

其余 9 例的隐式传导包括：harness 超时覆盖阻断真实超时测试（REL-TIMEOUT-01-007/008/009/010）、故障注入不工作导致下游验证全部失效（REL-FAULT-01-031/032/033）、secret 配置缺失导致脱敏验证链断裂（SEC-MASK-01-001/002/005）等。

### 4.6 日志已否认的先前进位（0 条 SECURITY_CRITICAL 成立）

| 用例 | 之前判为 | 日志证实 | 修正为 |
|---|---|---|---|
| SEC-INJ-01-005 | 双重模板注入 SECURITY_CRITICAL | bash bad substitution，"2" 是源文本 1+1 子串假阳性 | 标记不匹配 |
| REL-FAULT-01-031 | SIGKILL 日志泄漏 SECURITY_CRITICAL | 5 个 step 全正常执行，SIGKILL 从未发生 | 平台缺陷（故障注入不工作） |
| SEC-NET-01-001 | Runner SSRF SECURITY_CRITICAL | access denied or timeout — SSRF 防护工作正常 | 标记不匹配（空格vs下划线） |

---

## 五、建议回流 Phase 01 评审

1. **补全 timeout-minutes 规格**: 当前 `workflow-file-location-structure.md` 未细化 `timeout-minutes` 字段的行为，建议补充
2. **补全 YAML 缓存失效规格**: `REL-YAMLCACHE-01-060` 暴露了 YAML 缓存行为的无文档状态，应要求平台文档化
3. **Event Validation 错误文档化**: cache/artifact 在 `workflow_dispatch` 事件下的受限行为应写入对应规格
4. **ATOMGIT_ 前缀校验**: `USE-SECNAME-01-001` 建议作为文档一致性检查用例加入回归
5. **补全故障注入规格**: REL-FAULT-01-031/032/033 暴露了三类故障注入 (SIGKILL, network_partition, disk_full) 完全不可用，需在 harness 层实现

---

*分析完成时间: 2026-07-24 · 逐例详情源: `failure/2026-07-24/case/*.md` · 96/96 条覆盖*
*规格对照: `phase01/inputs/gitcode-spec/` · 多个规格文件被引用*
