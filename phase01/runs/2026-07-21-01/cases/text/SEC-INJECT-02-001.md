用例 ID:   SEC-INJECT-02-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-009
标题:      PR 标题中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

前置条件:
  - 目标仓库配置了 PR 触发 workflow
  - fork 侧提交 PR，标题包含 shell 元字符（如 `fix"; ls /"`）

操作步骤:
  1. fork PR 标题含分号+命令，workflow 将 `${{ atomgit.event.pull_request.title }}` 直接插入 run:
  2. 检查 job 日志中是否出现 ls 命令执行输出

预期结果:
  - 注入的额外 shell 命令不应在 runner 上执行
  - 若平台选择报错，应有明确的错误信息

验证点:
  - [负向] 日志中不出现注入命令执行痕迹
  - [负向] 反引号命令替换不应被执行
  - [正向] 平台对危险字符的处理行为一致（报错或转义）

清理:      fixture
