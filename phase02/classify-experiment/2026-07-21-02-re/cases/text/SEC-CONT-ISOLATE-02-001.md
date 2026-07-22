用例 ID:   SEC-CONT-ISOLATE-02-001
维度标签:   [security, completeness]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-040
标题:      container 运行时 step 对宿主机环境变量/Secret 的隔离有效性

前置条件:
  - 目标仓库配置了项目级 Secret（如 HOST_SECRET_MARKER）
  - Runner 宿主机上注入了可识别的标记性环境变量
  - 工作流中某 job 声明了 container 字段，且未显式映射上述宿主机 secret

操作步骤:
  1. 触发工作流，使 job 在自定义容器内执行
  2. 在容器内 step 中，尝试读取未显式传入的宿主机环境变量/secret
  3. 尝试通过 /proc 枚举宿主机进程环境，或访问宿主机默认敏感路径（如 runner 家目录、全局 /tmp）
  4. 确认显式声明的 job env / step env / container env 在容器内正常可用

预期结果:
  - 显式传入 container env 或 step env 的变量在容器内正常可用
  - 容器内 step 无法读取宿主机 runner 的未映射进程环境变量或 secret
  - 容器内无法通过默认挂载访问宿主机 /tmp、runner 家目录或工作区外的敏感文件

验证点:
  - [正向] 显式传入的环境变量在容器内可被正确读取
  - [负向] 容器内 step 不应能读取宿主机 runner 的未映射进程环境变量（如 HOST_SECRET_MARKER）
  - [负向] 容器内不应通过默认挂载访问宿主机敏感路径
  - [非功能] 隔离对官方托管 Runner 与自托管 Runner 的差异可被判定

清理:      fixture
