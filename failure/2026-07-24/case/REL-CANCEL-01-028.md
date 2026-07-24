## 失败分诊 · REL-CANCEL-01-028 · 手动取消 workflow——运行中取消时 always() cleanup step 仍应执行

**判定结果**: FAIL
**失败断言**: 正向/cleanup_step_status expected=success actual=completed(但job未cancel); 正向/run_status expected=canceled actual=completed

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（10 行）:
  ```
  === JOB: cancel semantics test job (status=COMPLETED) ===
  [2026/07/23 22:26:49.936] [INFO] Job(1529978119413174272_1529978119388008455) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9ba3c7a9-e8da-440c-adcb-78eef9857334.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9ba3c7a9-e8da-440c-adcb-78eef9857334.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/57a424b2-69c1-4f3a-b2c1-b663a18b280c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/57a424b2-69c1-4f3a-b2c1-b663a18b280c.sh
  cleanup executed
  ```

- **预期行为**（Phase 01 文本用例 REL-CANCEL-01-028，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库存在一条正在运行的 workflow
  - 操作步骤 1: 手动取消该 workflow
  - 预期结果: 非 always step 被终止; if: always() 的 cleanup step 被执行; workflow 最终状态=cancelled

- **实际行为**:
  - job 以 COMPLETED 状态完成（非 CANCELED）
  - sleep 60 的 main step 正常执行完成，cleanup always step 也正常执行（打印 "cleanup executed"）
  - 测试 harness 未在 sleep 60 期间触发 workflow cancel，导致 job 自然完成而非被取消

- **对照 GitCode 规格**:
  - 无直接相关规格段落；此用例测试 cancel 机制，需要 harness 在运行中主动取消

- **环境前置条件验证**: runner 可用，job 正常调度并执行，但 harness 未注入 cancel 事件

**置信度**: 高 (job 状态为 COMPLETED 而非 CANCELED，明确说明 cancel 事件未触发)

**影响**:
- **阻塞性**: 🟡非阻塞 — cancel 功能本身可能正常，只是 harness 未触发
- **静默性**: 🔴静默错误 — harness 未触发 cancel 却期望 cancel 结果
- **影响面**: 🟡同维度 — 影响所有依赖 cancel 机制的测试
- **综合**: harness 未在 sleep 60 窗口内发送 cancel 请求，job 跑完自然结束
- **是否有规避手段**: 是（harness 在 job 异步启动后立即发送 cancel API 调用）

**建议**:
- Phase 02 harness 增加 cancel 触发逻辑：检测到 cancel 测试用例时，在 workflow 启动后通过 API 发送 cancel 请求
- 建议在 job 日志中增加 cancel 事件的时间戳标记以供验证
