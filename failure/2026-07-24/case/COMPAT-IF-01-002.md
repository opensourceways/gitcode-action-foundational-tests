## 失败分诊 · COMPAT-IF-01-002 · continue-on-error 标记后失败 step 不阻断后续执行

**判定结果**: FAIL
**失败断言**:
assertions (continue-on-error) — job COMPLETED，'exit code 1' + 'This should appear' 正确，断言检查 outcome/conclusion

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（共 11 行）:
```
  === JOB: Test continue on error (status=COMPLETED) ===
  [2026/07/23 22:21:22.562 GMT+08:00] [INFO] Job(1529976746424537088_1529976746403565575) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/50a9cce2-d74a-4d72-b24f-f866c81d9e54.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/50a9cce2-d74a-4d72-b24f-f866c81d9e54.sh
  ::error::Process exited with code 1
  
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0ad931c3-77b7-4f35-b78a-1b196294457d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0ad931c3-77b7-4f35-b78a-1b196294457d.sh
  This should appear
```

- **预期行为**（Phase 01 文本用例 `COMPAT-IF-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: - 仓库已启用 GitCode Action
  - 操作步骤: 1. 提交一个包含两个 step 的 workflow
    2. 第一个 step 显式返回非零退出码，但设置 continue-on-error 为 true
    3. 第二个 step 输出一条消息
    4. 手动触发该 workflow
  - 预期结果: - 第一个 step 虽失败，但因 continue-on-error 标记，后续 step 仍继续执行
    - job 整体状态可能为成功或特殊标记，但不因该失败而中断
  - 验证点: - [正向] 第二个 step 成功执行并输出消息
    - [正向] 第一个 step 的失败后，后续 step 未被跳过
    - [正向] job 未在第一个 step 处中断

- **实际行为**:
  - Job "Test continue on error" status=COMPLETED

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/workflow-job-step-action.md`:
  - 规格摘要:
    ```
# 工作流、任务、步骤和 Action
AtomGit Action 的执行模型遵循清晰的层级链：
```
Event → Workflow → Stages → Jobs → Runner → Steps → Scripts / Actions
```
当特定 **Event（事件）** 触发后，系统加载对应的 **Workflow（工作流）** 定义文件，按 **Stages（阶段）** 顺序串行推进，每个 Stage 内的 **Jobs（任务）** 默认并行执行，每个 Job 被分配到一台 **Runner（运行器）** 上，Job 内的 **Steps（步骤）** 串行依次运行。
## Workflow（工作流）
Workflow 是自动化流程的顶层定义，存储在仓库的 `.gitcode/workflows/` 目录下，以 YAML 格式描述。
```yaml
name: Build and Deploy
on:
push:
branches: [main]
stages:
- build
    ```
  - 测试 YAML 工作流模式与此规格承诺一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库已启用 GitCode Action

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-IF-01-002 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-IF-01-002 的判断逻辑
- 相关用例: COMPAT-IF-01-001
