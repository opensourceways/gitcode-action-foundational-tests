## 失败分诊 · SEC-DEFPERM-01-001 · ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "write_successful"，实际该关键词未出现（PASS）；assertions[1] (positive, run_logs) — 期望日志含 "403_or_permission_denied"，实际返回 401 UNAUTHORIZED，"token not found"

**根因初判**: 环境问题

**证据**:

- **Job 日志全量**（仅 6 行）:
  ```
  === JOB: Test permission inheritance (status=FAILED) ===
  [2026/07/23 22:06:10.148 GMT+08:00] [INFO] Job(1529972919336046592_1529972919310880775) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/6524ea65-d3b3-42b6-82f2-1c4a1c56c494.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/6524ea65-d3b3-42b6-82f2-1c4a1c56c494.sh
  000{"error_code":401,"error_code_name":"UNAUTHORIZED","error_message":"401, token not found","trace_id":"fc37cf8321aebc57a99740e7bfd2ddd9"}401000000::error::Process exited with code 6
  ```
  日志显示 API 返回 401 UNAUTHORIZED，"token not found"。错误是 ATOMGIT_TOKEN 本身不可用（token not found），而非权限校验返回 403。这是一个环境/token 注入问题，不是权限控制逻辑问题。Job status 为 FAILED（exit code 6），而断言期望的是权限错误关键词 "403_or_permission_denied"。

- **预期行为**（Phase 01 文本用例 `SEC-DEFPERM-01-001`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个 workflow，顶层声明 repository: read，job 级覆盖为 repository: write"
  - 操作步骤 2: "触发 workflow 并验证实际权限"
  - 预期结果: "顶层声明被各 job 继承；job 级声明覆盖顶层"
  - 验证点: "[正向] 顶层声明被各 job 继承；job 级声明覆盖顶层"

- **实际行为**:
  - ATOMGIT_TOKEN 不可用（"token not found"），导致 curl 请求返回 401 而非权限拒绝 403
  - 无法判断 permissions 继承/覆盖逻辑是否工作——token 本身没有被正确注入

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `inherit-test` job 的 `Attempt write` 步骤:
    ```yaml
    - name: Attempt write
      run: |
        curl -s -o /dev/null -w "%{http_code}" -X POST \
          "https://api.gitcode.com/api/v5/repos/${{ atomgit.repository }}/issues" \
          -H "Authorization: token ${{ atomgit.token }}" \
          -d '{"title": "test"}'
    ```
  - 这对应 GitCode 规格 `security-permissions/token-permissions.md` 第 49-65 行的最小权限原则实践，以及第 97-103 行的 permissions 与 ATOMGIT_TOKEN 关系表:
    ```
    | permissions 配置 | ATOMGIT_TOKEN 实际权限 |
    |------------------|----------------------|
    | 未声明 permissions | 使用仓库设置中定义的权限 |
    | 顶层声明 permissions | 所有 job 继承顶层权限，除非 job 级覆盖 |
    | permissions: {}（空） | ATOMGIT_TOKEN 仅拥有最小默认权限（repository:read） |
    ```
    规格第 101 行明确承诺"顶层声明 permissions：所有 job 继承顶层权限，除非 job 级覆盖"。测试 YAML 在顶层声明了 `permissions: {repository: read}`，验证 API 调用被拒绝（因无 issue:write 权限）是符合规格期望的——但当前日志中 ATOMGIT_TOKEN 根本不可用，跳过了权限验证逻辑。
  - 同时也对应规格第 26-36 行的 permissions 字段详解示例，文档确凿承诺了 permissions 字段的权限控制能力。

**置信度**: 中（token not found 是环境问题已被日志确凿证实，但此环境下 permissions 继承逻辑是否正确无法判断）

**建议**:
- 修复 ATOMGIT_TOKEN 在 workflow_dispatch 事件下的注入问题
- 修复后重跑此用例以验证 permissions 继承逻辑
- 相关用例: SEC-PERM-01-003, SEC-PERM-01-004
