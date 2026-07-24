用例 ID:   SEC-TOKEN-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-003
参照来源:  inputs/gitcode-spec/
母意图:    SEC-TOKEN-01-001
标题:      fork PR 中 ATOMGIT_TOKEN 写操作被平台拒绝

前置条件:
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 以 fork 贡献者身份提交一个尝试用 ATOMGIT_TOKEN 推送代码的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - 推送操作返回权限拒绝（403）
  - 运行日志中显示权限不足

验证点:
  - [负向] 写操作绝不应成功
  - [正向] 权限拒绝信息明确

清理:      重置 fixture 仓库
