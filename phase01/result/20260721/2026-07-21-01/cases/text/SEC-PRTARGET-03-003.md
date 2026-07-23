用例 ID:   SEC-PRTARGET-03-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-038
母意图:    —
标题:      非默认分支上的旧版 workflow 文件不应成为攻击入口

前置条件:
  - 默认分支和非默认分支各有 pull_request_target workflow
  - 非默认分支 workflow 版本较旧含不安全代码

操作步骤:
  1. 攻击者向非默认分支提 PR
  2. pull_request_target 触发
  3. 验证执行的是否是默认分支的 workflow 版本

预期结果:
  - pull_request_target 应始终使用默认分支的 workflow 版本
  - 非默认分支上的旧 workflow 不应被执行

验证点:
  - [负向] 非默认分支上有不安全的 pull_request_target workflow，实际执行的应是默认分支版本
  - [负向] 攻击者修改非默认分支的 workflow 添加恶意命令，不应被执行

清理:      none
