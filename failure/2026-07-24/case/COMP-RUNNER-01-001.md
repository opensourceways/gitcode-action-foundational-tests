## 失败分诊 · COMP-RUNNER-01-001 · 三段式标签正确调度到对应规格 Runner

**判定结果**: FAIL
**失败断言**:
assertions (positive, runner label) — job COMPLETED，'os=linux' 'arch=x86_64' 正确输出

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（共 7 行）:
```
  === JOB: Verify 3 segment label (status=COMPLETED) ===
  [2026/07/23 22:14:06.404 GMT+08:00] [INFO] Job(1529974916940435456_1529974916919463943) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/6349b2ff-42a6-4407-bdac-e3908cc479dc.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/6349b2ff-42a6-4407-bdac-e3908cc479dc.sh
  os=linux
  arch=x86_64
```

- **预期行为**（Phase 01 文本用例 `COMP-RUNNER-01-001`，优先级 P1，维度 completeness）:
  - 前置条件: - 平台存在对应三段式标签的 Runner
  - 操作步骤: 1. 配置 runs-on: [ubuntu-latest, x64, small]
    2. 触发 workflow
  - 预期结果: - job 被调度到符合标签的 Runner
    - 运行成功
  - 验证点: - [正向] 运行状态为 success
    - [正向] job 的 Runner 标签与声明一致

- **实际行为**:
  - Job "Verify 3 segment label" status=COMPLETED

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/runner-management/selecting-runner-labels.md`:
  - 规格摘要:
    ```
# 选择 Runner 标签
## 配置说明
### 标签类型对照
| Runner 类型 | 标签格式 | 示例 |
|-----------|---------|------|
| 官方托管 | 三段式 `{os},{arch},{spec}` 或组合标签 | `{ubuntu-24,x64,small}` |
| 官方托管（默认） | `default` | `default`（等效 [ubuntu-latest, x64, small]） |
| 自托管 | `self-hosted` + 自定义标签 | `[self-hosted, linux, gpu]` |
### 匹配规则
`runs-on` 中的所有标签必须同时存在于 Runner 的标签集合中，才视为匹配。
```yaml
# 选择 Runner 标签
# ✅ 匹配
runs-on: [self-hosted, linux, x64]
# ✅ 匹配
    ```
  - 测试 YAML 工作流模式与此规格承诺一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 平台存在对应三段式标签的 Runner

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMP-RUNNER-01-001 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMP-RUNNER-01-001 的判断逻辑
