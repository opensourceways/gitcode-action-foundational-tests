用例 ID:   SEC-CONT-CRED-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-039
标题:      私有 container 镜像拉取凭证的安全传递与日志不泄露

前置条件:
  - 仓库配置了用于私有镜像仓库认证的 Secret（REGISTRY_USERNAME、REGISTRY_PASSWORD）
  - 工作流中某 job 声明了 container 字段并引用上述 secret 作为 credentials

操作步骤:
  1. 触发工作流，使 job 尝试拉取私有镜像
  2. 观测镜像拉取阶段日志，确认凭证未以明文出现
  3. 若拉取失败，检查错误消息是否仅显示仓库地址而不暴露认证头或密码
  4. 确认 runner 系统日志与 daemon 输出中同样不含凭证明文

预期结果:
  - 使用 secrets 引用时，私有镜像可被正常拉取，job 正常执行
  - 镜像拉取阶段及运行日志中不出现 registry 用户名/密码明文
  - 拉取失败时的错误消息不暴露认证信息

验证点:
  - [正向] 使用 ${{ secrets.REGISTRY_USERNAME }} / ${{ secrets.REGISTRY_PASSWORD }} 时私有镜像可正常拉取
  - [负向] 镜像拉取成功或失败的日志中，不得出现 REGISTRY_USERNAME / REGISTRY_PASSWORD 的明文原值
  - [负向] runner 系统日志、daemon 输出中不得出现凭证明文
  - [非功能] 凭证脱敏覆盖 stdout、stderr 及异常堆栈回显

清理:      fixture
