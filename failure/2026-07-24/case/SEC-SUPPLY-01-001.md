## 失败分诊 · SEC-SUPPLY-01-001 · 第三方 Action 引用应支持完整 commit hash 固定

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 equals "success_or_action_executed"，实际 run_status=FAILED 且 0 字节有效日志；assertions[1] (negative, run_logs) — must_not_contain "unauthorized_action_execution"，无法验证（无日志内容）

**根因初判**: 平台缺陷

**证据**:

- **Job 日志全量**（仅 2 行）:
  ```
  === JOB: Test commit hash pinning (status=FAILED) ===
  [2026/07/23 22:10:27.138 GMT+08:00] [INFO] Job(1529973997196677120_1529973997171511303) duration check: true

  ```
  日志仅包含 job header 和 duration check 行。无 Shell 启动、无 `::debug::Script file created`、无任何步骤执行痕迹。平台在遇到无效的 commit hash action 引用（`uses: docker/build-push-action@1234567890abcdef1234567890abcdef12345678`）时，job 直接 FAILED 无任何诊断输出。关键的安全问题：平台未对无效的 commit hash 引用给出任何可观测的错误信息——用户无法知晓为什么 job 失败了。

- **预期行为**（Phase 01 文本用例 `SEC-SUPPLY-01-001`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个 workflow，使用完整 commit SHA 引用第三方 Action"
  - 操作步骤 2: "触发 workflow"
  - 预期结果: "完整 commit SHA 引用可成功执行 action；commit SHA 不匹配时 job 应失败或拒绝执行"
  - 验证点: "[正向] 完整 commit SHA 引用可成功执行 action"

- **实际行为**:
  - 平台遇到不存在的 commit hash action 引用时，job 直接进入 FAILED 状态
  - 无任何 error 日志、无 `::error::` 注释、无 "action not found" 诊断——0 字节有效日志
  - 这本身是平台缺陷：缺乏可观测的错误诊断输出，用户无法排查问题

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `hash-pin` job 的 `Use pinned action` 步骤:
    ```yaml
    - name: Use pinned action
      uses: docker/build-push-action@1234567890abcdef1234567890abcdef12345678
    ```
  - 这对应 GitCode 规格 `action-development/plugin-security-specification.md` 第 3-5 行的安全规范概述:
    ```
    插件安全规范要求敏感数据禁止硬编码、必须通过安全输入获取并加密存储和及时清理，
    且所有输入参数须经严格验证。
    ```
    规格第 3-5 行要求插件安全规范，但未涵盖 action 引用的供应链安全（commit hash pinning）——这是测试意图探索的安全边界。在 GitHub Actions 生态中，commit hash pinning 是防止 tag 被重写的关键供应链安全措施。平台在此测试中暴露了 hash pinning 引用缺乏诊断输出的缺陷。
  - 同时对应 `writing-pipelines/using-actions.md`（action 引用规范），但当前行为是平台不支持无效 hash 引用的诊断。

**置信度**: 中（0 字节有效日志是平台诊断缺失的确凿证据；但无法区分是"commit hash 不支持"还是"该 hash 恰好不存在"还是"平台完全不支持 hash pinning 引用"）

**影响**:
- **阻塞性**: 🔴阻塞 — 工作流在遇到无效 commit hash action 引用时 job 直接 FAILED 且 0 字节有效日志，用户完全无法获知失败原因
- **静默性**: 🔴静默错误 — job FAILED 但无任何 `::error::` 注释、无 "action not found" 诊断、无步骤执行痕迹，用户面临完全的诊断盲区
- **影响面**: 🟡同维度 — 影响所有使用 commit hash pinning 引用第三方 action 的场景（SEC-SUPPLY 全系列），不可信的无效引用同样缺乏诊断
- **综合**: 平台对无效 action 引用（不存在的 commit hash）完全静默失败，缺乏可观测诊断输出，既是功能缺陷也是供应链安全可观测性缺口
- **是否有规避手段**: 否 — 当前平台无内置诊断输出，用户无法在当前行为下自行排查无效 action 引用的问题

**建议**:
- 平台应为无效的 action 引用（包括不存在 hash、非法 hash 格式）输出明确错误信息（如 `::error:: Action not found: docker/build-push-action@1234567...`）
- 使用真实存在的 action 仓库的完整 commit SHA 来验证正向 case（测试 commit hash pinning 是否被支持）
- 相关用例: SEC-SUPPLY-01-002
