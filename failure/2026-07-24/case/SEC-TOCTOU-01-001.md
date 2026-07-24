## 失败分诊 · SEC-TOCTOU-01-001 · 审批后推送新 commit 不应被已授权特权运行执行

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "unapproved_commit_executed" — 通过（无未审批 commit）
- positive, run_logs, equals "approved_sha_matched" — 日志中 SHA 为空，不匹配

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Test TOCTOU protection (status=COMPLETED) ===
  [2026/07/23 22:10:48.247 GMT+08:00] [INFO] Job(1529974085599641600_1529974085566087175) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/89cfca38-c55f-46eb-acf8-5bf6a7c6d07b.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/89cfca38-c55f-46eb-acf8-5bf6a7c6d07b.sh
  Running commit: 
  ```

- **预期行为** (Phase 01 文本用例 SEC-TOCTOU-01-001, 优先级 P0, 维度 security):
  - 前置条件: 仓库配置了审批触发 workflow
  - 操作步骤 1: 管理员审批一个 workflow 运行
  - 操作步骤 2: 在审批后、执行前，攻击者推送恶意 commit
  - 操作步骤 3: 观察特权运行是否执行了新 commit
  - 预期结果: 特权运行应绑定审批时刻的具体 commit SHA；审批后推送的新 commit 不应被已授权的特权运行自动采用

- **实际行为**:
  - `echo "Running commit: ${{ atomgit.sha }}"` 输出 `Running commit: ` 后为空
  - `atomgit.sha` 上下文变量在 workflow_dispatch 触发下为空
  - TOCTOU 验证因缺少 commit SHA 而无法进行
  - 失败传导链: 单 job，无传导

- **对照 GitCode 规格** `syntax-reference/context.md`:
  - 第 N-M 行: `atomgit.sha` — 当前提交 SHA
  - workflow_dispatch 事件下，`atomgit.sha` 可能为触发分支的 HEAD 而非具体值

- **环境前置条件验证**: YAML `setup.repo_fixture: default`, 无 secrets, 无 config_probe。`workflow_dispatch` 触发方式下 `atomgit.sha` 未填充，TOCTOU 审批锁定场景未被模拟。

**置信度**: 高 (atomgit.sha 为空，环境未模拟审批锁定场景)

**影响**:
- **阻塞性**: 🔴阻塞 — TOCTOU 验证完全无法执行
- **静默性**: 🔴静默错误 — SHA 为空但不报错，静默通过
- **影响面**: 🟢单用例 — 仅影响此 TOCTOU 审批场景测试
- **综合**: workflow_dispatch 触发下 atomgit.sha 为空，TOCTOU 场景需审批事件支持
- **是否有规避手段**: 否

**建议**:
- TOCTOU 测试需特殊的事件触发方式（如 `deployment` 或自定义审批事件的模拟）
- 测试 YAML 可改用 `pull_request_target` + 审批流程来模拟 TOCTOU 场景
- 添加 config_probe 验证 `atomgit.sha` 在目标事件下非空
- 若平台缺乏审批触发机制，此用例应标记为编译缺口
