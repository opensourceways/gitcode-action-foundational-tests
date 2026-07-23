用例 ID:   COMP-ACT-03-004
维度标签:   [completeness, reliability]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-ACT-004
母意图:    —
标题:      docker/login 登录认证与 daemon 可用性——已知默认资源池不支持 daemon (#86)

前置条件:
  - 仓库配置了 Docker 登录相关 workflow
  - 已知默认资源池不支持 Docker daemon (#86 P1 blocker)

操作步骤:
  1. 配置 workflow 使用 `uses: official_docker_login`，提供 username/password
  2. 在默认资源池（`ubuntu-latest`）上触发，观察 daemon 不可用时的报错行为
  3. 在支持 Docker daemon 的自定义资源池（如有）上触发
  4. 登录成功后尝试 `docker pull` 私有镜像
  5. 检查后续 step 的日志中是否有登录凭证残留

预期结果:
  - 默认资源池上 daemon 不可用时，报错信息清晰（不应静默挂起或超时）
  - 支持 daemon 的资源池上，登录成功后可拉取私有镜像
  - 登录凭证不在后续 step 日志中明文出现

验证点:
  - [正向] 默认资源池 daemon 不可用时给出明确报错（已知 #86）
  - [正向] 有 daemon 时登录成功，`docker pull` 私有镜像可用
  - [负向] 后续 step 日志不含密码明文
  - [状态] 若无可用的 Docker daemon 资源池——标记为 blocked-by-platform

清理: fixture
