用例 ID:   SEC-INJECT-03-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-011
母意图:    —
标题:      分支名中的不可信输入不应通过 ${{ }} 直接插入 run 导致命令注入

前置条件: 主仓库有 push 触发 workflow，run 中引用 `${{ atomgit.ref_name }}`

操作步骤:
  1. 创建分支名含 `zzz";echo${IFS}"INJECTED_BRANCH";#`
  2. 推送该分支触发 workflow
  3. 观察 job 日志中是否出现 INJECTED_BRANCH

预期结果: 分支名中的分号+命令不应被执行；INJECTED_BRANCH 不应出现在日志中

验证点:
  - [负向] job 日志不出现 INJECTED_BRANCH
  - [负向] 分支名中的分号和 echo 命令不产生副作用
  - [正向] workflow 正常完成（分支名被当作字面字符串处理）

清理: fixture
