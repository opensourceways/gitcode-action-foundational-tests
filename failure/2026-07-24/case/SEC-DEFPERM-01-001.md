## 失败分诊 · SEC-DEFPERM-01-001 · ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "write_successful"` — **PASS**: 未出现 "write_successful"
  - 正向 `run_logs` `equals: "403_or_permission_denied"` — **FAIL**: 实际返回 `401` (UNAUTHORIZED)，非 403

**根因初判**: 环境问题（token 未注入或无效，返回 401 而非 403）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test permission inheritance (status=FAILED) ===
  [2026/07/23 22:06:10.148 GMT+08:00] [INFO] Job(1529972919336046592_1529972919310880775) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/6524ea65-d3b3-42b6-82f2-1c4a1c56c494.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/6524ea65-d3b3-42b6-82f2-1c4a1c56c494.sh
  000{"error_code":401,"error_code_name":"UNAUTHORIZED","error_message":"401, token not found","trace_id":"fc37cf8321aebc57a99740e7bfd2ddd9"}401000000::error::Process exited with code 6
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库未声明或声明了部分 permissions
  - 操作步骤: 1. 提交一个 workflow，顶层声明 repository: read，job 级覆盖为 repository: write；2. 触发 workflow 并验证实际权限
  - 预期结果: 顶层声明被各 job 继承；job 级声明覆盖顶层

- **实际行为**:
  - API 返回 401 (UNAUTHORIZED)，错误信息为 "token not found"
  - 这说明 `${{ atomgit.token }}` 为空或无效，平台无法识别请求身份
  - 权限继承测试的前提（token 有效且具有 read 权限）未成立
  - **失败传导链**: atomgit.token 未注入或无效 → 所有 API 调用返回 401 → 无法区分"有 read 权限但拒绝 write"和"无任何权限" → 正向断言"403_or_permission_denied"无法满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `inherit-test` 的 `Attempt write`:
    ```yaml
    permissions:
      repository: read
    jobs:
      inherit-test:
        name: Test permission inheritance
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Attempt write
            run: |
              curl -s -o /dev/null -w "%{http_code}" -X POST
              "https://api.gitcode.com/api/v5/repos/${{ atomgit.repository }}/issues"
              -H "Authorization: token ${{ atomgit.token }}"
              -d '{"title": "test"}'
    ```
  - **GitCode 规格** `core-concepts/workflow-job-step-action.md` 第 69-83 行:
    ```yaml
    ## Job（任务）
    Job 是 Stage 内的可执行单元...核心属性：
    | `env` | Job 级环境变量 |
    ```
  - **逐项映射**:
    - `permissions.repository`: 测试 YAML 声明 `read` — 规格中无 `permissions` 字段的直接 YAML 示例
    - `${{ atomgit.token }}`: 测试 YAML 使用此表达式获取 token — 若平台未注入，返回空
    - HTTP 方法 (POST) 与 API 端点 (/api/v5/repos/.../issues)：此为写操作，应被 read 权限拒绝

- **环境前置条件验证**: **FAIL** — `${{ atomgit.token }}` 为空或无效，返回 "token not found"（401）。未执行 config_probe 验证。符合"Secret/token empty in logs + no config_probe → 环境问题 (Phase 02)"规则

**置信度**: 高（token not found 明确指示环境问题）

**影响**:
- **阻塞性**: 低 — 可在修复 token 注入后重新测试；token 场景在多个 SEC 用例中均可复现
- **静默性**: 低 — 平台明确报出 401 错误
- **影响面**: 中 — 影响所有依赖 `atomgit.token` 的权限测试用例
- **综合**: token 未注入（401 "token not found"），权限继承测试的前置条件不成立，需要 Phase 02 检查 pipeline 中的 secret 注入配置
- **是否有规避手段**: 是 — 确保 workflow dispatch 或 trigger 配置正确注入 `ATOMGIT_TOKEN`

**建议**:
- Phase 02: 检查 pipeline 模板中 `atomgit.token` 的注入机制；确认 `workflow_dispatch` trigger 下 token 是否正常可用
- Phase 01: 若 token 注入在 `workflow_dispatch` 下不可用，需将 trigger 改为 `push` 或确认平台限制后更新用例前提
