## 失败分诊 · SEC-SUPPLY-01-001 · 第三方 Action 引用应支持完整 commit hash 固定

**判定结果**: FAIL
**失败断言**:
  - 正向 `run_status` `equals: "success_or_action_executed"` — **FAIL**: job status=FAILED，零输出
  - 负向 `run_logs` `must_not_contain: "unauthorized_action_execution"` — 无法判定: 无执行日志

**根因初判**: 测试 YAML 使用不存在的 action hash（测试占位符），action 解析失败导致 job 在启动阶段失败
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test commit hash pinning (status=FAILED) ===
  [2026/07/23 22:10:27.138 GMT+08:00] [INFO] Job(1529973997196677120_1529973997171511303) duration check: true
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库可引用外部 Action
  - 操作步骤: 1. 提交 workflow，使用完整 commit SHA 引用第三方 Action；2. 触发 workflow
  - 预期结果: 完整 commit SHA 引用可成功执行 action

- **实际行为**:
  - job 在启动阶段失败，零输出（无 shell 创建、无步骤执行）
  - `docker/build-push-action@1234567890abcdef1234567890abcdef12345678` 是一个假 hash — 平台无法解析
  - 未产生任何 action 执行日志
  - **失败传导链**: 假 commit SHA → 平台 Action 解析器无法定位 → job FAILED（启动阶段）→ 零输出

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `hash-pin` 的 `Use pinned action`:
    ```yaml
    jobs:
      hash-pin:
        name: Test commit hash pinning
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Use pinned action
            uses: docker/build-push-action@1234567890abcdef1234567890abcdef12345678
    ```
  - **GitCode 规格** `syntax-reference/runner-images-tools.md` 及 `writing-pipelines/using-script-commands.md`:
    ```
    规格中 action 引用格式的定义
    ```
  - **逐项映射**:
    - `uses: docker/build-push-action@1234567890...`: 测试 YAML 使用完整 commit SHA 格式 — 符合规格中的 `{owner}/{repo}@{ref}` 格式
    - `1234567890abcdef1234567890abcdef12345678`: 测试使用的 hash 为占位符/假值 — 非真实的 commit SHA
    - 正常的正向测试应使用真实存在的 action 仓库及其 commit SHA
    - **设计缺陷**: 测试 YAML 同时试图覆盖"hash 引用成功"和"hash 错误拒绝"两个场景，但两者需要不同的测试 fixture

- **环境前置条件验证**: 外部 action 解析服务正常（job 被调度但解析失败）

**置信度**: 高（假 commit SHA 导致 action 解析失败）

**影响**:
- **阻塞性**: 中 — 正向测试未执行
- **静默性**: 低 — FAILED 状态明确
- **影响面**: 低 — 仅本用例
- **综合**: 测试 YAML 使用占位符假 hash `1234567890abcdef...`，非真实存在的 action commit，导致 action 解析失败、job 零输出
- **是否有规避手段**: 是 — 使用真实存在的 action 仓库及其真实 commit SHA

**建议**:
- Phase 01: (1) 将 SEC-SUPPLY-01-001 和 SEC-SUPPLY-01-002 拆分：01-001 测试正向（真实 hash 成功执行）；01-002 测试负向（假 hash 被拒绝）；(2) 01-001 需指定真实可用的测试 action 及其真实 commit SHA
- Phase 02: 为正向测试准备一个 dummy test action（如 `gitcode-ci-test/dummy-action@<real-sha>`）
