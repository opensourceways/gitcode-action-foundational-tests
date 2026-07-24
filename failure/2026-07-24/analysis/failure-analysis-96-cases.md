# 169 条 FAIL 日志交叉验证 · 逐条归因 + 汇总分析
> Run: 2026-07-23-valid-clean | 分析日期: 2026-07-24
> 逐例详情: `failure/2026-07-24/case/*.md` (169 cases)

---

## 一、逐条归因表

| # | case_id | dim | 根因初判 | 责任人 | 置信度 | 阻塞性 | 静默性 | 影响面 | 失败断言摘要 | spec_file | spec_lines | 失败传导链 | 规避手段 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | COMP-ARTIFACT-01-002 | completeness | 平台缺陷 | 平台方 | 高（job status=FAILED 且下游 IGNORE | 🔴阻塞 — 上游 job FAILED 导致下游全部跳过，功 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🔴跨维度 — 两端传播（上游 FAILED + 下游 IGNORED），平台核心 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED assertions[1] (positive, ru | phase02/classify-experiment/2026-07-23/VALID/COMP-ARTIFACT-01-002.yaml | 5-20 | **Build multiple artifacts** (FAILED) → **Download all artifacts** (IGNORED) | 否 — 平台功能缺陷 |
| 2 | COMP-ARTIFACT-01-003 | completeness | 平台缺陷 | 平台方 | 中（job status=FAILED 但日志信息有限） | 🔴阻塞 — job FAILED 导致功能不可用 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🟡局部 — 影响单一功能点 | assertions[0] (positive, artifact_available) — 期望 `yes_within_retention`，实际 job status=FAILED assert | phase02/classify-experiment/2026-07-23/VALID/COMP-ARTIFACT-01-003.yaml | 1-50 |  | 否 — 平台功能缺陷 |
| 3 | COMP-ATOMGIT-01-049 | completeness | API调用失败(WAF) | 平台方 |  |  |  |  |  |  |  |  |  |
| 4 | COMP-BOUND-01-085 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 5 | COMP-CACHE-01-001 | completeness | 平台缺陷 | 平台方 | 中（job status=FAILED 但日志信息有限） | 🔴阻塞 — job FAILED 导致功能不可用 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🟡局部 — 影响单一功能点 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED assertions[1] (positive, ca | phase02/classify-experiment/2026-07-23/VALID/COMP-CACHE-01-001.yaml | 21-34 |  | 否 — 平台功能缺陷 |
| 6 | COMP-CACHE-01-002 | completeness | 平台缺陷 | 平台方 | 中（job status=FAILED 但日志信息有限） | 🔴阻塞 — job FAILED 导致功能不可用 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🟡局部 — 影响单一功能点 | assertions[0] (positive, cache_step) — 期望 `restore_hit`，实际 job status=FAILED | phase02/classify-experiment/2026-07-23/VALID/COMP-CACHE-01-002.yaml |  |  | 否 — 平台功能缺陷 |
| 7 | COMP-CALL-01-001 | completeness | 平台缺陷 | 平台方 | 中（job status=FAILED 但日志信息有限） | 🔴阻塞 — job FAILED 导致功能不可用 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🟡局部 — 影响单一功能点 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED | phase02/classify-experiment/2026-07-23/VALID/COMP-CALL-01-001.yaml | 1-32 |  | 否 — 平台功能缺陷 |
| 8 | COMP-DIR-01-001 | completeness | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMP-DIR-01-001.yaml | 1-32 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 9 | COMP-EXPR-01-058 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 10 | COMP-ISOLATION-01-001 | completeness | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMP-ISOLATION-01-001.yaml | 13-42 | Write isolation markers (COMPLETED) → Verify isolation from job A (COMPLETED) | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 11 | COMP-ISOLATION-01-002 | completeness | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMP-ISOLATION-01-002.yaml | 4-7 | Create tmp isolation marker (COMPLETED) → Check tmp marker isolation (COMPLETED) | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 12 | COMP-PERMS-01-001 | completeness | 平台缺陷 | 平台方 | 中（job status=FAILED 但日志信息有限） | 🔴阻塞 — job FAILED 导致功能不可用 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🟡局部 — 影响单一功能点 | assertions[0] (negative, run_status) — 期望 `success`，实际 job status=FAILED assertions[1] (positive, ru | phase02/classify-experiment/2026-07-23/VALID/COMP-PERMS-01-001.yaml |  |  | 否 — 平台功能缺陷 |
| 13 | COMP-PERMS-01-002 | completeness | 平台缺陷 | 平台方 | 中（job status=FAILED 但日志信息有限） | 🔴阻塞 — job FAILED 导致功能不可用 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🟡局部 — 影响单一功能点 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED | phase02/classify-experiment/2026-07-23/VALID/COMP-PERMS-01-002.yaml |  |  | 否 — 平台功能缺陷 |
| 14 | COMP-PUSH-01-001 | completeness | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMP-PUSH-01-001.yaml | 1-32 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 15 | COMP-RUNNER-01-001 | completeness | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMP-RUNNER-01-001.yaml | 3-6 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 16 | COMP-RUNNER-01-003 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 17 | COMP-SCHEDULE-01-001 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 18 | COMP-SCHEDULE-01-002 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 19 | COMP-SCHEDULE-01-003 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 20 | COMP-SCRIPT-01-082 | completeness | API调用失败(WAF) | 平台方 |  |  |  |  |  |  |  |  |  |
| 21 | COMP-SECRET-01-001 | completeness | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_logs) — 期望日志包含 `"***"`，待确认 assertions[1] (negative, run_logs) — 期望通过，实际 | phase02/classify-experiment/2026-07-23/VALID/COMP-SECRET-01-001.yaml |  |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 22 | COMP-STAGES-01-001 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 23 | COMP-STAGES-01-002 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 24 | COMP-STAGES-01-003 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 25 | COMP-STATUS-01-001 | completeness | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status_sequence) — 期望 `queued_in_progress_completed`，实际 job status=COMP | phase02/classify-experiment/2026-07-23/VALID/COMP-STATUS-01-001.yaml | 1-50 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 26 | COMP-TIMEOUT-01-001 | completeness | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMP-TIMEOUT-01-001.yaml | 1-50 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 27 | COMP-TIMEOUT-01-002 | completeness | 平台缺陷 | 平台方 | 低（缺乏足够信息判断根因） | 🟡可能阻塞 | 🟡可察觉 | 🟡局部 | assertions[0] (negative, run_status) — 期望 `success`，实际 job status=CANCELED assertions[1] (positive,  | phase02/classify-experiment/2026-07-23/VALID/COMP-TIMEOUT-01-002.yaml | 1-50 |  | 否 |
| 28 | COMP-TRIG-01-075 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 29 | COMP-UNKNOWN-01-001 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 30 | COMP-WFLOW-01-065 | completeness | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 31 | COMPAT-ACTION-01-001 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配） asse | phase02/classify-experiment/2026-07-23/VALID/COMPAT-ACTION-01-001.yaml | 1-50 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 32 | COMPAT-ACTION-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配） asse | phase02/classify-experiment/2026-07-23/VALID/COMPAT-ACTION-01-002.yaml | 1-50 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 33 | COMPAT-ACTIONDEV-01-001 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 34 | COMPAT-ARTIFACT-01-001 | compatibility | 平台缺陷 | 平台方 | 高（job status=FAILED 且下游 IGNORE | 🔴阻塞 — 上游 job FAILED 导致下游全部跳过，功 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🔴跨维度 — 两端传播（上游 FAILED + 下游 IGNORED），平台核心 | assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=FAILED assertions[1] (po | phase02/classify-experiment/2026-07-23/VALID/COMPAT-ARTIFACT-01-001.yaml | 1-50 | **Upload artifact** (FAILED) → **Download and verify artifact** (IGNORED) | 否 — 平台功能缺陷 |
| 35 | COMPAT-ARTIFACT-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配） asse | phase02/classify-experiment/2026-07-23/VALID/COMPAT-ARTIFACT-01-002.yaml | 1-50 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 36 | COMPAT-CACHE-01-001 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_logs) — "第二次运行日志中应出现 CACHE_HIT"，实际: 待评估 assertions[1] (negative, run_lo | phase02/classify-experiment/2026-07-23/VALID/COMPAT-CACHE-01-001.yaml | 21-34 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 37 | COMPAT-CONCUR-01-001 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 38 | COMPAT-CONCUR-01-002 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 39 | COMPAT-CONCUR-01-003 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 40 | COMPAT-CONCUR-01-004 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 41 | COMPAT-CTX-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMPAT-CTX-01-002.yaml | 1-32 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 42 | COMPAT-DIR-01-001 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配） asse | phase02/classify-experiment/2026-07-23/VALID/COMPAT-DIR-01-001.yaml | 13-42 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 43 | COMPAT-DIR-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (negative, workflow_discovery) — ".github/workflows/ 下的工作流不应被识别触发"，实际: 待评估 assertions[ | phase02/classify-experiment/2026-07-23/VALID/COMPAT-DIR-01-002.yaml | 13-42 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 44 | COMPAT-ENV-01-001 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMPAT-ENV-01-001.yaml | 1-32 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 45 | COMPAT-ENVIRON-01-001 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 46 | COMPAT-ENVIRON-01-002 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 47 | COMPAT-EXPR-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_logs) — 期望日志包含 `"Job B ran after Job A success"`，待确认 assertions[1] (pos | phase02/classify-experiment/2026-07-23/VALID/COMPAT-EXPR-01-002.yaml | 4-7 | Job A that succeeds (COMPLETED) → Job B depends on A (COMPLETED) | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 48 | COMPAT-EXPR-01-003 | compatibility | 平台缺陷 | 平台方 | 高（job status=FAILED 且有明确错误输出） | 🔴阻塞 — job FAILED 导致功能不可用 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🟡局部 — 影响单一功能点 | assertions[0] (positive, run_logs) — 期望日志包含 `"Cleanup ran after failure"`，因 job FAILED 未执行验证 asserti | phase02/classify-experiment/2026-07-23/VALID/COMPAT-EXPR-01-003.yaml | 4-7 |  | 否 — 平台功能缺陷 |
| 49 | COMPAT-EXPR-01-013 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 50 | COMPAT-EXPR-01-014 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 51 | COMPAT-FIELD-01-001 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 52 | COMPAT-FIELD-01-002 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 53 | COMPAT-FIELD-01-003 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 54 | COMPAT-IF-01-001 | compatibility | 平台缺陷 | 平台方 | 高（job status=FAILED 且有明确错误输出） | 🔴阻塞 — job FAILED 导致功能不可用 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🟡局部 — 影响单一功能点 | assertions[0] (positive, run_status) — 期望 `failure`，实际 job status=FAILED assertions[1] (negative, ru | phase02/classify-experiment/2026-07-23/VALID/COMPAT-IF-01-001.yaml | 1-50 |  | 否 — 平台功能缺陷 |
| 55 | COMPAT-IF-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_logs) — 期望日志包含 `"This should appear"`，待确认 assertions[1] (positive, run_ | phase02/classify-experiment/2026-07-23/VALID/COMPAT-IF-01-002.yaml | 1-50 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 56 | COMPAT-INPUTS-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMPAT-INPUTS-01-002.yaml | 1-32 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 57 | COMPAT-MASK-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (negative, run_logs) — ，实际: 待评估 assertions[1] (positive, run_logs) — "日志中出现 *** 替代通过 e | phase02/classify-experiment/2026-07-23/VALID/COMPAT-MASK-01-002.yaml |  |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 58 | COMPAT-MIGRATE-01-001 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 59 | COMPAT-MIGRATE-01-002 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 60 | COMPAT-OUTCOME-01-001 | compatibility | 平台缺陷 | 平台方 | 高（job status=FAILED 且有明确错误输出） | 🔴阻塞 — job FAILED 导致功能不可用 | 🟡可察觉 — 通过 job status=FAILED 可见 | 🟡局部 — 影响单一功能点 | assertions[0] (positive, step_status) — 期望 `failure`，实际 job status=FAILED assertions[1] (positive, s | phase02/classify-experiment/2026-07-23/VALID/COMPAT-OUTCOME-01-001.yaml | 1-50 |  | 否 — 平台功能缺陷 |
| 61 | COMPAT-OUTCOME-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, step_status) — 期望 `failure`，实际 job status=COMPLETED assertions[1] (positive | phase02/classify-experiment/2026-07-23/VALID/COMPAT-OUTCOME-01-002.yaml | 1-50 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 62 | COMPAT-PATHS-01-001 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 63 | COMPAT-PATHS-01-002 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 64 | COMPAT-PERM-01-001 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMPAT-PERM-01-001.yaml |  |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 65 | COMPAT-PERM-01-003 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 66 | COMPAT-PERM-01-004 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配） asse | phase02/classify-experiment/2026-07-23/VALID/COMPAT-PERM-01-004.yaml |  |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 67 | COMPAT-PR-01-002 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 68 | COMPAT-PR-01-003 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 69 | COMPAT-PR-01-004 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 70 | COMPAT-PR-01-005 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 71 | COMPAT-RUNNER-01-001 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMPAT-RUNNER-01-001.yaml | 3-6 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 72 | COMPAT-RUNNER-01-002 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMPAT-RUNNER-01-002.yaml | 3-6 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 73 | COMPAT-RUNNER-01-004 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 74 | COMPAT-RUNNER-01-005 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 75 | COMPAT-RUNSON-01-001 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配） asse | phase02/classify-experiment/2026-07-23/VALID/COMPAT-RUNSON-01-001.yaml | 3-6 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 76 | COMPAT-SCHEDULE-01-001 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 77 | COMPAT-SCHEDULE-01-002 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 78 | COMPAT-SCHEDULE-01-003 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 79 | COMPAT-SECRET-01-005 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 80 | COMPAT-SHELL-01-003 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 81 | COMPAT-TOKEN-01-001 | compatibility | API调用失败(WAF) | 平台方 |  |  |  |  |  |  |  |  |  |
| 82 | COMPAT-TOKEN-01-002 | compatibility | API调用失败(WAF) | 平台方 |  |  |  |  |  |  |  |  |  |
| 83 | COMPAT-VARS-01-001 | compatibility | 标记不匹配 | 平台方 | 中（job 执行完成（COMPLETED）但断言不匹配，需核 | 🟢不阻塞 — job 状态为 COMPLETED，功能可能正 | 🟡可察觉 — 通过断言对比可见 | 🟡局部 — 影响单一断言与平台状态值的匹配 | assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配） assertions[1]  | phase02/classify-experiment/2026-07-23/VALID/COMPAT-VARS-01-001.yaml | 4-7 |  | 是 — 可通过直接检查日志内容自行验证功能是否正常 |
| 84 | COMPAT-VARS-01-005 | compatibility | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 85 | REL-ART-01-041 | reliability | 平台缺陷 | 平台方 | 高（artifact 名称冲突是明确的平台行为，非用例或环境 | 🔴阻塞 — 同一 repo 下同名 artifact 无法重 | 🟢明确报错 — `error::Upload artifac | 🔴跨维度 — 影响所有 artifact 上传相关用例 |  |  | 52-58 | upload FAILED → download IGNORED → 所有正向断言不满足 | 是（每次使用唯一 artifact 名称，或在测试前清理历史 artifact） |
| 86 | REL-ARTCONC-01-063 | reliability | 用例问题 | Phase 01 | 高（`bad substitution` 是明确的模板渲染错 | 🔴阻塞 — job 一步也未执行成功 | 🟢明确报错 — `bad substitution` 即时失 | 🟡同模板 — 影响所有使用 `{{ matrix.<var> }}` 的 mat |  |  | 21-27 | 语法错误 → 所有实例 FAILED → upload 未执行 → 所有断言不满足 | 是（修复模板嵌套花括号渲染逻辑，确保仅产出 `${{ matrix.instance }}`） |
| 87 | REL-ARTPERF-01-053-V2 | reliability | 平台缺陷 | 平台方 | 高（`Namespace artifact quota ex | 🔴阻塞 — namespace quota 限制 1GB，任 | 🟢明确报错 — `Namespace artifact qu | 🟡同 namespace — 影响所有大 artifact 用例（共享同一 na |  |  | 51-58 | upload 分片全部上传成功 → finalize 时 quota 检查失败 → upload FAILED → download IGNORED | 是（先清理历史 artifact 释放 namespace quota，或申请提高配额） |
| 88 | REL-ARTPERF-01-053 | reliability | 用例问题 | Phase 01 | 高（`ls: cannot access 'perf-art | 🟢不阻塞 — 上传/下载核心功能正常，仅 verify 步骤 | 🟢明确报错 — `ls: cannot access` 即时 | 🟡同模板 — 影响所有未指定 download-artifact path 且  |  |  | 82-88 | download step 成功（二进制正确下载）→ verify step 因文件名不匹配 FAILED → hash_match 断言失败 | 是（在 download-artifact 中指定 `path: perf-artifact` 或  |
| 89 | REL-CANCEL-01-028 | reliability | 环境/Harness | Phase 02 | 中（job 确实完成了全部步骤，但无法从日志判断取消操作是否 | 🟡中等 — 核心取消语义待验证但未被充分测试 | 🟡中等 — job 静默完成，无 cancel 行为可观测 | 🟡同用例 — 仅影响取消语义验证用例 |  |  | 86-87 | job 执行过快（sleep 60s 可能被 runner 提前分配并快速完成）→ test harness 发出的 cancel API 调用到达时 job 已 COMPLETED → 断言的 ru | 是（增加 sleep 时长到 120-180 秒确保有足够窗口执行取消；或检查 test harne |
| 90 | REL-CONC-01-001 | reliability | 环境/Harness | Phase 02 | 低（日志严重不全，无法判断是 test harness 触发 | 🟡中等 — 无法判断是 log 收集问题还是平台并发控制问题 | 🔴静默 — 无错误日志，仅在断言阶段因数据不足而失败 | 🟡同用例 — 仅影响此并发用例 |  |  | 154-165 | 日志收集不全 → 无法验证 5 并发断言 → case FAIL | 是（检查 test harness 是否确实触发了 5 次 workflow run，并确认 log |
| 91 | REL-CONTINUE-01-030 | reliability | 平台缺陷 | 平台方 | 高（job_a 正确失败，job_b 正确执行；workfl | 🟢不阻塞 — 核心 continue-on-error 功能 | 🟢明确 — job_a 明确 fail，job_b 明确 s | 🟡同用例 — 仅影响 workflow_status 断言 |  |  | 172-183 | job_a exit 1 → FAILED / continue-on-error 允许继续 → job_b COMPLETED → 但 workflow_status 断言可能因平台将含失败 job | 是（修改断言：将 `workflow_status=success` 改为仅验证 `job_b_st |
| 92 | REL-FAULT-01-031 | reliability | 环境/Harness | Phase 02 | 高（所有 5 个 step 均成功执行，明确表明故障注入未生 | 🟢不阻塞 — 故障注入机制需要修复，但不影响正常功能测试 | 🟡中等 — job 静默成功，无任何 fault 提示 | 🟡同机制 — 影响所有依赖 fault_injection 的用例 |  |  |  | fault injection 未生效 → job 正常完成 → job_status=COMPLETED → 断言 job_status=failure 失败 | 是（确认测试环境的 fault injection 机制；考虑用 step timeout 替代进程 |
| 93 | REL-FAULT-01-032 | reliability | 环境/Harness | Phase 02 | 高（artifact 上传完整成功，无任何网络错误；明确表明 | 🟢不阻塞 — 故障注入机制问题，不影响正常功能 | 🟡中等 — job 静默成功，fault 期望未被触发 | 🟡同机制 — 影响所有依赖 fault_injection 的用例 |  |  | 51-58 | network_partition 未注入 → artifact 正常上传 → step_status=COMPLETED → 断言全部失败 | 是（检查 fault injection 实现：network_partition 是否是 ipta |
| 94 | REL-FAULT-01-033 | reliability | 环境/Harness | Phase 02 | 高（2GB 写入成功证明磁盘空间充足；预填充量不足或 run | 🟢不阻塞 — 不影响正常功能，仅故障注入场景不满足 | 🟡中等 — 预填充和写入均静默成功 | 🟡同用例 — 仅影响磁盘满载入用例 |  |  | 43-53 | 磁盘未满 → 2GB 写入成功 → job COMPLETED → 所有断言不满足 | 是（增大预填充量至接近 runner 实际磁盘容量；或使用 tmpfs/loopback 设备限制空 |
| 95 | REL-IGNORE-01-004 | reliability | 环境/Harness | Phase 02 | 低（数据严重不全，无法判断是并发触发失败还是 log 收集遗 | 🟡中等 — 无法判断 IGNORE 语义是否正确 | 🔴静默 — 无错误日志 | 🟡同模式 — 影响所有并发测试用例 |  |  | 154-165 | log 不完整 → 无法验证 4/4 runs → case FAIL | 是（检查 test harness 是否确实触发了 4 次 workflow_dispatch；确认 |
| 96 | REL-K8S-01-045 | reliability | 环境/Harness | Phase 02 | 中（runner 不可用可能性大，但日志信息极少——仅 2  | 🔴阻塞 — K8s runner 不可用导致用例完全无法执行 | 🟡中等 — 仅 `status=FAILED` 但无详细错误 | 🟡同 runner — 影响所有 K8s runner 用例 |  |  | 57-65 | runner 未分配/启动失败 → 无 step 执行 → job FAILED → 所有断言不满足 | 是（确认 K8s Runner 组 Pod 状态，手动注册 K8s runner 后再执行） |
| 97 | REL-LOG-01-040 | reliability | API调用失败(WAF) | 平台方 |  |  |  |  |  |  |  |  |  |
| 98 | REL-MATRIX-01-027 | reliability | 用例问题 | Phase 01 | 高（Phase 01 文本描述 3x3=9 组合，YAML  | 🟡中等 — 用例目的（max-parallel=4 控制 9 | 🟢明确 — 3 个 jobs 成功但未覆盖完整场景 | 🟡同用例 — 仅此矩阵用例 |  |  | 46-53 | Phase 01 文本与 test YAML 不一致 → 仅 3 个组合而非 9 个 → 无法验证 max-parallel 在 9 组合下的行为 | 是（将 matrix 改为二维：添加第二个维度如 `os: [ubuntu, euler, debi |
| 99 | REL-MATRIX-01-038 | reliability | 四括号模板缺陷 | Phase 01 | 高（同 REL-ARTCONC-01-063——`bad s | 🔴阻塞 — 全部 20 个 jobs 均失败 | 🟢明确报错 — `bad substitution` 即时失 | 🟡同模板 — 影响所有使用 `{{ matrix.* }}` 的 matrix  |  |  | 56-63 | 模板变量嵌套 → 所有 instance FAILED → 所有断言不满足 | 是（修复模板嵌套花括号渲染逻辑） |
| 100 | REL-MATRIX-01-039 | reliability | 四括号模板缺陷 | Phase 01 | 高（与其他 matrix 用例相同根因——模板渲染花括号层级 | 🔴阻塞 — 全部 50 个 jobs 均失败 | 🟢明确报错 — `bad substitution` | 🔴跨用例 — 与 REL-ARTCONC-01-063、REL-MATRIX-0 |  |  | 56-63 | 同模板错误 → 全部 50 instances FAILED → 所有断言不满足 | 是（修复模板渲染后统一去重花括号） |
| 101 | REL-NEEDS-01-025 | reliability | 平台缺陷 | 平台方 | 高（IGNORED vs skipped 是确定的字符串不匹 | 🟢不阻塞 — 功能正确（needs 失败传播生效，job_b | 🟢明确 — job_b 状态 IGNORED 清晰 | 🟡断言层 — 仅影响状态标签断言 |  |  | 73-95 | job_a FAILED → needs 依赖导致 job_b IGNORED（非 skipped）→ 断言字符串匹配失败 | 是（将断言从 `equals: "skipped"` 改为 `equals: "IGNORED"`  |
| 102 | REL-OUTPUT-01-016 | reliability | 四括号模板缺陷 | Phase 01 | 高（同 matrix 用例的模板渲染问题——系统性错误而非个 | 🔴阻塞 — read step 一步也无法执行 | 🟢明确报错 — `bad substitution` | 🔴跨用例 — 与所有使用 `{{ steps.*.outputs.* }}` 的 |  |  | 25-28 | write step 成功 → read step 因表达式渲染错误 FAILED → 断言不满足 | 是（修复模板花括号嵌套渲染逻辑） |
| 103 | REL-OUTPUT-01-017 | reliability | API调用失败(WAF) | 平台方 |  |  |  |  |  |  |  |  |  |
| 104 | REL-PREEMPT-01-005 | reliability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 105 | REL-PREEMPT-01-006 | reliability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 106 | REL-QUEUE-01-003 | reliability | 环境/Harness | Phase 02 | 低（与 REL-CONC-01-001 / REL-IGNO | 🟡中等 — 无法判断 QUEUE 语义是否正确 | 🔴静默 — 无错误日志 | 🟡同模式 — 与其他 concurrency 用例共享相同根因 |  |  | 154-165 | log 不完整 → 无法验证 queue 行为 → case FAIL | 是（排查 test harness 多 run 触发和 log 收集逻辑） |
| 107 | REL-RACE-01-048 | reliability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 108 | REL-RERUN-01-011 | reliability | 环境/Harness | Phase 02 | 中（log 中无 rerun 记录，可能是 test har | 🟡中等 — rerun 功能未被验证 | 🔴静默 — 无 rerun 记录或错误 | 🟡同用例 — 仅 rerun 用例 |  |  | 11-13 | 原始 run 成功 → rerun 未触发或未被收集 → rerun_count 断言失败 | 是（手动验证 rerun 功能，或修复 test harness 的 rerun 触发逻辑） |
| 109 | REL-STAGES-01-029 | reliability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 110 | REL-STEPS-01-042 | reliability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 111 | REL-TIMEOUT-01-007 | reliability | 平台缺陷 | 平台方 | 中（CANCELED 状态明确但 cancel 来源不确定— | 🟡中等 — timeout-minutes 边界行为未被验证 | 🟡中等 — CANCELED 状态明确但原因不明 | 🟡同用例 — 仅影响 timeout 边界用例 |  |  | 110-121 | job 被提前 cancel（非 timeout）→ job_status=CANCELED → 断言全不满足 | 是（确认平台是否有比 360 分钟更低的全局 timeout 限制；减小 sleep 时长测试更短的 |
| 112 | REL-TIMEOUT-01-008 | reliability | 平台缺陷 | 多方联合 | 中（与 TIMEOUT-007 相同模式——平台/环境阻止超 | 🟡中等 — timeout 越界行为未被验证 | 🟡中等 — CANCELED 明确但原因不明 | 🔴跨用例 — 与 TIMEOUT-007/009/010 共享相同根因 |  |  | 110-121 | 平台提前 cancel → CANCELED 非 failure → timeout 日志不存在 → 断言全部失败 | 是（确认平台级运行时长限制；使用更短的 timeout-minutes 如 5 分钟和 3 分钟 s |
| 113 | REL-TIMEOUT-01-009 | reliability | 平台缺陷 | 平台方 | 中（CANCELED 状态可能是 timeout 触发的正确 | 🟢不阻塞 — timeout 机制可能正在正确工作（如果 C | 🟡中等 — CANCELED 无详细 reason | 🟡同规范 — 影响所有 timeout 相关断言 |  |  | 110-121 | job 被 cancel（可能是 timeout 触发）→ status=CANCELED（非 failure）→ 断言不满足 | 是（将断言从 `equals: "failure"` 改为 `equals: "CANCELED"` |
| 114 | REL-TIMEOUT-01-010 | reliability | 平台缺陷 | 多方联合 | 中（同 TIMEOUT-007/008 模式——所有长 sl | 🟡中等 — 默认 timeout 行为未被验证 | 🟡中等 — CANCELED 明确 | 🔴跨用例 — 4 个 TIMEOUT 用例全部无法验证 |  |  |  | 同 TIMEOUT-007/008 → 平台 prevent long sleep → job CANCELED → 断言全部失败 | 是（使用更短的 timeout-minutes 和更短的 sleep 进行时间边界测试；例如 tim |
| 115 | REL-YAMLCACHE-01-060 | reliability | 平台缺陷 | 平台方 | 中（输出 marker_v1 明确，但根因可能是 push  | 🟡中等 — workflow YAML 缓存/更新机制待验证 | 🟡中等 — job 静默成功但输出了旧版本内容 | 🟡同用例 — 仅影响 YAML 缓存失效验证 |  |  | 79-89 | YAML 未更新到 v2 → job 执行旧 v1 代码 → marker_v1 出现 → marker_v2 断言失败 | 是（检查 test harness push 后等待时间；确认 git push 返回码；手动验证  |
| 116 | SEC-ARTF-01-002 | security | 平台行为偏差 | 多方联合 | 高（日志证据清晰：平台返回 400 而非预期的 403/40 | 高 — 跨仓库 artifact 隔离是安全关键特性，当前测 | 高 — 平台未静默放行（返回了错误），但错误码类型(400) | 中 — 影响安全审计结论的可信度 | - 负向 `run_logs` `must_not_contain: "200"` — **FAIL**: 日志中出现 `000` + `error_code:400` 即 HTTP 400 BAD_ |  | 7-19 | 测试 YAML 断言期望 `403_or_404` → 实际得到 `400` → 平台返回的错误码与规格预期存在偏差 | 是 — 修改测试 YAML 使用 `download-artifact` action；同时在规格中 |
| 117 | SEC-CACHE-01-002 | security | 用例问题 | Phase 01 | 高（日志明确显示 Event Validation Erro | 中 — 测试无法达到验证目标，但核心功能（跨仓库 cache | 低 — 平台明确报出 warning，行为可观测 | 低 — 仅限于本用例；修改 trigger 即可回复测试能力 | - 负向 `cache_restore` `must_not_hit: "fork_cache_key"` — 无法验证: cache action 被跳过，未实际执行 restore - 正向 `r |  | 25-33 | 测试 YAML trigger 设为 `workflow_dispatch` → 平台 cache 组件 Event Validation 拒绝 Manual 事件 → cache action 被跳 | 是 — 修改 trigger 为 `push` 或 `pull_request` |
| 118 | SEC-DEFPERM-01-001 | security | 环境/Harness | Phase 02 | 高（token not found 明确指示环境问题） | 低 — 可在修复 token 注入后重新测试；token 场 | 低 — 平台明确报出 401 错误 | 中 — 影响所有依赖 `atomgit.token` 的权限测试用例 | - 负向 `run_logs` `must_not_contain: "write_successful"` — **PASS**: 未出现 "write_successful" - 正向 `run_ |  | 69-83 | atomgit.token 未注入或无效 → 所有 API 调用返回 401 → 无法区分"有 read 权限但拒绝 write"和"无任何权限" → 正向断言"403_or_permission_d | 是 — 确保 workflow dispatch 或 trigger 配置正确注入 `ATOMGIT |
| 119 | SEC-DEFPERM-01-002 | security | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 120 | SEC-DOS-01-001 | security | 平台缺陷 | 平台方 | 高（平台未拒绝 1100MB 文件上传，无大小限制报错） | 高 — 无 artifact 大小配额，可能导致 DoS 攻 | 极高 — 平台静默成功上传超大文件，用户/管理员无感知 | 高 — 影响所有项目的 artifact 配额管控 | - 负向 `run_status` `must_not_equal: "success"` — **FAIL**: job status=COMPLETED（成功），1100MB 文件上传成功 - 正 |  | 7-19 | dd 创建 1100MB 零填充文件 → zip 压缩为 ~1MB → 平台未执行大小检查（应在压缩前检查原始大小？）→ 上传成功 → 负向和正向断言均失败 | 否 — 用户侧无法控制平台 artifact 大小限制 |
| 121 | SEC-ENV-01-001 | security | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 122 | SEC-ENV-01-002 | security | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 123 | SEC-INJ-01-004 | security | 用例问题 | Phase 01 | 中（push 触发成功但 commit message 为空 | 中 — 测试未覆盖注入场景，无法验证平台的安全性 | 高 — 若平台存在注入漏洞，当前测试不会发现 | 高 — commit message 注入是常见的 CI/CD 攻击向量 | - 负向 `run_logs` `must_not_contain: "injected_command_executed"` — **PASS**: 未出现注入执行 - 正向 `run_status |  | 25-30 | push trigger 未提供包含元字符的 commit message → `${{ atomgit.event.commits[0].message }}` 求值为空 → 无注入输入 → 断言无 | 是 — 在测试 fixture 中显式推送包含反引号/分号的 commit |
| 124 | SEC-INJ-01-005 | security | 用例问题 | Phase 01 | 中（bash 报错清晰，但该行为可能恰好是平台的设计预期—— | 低 — 可通过修改测试 YAML 中的 echo 字符串避开 | 中 — 若平台存在二次求值漏洞，当前测试会因 bash 报错 | 低 — 仅影响该特定测试用例 | - 负向 `run_logs` `must_not_contain: "2"` — **PASS**: 日志中未出现 "2"（即内层 `{{ 1 + 1 }}` 未被求值） - 正向 `run_log |  | 40-45 | `${{ '{{ 1 + 1 }}' }}` → 平台表达式引擎求值 → 输出 `${{ 1 + 1 }}` → bash 尝试解释 `${{ }}` → bad substitution → exi | 是 — 修改 echo 为 `echo 'Input: ${{ 1 + 1 }}'` 或使用 `pr |
| 125 | SEC-MASK-01-001 | security | 环境/Harness | Phase 02 | 高（日志输出为空，secret 未正常注入） | 中 — 依赖 secret 注入前置条件，需验证 secre | 高 — 若平台脱敏功能有问题，当前测试无法发现 | 中 — 影响所有 secret mask 系列用例（SEC-MASK-01-00 | - 负向 `run_logs` `must_not_contain_secret: "DEPLOY_TOKEN"` — 无法判定: 日志仅显示 "The secret is "（空），未出现 secr |  | 10-16 | `${{ secrets.DEPLOY_TOKEN }}` 求值 → 结果输出到日志 → 日志显示为空 → 无法区分"空 secret"、"脱敏为空串"还是"脱敏为 *** 但未显示" | 是 — 验证并配置 secret 在 `workflow_dispatch` trigger 下的注 |
| 126 | SEC-MASK-01-002 | security | 环境/Harness | Phase 02 | 高（secret 值为空，与 SEC-MASK-01-001 | 中 — 与 SEC-MASK-01-001 相同，依赖 se | 高 — 无法验证脱敏效果 | 中 — 影响 MASKS 系列用例 | - 负向 `step_summary` `must_not_contain_secret: "API_KEY"` — 无法验证: step summary 未产生可验证的明文泄露 - 负向 `erro |  | 10-16 | `${{ secrets.API_KEY }}` 求值为空 → step summary 与 error stack 中均无明文泄露 → 无法验证脱敏是否生效 | 是 — 修复 secret 注入后重新测试 |
| 127 | SEC-MASK-01-005 | security | 环境/Harness | Phase 02 | 高（secret 值空，与 SEC-MASK-01-001  | 中 — 依赖 secret 注入 | 高 — 多行 secret 泄露是实际攻击向量（如 RSA  | 中 — 与其他 MASK 用例共享根因 | - 负向 `run_logs` `must_not_contain_secret: "MULTI_LINE_SECRET"` — 无法判定: 日志仅输出空行 - 正向 `run_logs` `equa |  | 10-16 | `${{ secrets.MULTI_LINE_SECRET }}` 求值为空 → echo 空内容 → 日志无输出 → 无法验证多行脱敏行为 | 是 — 修复 secret 注入后重新测试 |
| 128 | SEC-NAME-01-001 | security | 环境/Harness | Phase 02 | 中（secret 值为空且未触发 YAML 解析错误，无法区 | 低 — secret 值未泄露（空输出），但无法验证安全性 | 高 — 若平台静默吞掉不支持的 secret 名，用户将无法 | 低 — 仅影响含特殊字符的 secret 命名场景 | - 负向 `run_logs` `must_not_contain_secret: "MY-VAR"` — 无法判定: 日志输出 "value is " 后为空 - 正向 `run_status` ` |  | 10-16 | `${{ secrets.MY-VAR }}` 求值为空 → 无法确认是 secret 未注入、被正确脱敏为空、还是解析异常导致 | 是 — 修复 secret 注入；或改为无中划线的 secret 名对比测试 |
| 129 | SEC-NAME-01-002 | security | 环境/Harness | Phase 02 | 中（日志中 printenv 结果被过滤或 secret 未 | 低 — 未发现 secret 泄露 | 中 — 若脱敏引擎正常但日志采集丢弃了脱敏后的输出，测试无法 | 低 — 与其他 secret 系列共享环境问题 | - 负向 `run_logs` `must_not_contain_secret: "API_KEY"` — **PASS**: 日志中 API_KEY 原值未出现 - 正向 `run_logs` ` |  | 25-39 | printenv / grep API_KEY 执行 → 输出被日志系统捕获 → 日志中仅显示 input 参数脚本，grep 结果未显示 → 缺少"masked_or_not_found"的显式证据 | 是 — 增加显式的 `echo "found"` 或 `echo "not found"` 输出，而 |
| 130 | SEC-NET-01-001 | security | 平台行为偏差 | Phase 01 | 低（Step 1 输出异常版本号列表；测试脚本用 `|| e | 高 — SSRF 防护是核心安全边界，测试无法得出可靠结论 | 极高 — `|| echo` 掩盖了真实网络行为 | 高 — 影响对整个 CI Runner 网络安全性的评估 | - 负向 `run_logs` `must_not_contain: "metadata_service_response"` — **PASS**: 未出现 metadata 服务响应 - 正向 ` |  |  | curl 到内网地址失败 → 触发 `//` 分支打印固定字符串 → curl 原始错误信息被丢弃 → 无法判断是超时、连接拒绝还是路由不可达 | 是 — 修改测试脚本为 `curl -v --max-time 5 ... 2>&1` 保留完整错误 |
| 131 | SEC-PERM-01-001 | security | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 132 | SEC-PERM-01-002 | security | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 133 | SEC-PERM-01-003 | security | 环境/Harness | Phase 02 | 高（与 SEC-DEFPERM-01-001 完全一致的 4 | 中 — token 未注入使权限测试无法进行 | 低 — 401 错误明确可观测 | 中 — 影响所有权限测试用例 | - 负向 `run_logs` `must_not_contain: "write_permission_granted"` — **PASS**: 未出现写权限授予 - 正向 `run_status |  |  | `${{ atomgit.token }}` 为空 → API 调用没有有效 token → 返回 401 → 退出码 6（非成功）→ job FAILED | 是 — 修复 token 注入 |
| 134 | SEC-PERM-01-004 | security | 用例问题 | Phase 01 | 高（git config 缺失导致测试阻断，与权限验证无关） | 中 — git 前置条件缺失阻止了权限测试 | 低 — 错误信息清晰（"Please tell me who | 低 — 仅影响本用例 | - 负向 `run_logs` `must_not_contain: "push_successful"` — **PASS**: 未出现 push 成功 - 正向 `run_logs` `equal |  |  | git clone 成功 → `echo test > test.txt` 成功 → `git add` 成功 → `git commit` 失败（Author identity unknown）→  | 是 — 在脚本开头增加 `git config user.email "test@test.com" |
| 135 | SEC-RUN-01-001 | security | 标记不匹配 | Phase 01 | 低（测试表面通过但设计存在缺陷：若两个 job 在不同容器/ | 中 — 无法区分 "清理生效" 和 "容器隔离"，安全评估无 | 极高 — 测试结果是"好的假阳性"：若清理未生效但容器隔离掩 | 中 — 影响所有 job 间隔离清理类测试 | - 负向 `run_logs` `must_not_contain: "residual found"` — **PASS**: 未出现 "residual found" - 正向 `run_logs |  | 69-83 | 两个 job 可能不在同一文件系统空间 → job B 检测不到 job A 的文件 → "cleaned as expected" 可能是隔离而非清理的结果 | 是 — 修改测试 YAML 使用 `workspace` 目录（`$ATOMGIT_WORKSPAC |
| 136 | SEC-RUN-01-002 | security | 标记不匹配 | Phase 01 | 低（与 SEC-RUN-01-001 相同问题 — 容器级隔 | 中 — 无法区分容器隔离和清理隔离 | 极高 — 测试的"通过"可能是假阳性 | 中 — 影响 RUN 系列隔离测试 | - 负向 `run_logs` `must_not_contain: "isolation broken"` — **PASS**: 未出现 - 正向 `run_logs` `equals: "iso |  |  | 并行 job 在不同容器 → 天然隔离 → "isolated as expected" 可能不是清理的效果 | 是 — 使用 `needs: job-a-env` 确保串行执行+同一 runner；或使用 wor |
| 137 | SEC-RUN-01-003 | security | 标记不匹配 | Phase 01 | 高（job 零输出，自托管 runner 不可用） | 高 — 自托管 runner 测试场景完全不可用 | 低 — FAILED 状态明确 | 中 — 影响所有依赖自托管 runner 的测试 | - 负向 `run_logs` `must_not_contain: "cross project leak"` — 无法判定: 两个 job 均 FAILED，无有用输出 - 正向 `run_log |  |  | 自托管 runner 不可用 → job 无法被调度 → 进入 FAILED 状态 → 测试完全未执行 | 是 — 部署或配置自托管 runner；或使用 dedicate-hosted runner 模拟 |
| 138 | SEC-SIDE-01-002 | security | 环境/Harness | Phase 02 | 高（artifact name 冲突，与 secret 泄露 | 中 — artifact 名称冲突阻止了核心验证 | 低 — 平台明确报出名称冲突错误 | 低 — 可通过清理 artifact 或使用动态名称解决 | - 负向 `artifact_content` `must_not_contain_secret: "DEPLOY_TOKEN"` — 无法验证: artifact 上传失败 - 正向 `run_st |  | 7-19 | 上次 test run 残留同名 artifact → Twirp 服务拒绝重复 → 上传失败 → 无法下载检查内容 | 是 — 在测试 setup 中清理残留 artifact；或使用带时间戳的动态名称 |
| 139 | SEC-SUPPLY-01-001 | security | 用例问题 | Phase 01 | 高（假 commit SHA 导致 action 解析失败） | 中 — 正向测试未执行 | 低 — FAILED 状态明确 | 低 — 仅本用例 | - 正向 `run_status` `equals: "success_or_action_executed"` — **FAIL**: job status=FAILED，零输出 - 负向 `run |  |  | 假 commit SHA → 平台 Action 解析器无法定位 → job FAILED（启动阶段）→ 零输出 | 是 — 使用真实存在的 action 仓库及其真实 commit SHA |
| 140 | SEC-SUPPLY-01-002 | security | 用例问题 | Phase 01 | 中（job 正确 FAILED 但无错误消息，无法验证"返回 | 低 — 安全行为达标（不执行假 action），但可观测性不 | 高 — 用户无法从日志中理解失败原因 | 中 — 影响所有使用 action 引用的用户体验 | - 负向 `run_status` `must_not_equal: "success"` — **PASS**: job status=FAILED - 正向 `run_logs` `equals: |  |  | 全零 commit SHA → 平台 Action 解析器找不到 → job FAILED 零输出 → 缺少明确的错误信息 | 否 — 用户侧无法获得更详细的错误信息 |
| 141 | SEC-SUPPLY-01-003 | security | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 142 | SEC-TOCTOU-01-001 | security | 用例问题 | Phase 01 | 高（`atomgit.sha` 为空，与测试设计不符） | 高 — 测试场景与平台能力不匹配（审批流程未就绪） | 高 — 当前测试无法发现 TOCTOU 漏洞 | 中 — TOCTOU 是审批类 CI/CD 的关键安全威胁 | - 负向 `run_logs` `must_not_contain: "unapproved_commit_executed"` — 无法判定: commit SHA 输出为空 - 正向 `run_l |  |  | `workflow_dispatch` trigger → 无 commit SHA 上下文 → `atomgit.sha` 为空 → 无法绑定审批时刻的 commit → TOCTOU 验证无法进行 | 是 — 等待平台审批流程功能就绪后重新设计测试 |
| 143 | SEC-WCMD-01-001 | security | 环境/Harness | Phase 02 | 中（命令响应不含 secret 明文，但无法确认 secre | 低 — add-mask 命令日志表现合格（无 secret | 中 — 若 add-mask 实际未生效（secret 为空 | 低 — 仅影响本用例 | - 负向 `run_logs` `must_not_contain_secret: "API_KEY"` — **PASS**: 日志无 API_KEY 明文 - 正向 `run_logs` `equ |  |  | `${{ secrets.API_KEY }}` 求值 → add-mask 命令执行 → 日志仅显示 `::add-mask::` → secret 值未泄露在命令响应中（正向）→ 但无后续验证确认 | 是 — 修复 secret 注入后，增加 `echo "Value after mask: ${{  |
| 144 | SEC-WCMD-01-002 | security | 环境/Harness | Phase 02 | 高（artifact 不存在，跨运行边界未建立） | 高 — 测试核心流程缺失前置步骤 | 高 — 错误 "not found" 掩盖了信任边界验证 | 中 — 跨运行 artifact 信任是 CI/CD 供应链安全关键 | - 负向 `run_logs` `must_not_contain: "auto_executed"` — **PASS**: 未出现 auto_executed - 正向 `run_status`  |  | 7-19 | 不可信来源的 artifact 未创建 → 特权运行中 download-artifact 找不到 → "Available artifacts: (none)" → 测试未达到验证边界 | 是 — 需两阶段测试：(1) 触发不可信运行上传 artifact；(2) 特权运行下载时指定不可信 |
| 145 | SEC-WCMD-01-003 | security | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 146 | SEC-WCMD-01-004 | security | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 147 | USE-CONC-01-001 | usability | 平台缺陷 | 平台方 | 高（日志明确显示 job 成功完成但预期应被拒绝；规格中确实 | 🔴 用户配置 concurrency.max 超出平台内部限 | 🔴 完全静默 — 无 WARNING、无 ERROR、无 I | 🟡 所有配置了 concurrency 的 workflow（尤其是从 GitH | - negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝 max: 10） - nonfunctional/error |  | 152-166 | 平台 → 跳过 concurrency.max 范围校验 → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败 | 否 |
| 148 | USE-CONC-01-002 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 149 | USE-CTX-01-001 | usability | 平台缺陷 | 平台方 | 高（日志直接证明 atomgit.ref 返回 `main` | 🟡 如果用户依赖 `${{ atomgit.ref == ' | 🔴 完全静默 — job 正常完成，无任何警告 | 🟡 所有使用 `atomgit.ref` 做字符串匹配（如条件执行、分支判断）的 | - positive/run_logs: contains `"ref=refs/heads/"` — actual log contains `"ref=main"`（不含 `refs/heads/ |  | 27-31 | 平台 → `atomgit.ref` 返回短引用名 `main` → 日志中不含 `refs/heads/` → 测试断言包含匹配失败 | 是（使用 `atomgit.ref_name` 获取短名、或拼接 `refs/heads/${{ a |
| 150 | USE-CTX-01-002 | usability | 平台缺陷 | 平台方 | 高（日志直接证明 github.ref 静默求值为 plac | 🔴 GitHub Actions 迁移用户引用 `githu | 🔴 完全静默 — 无任何错误、警告或提示 | 🔴 所有从 GitHub Actions 迁移的 workflow（`githu | - negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝 `github.ref`） - nonfunctional/ |  | 9-21 | 平台 → `github.ref` 静默求值为 `placeholder_ref` → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败 | 否（用户不知道 github 上下文不被支持，且无反馈机制告知） |
| 151 | USE-DISP-01-002 | usability | 平台缺陷 | 平台方 | 高（job 直接 FAILED 未进入任何 step；日志极 | 🔴 所有包含有 default 值 input 的 work | 🟡 job 状态为 FAILED 可见，但无任何错误消息说明 | 🔴 所有使用 workflow_dispatch inputs + defaul | - positive/run_logs: contains `"env=staging"` — job 在 step 执行前已失败，日志不含任何表达式输出 |  | 54-67 | 平台 → workflow_dispatch 触发时未传 params → inputs 解析失败 → job 在 setup 阶段直接标记 FAILED → 测试断言 positive/run_lo | 是（手动触发时总是显式传入所有 input 参数值；但这违背了 default 的设计目的） |
| 152 | USE-ENV-01-002 | usability | 平台缺陷 | 平台方 | 高（日志仅含 bash 级的 "unbound variab | 🟡 使用 `$GITHUB_SHA` 等 GitHub 变量 | 🟡 脚本因 `set -u` 终止有明确错误输出，但完全无平 | 🟡 从 GitHub Actions 迁移的 workflow（`$GITHUB | - nonfunctional/error_message: rubric "日志警告是否足够醒目且包含有效指引：应提示 GITHUB_* 环境变量在 GitCode 中对应为 ATOMGIT_*"  |  | 124-138 | 平台 → 环境中无 `GITHUB_SHA` 变量 → `set -u` 触发 bash 错误 → 进程退出码 1 → job FAILED → 测试断言 error_message rubric 不 | 是（手动替换 `GITHUB_*` → `ATOMGIT_*`；但用户需要从文档中主动发现这个差异） |
| 153 | USE-EXPR-01-001 | usability | 平台缺陷 | 平台方 | 高（日志直接证明 undefined property 静默 | 🔴 用户使用不存在的上下文属性（拼写错误、迁移遗留等）不会得 | 🔴 完全静默 — 无任何错误、警告 | 🔴 所有 workflow — 对任何上下文属性的拼写错误都无校验 | - negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝未定义属性） - nonfunctional/error_me |  | 25-48 | 平台 → `atomgit.nonexistent_property` 静默求值为 `""` → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败 | 否（用户无法区分"属性不存在返回空"和"属性值为空"） |
| 154 | USE-EXPR-01-002 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 155 | USE-INPT-01-002 | usability | 平台缺陷 | 平台方 | 高（日志直接证明 boolean 类型被静默接受；规格明确仅 | 🟡 使用 boolean 类型的 workflow 可以运行 | 🔴 完全静默 — 无任何类型校验警告 | 🟡 从 GitHub Actions 迁移的 workflow（GitHub 支 | - negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝 boolean 类型） - nonfunctional/er |  | 54-67 | 平台 → 跳过 inputs type 校验 → boolean 静默降级为 string → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败 | 是（手动将所有 input type 改为 string，并在条件表达式中用 `== 'true'` |
| 156 | USE-LBL-01-001 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 157 | USE-LOG-01-001 | usability | 用例问题 | Phase 01 | 中（断言将 UI 展示特征（step name）映射到 ra | 🟢 不影响功能性 — 5 个 step 全部成功执行且输出正 | 🟢 无静默问题 — step 输出清晰可见 | 🟢 仅影响测试断言层，不影响平台功能 | - positive/run_logs: contains `"step one prepare"` — raw log 中不含 step 名称，仅含 step 的 run 命令输出 - nonfun |  | 15-34 | 测试断言检查 `run_logs` 包含 `"step one prepare"` → raw log 中不含 step `name` 字段文本 → 包含匹配失败 | 是（将断言目标从 `run_logs` 改为 UI DOM 检测或不检查 step name 文本） |
| 158 | USE-MASK-01-001 | usability | API调用失败(WAF) | 平台方 |  |  |  |  |  |  |  |  |  |
| 159 | USE-NEST-01-001 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 160 | USE-NEST-01-002 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 161 | USE-OS-01-001 | usability | 平台缺陷 | 平台方 | 高（日志直接输出 `os=linux`；规格明确列出 `Li | 🟡 如果用户依赖 `${{ runner.os == 'Li | 🟡 runner.os 返回了值，但值与文档声明不一致 | 🟡 所有依赖 `runner.os` 做条件判断或矩阵选择的 workflow | - positive/run_logs: contains `"os=Linux"` — actual log contains `"os=linux"`（小写 l） |  | 209-228 | 平台 → `runner.os` 返回 `linux`（lowercase） → 日志输出 `os=linux` → 测试断言 contains `"os=Linux"` 匹配失败 | 是（使用 `${{ runner.os == 'linux' }}` 小写比较；但用户只能通过试错发 |
| 162 | USE-PERM-01-002 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 163 | USE-RUN-01-002 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 164 | USE-SECNAME-01-001 | usability | 平台缺陷 | 平台方 | 高（日志显示 secret 值被脱敏输出 `***` 说明系 | 🟡 用户自己创建名为 `ATOMGIT_TOKEN` 的 s | 🔴 完全静默 — workflow 正常运行，但使用的 se | 🟡 所有使用了 ATOMGIT_ 前缀自定义 secret 的项目（安全敏感场景 | - negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝 `ATOMGIT_TOKEN` 作为 secret 名称）  |  | 43-47 | 平台 → `ATOMGIT_TOKEN` 未被拒绝 → 系统 token 值被注入 → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败 | 否（用户不知道自己的 secret 被系统值覆盖，且无反馈） |
| 165 | USE-STAT-01-002 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 166 | USE-TYPE-01-002 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 167 | USE-UNKN-01-001 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 168 | USE-YAML-01-001 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |
| 169 | USE-YAML-01-002 | usability | 平台 schema 校验不通过 | Phase 01 |  |  |  |  |  |  |  |  |  |

---

## 二、归因汇总

### 2.1 分类统计

| 根因 | 数量 | 占比 |
|---|---|---|
| 平台缺陷 | 31 | 18% |
| 标记不匹配 | 30 | 18% |
| 四括号模板缺陷 | 3 | 2% |
| 用例问题 | 11 | 7% |
| 环境/Harness | 19 | 11% |
| 平台行为偏差 | 2 | 1% |
| 平台 schema 校验不通过 | 66 | 39% |
| API调用失败(WAF) | 7 | 4% |
| **总计** | **169** | **100%** |

### 2.2 按维度分布

| 维度 | 平台缺陷 | 标记不匹配 | 四括号模板缺陷 | 用例问题 | 环境/Harness | 平台行为偏差 | 平台 schema 校验不通过 | API调用失败(WAF) | 总计 |
|---|---|---|---|---|---|---|---|---|---|---|
| completeness | 8 | 8 | 0 | 0 | 0 | 0 | 12 | 2 | **30** |
| compatibility | 4 | 19 | 0 | 0 | 0 | 0 | 29 | 2 | **54** |
| reliability | 9 | 0 | 3 | 3 | 9 | 0 | 5 | 2 | **31** |
| security | 1 | 3 | 0 | 7 | 10 | 2 | 8 | 0 | **31** |
| usability | 9 | 0 | 0 | 1 | 0 | 0 | 12 | 1 | **23** |

### 2.3 按责任人分布

| 责任人 | 平台缺陷 | 标记不匹配 | 四括号模板缺陷 | 用例问题 | 环境/Harness | 平台行为偏差 | 平台 schema 校验不通过 | API调用失败(WAF) | 总计 |
|---|---|---|---|---|---|---|---|---|---|---|
| Phase 01 | 0 | 3 | 3 | 11 | 0 | 1 | 66 | 0 | **84** |
| Phase 02 | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | **19** |
| 平台方 | 29 | 27 | 0 | 0 | 0 | 0 | 0 | 7 | **63** |
| 多方联合 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | **3** |

### 2.4 合并视图——消除假阳性后的实际通过率

| 场景 | PASS (of 169) | FAIL | 通过率 |
|---|---|---|---|
| 原始报告 | 0 | 169 | 0% |
| 消除 schema 校验不通过（66条） | 66 | 103 | 39% |
| 消除 schema + WAF（73条） | 73 | 96 | 43% |
| 消除 schema + WAF + 标记不匹配（103条） | 103 | 66 | 61% |
| 消除所有非平台因素（136条） | 136 | 33 | 80% |
| **需平台修复的真实缺陷** | — | **33** | — |

---

## 三、影响汇总

### 3.1 三维度统计

| 指标 | 类别 | 数量 | 说明 |
|---|---|---|---|
| 阻塞性 | 🔴阻塞 | 18 | 功能完全不可用或测试无法执行 |
| | 🟡中等 | 16 | 功能部分可用或测试未充分覆盖 |
| | 🟢不阻塞 | 34 | 功能正常，仅断言/标签不匹配 |
| | 未标注 | 101 | schema 校验不通过/WAF 等预执行失败 |
| 静默性 | 🔴高度静默 | 14 | 无任何错误/警告，用户完全无感知 |
| | 🟡可察觉 | 52 | 有可见错误但可能被忽略 |
| | 🟢明确报错 | 11 | 有清晰的错误信息 |
| | 未标注 | 92 | — |
| 影响面 | 🔴跨维度 | 10 | 影响多条测试或多功能维度 |
| | 🟡局部 | 62 | 仅影响单一用例或功能点 |
| | 🟢单点 | 1 | 影响极小 |
| | 未标注 | 96 | — |

### 3.2 核心发现

- **最大一类：平台 schema 校验不通过（66条, 39%）** — workflow YAML 在平台入口被拒，测试未执行
- **平台缺陷（33条, 20%）** — 需平台方修复的真实 bug
- **标记不匹配（30条, 18%）** — 断言词汇与平台状态值不一致，功能本身正常
- **环境/Harness（19条, 11%）** — 测试环境问题（token 未注入、runner 不可用、故障注入未生效等）
- **用例问题（14条）** — 测试 YAML 或用例设计需修正
- **WAF 拦截（7条）** — API 调用被 WAF 阻断，非测试问题

### 3.3 按维度影响分布

| 维度 | 平台缺陷 | 标记不匹配 | 四括号缺陷 | 用例问题 | 环境/Harness | 行为偏差 | Schema不通过 | WAF | 总计 |
|---|---|---|---|---|---|---|---|---|---|
| completeness | 8 | 8 | 0 | 0 | 0 | 0 | 12 | 2 | 30 |
| compatibility | 4 | 19 | 0 | 0 | 0 | 0 | 29 | 2 | 54 |
| reliability | 9 | 0 | 3 | 3 | 9 | 0 | 5 | 2 | 31 |
| security | 1 | 3 | 0 | 7 | 10 | 2 | 8 | 0 | 31 |
| usability | 9 | 0 | 0 | 1 | 0 | 0 | 12 | 1 | 23 |

### 3.4 规避手段统计

| 规避手段 | 数量 | 占比 |
|---|---|---|
| 有规避手段 | 78 | 46% |
| 无规避手段（需平台修复） | 18 | 11% |
| 未标注/不适用 | 73 | 43% |

---

## 四、系统性发现

### 4.1 run_status 词汇映射缺失

| 模式 | 数量（估） | 示例 |
|---|---|---|
| 断言 `success` / `completed(success)` ≠ 平台 `COMPLETED` | ~25 | COMP-DIR-01-001, REL-CONC-01-001, COMPAT-ENV-01-001... |
| 断言 `failure` ≠ 平台 `FAILED` (大小写) | ~3 | COMPAT-EXPR-01-003, COMPAT-IF-01-001, COMPAT-OUTCOME-01-001 |
| 断言 `canceled` ≠ 平台 `CANCELED` | ~1 | REL-CANCEL-01-028 |

**根因**: 合约 rubric 使用人类语义词汇，平台 API 返回大写枚举值。`compile_asserts.py` 缺少平台值→语义值的映射表。
**修复预估**: `COMPLETED→success, FAILED→failure, CANCELED→canceled, IGNORED→skipped` 四行映射即可。

### 4.2 空格 vs 下划线——系统性缺陷

| 合约期望（下划线） | 日志实际（空格） | 用例 |
|---|---|---|
| `cleaned_as_expected` | `cleaned as expected` | SEC-RUN-01-001 |
| `isolated_as_expected` | `isolated as expected` | SEC-RUN-01-002 |
| `access_denied_or_timeout` | `access denied or timeout` | SEC-NET-01-001 |
| `push_denied_or_403` | `push denied as expected` | SEC-PERM-01-004 |
| `masked_or_not_found` | `masked or not found` | SEC-NAME-01-002 |

**根因**: 合约编写者用下划线连词，shell `echo` 自然输出空格。编译器应在提取关键词时归一化处理。

### 4.3 `${{{{ }}}}` 四括号——合约生成缺陷

共 **3 条** 因 bash `bad substitution` 失败：
- REL-ARTCONC-01-063: `${{{{ matrix.instance }}}}`
- REL-MATRIX-01-038: `${{{{ matrix.os }}}}`（20 jobs 全 FAIL）
- REL-MATRIX-01-039: `${{{{ matrix.v1 }}}}`（50 jobs 全 FAIL）
- REL-OUTPUT-01-016: `${{{{ steps.writer.outputs.data }}}}`

**根因**: 合约生成时将表达式包裹了过多括号层（四层 vs 两层 `${{ }}`），bash 无法解析。

### 4.4 确认真实平台缺陷（P0 + P1）

#### P0 高价值缺陷

| 用例 | 缺陷 | 影响 |
|---|---|---|
| COMPAT-DIR-01-002 | `.github/workflows/` 被错误识别并触发 | 安全边界破坏 |
| REL-YAMLCACHE-01-060 | YAML 修改后缓存未失效，执行旧版 workflow | SECURITY_CRITICAL |
| SEC-DOS-01-001 | 1.1GB 制品未被配额拒绝 | DoS 攻击面 |
| USE-CONC-01-001 | `concurrency.max: 10` 非法值静默接受 | 用户无感知 |
| USE-SECNAME-01-001 | `ATOMGIT_` 前缀 secret 名被接受（违反文档命名规则） | secret 值冲突 |
| USE-INPT-01-002 | `type: boolean` 被静默接受并转换（文档仅支持 string） | 类型语义错误 |
| USE-EXPR-01-001 | `atomgit.nonexistent_property` 解析为空串而非报错 | 拼写错误无反馈 |
| USE-CTX-01-002 | `github.ref` 被解析为占位符而非引导至 atomgit | 迁移用户困惑 |
| USE-CTX-01-001 | `atomgit.ref` 返回 `main` 而非 `refs/heads/main` | 条件判断恒false |
| USE-OS-01-001 | `runner.os` 返回 `linux`（小写）而非文档声明的 `Linux` | 条件判断恒false |
| USE-ENV-01-002 | `GITHUB_SHA` 未定义导致 bash 错误，无平台指引 | 迁移成本高 |
| USE-DISP-01-002 | workflow_dispatch inputs default 值未生效导致 job 直接 FAILED | 阻塞性缺陷 |

#### P1 常规缺陷

| 用例 | 缺陷 |
|---|---|
| COMP-ARTIFACT-01-002/003 | artifact 上传/下载失败（job FAILED 无执行） |
| COMP-CACHE-01-001/002 | cache action 完全不可用（无步骤执行） |
| COMP-CALL-01-001 | workflow_call 嵌套失败 |
| COMP-SECRET-01-001 | secret 值为空/截断 |
| COMPAT-ARTIFACT-01-001 | 跨 job artifact 名称冲突 |
| COMPAT-CACHE-01-001 | cache 在 workflow_dispatch 事件下不工作 |
| SEC-CACHE-01-002 | cache action Event Validation 拒绝 workflow_dispatch |
| SEC-MASK-01-001 | secret 掩码 `***` 未完全生效 |
| REL-FAULT-01-031/032/033 | 故障注入（SIGKILL/网络分区/磁盘满）全未生效 |
| REL-TIMEOUT-01-007/008/009/010 | timeout-minutes 边界行为被平台提前 cancel 覆盖 |
| REL-NEEDS-01-025 | job_b 依赖失败后状态 IGNORED 而非 skipped |
| REL-CONTINUE-01-030 | continue-on-error 后 workflow_status 判定逻辑问题 |
| REL-ART-01-041 | artifact 同名冲突导致上传失败 |
| REL-ARTPERF-01-053-V2 | Namespace artifact quota 超限（1074MB > 1024MB） |

### 4.5 失败传导链统计

| 传导模式 | 数量 |
|---|---|
| 其他传导模式 | 28 |
| Job COMPLETED → 断言期望不匹配 → FAIL | 8 |
| 上游FAILED → 下游IGNORED | 5 |
| 平台cancel → CANCELED → 断言失败 | 5 |
| YAML语法错误 → 全job FAILED | 4 |
| Token缺失 → 401 → job FAILED | 4 |
| Runner不可用 → Job无法调度 → FAILED | 3 |
| Secret未注入 → 值空 → 断言无法验证 | 3 |
| Log收集不全 → 无法验证 → 断言失败 | 2 |

### 4.6 日志否认的先前判定

| 用例 | 之前判为 | 日志证实 | 修正为 |
|---|---|---|---|
| SEC-INJ-01-005 | 双重模板注入 SECURITY_CRITICAL | bash `bad substitution`，`"2"` 是源文本子串假阳性 | 用例问题（表达式嵌套写法） |
| REL-FAULT-01-031 | SIGKILL 日志泄漏 SECURITY_CRITICAL | 5 个 step 全正常执行，**SIGKILL 从未发生** | 环境/Harness（故障注入不工作） |
| SEC-NET-01-001 | Runner SSRF SECURITY_CRITICAL | `access denied or timeout` — **SSRF 防护工作正常** | 平台行为偏差（空格vs下划线） |

---

## 五、建议回流 Phase 01 评审

### 5.1 紧急修复（合约生成模板）

1. **四括号 `${{{{ }}}}` ** — 合约生成器中表达式变量替换逻辑需修复，保证仅产出 `${{ }}` 两层花括号
2. **run_status 词汇映射表** — `compile_asserts.py` 添加映射: `COMPLETED→success, FAILED→failure, CANCELED→canceled, IGNORED→skipped`
3. **空格/下划线归一化** — 合约编译器需在提取关键词时对 shell echo 输出做下划线/空格归一化处理

### 5.2 Schema 校验不通过（66 条，39%）

66 个 workflow YAML 在平台入口被 schema 校验拒绝，主要原因：
- `stages` 字段可见但 `jobs` 字段未被包含在对应 stage 中
- 触发事件类型不被平台识别（如 `pull_request_target`）
- 部分字段格式与平台 schema 不兼容

**建议**: 在合约生成后增加平台 schema 预校验步骤，或对齐合约生成模板与平台 schema 规范。

### 5.3 用例设计改进

1. **secret/token 注入前置** — SEC-MASK/SEC-NAME/SEC-DEFPERM 系列需确保 workflow_dispatch 事件下 secret 正常注入
2. **matrix 维度对齐** — REL-MATRIX-01-027 文本描述 3x3=9 组合，YAML 仅 1维3值
3. **artifact 命名去重** — REL-ART/ARTPERF/SEC-SIDE 需使用唯一名称或前置清理
4. **commit message 注入测试** — SEC-INJ-01-004 需显式推送含特殊字符的 commit
5. **git config 前置** — SEC-PERM-01-004 需先配置 user.email/user.name

### 5.4 平台修复优先级建议

| 优先级 | 用例 | 问题 | 影响 |
|---|---|---|---|
| **P0** | COMPAT-DIR-01-002 | `.github/` 目录被错误触发 | 安全边界破坏 |
| **P0** | REL-YAMLCACHE-01-060 | YAML 缓存未失效 | SECURITY_CRITICAL |
| **P0** | SEC-DOS-01-001 | 1.1GB 制品无配额拒绝 | DoS 风险 |
| **P0** | USE-SECNAME-01-001 | ATOMGIT_ 前缀被接受 | secret 值被系统覆盖 |
| **P1** | USE-CTX-01-002 | github.ref 静默占位符 | 迁移用户无反馈 |
| **P1** | USE-CTX-01-001 | atomgit.ref 返回短名 | 条件判断错误 |
| **P1** | USE-EXPR-01-001 | undefined 属性静默求值空串 | 拼写错误无感知 |
| **P1** | USE-OS-01-001 | runner.os 返回值小写 | 文档不一致 |
| **P1** | USE-DISP-01-002 | inputs default 值未生效 | 阻塞性功能缺陷 |
| **P1** | USE-CONC-01-001 | concurrency.max 非法值静默接受 | 用户无感知 |
| **P1** | USE-INPT-01-002 | boolean 类型静默接受 | 类型安全缺失 |
| **P1** | USE-ENV-01-002 | GITHUB_SHA 无平台指引 | 迁移成本高 |

---

*分析完成时间: 2026-07-24 · 案例源: failure/2026-07-24/case/*.md · 169/169 条覆盖*