## 失败分诊 · COMPAT-DIR-01-002 · 工作流目录差异——.github/workflows/ 不应被识别

**判定结果**: FAIL
**失败断言**: 

**根因初判**: 产品bug

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

  **日志分析**: "GITHUB_DIR_WORKFLOW_RAN" FOUND — 平台错误触发了 .github/workflows/, 安全边界破坏

- **预期行为**（Phase 01 文本用例 `COMPAT-DIR-01-002`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在 .github/workflows/ci.yml 中创建工作流定义"
  - 操作步骤 2: "同时确保 .gitcode/workflows/ 下无同名工作流"
  - 操作步骤 3: "提交并推送到仓库，触发对应事件"
  - 操作步骤 4: "观察平台是否识别并执行 .github/workflows/ 下的工作流"

  预期结果:
  - .github/workflows/ 下的工作流文件不被 GitCode 平台识别
  - 对应事件触发时，该目录下的工作流不会执行
  - 平台优先且仅识别 .gitcode/workflows/ 目录

  验证点:
  - [负向] .github/workflows/ 下的工作流不应被触发执行
  - [正向] 平台应仅识别 .gitcode/workflows/ 目录
  - [正向] 事件触发后不应出现来自 .github 目录的意外运行记录

- **实际行为**:
  - "GITHUB_DIR_WORKFLOW_RAN" FOUND — 平台错误触发了 .github/workflows/, 安全边界破坏


- **测试 YAML 与规格精确对照**:
  - 规格文件: `workflow-file-location-structure.md` (路径: `phase01/inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md`)
  - 规格节选:
```yaml
# .gitcode/workflows/<workflow-name>.yml 目录
# 仅 .yml 和 .yaml 后缀的文件会被识别
```
    该规格明确声明: 37-41行明确规定 `.gitcode/workflows/` 为 workflow 文件存放目录

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"GITHUB_DIR_WORKFLOW_RAN" FOUND — 平台错误触发了 .github/workflows/, 安全边界破坏）

**建议**:
- 将此缺陷提交给平台工程团队，附上日志文件 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-DIR-01-002.log`
- 建议修复后重新验跑 COMPAT-DIR-01-002
- 相关用例: COMPAT-DIR-01-001
