用例 ID:   SEC-TOKEN-01-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-023
标题:      ATOMGIT_TOKEN 在 job 结束后应自动失效
前置条件:  仓库无特殊设置；需在 job 结束后 replay API 调用
操作步骤:
  1. job 运行期间使用 ATOMGIT_TOKEN 做 API 调用 → 正常返回
  2. job 完成后使用同一 token 值 replay 同一 API 调用
预期结果: job 完成后 token 返回 401/403
验证点:
  - [正向] job 运行期间 token 有效
  - [负向] job 完成后同一 token 返回认证失败
清理:      fixture
