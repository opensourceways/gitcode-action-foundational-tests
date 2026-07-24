## 失败分诊 · REL-QUEUE-01-003 · concurrency QUEUE 策略——超上限运行应排队等待

**判定结果**: FAIL
**失败断言**: 正向/run_status expected=completed(success) actual=N/A (仅 1 run log); 非功能/queued_count expected=2 actual=N/A

**根因初判**: 环境/Harness（log 仅记录 1 个 run——同 REL-CONC-01-001 / REL-IGNORE-01-004）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: concurrency test job (status=COMPLETED) ===
  [2026/07/23 22:35:33.589 GMT+08:00] [INFO] Job(1529980315802152960_1529980315781181447) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/b2589d39-e1b0-4c93-9631-c612f5dc9207.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/b2589d39-e1b0-4c93-9631-c612f5dc9207.sh
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库已配置 concurrency.max=2 exceed-action=QUEUE 的 workflow
  - 操作步骤: 同时触发 4 次该 workflow
  - 预期结果: 运行 1-2 进入 in_progress; 运行 3-4 进入 queued; 前 2 个完成后 3-4 自动启动; 4 个最终全部 success

- **实际行为**:
  - 仅 1 个 job instance 有 log（status=COMPLETED），30 秒 sleep 正常执行
  - 预期 4 次并发 run，实际仅记录 1 次
  - 与 REL-CONC-01-001（QUEUE）和 REL-IGNORE-01-004（IGNORE）相同的 log 不全问题
  - **失败传导链**: log 不完整 → 无法验证 queue 行为 → case FAIL

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 workflow 级 concurrency:
    ```yaml
    concurrency:
      max: 2
      exceed-action: QUEUE
    ```
  - **测试 YAML** 中 `test` step:
    ```yaml
    - name: sleep step
      run: |
        sleep 30
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 154-165 行:
    ```yaml
    concurrency:
      enable: true
      max: 1
      exceed-action: IGNORE
    ```
  - **逐项映射**: `concurrency.max: 2` + `exceed-action: QUEUE` → 匹配规格; 触发 4 次期望 QUEUE 策略让 3-4 号排队。但日志不全无法验证。

- **环境前置条件验证**: runner 可用，但仅 1/4 run log 被收集

**置信度**: 低（与 REL-CONC-01-001 / REL-IGNORE-01-004 完全相同的数据不全问题）

**影响**:
- **阻塞性**: 🟡中等 — 无法判断 QUEUE 语义是否正确
- **静默性**: 🔴静默 — 无错误日志
- **影响面**: 🟡同模式 — 与其他 concurrency 用例共享相同根因
- **综合**: 所有 3 个并发相关用例（CONC-001, IGNORE-004, QUEUE-003）均只有 1 次 run 有 log——存在系统性 log 收集缺漏
- **是否有规避手段**: 是（排查 test harness 多 run 触发和 log 收集逻辑）

**建议**:
- 与 REL-CONC-01-001 / REL-IGNORE-01-004 统一排查 test harness 的并发触发 + log 收集
- 检查是否每次 workflow_dispatch 都等待完成后再触发下一次（导致 log 被覆盖）
