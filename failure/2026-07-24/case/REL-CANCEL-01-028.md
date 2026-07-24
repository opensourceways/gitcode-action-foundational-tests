## 失败分诊 · REL-CANCEL-01-028 · 手动取消 workflow——运行中取消时 always() cleanup step 仍应执行

**判定结果**: FAIL
**失败断言**: 正向/cleanup_step_status expected=success actual=N/A（job 未被 cancel 即完成）; 正向/run_status expected=canceled actual=completed

**根因初判**: 环境/Harness（取消时机太晚，job 已提前完成）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: cancel semantics test job (status=COMPLETED) ===
  [2026/07/23 22:26:49.936 GMT+08:00] [INFO] Job(1529978119413174272_1529978119388008455) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9ba3c7a9-e8da-440c-adcb-78eef9857334.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9ba3c7a9-e8da-440c-adcb-78eef9857334.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/57a424b2-69c1-4f3a-b2c1-b663a18b280c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/57a424b2-69c1-4f3a-b2c1-b663a18b280c.sh
  cleanup executed
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库存在一条正在运行的 workflow
  - 操作步骤: 手动取消该 workflow
  - 预期结果: 非 always step 被终止; `if: ${{ always() }}` 的 cleanup step 被执行; workflow 最终状态=cancelled

- **实际行为**:
  - Job 的 sleep 和 cleanup step 均正常执行完毕，status=COMPLETED（而非 CANCELED）
  - cleanup step 输出了 `cleanup executed`
  - 说明 workflow 在取消操作到达前已完成全部 steps 的正常执行
  - **失败传导链**: job 执行过快（sleep 60s 可能被 runner 提前分配并快速完成）→ test harness 发出的 cancel API 调用到达时 job 已 COMPLETED → 断言的 run_status=canceled 不满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` 的 steps:
    ```yaml
    - name: sleep main step
      run: |
        sleep 60
    - name: cleanup always step
      if: ${{ always() }}
      run: |
        echo cleanup executed
    ```
  - **GitCode 规格** `writing-pipelines/configure-conditional-execution.md` 第 86-87 行:
    ```yaml
    - name: Cleanup
      if: ${{ always }}
      run: ./cleanup.sh
    ```
  - **GitCode 规格** `writing-pipelines/configure-conditional-execution.md` 第 90 行:
    `if: ${{ always }}` 会强制 step 执行，即使前置步骤失败或 workflow 被取消
  - **GitCode 规格** `syntax-reference/context.md` — 状态函数 `always` 在任何状态都返回 true
  - **逐项映射**: `if: ${{ always() }}` → 匹配规格示例 `${{ always }}`; `run: echo cleanup executed` → 匹配; `sleep 60` → 作为取消前的延时主步骤已执行。测试 YAML 写法与规格一致。

- **环境前置条件验证**: runner 可用，两个 steps 均正常执行；cleanup step 成功输出 `cleanup executed`；但 test harness 取消操作未在 60 秒窗口内发出或未及时生效

**置信度**: 中（job 确实完成了全部步骤，但无法从日志判断取消操作是否被正确触发、何时触达、或是否被平台忽略）

**影响**:
- **阻塞性**: 🟡中等 — 核心取消语义待验证但未被充分测试
- **静默性**: 🟡中等 — job 静默完成，无 cancel 行为可观测
- **影响面**: 🟡同用例 — 仅影响取消语义验证用例
- **综合**: test harness 的 cancel API 未能让 job 在 sleep 窗口内被取消，导致 cancel 断言不满足
- **是否有规避手段**: 是（增加 sleep 时长到 120-180 秒确保有足够窗口执行取消；或检查 test harness cancel 触发时机）

**建议**:
- test harness 在 workflow 启动后立即触发 cancel，而非等待 job 开始的延迟
- 将 sleep 时长增加到 120-180 秒，确保取消操作在 sleep 期间到达 runner
- 检查平台 cancel API 的响应延时和 runner 端信号处理
