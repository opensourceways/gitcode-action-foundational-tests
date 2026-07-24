## 失败分诊 · USE-CONC-01-001 · concurrency.max 配置 0 或 10 时报错应提示有效范围 1-5

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED，实际 COMPLETED；assertions[1] (nonfunctional, error_message) — 期望平台返回含"1-5"的校验错误，实际无任何校验错误

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（6 行）:
  ```
  === JOB: concurrency max out of range (status=COMPLETED) ===
  [2026/07/23 22:41:02.663 GMT+08:00] [INFO] Job(1529981696067907584_1529981696046936071) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/ce4cdef8-2756-4284-bf72-91077196f349.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/ce4cdef8-2756-4284-bf72-91077196f349.sh
  hello
  ```
  Job 状态为 COMPLETED，脚本正常执行并输出 `hello`。日志中无任何 YAML 校验报错信息，无 concurrency.max 范围限制相关错误提示。

- **预期行为**（Phase 01 文本用例 `USE-CONC-01-001`，优先级 P1，维度 usability）:
  - 操作步骤 1: "在 workflow 中配置 concurrency: max: 10"
  - 预期结果: "YAML 校验报错，明确说明 max 取值范围应为 1-5"
  - 验证点: "[负向] 不应静默截断为边界值"；"[非功能] 报错中是否包含 1、5、范围等关键词"

- **实际行为**:
  - 平台静默接受 `concurrency.max: 10`，workflow 正常调度、执行至 COMPLETED，输出 `hello`。未产生任何校验错误或警告，完全未达到"拒绝非法值并提示范围 1-5"的预期。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `bad` job 的 workflow 配置:
    ```yaml
    concurrency:
      max: 10
      exceed-action: QUEUE
    ```
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md` 第 181-187 行的 `concurrency` 字段表:
    ```yaml
    concurrency:
      enable: true
      max: 3
      exceed-action: QUEUE
    ```
    且表格第 184 行明确声明 `max` 字段"范围 1-5"。测试 YAML 配置的 `max: 10` 超出该范围，平台文档确凿承诺了应在该位置施加校验。

**置信度**: 高（Job 日志 6 行全量无任何校验报错，run_status=COMPLETED，与 spec 第 184 行"范围 1-5"声明直接矛盾）

**影响**:
- **阻塞性**: 🟡非阻塞 — concurrency.max 配置 10 超出范围但 workflow 正常完成，不阻塞执行
- **静默性**: 🔴静默错误 — 平台完全接受非法值，无任何校验错误或警告，用户无法察觉配置问题
- **影响面**: 🟡同维度 — 所有配置 concurrency 块的 workflow 均受影响，任何超过 1-5 范围的 max 值都会被静默接受
- **综合**: concurrency.max 超出范围被静默接受，所有配置 concurrency 块的 workflow 均受影响但不会阻塞执行
- **是否有规避手段**: 否 — 用户无法从平台获得任何校验反馈，只能通过查阅文档自行确认合法范围

**建议**:
- 平台后端需为 `concurrency.max` 添加输入值范围校验，拒绝 <1 或 >5 的值，并在 API 返回 / UI 提示中明确报出合法范围 1-5
- 相关用例: USE-CONC-01-002（同一维度 sibling）
