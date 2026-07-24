## 失败分诊 · REL-IGNORE-01-004 · concurrency IGNORE 策略——超上限运行应直接执行

**判定结果**: FAIL
**失败断言**: 正向/run_status expected=completed(success) actual=N/A (仅 1 run log); 负向/run_status expected!=queued actual=N/A

**根因初判**: 环境/Harness（log 仅记录 1 个 run，多 run 并发触发可能未正确完成或收集不全）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: concurrency test job (status=COMPLETED) ===
  [2026/07/23 22:29:52.595 GMT+08:00] [INFO] Job(1529978885519450112_1529978885485895687) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/1969b61c-ad5d-4fe1-9b68-d4a69501aa45.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/1969b61c-ad5d-4fe1-9b68-d4a69501aa45.sh
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库已配置 concurrency.max=2 exceed-action=IGNORE 的 workflow
  - 操作步骤: 同时触发 4 次该 workflow
  - 预期结果: 4 个运行全部进入 in_progress; 无 queued 状态

- **实际行为**:
  - 日志仅 1 个 job instance（status=COMPLETED），30 秒 sleep 正常执行
  - 预期 4 次并发 run，实际仅收集到 1 次
  - 无法验证 IGNORE 策略是否让 4 次 run 全部直接执行（未经 queue）
  - **失败传导链**: log 不完整 → 无法验证 4/4 runs → case FAIL

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 workflow 级 concurrency:
    ```yaml
    concurrency:
      max: 2
      exceed-action: IGNORE
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
  - **逐项映射**: `concurrency.max: 2` + `exceed-action: IGNORE` → 匹配规格; 触发 4 次期望 IGNORE 策略允许全部同时执行; 测试 YAML 无 `enable: true` 字段（规格中 job 级 concurrency 有 enable 字段）。

- **环境前置条件验证**: runner 可用（1 个 job 正常完成），但仅 1/4 run 被记录

**置信度**: 低（数据严重不全，无法判断是并发触发失败还是 log 收集遗漏）

**影响**:
- **阻塞性**: 🟡中等 — 无法判断 IGNORE 语义是否正确
- **静默性**: 🔴静默 — 无错误日志
- **影响面**: 🟡同模式 — 影响所有并发测试用例
- **综合**: 与 REL-CONC-01-001 相同——并发触发 log 收集仅覆盖 1 次 run
- **是否有规避手段**: 是（检查 test harness 是否确实触发了 4 次 workflow_dispatch；确认 log 收集逻辑覆盖所有 run）

**建议**:
- 与 REL-CONC-01-001 联合排查：test harness 的多 run 触发机制
- 考虑手动验证 concurrency IGNORE 行为，不依赖自动化多触发
