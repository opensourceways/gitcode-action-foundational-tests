## 失败分诊 · COMP-ISOLATION-01-002 · 环境变量不跨 job 泄漏

**判定结果**: FAIL
**失败断言**:
assertions — 两个 job 均 COMPLETED，ISOLATION_STRONG: marker not visible across jobs
断言评判器未解析 'ISOLATION_STRONG' / 'MARKER_CREATED' 为 PASS

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（共 14 行）:
```
  === JOB: Create tmp isolation marker (status=COMPLETED) ===
  [2026/07/23 22:02:49.185 GMT+08:00] [INFO] Job(1529972076444266496_1529972076419100679) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/7a47315a-85d1-414b-a441-7f632dade35f.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/7a47315a-85d1-414b-a441-7f632dade35f.sh
  MARKER_CREATED
  
  
  === JOB: Check tmp marker isolation (status=COMPLETED) ===
  [2026/07/23 22:03:02.555 GMT+08:00] [INFO] Job(1529972076444266496_1529972076419100681) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/b9bb0e2f-6080-4973-948c-712c5f45dde7.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/b9bb0e2f-6080-4973-948c-712c5f45dde7.sh
  ISOLATION_STRONG: marker not visible across jobs
```

- **预期行为**（Phase 01 文本用例 `COMP-ISOLATION-01-002`，优先级 P0，维度 completeness）:
  - 前置条件: - workflow 含两个串行 jobs
  - 操作步骤: 1. job 1 设置环境变量
    2. job 2 检查该环境变量
  - 预期结果: - job 2 不应看到 job 1 设置的环境变量
  - 验证点: - [负向] job 2 中环境变量值为空或未设置

- **实际行为**:
  - Job "Create tmp isolation marker" status=COMPLETED
  - Job "Check tmp marker isolation" status=COMPLETED
  - ISOLATION_STRONG: marker not visible across jobs

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md`:
  - 规格摘要:
    ```
# Variables, Secrets, Context and Expressions
AtomGit Action provides a four-level variable system using `env`, `vars`, `secrets`, and `inputs`, enabling flexible workflow configuration through context (primarily `atomgit`) and expressions (`${{ expression }}`).
## Four-Level Variable System
| Type | Suitable For | Sensitive | Reference Method |
|------|-------------|-----------|-------------------|
| `env` | Temporary variables within workflow | No | `$VAR_NAME` or `${{ env.VAR }}` |
| `vars` | Repository/organization-level regular variables | No | `${{ vars.VAR }}` |
| `secrets` | Passwords,
    ```
  - 测试 YAML 工作流模式与此规格承诺一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - workflow 含两个串行 jobs

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMP-ISOLATION-01-002 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMP-ISOLATION-01-002 的判断逻辑
- 相关用例: COMP-ISOLATION-01-001
