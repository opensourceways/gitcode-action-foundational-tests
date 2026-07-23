用例 ID:   SEC-INJECT-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-009
母意图:    —
标题:      PR 标题中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

前置条件:
  - 仓库配置了 pull_request 触发器
  - 存在一个来自 fork 的 PR
  - workflow 在 job 中直接使用 `${{ atomgit.event.pull_request.title }}` 插入 run 脚本

操作步骤:
  1. 创建 fork PR，标题设置为包含 shell 注入 payload 的字符串：
     `fix"; echo INJECTED_BY_TITLE; #`
  2. 触发 pull_request 事件（fork PR）
  3. workflow 中的 `run: echo "${{ atomgit.event.pull_request.title }}"` 被执行
  4. 观察日志中是否出现 `INJECTED_BY_TITLE` 的输出（如出现说明分号后的命令被执行）
  5. 对比：同时测试通过 env 中间变量安全引用方式的场景

预期结果:
  - 被插入 run 脚本的 PR 标题中，分号后的 `echo INJECTED_BY_TITLE` 不应被作为独立命令执行
  - 日志中不应出现注入命令的执行痕迹
  - 若平台对危险字符做转义处理，job 应正常完成（标题作为字符串参数输出）
  - 若平台报错（如表达式求值阶段检测到危险字符），应有明确错误信息

验证点:
  - [负向] 日志中不应出现 `INJECTED_BY_TITLE`（注入命令的执行痕迹）
  - [负向] PR 标题中的 shell 元字符不应被解释执行
  - [正向] 通过 env 中间变量安全引用方式的 step 应正常完成
  - [负向] 不应出现因注入导致的额外副作用（如文件创建、网络请求）

清理:      fixture
