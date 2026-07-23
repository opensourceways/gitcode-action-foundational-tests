用例 ID:   REL-CHAOS-02-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-017
标题:      runner 在 checkout 步骤前意外崩溃，重新运行后 workflow 可完整完成

前置条件:
  - workflow 有 checkout + build + test 步骤
  - runner 在 checkout 前被 kill（模拟宿主宕机）

操作步骤:
  1. job 启动后 5s 内 kill runner 进程（checkout 前）
  2. 验证 job 最终到达 failure/cancelled（心跳超时后）
  3. Re-run all jobs → 全部 job 在干净 runner 上 success

预期结果:
  - 因 runner 崩溃未执行的 job 到终态（不 stuck）
  - Re-run all jobs 后全部 success
  - 无残留状态导致重复失败

验证点:
  - [正向] 崩溃 job 最终到达终态
  - [正向] Re-run all jobs → 全部 success
  - [负向] 重新运行不出残留状态错误

恢复预期:   Re-run all jobs 后所有 job success
清理:      full_instance
