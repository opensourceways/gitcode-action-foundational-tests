## 失败分诊 · COMPAT-DIR-01-002 · 工作流目录差异——.github/workflows/ 不应被识别

**判定结果**: FAIL
**失败断言**:
assertions (.github dir ignored) — job COMPLETED，但 GITHUB_DIR_WORKFLOW_RAN 表明 .github 下 workflow 被非预期执行
平台未隔离 GitHub Actions 目录 .github/workflows，与兼容性规范不符

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 6 行）:
```
  === JOB: Verify .github workflows dir ignored (status=COMPLETED) ===
  [2026/07/23 22:17:47.119 GMT+08:00] [INFO] Job(1529975842702766080_1529975842677600263) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/59368d05-2ae4-4cc8-a813-3504c1bbe144.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/59368d05-2ae4-4cc8-a813-3504c1bbe144.sh
  GITHUB_DIR_WORKFLOW_RAN
```

- **预期行为**（Phase 01 文本用例 `COMPAT-DIR-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: - 仓库已创建 .github/workflows/ 目录
    - 该目录下存在工作流定义文件
  - 操作步骤: 1. 在 .github/workflows/ci.yml 中创建工作流定义
    2. 同时确保 .gitcode/workflows/ 下无同名工作流
    3. 提交并推送到仓库，触发对应事件
    4. 观察平台是否识别并执行 .github/workflows/ 下的工作流
  - 预期结果: - .github/workflows/ 下的工作流文件不被 GitCode 平台识别
    - 对应事件触发时，该目录下的工作流不会执行
    - 平台优先且仅识别 .gitcode/workflows/ 目录
  - 验证点: - [负向] .github/workflows/ 下的工作流不应被触发执行
    - [正向] 平台应仅识别 .gitcode/workflows/ 目录
    - [正向] 事件触发后不应出现来自 .github 目录的意外运行记录

- **实际行为**:
  - Job "Verify .github workflows dir ignored" status=COMPLETED
  - .github/workflows 下 workflow 被非预期执行（GITHUB_DIR_WORKFLOW_RAN）

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
  - setup.repo_fixture: `with-github-dir`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库已创建 .github/workflows/ 目录
    - 该目录下存在工作流定义文件

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-DIR-01-002 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-DIR-01-002 的判断逻辑
- 相关用例: COMPAT-DIR-01-001
