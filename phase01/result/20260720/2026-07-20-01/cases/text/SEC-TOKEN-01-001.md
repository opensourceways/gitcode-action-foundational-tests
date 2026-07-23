用例 ID:   SEC-TOKEN-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-036
母意图:    —
标题:      平台内置 secret（ATOMGIT_TOKEN）不应在未授权上下文被引用泄露

前置条件:
  - 仓库无特殊 permissions 设置
  - 比较两种场景：内部 push 触发 vs fork PR 触发
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 提交 workflow（内部 push 触发），在 job 中 `echo "${{ secrets.atomgit_token }}"`
  2. 从 fork 提交 PR，触发同一 workflow（fork PR 场景）
  3. 在两种场景下分别观察 echo 输出
  4. 通过 API 拉取 job 日志，搜索 ATOMGIT_TOKEN 的明文（及其前缀模式）
  5. 尝试在 fork PR 下使用该 token 做 API 认证调用

预期结果:
  - 内部 push 触发时，日志中 `${{ secrets.atomgit_token }}` 被脱敏为 `***`
  - fork PR 触发时，`${{ secrets.atomgit_token }}` 返回空值或降级后的只读 token
  - fork PR 下日志全文中不出现有效 token 明文
  - 任何情况下日志中不泄露 ATOMGIT_TOKEN 明文（包括 token 前缀如 `ghs_` 或等效前缀）

验证点:
  - [负向] fork PR 下 echo ATOMGIT_TOKEN 日志输出为 `***` 或空，不应是有效 token
  - [负向] 内部 push 下 echo ATOMGIT_TOKEN 日志输出应被遮蔽为 `***`
  - [负向] 日志全文搜索 token 前缀模式命中数为 0
  - [负向] fork PR 下 ATOMGIT_TOKEN 为空时，基于它的 API 调用应返回认证失败

清理:      fixture
