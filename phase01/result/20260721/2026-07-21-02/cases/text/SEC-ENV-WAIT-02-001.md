用例 ID:   SEC-ENV-WAIT-02-001
维度标签:   [security, reliability]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-038
标题:      环境保护 wait timer 倒计时期间环境 Secret 不可访问

前置条件:
  - 目标仓库配置了含 wait timer 的环境（如 production）
  - 该环境关联了环境级 Secret（如 DEPLOY_TOKEN）
  - 工作流中某 job 声明了 environment: production

操作步骤:
  1. 触发工作流，使声明了 environment 的 job 进入 wait timer 等待阶段
  2. 在等待阶段观测 job 是否已开始执行含环境 secret 的步骤
  3. 检查环境变量注入与 secrets 上下文访问情况
  4. wait timer 结束后，确认环境 secret 可被正常读取和使用

预期结果:
  - wait timer 倒计时期间，对应 job 处于等待/挂起状态，不执行步骤
  - 环境 secret 在倒计时期间未被注入 job 运行时
  - 倒计时结束后且审批要求已满足，job 继续执行并可访问环境 secret

验证点:
  - [正向] wait timer 结束后且审批通过，环境 secret 可被授权 job 正常读取
  - [负向] wait timer 倒计时期间，job 不应开始执行含环境 secret 的步骤
  - [负向] 环境 secret 不应以环境变量或 secrets 上下文形式注入等待中的 job
  - [负向] 日志中不应出现环境 secret 的引用或值
  - [非功能] wait timer 剩余时间可被观测；倒计时状态与 secret 可访问性强绑定，不可被重触发/跳过事件绕过

清理:      fixture
