用例 ID:   COMP-ACT-03-006
维度标签:   [completeness]
维度:      功能完备性
优先级:    P2
溯源意图:  INTENT-ACT-006
母意图:    —
标题:      setup-buildx 构建器配置——安装/自定义 builder/多架构/缓存/daemon 不可用场景

前置条件:
  - 仓库配置了使用 Buildx 构建器的 workflow
  - 已知默认资源池不支持 Docker daemon (#86)

操作步骤:
  1. 配置 workflow 使用 `uses: docker/setup-buildx-action`
  2. 在有 Docker daemon 的资源池上触发
  3. 在后续 step 中执行 `docker buildx version` 验证安装
  4. 执行 `docker buildx create --name test-builder` 创建自定义 builder
  5. 结合 setup-qemu 测试多架构镜像构建（`--platform linux/amd64,linux/arm64`）
  6. 测试 buildx 缓存（`--cache-from`/`--cache-to`）在 GitCode runner 上的行为
  7. 在无 daemon 的资源池上触发，观察报错

预期结果:
  - `docker buildx version` 正常输出版本信息
  - 自定义 builder 创建成功
  - 多架构构建正常产生多平台镜像
  - 无 daemon 时报错清晰

验证点:
  - [正向] `docker buildx version` 可用
  - [正向] 自定义 builder 创建后可正常构建
  - [正向] 多架构镜像构建成功
  - [负向] 无 daemon 时报错清晰（不含静默挂起）
  - [状态] 若无可用的 Docker daemon 资源池——标记为 blocked-by-platform

清理: fixture
