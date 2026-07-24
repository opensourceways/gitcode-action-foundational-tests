## 失败分诊 · SEC-SUPPLY-01-002 · commit hash 不匹配时第三方 Action 应被拒绝执行

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_status` `must_not_equal: "success"` — **PASS**: job status=FAILED
  - 正向 `run_logs` `equals: "action_not_found_or_sha_mismatch"` — 无法判定: job 零输出，无错误信息

**根因初判**: 与 SEC-SUPPLY-01-001 共享根因 — action 解析失败但日志中无明确的 SHA 不匹配错误信息
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test hash mismatch rejection (status=FAILED) ===
  [2026/07/23 22:10:37.801 GMT+08:00] [INFO] Job(1529974041978880000_1529974041945325575) duration check: true
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库可引用外部 Action
  - 操作步骤: 1. 提交 workflow，使用一个不存在的 commit SHA 引用 Action；2. 触发 workflow
  - 预期结果: job 进入失败状态或明确拒绝执行；系统不应静默回退到分支 HEAD

- **实际行为**:
  - job FAILED（符合负向断言）但零输出
  - 平台拒绝了不存在的 action hash（全零 SHA），但未输出任何错误消息
  - 无法确认是 "action not found" 还是 "SHA mismatch"
  - 平台未静默回退到分支 HEAD（正确行为），但缺少正面证据
  - **失败传导链**: 全零 commit SHA → 平台 Action 解析器找不到 → job FAILED 零输出 → 缺少明确的错误信息

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `hash-mismatch` 的 `Use invalid hash action`:
    ```yaml
    jobs:
      hash-mismatch:
        name: Test hash mismatch rejection
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Use invalid hash action
            uses: docker/build-push-action@0000000000000000000000000000000000000000
    ```
  - **GitCode 规格** `syntax-reference/runner-images-tools.md`:
    ```
    规格中 action 引用格式：{owner}/{repo}@{ref}，ref 可为分支、标签或 commit SHA
    ```
  - **逐项映射**:
    - `0000000000000000000000000000000000000000`: 全零 SHA — 明确不存在的 hash
    - 测试 YAML 期望平台报出 "action not found" 或 "SHA mismatch" 错误
    - 实际平台行为：job FAILED 但错误信息未输出到日志（可能在平台内部日志中）
    - **正确行为验证**: 系统未静默回退到分支 HEAD（job 直接失败）

- **环境前置条件验证**: 外部 action 解析服务正常调度但缺乏日志输出

**置信度**: 中（job 正确 FAILED 但无错误消息，无法验证"返回明确的错误"这一正向断言）

**影响**:
- **阻塞性**: 低 — 安全行为达标（不执行假 action），但可观测性不足
- **静默性**: 高 — 用户无法从日志中理解失败原因
- **影响面**: 中 — 影响所有使用 action 引用的用户体验
- **综合**: 平台正确拒绝了不存在的 commit SHA（job FAILED），但未输出 "action not found" 或 "SHA mismatch" 错误消息到日志，用户无法诊断失败原因
- **是否有规避手段**: 否 — 用户侧无法获得更详细的错误信息

**建议**:
- 平台方: 在 action 解析失败时，将 "action not found: docker/build-push-action@0000...(SHA mismatch)" 或类似错误消息输出到 job 日志
- Phase 01: 更新正向断言，在平台增加错误输出后再回归此用例
