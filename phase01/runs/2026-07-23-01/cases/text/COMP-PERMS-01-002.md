用例 ID:   COMP-PERMS-01-002
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-013
参照来源:  inputs/gitcode-spec/
母意图:    —
标题:      声明 repository write 后 TOKEN 可推送代码

前置条件:
  - 仓库具备写权限测试条件

操作步骤:
  1. 配置 permissions: repository: write
  2. 使用 ATOMGIT_TOKEN 推送代码

预期结果:
  - 写操作成功

验证点:
  - [正向] 推送代码成功返回 200/201

清理:      重置 fixture 仓库
