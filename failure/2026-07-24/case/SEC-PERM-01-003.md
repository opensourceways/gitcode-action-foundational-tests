## 失败分诊 · SEC-PERM-01-003 · 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only）

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "write_permission_granted" — 无法验证
- positive, run_status, equals "completed" — job 状态 FAILED，不匹配

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Test default permissions (status=FAILED) ===
  [2026/07/23 22:08:23.568 GMT+08:00] [INFO] Job(1529973478763544576_1529973478729990151) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c525be66-2200-49bc-a600-269befedd1ba.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c525be66-2200-49bc-a600-269befedd1ba.sh
  000{"error_code":401,"error_code_name":"UNAUTHORIZED","error_message":"401, token not found","trace_id":"e52c578851200f198792d2fc6f5c93aa"}401000000::error::Process exited with code 6
  ```

- **预期行为** (Phase 01 文本用例 SEC-PERM-01-003, 优先级 P0, 维度 security):
  - 前置条件: 仓库未配置 permissions 声明
  - 操作步骤 1: 提交一个未声明 permissions 的 workflow
  - 操作步骤 2: 触发 workflow 并尝试执行写操作
  - 预期结果: 默认状态下 ATOMGIT_TOKEN 仅拥有仓库 read 权限；写操作被平台拒绝

- **实际行为**:
  - API 返回 401 UNAUTHORIZED + `"token not found"`
  - `${{ atomgit.token }}` 展开为空字符串，API 调用因缺少有效 token 而返回 401
  - 测试无法区分 "token 存在但权限不足(403)" 与 "token 不存在(401)"
  - 失败传导链: 单 job，无传导

- **对照 GitCode 规格** `security-permissions/token-permissions.md`:
  - 第 13 行: "每次流水线运行时，AtomGit Action 自动生成 ATOMGIT_TOKEN"
  - 第 103 行: "permissions: {}（空）| ATOMGIT_TOKEN 仅拥有最小默认权限（repository:read）"
  - 第 99 行: "未声明 permissions | 使用仓库设置中定义的权限"

- **环境前置条件验证**: YAML `setup.repo_fixture: default`，无 `secrets` 字段，无 config_probe。`atomgit.token` 展开为空导致 401 而非 403。与 SEC-DEFPERM-01-001 相同模式。

**置信度**: 高 (401 + "token not found" 明确指示 ATOMGIT_TOKEN 未注入)

**影响**:
- **阻塞性**: 🔴阻塞 — 无法验证 ATOMGIT_TOKEN 默认权限范围为 read-only
- **静默性**: 🟡可察觉 — 有 401 错误但非预期语义
- **影响面**: 🟡同维度 — SEC-DEFPERM-01-001、SEC-PERM-01-004 同样受影响
- **综合**: 测试环境未注入有效的 ATOMGIT_TOKEN，空值导致 401 而非预期的 403 权限拒绝
- **是否有规避手段**: 否

**建议**:
- 测试 YAML 添加 config_probe 步骤：`echo "TOKEN_LEN:${#ATOMGIT_TOKEN}"` 确认 token 存在
- 检查 workflow_dispatch 触发下 ATOMGIT_TOKEN 的注入机制是否与 push/PR 一致
- 若 token 确实存在但权限不足，期望值应为 403 而非 401
