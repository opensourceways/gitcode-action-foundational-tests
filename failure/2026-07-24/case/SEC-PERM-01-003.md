## 失败分诊 · SEC-PERM-01-003 · 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only）

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "write_permission_granted"` — **PASS**: 未出现写权限授予
  - 正向 `run_status` `equals: "completed"` — **PASS**: job status=FAILED（但断言期望 completed）

**根因初判**: 环境问题（token 未注入，与 SEC-DEFPERM-01-001 共享根因）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test default permissions (status=FAILED) ===
  [2026/07/23 22:08:23.568 GMT+08:00] [INFO] Job(1529973478763544576_1529973478729990151) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c525be66-2200-49bc-a600-269befedd1ba.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c525be66-2200-49bc-a600-269befedd1ba.sh
  000{"error_code":401,"error_code_name":"UNAUTHORIZED","error_message":"401, token not found","trace_id":"e52c578851200f198792d2fc6f5c93aa"}401000000::error::Process exited with code 6
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库未配置 permissions 声明
  - 操作步骤: 1. 提交一个未声明 permissions 的 workflow；2. 触发 workflow 并尝试执行写操作
  - 预期结果: 默认状态下 ATOMGIT_TOKEN 仅拥有仓库 read 权限；写操作被平台拒绝

- **实际行为**:
  - API 返回 401 (UNAUTHORIZED)，"token not found"
  - 这是身份认证失败（token 不存在），而非权限不足（403 Forbidden）
  - 无法区分"有 read 权限但无 write"和"无任何权限"
  - **失败传导链**: `${{ atomgit.token }}` 为空 → API 调用没有有效 token → 返回 401 → 退出码 6（非成功）→ job FAILED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `default-perm` 的 `Attempt write without permissions`:
    ```yaml
    jobs:
      default-perm:
        name: Test default permissions
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Attempt write without permissions
            run: |
              curl -s -o /dev/null -w "%{http_code}" -X POST
              "https://api.gitcode.com/api/v5/repos/${{ atomgit.repository }}/issues"
              -H "Authorization: token ${{ atomgit.token }}"
              -d '{"title": "test"}'
    ```
  - **GitCode 规格** `security-permissions/` 目录:
    ```
    规格中安全权限部分定义 ATOMGIT_TOKEN 的默认权限范围
    ```
  - **逐项映射**:
    - 测试 YAML 未声明 `permissions:` 字段 — 期望触发默认权限
    - `${{ atomgit.token }}`: 引用运行时 token — 若值为空，请求本身即失败
    - 规格期望默认 token 具有 read 权限 — 但前提是 token 被正常注入

- **环境前置条件验证**: **FAIL** — "token not found" (401)。符合"Secret/token empty in logs → 环境问题 (Phase 02)"规则

**置信度**: 高（与 SEC-DEFPERM-01-001 完全一致的 401 token not found）

**影响**:
- **阻塞性**: 中 — token 未注入使权限测试无法进行
- **静默性**: 低 — 401 错误明确可观测
- **影响面**: 中 — 影响所有权限测试用例
- **综合**: token 未注入（401），默认权限最小化测试的前提不成立；与 SEC-DEFPERM-01-001 共享同一根因
- **是否有规避手段**: 是 — 修复 token 注入

**建议**:
- Phase 02: 与 SEC-DEFPERM-01-001 合并修复 — 验证 `workflow_dispatch` 下 `atomgit.token` 的注入机制
