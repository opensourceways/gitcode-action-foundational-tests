## 失败分诊 · REL-CONC-01-001 · concurrency.max=5 时同时触发 5 个运行应全部进入执行态

**判定结果**: FAIL
**失败断言**: 正向/run_status expected=completed(success) actual=N/A (仅 1 个 run log); 非功能/queued_to_running_latency le=60s actual=N/A

**根因初判**: 环境/Harness（仅记录到 1 个 run 的 log，多 run 并发触发可能未正确完成或 log 收集不全）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: concurrency test job (status=COMPLETED) ===
  [2026/07/23 22:27:10.892 GMT+08:00] [INFO] Job(1529978207228936192_1529978207195381767) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/dd24ba4a-9120-473f-abbc-4663e320e1bb.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/dd24ba4a-9120-473f-abbc-4663e320e1bb.sh
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库已配置 concurrency.max=5 的 workflow
  - 操作步骤: 同时通过 API 触发 5 次该 workflow
  - 预期结果: 5 个运行均进入 in_progress 状态; 全部在合理时间内完成

- **实际行为**:
  - 日志中仅 1 个 job instance 的 log（status=COMPLETED），sleep 10 秒后正常退出
  - 预期应有 5 次 workflow run 的 log，实际仅收集到 1 次
  - 无法从现有 log 判断其他 4 次是否被触发、是否排队、是否成功执行
  - **失败传导链**: 日志收集不全 → 无法验证 5 并发断言 → case FAIL

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 workflow 级 `concurrency`:
    ```yaml
    concurrency:
      max: 5
      exceed-action: QUEUE
    ```
  - **测试 YAML** 中 `test` 的 step:
    ```yaml
    - name: sleep step
      run: |
        sleep 10
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 154-165 行:
    ```yaml
    jobs:
      deploy:
        runs-on: [ubuntu-latest, x64, small]
        concurrency:
          enable: true
          max: 1
          exceed-action: IGNORE
    ```
  - **逐项映射**: `concurrency.max: 5` → 规格支持 `concurrency`; `exceed-action: QUEUE` → 规格支持 `QUEUE/IGNORE`; `sleep 10` → 匹配。注：规格中 `concurrency` 是 job 级别，测试 YAML 使用的是 workflow 级别——需确认平台是否支持 workflow 级 concurrency。
  - **GitCode 规格** `syntax-reference/context.md` — concurrency 配置在 job 级别的文档中有 `enable` 字段，但测试 YAML 未包含 `enable: true`。

- **环境前置条件验证**: runner 可用（1 个 job 正常完成），但 log 仅收集到 1 次 run

**置信度**: 低（日志严重不全，无法判断是 test harness 触发失败、log 收集遗漏、还是平台 concurrency 行为异常）

**影响**:
- **阻塞性**: 🟡中等 — 无法判断是 log 收集问题还是平台并发控制问题
- **静默性**: 🔴静默 — 无错误日志，仅在断言阶段因数据不足而失败
- **影响面**: 🟡同用例 — 仅影响此并发用例
- **综合**: log 收集不全，仅 1/5 次 run 有记录，根因待确认
- **是否有规避手段**: 是（检查 test harness 是否确实触发了 5 次 workflow run，并确认 log 收集逻辑覆盖所有 run）

**建议**:
- 检查 test harness 多 run 触发逻辑：是否等待每次 workflow_dispatch 完成后再触发下一次
- 确认 log 收集是否覆盖所有 run（目前仅 1 个 job log）
- 考虑使用独立 workflow YAML 文件（不同 name）分别触发，或增加 `sleep 10` > `sleep 60` 以确保同时观察并发
