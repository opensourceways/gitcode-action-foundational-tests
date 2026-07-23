```
用例 ID:   COMPAT-PERM-01-002
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-002
母意图:    —
标题:      未声明 permissions 时 fork PR 写操作隔离

前置条件:
  - 仓库已启用 GitCode Action
  - 存在一个来自外部 fork 的 PR
  - workflow 中未显式声明 permissions 块

操作步骤:
  1. 以外部 fork 贡献者身份，提交一个尝试执行写操作（如推送标签、修改文件）的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - 系统对 fork PR 的默认 TOKEN 进行写操作隔离
  - 写操作被拒绝或失败，不会实际修改目标仓库

验证点:
  - [负向] 写操作（如 git push 或 API 写调用）失败或被阻止
  - [负向] 目标仓库内容未被修改
  - [正向] fork 身份无法获得写权限

清理:      重置 fixture 仓库并清理测试分支
```
