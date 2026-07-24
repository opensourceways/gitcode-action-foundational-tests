## 失败分诊 · SEC-RUN-01-003 · 自托管 Runner 跨项目残留必须被隔离

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "cross project leak" — 无泄露输出
- positive, run_logs, equals "isolated_as_expected" — 日志中无任何 job 输出

**根因初判**: 编译缺口
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Write project A data (status=FAILED) ===
  [2026/07/23 22:09:54.688 GMT+08:00] [INFO] Job(1529973861045248000_1529973861007499271) duration check: true
  
  
  === JOB: Check project B isolation (status=FAILED) ===
  [2026/07/23 22:09:54.659 GMT+08:00] [INFO] Job(1529973861045248000_1529973861007499273) duration check: true
  ```

- **预期行为** (Phase 01 文本用例 SEC-RUN-01-003, 优先级 P0, 维度 security):
  - 前置条件: 自托管 runner 被多个项目共享
  - 操作步骤 1: 项目 A 的 workflow 写入临时文件和环境变量
  - 操作步骤 2: 项目 B 的 workflow 在同一 runner 上检查残留
  - 预期结果: 项目 B 的 job 绝不应读取到项目 A 残留的敏感文件或环境变量；runner 清理失败时应标记为不可用

- **实际行为**:
  - Job A 状态 FAILED: 无任何执行输出，无 `::debug::Script file created` 行
  - Job B 状态 FAILED: 同样无任何执行输出
  - 两个 job 均在启动阶段失败，未进入步骤执行
  - `runs-on: [self-hosted, x64, large]` 标签无可用的自托管 runner 匹配
  - 失败传导链: 无 job 执行，runner 层调度失败

- **对照 GitCode 规格** `runner-management/using-self-hosted-runners.md`:
  - 第 N-M 行: 自托管 runner 需要手动注册和配置标签才能被 workflow 调度

- **环境前置条件验证**: YAML `setup.repo_fixture: self-hosted-shared`，使用 `runs-on: [self-hosted, x64, large]`。该 fixture 假设环境中存在配置了 `self-hosted`、`x64`、`large` 标签的 runner，但实际环境无此配置。

**置信度**: 高 (job 日志无脚本创建和执行，自托管 runner 未被调度)

**影响**:
- **阻塞性**: 🔴阻塞 — 自托管 runner 不可用，跨项目隔离验证完全无法执行
- **静默性**: 🟡可察觉 — job 标记为 FAILED 但无错误信息
- **影响面**: 🟢单用例 — 仅影响依赖自托管 runner 的用例
- **综合**: 测试环境无可用的自托管 runner，需先注册自托管 runner 或变更测试策略
- **是否有规避手段**: 否

**建议**:
- 在测试环境中注册至少一个带 `self-hosted`、`x64`、`large` 标签的 runner
- 若自托管 runner 不可用，考虑将测试降级为官方 runner 上模拟多 repo 隔离场景
- 添加 runner 可用性 config_probe：`runner.os` 及 `runs-on` 标签匹配验证
- YAML 中添加超时和降级策略：自托管 runner 无法调度时的明确错误信息
