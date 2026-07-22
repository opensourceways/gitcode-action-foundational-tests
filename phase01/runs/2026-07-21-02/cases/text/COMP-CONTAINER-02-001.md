用例 ID:   COMP-CONTAINER-02-001
维度标签:   [completeness, security]
维度:      完备性
优先级:    P1
溯源意图:  INTENT-COMP-009
标题:      验证 job 级 container 自定义镜像执行能力（含私有镜像认证）

前置条件:
  - 仓库配置了可访问的公共容器镜像
  - 如需测试私有镜像，仓库配置了 registry 认证 Secret（REGISTRY_USERNAME、REGISTRY_PASSWORD）

操作步骤:
  1. 配置 job 级 container.image 为公共镜像，触发工作流
  2. 在 job 步骤中验证文件系统/工具链与镜像声明一致
  3. 配置 job 级 container.image 为私有镜像 + credentials 引用 secret，触发工作流
  4. 验证私有镜像可成功拉取且 job 正常执行
  5. 配置错误的 credentials，验证平台给出明确报错而非静默回退到默认 Runner

预期结果:
  - 配置公共镜像后，job 在指定容器内执行，文件系统/工具链与镜像一致
  - 配置私有镜像 + 正确 credentials 后，平台成功认证并拉取镜像
  - 错误 credentials 时平台明确报错，不静默回退到宿主机 Runner 环境

验证点:
  - [正向] 公共镜像 job 内步骤输出与镜像环境一致（如特定预装命令可用）
  - [正向] 私有镜像 + 正确 secret 引用可成功拉取，job 正常执行
  - [负向] 私有镜像配错 credentials 时不应静默回退到默认 Runner，应给出镜像拉取失败的明确报错
  - [负向] 不存在的镜像地址不应无限挂起，应在合理超时后报错
  - [非功能] 容器启动/镜像拉取日志可被观测，错误信息需指明是镜像问题还是认证问题

清理:      fixture
