用例 ID:   COMP-ACT-03-005
维度标签:   [completeness]
维度:      功能完备性
优先级:    P2
溯源意图:  INTENT-ACT-005
母意图:    —
标题:      setup-qemu 多架构仿真——平台列表/与 buildx 联用/daemon 不可用场景

前置条件:
  - 仓库配置了使用 QEMU 仿真的 workflow
  - 已知默认资源池不支持 Docker daemon (#86)

操作步骤:
  1. 配置 workflow 使用 `uses: docker/setup-qemu-action`
  2. 在有 Docker daemon 的资源池上触发（如自定义资源池）
  3. 在后续 step 中执行 `docker run --platform linux/arm64 hello-world` 验证 arm64 仿真
  4. 验证支持的平台列表（arm64、arm/v7、s390x 等）
  5. 结合 `setup-buildx` 测试多架构镜像构建
  6. 在无 Docker daemon 的资源池上触发，观察报错行为

预期结果:
  - QEMU 二进制安装成功，`docker run --platform linux/arm64` 可正常执行
  - 支持的平台列表与声明一致（arm64 至少可用）
  - 与 buildx 联用时，多架构构建正常
  - 无 daemon 时给出清晰报错（已知 #86）

验证点:
  - [正向] `docker run --platform linux/arm64 hello-world` 成功执行
  - [正向] 多架构构建（buildx + qemu）产生多平台镜像
  - [负向] 无 daemon 时报错清晰（不含静默挂起）
  - [状态] 若无可用的 Docker daemon 资源池——标记为 blocked-by-platform

清理: fixture
