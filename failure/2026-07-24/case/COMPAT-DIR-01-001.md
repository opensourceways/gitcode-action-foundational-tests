## 失败分诊 · COMPAT-DIR-01-001 · 工作流目录差异——.gitcode/workflows/ 正常识别

**判定结果**: FAIL
**失败断言**:
assertions (.gitcode dir) — job COMPLETED，GITCODE_DIR_RECOGNIZED_OK 正确输出

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（共 6 行）:
```
  === JOB: Verify .gitcode workflows dir (status=COMPLETED) ===
  [2026/07/23 22:17:42.925 GMT+08:00] [INFO] Job(1529975825048813568_1529975825011064839) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/597789f8-f4eb-4c9d-b32d-5f1d73680286.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/597789f8-f4eb-4c9d-b32d-5f1d73680286.sh
  GITCODE_DIR_RECOGNIZED_OK
```

- **预期行为**（Phase 01 文本用例 `COMPAT-DIR-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: - 仓库已创建 .gitcode/workflows/ 目录
  - 操作步骤: 1. 在 .gitcode/workflows/ci.yml 中创建工作流定义
    2. 提交并推送到仓库
    3. 触发对应事件，验证工作流被正确识别和执行
  - 预期结果: - .gitcode/workflows/ 下的 .yml 文件被平台识别为有效工作流
    - 对应事件触发时工作流正常执行
    - 此行为与 GitCode 官方文档一致
  - 验证点: - [正向] .gitcode/workflows/*.yml 被正确识别
    - [正向] 对应事件触发后工作流正常执行
    - [负向] 不应出现 .gitcode 目录下文件被忽略的情况

- **实际行为**:
  - Job "Verify .gitcode workflows dir" status=COMPLETED

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
  - Phase 01 前置条件: - 仓库已创建 .gitcode/workflows/ 目录

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-DIR-01-001 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-DIR-01-001 的判断逻辑
- 相关用例: COMPAT-DIR-01-002
