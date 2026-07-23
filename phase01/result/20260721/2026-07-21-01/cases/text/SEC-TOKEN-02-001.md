用例 ID:   SEC-TOKEN-02-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-036
标题:      平台内置 ATOMGIT_TOKEN 在 fork PR 下不应为有效完整 token

前置条件:
  - fork PR 触发 pull_request 事件
  - workflow 中 echo `${{ secrets.atomgit_token }}`

操作步骤:
  1. fork PR 下 echo `${{ secrets.atomgit_token }}`
  2. 内部 push 下 echo `${{ secrets.atomgit_token }}`（对照）
  3. 日志搜索 token 前缀

预期结果:
  - fork PR 下 token 被遮蔽或为空
  - 内部事件下同等脱敏
  - 任何情况下日志不泄露 token 明文

验证点:
  - [负向] fork PR 下 token 值为空或降级
  - [负向] 日志不出现有效 token 值
  - [正向] 内部事件下 token 正常可用但脱敏

清理:      fixture
