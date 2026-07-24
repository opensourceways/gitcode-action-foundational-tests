## 失败分诊 · COMPAT-RUNSON-01-001 · runs-on 标签体系——三段式数组正常匹配

**判定结果**: FAIL
**失败断言**:
assertions (runs-on array) — job COMPLETED，RUNSON_ARRAY_OK，Runner labels: dedicate-hosted x64 large

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（共 7 行）:
```
  === JOB: Verify three-part runs-on array (status=COMPLETED) ===
  [2026/07/23 22:23:59.912 GMT+08:00] [INFO] Job(1529977405961936896_1529977405928382471) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0e2eff48-33b4-4714-afd2-7d43714c9b48.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0e2eff48-33b4-4714-afd2-7d43714c9b48.sh
  RUNSON_ARRAY_OK
  Runner labels: dedicate-hosted x64 large
```

- **预期行为**（Phase 01 文本用例 `COMPAT-RUNSON-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: - 平台存在匹配 [dedicate-hosted, x64, large] 标签的 Runner
  - 操作步骤: 1. 在工作流中声明 `runs-on: [dedicate-hosted, x64, large]`
    2. 触发工作流，观察 Runner 调度行为
    3. 确认 job 被分配到满足所有标签的 Runner 上执行
  - 预期结果: - 三段式数组格式被平台正确解析
    - job 成功调度到同时满足三个标签的 Runner
    - 工作流正常执行，无标签匹配错误
  - 验证点: - [正向] 工作流成功启动并执行
    - [正向] 日志中显示 Runner 标签与声明一致
    - [负向] 不应因数组格式而被平台拒绝解析

- **实际行为**:
  - Job "Verify three-part runs-on array" status=COMPLETED

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
  - Phase 01 前置条件: - 平台存在匹配 [dedicate-hosted, x64, large] 标签的 Runner

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-RUNSON-01-001 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-RUNSON-01-001 的判断逻辑
