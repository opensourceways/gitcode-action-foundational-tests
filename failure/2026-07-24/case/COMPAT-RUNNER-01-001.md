## 失败分诊 · COMPAT-RUNNER-01-001 · runner.os 在 Linux Runner 上应返回 Linux

**判定结果**: FAIL
**失败断言**:
assertions (runner.os) — job COMPLETED，runner_os=linux 正确输出

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（共 7 行）:
```
  === JOB: Test runner.os value (status=COMPLETED) ===
  [2026/07/23 22:23:37.671 GMT+08:00] [INFO] Job(1529977312760053760_1529977312730693639) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/3be8b7d2-ec6d-4020-9809-502bab3ebdf8.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/3be8b7d2-ec6d-4020-9809-502bab3ebdf8.sh
  runner_os=linux
  done
```

- **预期行为**（Phase 01 文本用例 `COMPAT-RUNNER-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: - 仓库已启用 Actions
    - 存在 Linux 标签的 Runner
  - 操作步骤: 1. 在 workflow 的 run 步骤中输出 ${{ runner.os }}
    2. 触发 workflow 运行
  - 预期结果: - runner.os 应返回 Linux（首字母大写，与 GitHub 一致）
  - 验证点: - [正向] 日志中 runner.os 的值为 Linux
    - [负向] 不应返回小写的 linux

- **实际行为**:
  - Job "Test runner.os value" status=COMPLETED

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
  - Phase 01 前置条件: - 仓库已启用 Actions
    - 存在 Linux 标签的 Runner

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-RUNNER-01-001 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-RUNNER-01-001 的判断逻辑
- 相关用例: COMPAT-RUNNER-01-002
