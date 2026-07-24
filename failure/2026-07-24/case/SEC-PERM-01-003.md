## 失败分诊 · SEC-PERM-01-003 · 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only）

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "write_permission_granted"，该关键词未出现（PASS）；assertions[1] (positive, run_status) — 期望 equals "completed"，实际 run_status=FAILED，token 不可用导致 job 失败

**根因初判**: 环境问题

**证据**:

- **Job 日志全量**（仅 6 行）:
  ```
  === JOB: Test default permissions (status=FAILED) ===
  [2026/07/23 22:08:23.568 GMT+08:00] [INFO] Job(1529973478763544576_1529973478729990151) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c525be66-2200-49bc-a600-269befedd1ba.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c525be66-2200-49bc-a600-269befedd1ba.sh
  000{"error_code":401,"error_code_name":"UNAUTHORIZED","error_message":"401, token not found","trace_id":"e52c578851200f198792d2fc6f5c93aa"}401000000::error::Process exited with code 6
  ```
  API 返回 401 UNAUTHORIZED，"token not found"。ATOMGIT_TOKEN 在 workflow_dispatch 事件下不可用，导致 API 调用在认证层面就失败（exit code 6），而非进入权限校验逻辑。这与 SEC-DEFPERM-01-001 完全相同的环境问题模式。

- **预期行为**（Phase 01 文本用例 `SEC-PERM-01-003`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个未声明 permissions 的 workflow"
  - 操作步骤 2: "触发 workflow 并尝试执行写操作"
  - 预期结果: "默认状态下 ATOMGIT_TOKEN 仅拥有仓库 read 权限；写操作被平台拒绝"
  - 验证点: "[负向] 默认状态下 ATOMGIT_TOKEN 绝不应拥有写权限"

- **实际行为**:
  - ATOMGIT_TOKEN 本身不可用（"token not found"），导致 curl 请求返回 401 而非预期的权限拒绝
  - 无法判断默认 permissions 的最小化行为是否有效——token 未被正确注入到 workflow 运行环境中
  - run_status FAILED ≠ 断言期望 "completed"

- **失败传导链**: ATOMGIT_TOKEN 不可用 → curl 请求返回 401 → 脚本退出码 6 → Job FAILED → 断言 run_status "completed" FAIL

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `default-perm` job 的 `Attempt write without permissions` 步骤:
    ```yaml
    - name: Attempt write without permissions
      run: |
        curl -s -o /dev/null -w "%{http_code}" -X POST \
          "https://api.gitcode.com/api/v5/repos/${{ atomgit.repository }}/issues" \
          -H "Authorization: token ${{ atomgit.token }}" \
          -d '{"title": "test"}'
    ```
  - 这对应 GitCode 规格 `security-permissions/token-permissions.md` 第 97-103 行的 permissions 与 ATOMGIT_TOKEN 关系表:
    ```
    | permissions 配置 | ATOMGIT_TOKEN 实际权限 |
    |------------------|----------------------|
    | 未声明 permissions | 使用仓库设置中定义的权限 |
    | 顶层声明 permissions | 所有 job 继承顶层权限，除非 job 级覆盖 |
    | permissions: {}（空） | ATOMGIT_TOKEN 仅拥有最小默认权限（repository:read） |
    ```
    规格第 99 行承诺"未声明 permissions：使用仓库设置中定义的权限"。测试未声明 permissions，期望验证默认最小权限行为。但由于 ATOMGIT_TOKEN 不可用，权限校验从未被执行——这是环境注入问题，不是权限逻辑问题。
  - 同时对应 `workflow-file-location-structure.md` 第 189-224 行的 permissions 权限体系，文档确凿承诺了 permissions 字段的语义。

**置信度**: 中（token not found 是环境问题已在日志确凿证实——与 SEC-DEFPERM-01-001 同模式；但默认 permissions 的最小化行为在修复环境后是否能被验证仍未知）

**影响**:
- **阻塞性**: 🟡非阻塞 — job FAILED（exit code 6）但 workflow 能完成调度，permissions 继承逻辑因 token 不可用未能被验证
- **静默性**: 🟡可察觉 — 日志明确返回 `{"error_code":401,"error_code_name":"UNAUTHORIZED","error_message":"401, token not found"}`，可观测但根因需排查
- **影响面**: 🟢单用例 — 与 SEC-DEFPERM-01-001 同 token 注入问题，影响所有依赖 ATOMGIT_TOKEN 的 workflow_dispatch 测试
- **综合**: ATOMGIT_TOKEN 在 workflow_dispatch 事件下不可用（"token not found"），默认 permissions 最小化行为未被测试到，属环境问题
- **是否有规避手段**: 是 — 修复 ATOMGIT_TOKEN 注入或在 push 事件下触发测试

**建议**:
- 修复 ATOMGIT_TOKEN 在 workflow_dispatch 事件下的注入问题（同时影响 SEC-DEFPERM-01-001）
- 修复后重跑此用例以验证默认 permissions 的最小化行为
- 相关用例: SEC-DEFPERM-01-001, SEC-PERM-01-004
