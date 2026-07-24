## 失败分诊 · COMP-CACHE-01-002 · restore-keys 前缀匹配兜底生效

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 2 行）:
```
  === JOB: Verify restore keys fallback (status=FAILED) ===
  [2026/07/23 22:02:27.919 GMT+08:00] [INFO] Job(1529971987059707904_1529971987034542087) duration check: true
```

- **预期行为**（Phase 01 文本用例 `COMP-CACHE-01-002`，优先级 P0，维度 completeness）:
  - 前置条件: - 之前运行已生成前缀匹配的 cache
  - 操作步骤: 1. 触发 workflow，精确 key 不匹配但 restore-keys 前缀匹配
  - 预期结果: - restore-keys 前缀匹配成功，恢复最近同前缀缓存
  - 验证点: - [正向] cache 步骤通过 restore-keys 命中

- **实际行为**:
  - Job "Verify restore keys fallback" status=FAILED

- **对照 GitCode 规格**:
  - 文本用例参照来源: `inputs/gitcode-spec/`

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 之前运行已生成前缀匹配的 cache

**置信度**: 高（job status=FAILED，平台执行层明确故障）

**影响**:
- **阻塞性**: 🔴阻塞 — job FAILED 导致功能不可用
- **静默性**: 🟡可察觉 — status=FAILED，但 shell 诊断输出有限
- **影响面**: 🔴跨维度 — 平台核心功能故障
- **综合**: 基于上述证据，COMP-CACHE-01-002 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 否 — 平台功能缺陷

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-CACHE-01-002.log`
- 修复后重新验跑 COMP-CACHE-01-002
- 相关用例: COMP-CACHE-01-001
