## 失败分诊 · SEC-DEFPERM-01-001 · ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "write_successful" — 无法验证，403/401 未按预期生效
- positive, run_logs, equals "403_or_permission_denied" — 实际返回 401 UNAUTHORIZED，不匹配

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Test permission inheritance (status=FAILED) ===
  [2026/07/23 22:06:10.148 GMT+08:00] [INFO] Job(1529972919336046592_1529972919310880775) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/6524ea65-d3b3-42b6-82f2-1c4a1c56c494.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/6524ea65-d3b3-42b6-82f2-1c4a1c56c494.sh
  000{"error_code":401,"error_code_name":"UNAUTHORIZED","error_message":"401, token not found","trace_id":"fc37cf8321aebc57a99740e7bfd2ddd9"}401000000::error::Process exited with code 6
  ```

- **预期行为** (Phase 01 文本用例 SEC-DEFPERM-01-001, 优先级 P0, 维度 security):
  - 前置条件: 仓库未声明或声明了部分 permissions
  - 操作步骤 1: 提交一个 workflow，顶层声明 `repository: read`，job 级覆盖为 `repository: write`
  - 操作步骤 2: 触发 workflow 并验证实际权限
  - 预期结果: 顶层声明被各 job 继承；job 级声明覆盖顶层

- **实际行为**:
  - API 返回 401 UNAUTHORIZED + `"token not found"`
  - `${{ atomgit.token }}` 展开为空字符串，Authorization header 为 `token ` (空值)
  - 权限继承与覆盖逻辑因此无法被验证
  - job 状态为 FAILED（exit code 6）

- **对照 GitCode 规格** `security-permissions/token-permissions.md`:
  - 第 13 行: "每次流水线运行时，AtomGit Action 自动生成 ATOMGIT_TOKEN"
  - 第 99-103 行: "未声明 permissions | 使用仓库设置中定义的权限" / "顶层声明 permissions | 所有 job 继承顶层权限，除非 job 级覆盖"
  - 第 103 行: "permissions: {}（空）| ATOMGIT_TOKEN 仅拥有最小默认权限（repository:read）"

- **环境前置条件验证**: YAML `setup.repo_fixture: default`，无 `secrets` 字段，无 config_probe。`atomgit.token` 是平台自动注入变量，其值为空表明测试环境未正确初始化 runner token 上下文。

**置信度**: 高 (401 + "token not found" 明确指示 token 注入缺失)

**影响**:
- **阻塞性**: 🔴阻塞 — 权限验证用例完全无法执行
- **静默性**: 🟢明确报错 — 平台返回明确的 401 和 "token not found"
- **影响面**: 🟡同维度 — SEC-PERM-01-003 也因相同原因失败
- **综合**: 测试环境未注入有效的 ATOMGIT_TOKEN，导致所有权限验证类用例无法验证
- **是否有规避手段**: 否

**建议**:
- 在测试 YAML 中添加 config_probe 步骤验证 `ATOMGIT_TOKEN` 是否被正确注入
- 检查 workflow_dispatch 触发方式下 ATOMGIT_TOKEN 的注入策略是否与 push/PR 事件一致
