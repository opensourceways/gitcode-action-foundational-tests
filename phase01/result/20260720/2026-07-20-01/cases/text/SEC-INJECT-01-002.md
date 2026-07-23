用例 ID:   SEC-INJECT-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-010
母意图:    —
标题:      PR 正文（body）中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

前置条件:
  - 仓库配置了 pull_request 触发器
  - 存在一个来自 fork 的 PR，正文包含 shell 注入 payload
  - workflow 直接使用 `${{ atomgit.event.pull_request.body }}` 插入 run 脚本

操作步骤:
  1. 创建 fork PR，正文包含多行注入 payload：
     ```
     Normal PR description.
     `id`; echo INJECTED_BY_BODY; #
     Another line with $(whoami) injection
     ```
  2. 触发 pull_request 事件
  3. workflow 中的 `run: echo "${{ atomgit.event.pull_request.body }}"` 被执行
  4. 观察日志中是否出现 `INJECTED_BY_BODY` 或 `whoami` 的实际输出
  5. 同时测试 `$(...)` 命令替换和反引号命令替换

预期结果:
  - PR 正文中的 shell 元字符不应被解释执行（`;`、`$()`、反引号等）
  - 日志中不应出现注入命令的执行痕迹
  - 若平台选择报错（非静默），应有明确错误信息

验证点:
  - [负向] 日志中不应出现 `INJECTED_BY_BODY`（注入命令不应被执行）
  - [负向] 日志中不应出现注入命令的输出（如 `whoami` 结果）
  - [负向] PR 正文中的 `$()` 命令替换不应被执行
  - [负向] PR 正文中的反引号命令替换不应被执行

清理:      fixture
