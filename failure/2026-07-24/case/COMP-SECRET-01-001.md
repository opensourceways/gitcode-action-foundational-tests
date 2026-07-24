## 失败分诊 · COMP-SECRET-01-001 · echo secret 在日志中被脱敏为 ***

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_logs contains '***') — 期望日志含 `***`，实际 `secret is ` 后为空
assertions[1] (negative, must_not_contain_secret) — secret 未注入 runner 环境，无法验证脱敏

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（共 6 行）:
```
  === JOB: Verify secret masking (status=COMPLETED) ===
  [2026/07/23 22:03:21.266 GMT+08:00] [INFO] Job(1529972211043930112_1529972211014569991) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/d837651f-6cb6-4f17-b045-9a016dffd523.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/d837651f-6cb6-4f17-b045-9a016dffd523.sh
  secret is
```

- **预期行为**（Phase 01 文本用例 `COMP-SECRET-01-001`，优先级 P0，维度 completeness）:
  - 前置条件: - 仓库配置了 secret TEST_SECRET
  - 操作步骤: 1. 在 workflow 中执行 echo ${{ secrets.TEST_SECRET }}
    2. 查看运行日志
  - 预期结果: - 日志中 secret 值显示为 ***
  - 验证点: - [正向] 日志中包含 *** 而非真实 secret 值

- **实际行为**:
  - Job "Verify secret masking" status=COMPLETED
  - `secret is ` 后为空，TEST_SECRET 未注入 runner 环境

- **对照 GitCode 规格**:
  - 文本用例参照来源: `inputs/security-knowledge/issues.md; inputs/github-reference/security/`

- **环境前置条件验证**:
  - setup.secrets: `['TEST_SECRET']`
  - setup.repo_fixture: `with-secrets`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库配置了 secret TEST_SECRET

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMP-SECRET-01-001 的失败根因初步判定为 **环境问题**（责任人: **Phase 02**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMP-SECRET-01-001 的判断逻辑
- 在 Phase 02 补充环境配置（config_probe、secret 注入、event 匹配等）
