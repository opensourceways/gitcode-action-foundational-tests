用例 ID:   SEC-TOKEN-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-036
母意图:    —
标题:      平台内置 ATOMGIT_TOKEN 不应在未授权上下文被引用泄露

前置条件:
  - 主仓库配置了 ATOMGIT_TOKEN
  - fork PR 和内部 push 两种触发场景

操作步骤:
  1. fork PR workflow 中 echo `${{ secrets.atomgit_token }}`
  2. 内部 push workflow 中 echo `${{ secrets.atomgit_token }}`
  3. 对比两种场景下的日志输出

预期结果:
  - fork PR 下 ATOMGIT_TOKEN 返回空或降级后只读 token
  - 日志中被遮蔽为 `***`
  - 内部 push 下正常可用但也被遮蔽

验证点:
  - [负向] fork PR 下 echo 输出为 `***` 或空
  - [负向] 内部 push 下 echo 输出为 `***`
  - [负向] 日志搜索 token 前缀命中数 = 0

清理: fixture
