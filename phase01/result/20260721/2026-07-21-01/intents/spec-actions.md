# 规格分析：缺失 Action 完备性补全意图

> Agent: spec-analyst | 维度: completeness | Run: 2026-07-21-01
> 输入: `phase01/inputs/history/gitcode-actions-list.md` (25 官方 Action 清单)
> 生成依据: 14 个现有 intents (spec.md) 中未覆盖的 Action，需补充完备性意图
> ID 格式: `INTENT-ACT-NNN`，从 001 起

---

## 一、语言运行时安装 (setup-*)

### INTENT-ACT-001 | setup-gradle 安装与版本选择

- **维度**: completeness
- **来源**: `gitcode-actions-list.md` 行 3, `uses: setup-gradle`
- **优先级**: P1
- **说明**: 验证 `setup-gradle` Action 的完整安装链路：(1) 指定版本号时实际安装的 Gradle 版本是否与声明一致；(2) 不指定版本时的默认版本行为；(3) 指定不存在版本时的报错信息是否清晰（已知 setup-* 系列经常下载失败 #50/#98）；(4) 安装后 Gradle 在后续 step/job 中是否可用（`gradle --version` 可正常执行）。
- **Oracle 来源**: `gitcode-actions-list.md` 语言运行时安装 section 测试要点——各插件的版本范围与实际安装版本、指定不存在的版本时的报错信息、已安装工具在后续 step/job 中的可用性。
- **溯源风险**: 已知 setup-* 系列版本说明缺失、下载失败频繁 (#50, #98)；自定义资源池兼容性未知。

---

### INTENT-ACT-002 | setup-yarn 安装与版本选择

- **维度**: completeness
- **来源**: `gitcode-actions-list.md` 行 5, `uses: setup-yarn`
- **优先级**: P1
- **说明**: 验证 `setup-yarn` Action 的完整安装链路：(1) 指定版本号（如 `1.22.19`、`3.x`）时实际安装的 Yarn 版本是否与声明一致；(2) 不指定版本时的默认版本行为（Yarn 1.x vs 3.x）；(3) 指定不存在版本时的报错信息是否清晰；(4) 安装后 Yarn 在后续 step/job 中是否可用（`yarn --version` 可正常执行）；(5) 与 `setup-node` 联用时 Node.js 版本兼容性（Yarn 3+ 需要 Node.js 16+）。
- **Oracle 来源**: `gitcode-actions-list.md` 语言运行时安装 section 测试要点——各插件的版本范围与实际安装版本、指定不存在的版本时的报错信息、已安装工具在后续 step/job 中的可用性。
- **溯源风险**: 已知 setup-* 系列版本说明缺失、下载失败频繁 (#50, #98)；Yarn 版本与 Node.js 版本耦合可能导致间接失败。

---

### INTENT-ACT-003 | setup-pnpm 安装与版本选择

- **维度**: completeness
- **来源**: `gitcode-actions-list.md` 行 6, `uses: setup-pnpm`
- **优先级**: P1
- **说明**: 验证 `setup-pnpm` Action 的完整安装链路：(1) 指定版本号（如 `8.x`、`9.0.0`）时实际安装的 pnpm 版本是否与声明一致；(2) 不指定版本时的默认版本行为；(3) 指定不存在版本时的报错信息是否清晰；(4) 安装后 pnpm 在后续 step/job 中是否可用（`pnpm --version` 可正常执行）；(5) pnpm 依赖的 Node.js 版本兼容性。
- **Oracle 来源**: `gitcode-actions-list.md` 语言运行时安装 section 测试要点——各插件的版本范围与实际安装版本、指定不存在的版本时的报错信息、已安装工具在后续 step/job 中的可用性。
- **溯源风险**: 已知 setup-* 系列版本说明缺失、下载失败频繁 (#50, #98)。

---

## 二、Docker 生态

### INTENT-ACT-004 | docker/login 登录认证与 daemon 可用性

- **维度**: completeness, reliability
- **来源**: `gitcode-actions-list.md` 行 19, `uses: official_docker_login`
- **优先级**: P1
- **说明**: 验证 `docker/login` Action 的完整登录链路：(1) 使用 username/password 方式登录 Docker registry；(2) 登录成功后 `docker pull` 私有镜像是否可用；(3) **已知 daemon 不可用 #86**——默认资源池不支持 Docker daemon，验证在此场景下的报错信息是否清晰（而非静默挂起）；(4) 自定义资源池（支持 Docker daemon）中登录是否正常；(5) 登录凭证在后续 step/job 中是否残留（安全性）。
- **Oracle 来源**: `gitcode-actions-list.md` Docker section 测试要点——登录认证、daemon 可用性（已知默认资源池不支持 #86）。
- **溯源风险**: 已知 #86: 默认资源池 daemon 不可用（P1 blocker）；daemon 不可用时行为未文档化。

---

### INTENT-ACT-005 | setup-qemu 多架构仿真

- **维度**: completeness
- **来源**: `gitcode-actions-list.md` 行 21, `uses:` (setup-qemu-action)
- **优先级**: P2
- **说明**: 验证 QEMU 仿真 Action 的核心链路：(1) QEMU 二进制安装是否成功（`docker run --platform linux/arm64 hello-world`）；(2) 支持的平台列表（arm64、arm/v7、s390x 等）是否与声明一致；(3) 与 `setup-buildx` 联用时多架构构建是否正常；(4) 在非 Docker daemon 环境下的行为（已知 #86）。
- **Oracle 来源**: `gitcode-actions-list.md` Docker section 测试要点——多架构构建。
- **溯源风险**: 已知 #86 daemon 不可用影响 QEMU 全部功能；平台兼容性未文档化。

---

### INTENT-ACT-006 | setup-buildx 构建器配置

- **维度**: completeness
- **来源**: `gitcode-actions-list.md` 行 22, `uses:` (setup-buildx-action)
- **优先级**: P2
- **说明**: 验证 Buildx 构建器 Action 的核心链路：(1) Buildx 安装与 `docker buildx version` 可用性；(2) 创建自定义 builder 实例（`docker buildx create`）；(3) 多架构镜像构建（与 setup-qemu 联用）；(4) 缓存（`--cache-from`/`--cache-to`）在 GitCode runner 上的行为；(5) 在非 Docker daemon 环境下的行为（已知 #86）。
- **Oracle 来源**: `gitcode-actions-list.md` Docker section 测试要点——Buildx 构建器、多架构构建。
- **溯源风险**: 已知 #86 daemon 不可用影响 buildx 全部功能；buildx 缓存机制在 GitCode runner 上的兼容性未知。

---

## 三、对象存储 (OBS)

### INTENT-ACT-007 | OBS 上传完整链路

- **维度**: completeness, reliability
- **来源**: `gitcode-actions-list.md` 行 15, `uses: official_obs_upload`
- **优先级**: P1
- **说明**: 验证 OBS 上传 Action 的完整链路：(1) 基本文件上传——单文件上传成功后对象存在于 OBS bucket；(2) **已知目录路径 #15**——目录上传是否正确递归、路径格式是否正确（网络偶发失败）；(3) **已知变量路径 #16**——使用 `${{ env.BUILD_DIR }}` 等变量指定路径时是否可正确解析并上传；(4) bucket/endpoint/ak/sk 等参数的有效性校验（缺少必填参数时的报错）；(5) 大文件上传（>100MB）的稳定性。
- **Oracle 来源**: `gitcode-actions-list.md` OBS 对象存储 section 测试要点——网络可用性（已知偶发失败 #15）、目录上传、变量路径解析。
- **溯源风险**: 已知 #15: 网络偶发失败、目录路径问题（P1）；已知 #16: 变量路径无法解析（P1）。

---

### INTENT-ACT-008 | OBS 下载完整链路

- **维度**: completeness
- **来源**: `gitcode-actions-list.md` 行 16, `uses: official_obs_download`
- **优先级**: P1
- **说明**: 验证 OBS 下载 Action 的完整链路：(1) 基本文件下载——指定 bucket+object key 下载到本地路径；(2) 下载不存在的对象时的报错信息是否清晰（而非泛化 failure）；(3) 使用变量指定下载路径时的解析正确性；(4) 下载路径权限问题（本地无写权限时的报错）；(5) 大文件下载的稳定性；(6) 与 `official_obs_upload` 的端到端联调——上传后下载验证内容一致。
- **Oracle 来源**: `gitcode-actions-list.md` OBS 对象存储 section 测试要点——网络可用性、目录上传、变量路径解析。
- **溯源风险**: 网络偶发失败（同 #15）；变量路径解析（同 #16）。

---

## 四、容器镜像仓库 (SWR)

### INTENT-ACT-009 | SWR 上传/下载与 ak/sk 认证

- **维度**: completeness, security
- **来源**: `gitcode-actions-list.md` 行 17-18, `uses: official_swr`
- **优先级**: P1
- **说明**: 验证 SWR 容器镜像仓库 Action 的完整链路：(1) **已知 ak/sk 认证 #72-74**——使用 AK/SK 方式登录 SWR 是否成功；(2) 镜像上传——`docker push` 到 SWR registry 后镜像可见；(3) 镜像下载——`docker pull` 从 SWR registry 拉取镜像；(4) 认证失败（错误 ak/sk）时的报错信息是否清晰且不泄露密钥；(5) 镜像 tag 管理——多 tag 推送、latest tag 覆盖等。
- **Oracle 来源**: `gitcode-actions-list.md` SWR section 测试要点——认证（ak/sk 登录待验证 #72/#73/#74）、镜像 tag 管理。
- **溯源风险**: 已知 #72, #73, #74: ak/sk 认证待验证（P1）；SWR registry 网络连通性在大陆外区域可能不稳定。

---

## 五、构建加速与 IaC

### INTENT-ACT-010 | build_accelerate 构建加速与自定义资源池兼容性

- **维度**: completeness, reliability
- **来源**: `gitcode-actions-list.md` 行 10, `uses: official_build_accelerate`
- **优先级**: P1
- **说明**: 验证构建加速 Action 的核心链路：(1) 基本功能——启用 build_accelerate 后的构建时长是否明显短于未启用（需有对比基线）；(2) **已知自定义资源池兼容性**——在自定义资源池（self-hosted runner）上 build_accelerate 是否正常生效，还是仅支持托管 Runner；(3) 自定义镜像（`container.image`）场景下 build_accelerate 的行为；(4) 加速失败时的降级——是否回退到正常构建（graceful degradation）还是直接失败；(5) 输出信息中是否可观测到加速效果（如缓存命中率、加速比）。
- **Oracle 来源**: `gitcode-actions-list.md` 构建加速与 IaC section 测试要点——buildaccelarate 在自定义资源池的兼容性。
- **溯源风险**: 自定义资源池兼容性未知（P1）；降级行为未文档化。

---

### INTENT-ACT-011 | setup_terraform IaC 工具安装

- **维度**: completeness
- **来源**: `gitcode-actions-list.md` 行 11, `uses: setup_terraform`
- **优先级**: P2
- **说明**: 验证 Terraform 安装 Action 的完整链路：(1) 指定版本号（如 `1.5.0`）时实际安装的 Terraform 版本是否与声明一致；(2) 不指定版本时的默认版本行为；(3) 指定不存在版本时的报错信息是否清晰；(4) 安装后 `terraform version` 在后续 step 中是否可用；(5) Terraform CLI 基本操作（`terraform init`）在 GitCode runner 上是否可执行（网络连通性）。
- **Oracle 来源**: `gitcode-actions-list.md` 构建加速与 IaC section——setup_terraform IaC 基础设施部署。
- **溯源风险**: Terraform 二进制下载依赖 HashiCorp 官方源，大陆网络连通性需验证。

---

## 六、K8s 部署

### INTENT-ACT-012 | k8s_deploy 部署完整链路

- **维度**: completeness, security
- **来源**: `gitcode-actions-list.md` 行 23, `uses: official_k8s_deploy`
- **优先级**: P1
- **说明**: 验证 K8s 部署 Action 的完整链路：(1) **kubeconfig 认证**——提供有效的 kubeconfig（通过 secret）后 `kubectl` 能否正常连接集群；(2) **namespace**——指定与不指定 namespace 时的部署行为（默认 namespace、不存在的 namespace）；(3) 资源清单格式——支持 Deployment/Service/ConfigMap 等常见资源的 apply；(4) 部署失败时的错误回传——无效的 kubeconfig、不存在的集群、格式错误的清单是否能给出清晰报错；(5) kubeconfig 内容在日志中是否被脱敏。
- **Oracle 来源**: `gitcode-actions-list.md` K8s 部署 section 测试要点——kubeconfig 认证、命名空间、资源清单格式。
- **溯源风险**: kubeconfig 凭证安全性——日志脱敏未声明；网络连通性（集群 API server 是否可达）。

---

## 七、CI/CD 工具集成

### INTENT-ACT-013 | paths_filter 路径过滤

- **维度**: completeness
- **来源**: `gitcode-actions-list.md` 行 24, `uses: official_paths_filter`
- **优先级**: P2
- **说明**: 验证路径过滤 Action 的核心链路：(1) **glob pattern**——支持 `**/*.js`、`src/**`、`*.md` 等常见 glob 模式；(2) 多 pattern 组合——同时指定多个路径 pattern 时的 OR/AND 语义；(3) 变更文件匹配——当变更文件命中 pattern 时正确输出过滤结果；(4) 变更文件未命中 pattern 时正确标记为未变更；(5) 在 `if` 条件中使用过滤结果控制后续 step 执行；(6) 否定 pattern（如 `!docs/**`）是否支持。
- **Oracle 来源**: `gitcode-actions-list.md` CI/CD 工具集成 section 测试要点——paths-filter 的 glob pattern 支持。
- **溯源风险**: glob 语法支持范围未文档化（是否支持 `{,}` 花括号展开、`?` 单字符匹配等扩展语法）。

---

### INTENT-ACT-014 | codecov 覆盖率上报

- **维度**: completeness, security
- **来源**: `gitcode-actions-list.md` 行 25, `uses: codecov-action`
- **优先级**: P2
- **说明**: 验证 Codecov 覆盖率上报 Action 的完整链路：(1) **覆盖率文件路径**——指定 coverage 文件路径（如 `coverage/lcov.info`）后是否能正确上传；(2) 未指定覆盖率文件时是否能自动发现常见文件（lcov.info、cobertura.xml 等）；(3) **token 认证**——使用 Codecov token（通过 secret 传入）时上传是否成功；(4) 无 token 的公开仓库上传是否可用；(5) 覆盖率文件不存在时的报错信息是否清晰；(6) 大覆盖率文件（>1MB）的上传行为。
- **Oracle 来源**: `gitcode-actions-list.md` CI/CD 工具集成 section 测试要点——codecov 的覆盖率文件路径、token 认证。
- **溯源风险**: Codecov API 网络连通性（大陆访问 Codecov 服务）；token 在日志中的脱敏。

---

## 二、覆盖度总览

### 按 Action 分类

| # | INTENT-ACT | Action | uses: ref | 优先级 | 已知问题 |
|---|---|---|---|---|---|
| 001 | setup-gradle | Gradle 安装 | `setup-gradle` | P1 | setup-* 版本/下载 (#50, #98) |
| 002 | setup-yarn | Yarn 安装 | `setup-yarn` | P1 | setup-* 版本/下载 (#50, #98) |
| 003 | setup-pnpm | pnpm 安装 | `setup-pnpm` | P1 | setup-* 版本/下载 (#50, #98) |
| 004 | docker/login | Docker 登录 | `official_docker_login` | P1 | daemon 不可用 #86 |
| 005 | qemu | QEMU 仿真 | (setup-qemu-action) | P2 | daemon #86 |
| 006 | buildx | Buildx 构建器 | (setup-buildx-action) | P2 | daemon #86 |
| 007 | OBS上传 | OBS 对象上传 | `official_obs_upload` | P1 | 目录路径 #15, 变量路径 #16 |
| 008 | OBS下载 | OBS 对象下载 | `official_obs_download` | P1 | 网络偶发 (#15), 变量路径 (#16) |
| 009 | SWR | SWR 镜像仓库 | `official_swr` | P1 | ak/sk 认证 #72-74 |
| 010 | build_accelerate | 构建加速 | `official_build_accelerate` | P1 | 自定义资源池兼容性 |
| 011 | setup_terraform | Terraform 安装 | `setup_terraform` | P2 | 下载源连通性 |
| 012 | k8s_deploy | K8s 部署 | `official_k8s_deploy` | P1 | kubeconfig, namespace |
| 013 | paths_filter | 路径过滤 | `official_paths_filter` | P2 | glob pattern |
| 014 | codecov | 覆盖率上报 | `codecov-action` | P2 | coverage file, token |

### 按优先级

| 优先级 | 意图数量 | Action 列表 |
|---|---|---|
| P1 | 9 | setup-gradle, setup-yarn, setup-pnpm, docker/login, OBS上传, OBS下载, SWR, build_accelerate, k8s_deploy |
| P2 | 5 | qemu, buildx, setup_terraform, paths_filter, codecov |

### 与已有 spec.md intents 的关系

- `spec.md` 的 31 条 `INTENT-COMP-xxx` 定位于平台能力（语法、触发器、执行模型、Runner、变量、表达式、安全等）
- 本批 14 条 `INTENT-ACT-xxx` 定位于 **具体 Action 的安装/配置/行为**，互补而不重复
- `INTENT-ACT-007` (OBS上传) 的变量路径解析与 `INTENT-COMP-017` (job.outputs 三级传递) 有交集但关注点不同——前者是 Action 级别参数解析，后者是平台级 outputs 机制

---

## 三、质量自检

- [x] 14 个缺失 Action 全部生成意图（对应 `gitcode-actions-list.md` 中的 setup-gradle/setup-yarn/setup-pnpm/docker-login/qemu/buildx/OBS上传/OBS下载/SWR/build_accelerate/setup_terraform/k8s_deploy/paths_filter/codecov）
- [x] 每条意图包含 `uses:` 引用、已知问题、Oracle 来源
- [x] 已知缺陷（#15, #16, #25, #50, #59, #69, #71, #72-74, #82, #86, #90, #92, #98）中与该批 Action 相关的均已纳入
- [x] ID 格式 `INTENT-ACT-NNN`，从 001 连续到 014
- [x] 与 spec.md 的 31 条 `INTENT-COMP-*` 无重复
- [x] 无凭空编造——所有引用均可在 `gitcode-actions-list.md` 或已有 baseline 中溯源
