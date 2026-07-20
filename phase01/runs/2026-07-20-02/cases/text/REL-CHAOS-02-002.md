用例 ID:   REL-CHAOS-02-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-016
标题:      step 运行中网络中断 60s 后恢复，受影响 step 应失败但后续 step 和 job 状态正确

前置条件:
  - job 中有 step 需要网络（如 curl 外部 URL）
  - 网络中断 60s（iptables drop 出站流量）

操作步骤:
  1. step 执行 curl https://example.com 时网络被中断 60s
  2. 验证该 step 因网络不可用失败（非零退出）
  3. 验证网络恢复后 if: always() 的后续 step 正常执行
  4. 验证 job 终态正确为 failure（失败 step 未设 continue-on-error）

预期结果:
  - 网络中断期间的 curl step 失败
  - 60s 后后续 always() step 正常完成
  - job = failure

验证点:
  - [正向] curl step 失败（非零退出）
  - [正向] 网络恢复后 always() step 正常
  - [正向] job status = failure

恢复预期:   网络恢复后后续步骤正常执行
清理:      fixture
