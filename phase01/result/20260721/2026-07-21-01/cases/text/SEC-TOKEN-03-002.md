用例 ID:   SEC-TOKEN-03-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-023
母意图:    —
标题:      ATOMGIT_TOKEN 在 job 结束后应自动失效

前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. workflow job 运行期间使用 ATOMGIT_TOKEN 做 API 调用
  2. job 完成后取同 token 值尝试再次 API 调用
  3. 验证是否返回认证失败

预期结果:
  - job 运行期间 ATOMGIT_TOKEN API 调用正常
  - job 完成后同 token 值 API 调用返回 401/403

验证点:
  - [正向] job 运行期间 ATOMGIT_TOKEN API 调用正常
  - [负向] job 完成后同 token 值 API 调用返回 401/403

清理:      none
