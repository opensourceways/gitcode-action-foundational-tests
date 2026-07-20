# GitCode Actions 官方插件清单

> 来源：`gitcode issues.xlsx` 工作表「action」，26 行，2026-07-20 导出
> 状态：这些是 **明确需要使用的 GitCode Action 列表**，测试用例必须覆盖
> 用途：case-writer 编译 YAML 时的 `uses:` 引用依据；完备性 agent 验证各 action 功能的 intent 来源

---

## 官方 Action 清单（按用途分类）

### 代码检出

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 1 | checkout插件 | `official_checkout` | 代码检出 |

**测试要点**：浅克隆深度、PR 预合并（已知不支持 #25/#71）、子模块、fetch-depth 与 fetch-tags、不同分支/commit/tag 的 checkout、大仓库性能

---

### 语言运行时安装

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 2 | setup-jdk | `setup-jdk` | Java+Maven 的安装和配置 |
| 3 | setup-gradle | `setup-gradle` | Gradle 的安装和配置 |
| 4 | setup-node | `setup-node` | node 安装和配置环境 |
| 5 | setup-yarn | `setup-yarn` | yarn 安装和配置环境 |
| 6 | setup-pnpm | `setup-pnpm` | pnpm 安装和配置环境 |
| 7 | setup-python | `setup-python` | python 的环境安装和配置 |
| 8 | setup-go | `setup-go` | go 的环境安装和配置 |

**测试要点**：
- 各插件的版本范围与实际安装版本（已知 setup-* 未说明支持版本 #50）
- 指定不存在的版本时的报错信息（已知经常下载失败 #50/#92/#98）
- 自定义资源池 + 自定义镜像组合场景下的兼容性（已知 setup-node 异常 #69）
- 平台兼容性：EulerOS 2.0 不支持（#92）、minGlibc >= 2.35
- setup-jdk 是否支持 Java 21+（已知不支持 #59）
- 已安装工具在后续 step/job 中的可用性

---

### 构建加速与 IaC

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 9 | cache | `official_cache` | 缓存插件 |
| 10 | buildaccelarate | `official_build_accelerate` | 构建加速插件 |
| 11 | setup_terraform | `setup_terraform` | IaC 基础设施部署 |

**测试要点**：
- cache 的 key/hit/restore 行为（已知找不到插件 #90）
- cache 跨 job/跨 run/跨分支的作用域
- fork PR 是否可写 cache（cache 投毒安全关注 INTENT-SEC-019）
- buildaccelarate 在自定义资源池的兼容性

---

### Shell / 脚本执行

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 12 | 执行shell | `official_shell` | 执行脚本 |

**测试要点**：多行脚本、退出码传递、环境变量继承、不同 shell 类型（bash/sh/pwsh）

---

### 制品管理

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 13 | gitcode制品上传 | `official_upload_artifact` | 制品上传 |
| 14 | gitcode制品下载 | `official_download_artifact` | 制品下载 |

**测试要点**：
- 上传路径支持（已知目录上传需 atomgit 上下文 #16）
- 变量路径解析（已知变量目录无法解析 #16）
- 跨 job 传递、保留期、大小上限
- 下载不存在的 artifact 时的报错

---

### OBS 对象存储

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 15 | OBS上传 | `official_obs_upload` | 自定义 OBS 上传 |
| 16 | OBS下载 | `official_obs_download` | 自定义 OBS 下载 |

**测试要点**：网络可用性（已知偶发失败 #15）、目录上传、变量路径解析

---

### SWR 容器镜像仓库

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 17 | SWR上传 | `official_swr` | 支持基于华为云容器镜像仓库(SWR)的上传/下载能力 |
| 18 | SWR下载 | （同上，共享引用名） | SWR 下载 |

**测试要点**：认证（ak/sk 登录待验证 #72/#73/#74）、镜像 tag 管理

---

### Docker

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 19 | docker/login-action | `official_docker_login` | Docker 登录 |
| 20 | docker/build-push-action | `official_build_push` | 镜像构建和推送 |
| 21 | docker/setup-qemu-action | （待确认引用名） | QEMU 仿真 |
| 22 | docker/setup-buildx-action | （待确认引用名） | Buildx 构建器 |

**测试要点**：登录认证、daemon 可用性（已知默认资源池不支持 #86）、多架构构建

---

### K8s 部署

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 23 | k8s部署 | `official_k8s_deploy` | k8s 部署 |

**测试要点**：kubeconfig 认证、命名空间、资源清单格式

---

### CI/CD 工具集成

| # | 参考插件 | 插件引用名（`uses:`） | 用途 |
|---|---|---|---|
| 24 | dorny/paths-filter@v3 | `official_paths_filter` | 路径过滤 |
| 25 | codecov/codecov-action | `codecov-action` | 代码覆盖率上报 |

**测试要点**：
- paths-filter 的 glob pattern 支持
- codecov 的覆盖率文件路径、token 认证

---

## 总结：对用例生成的指导

### 必须覆盖的 Action（P0 完备性）

1. **`official_checkout`** — 代码检出是 workflow 的第一步，不可用则全链断裂。必测：基本 checkout、分支/commit/tag 指定、PR 预合并（已知不支持需文档化）
2. **`official_upload_artifact` / `official_download_artifact`** — 制品传递是 job 间通信的核心机制
3. **`official_cache`** — 缓存机制影响 CI 效率，且存在安全边界问题（fork PR cache 投毒）
4. **`official_shell`** — 最基础但最关键的执行单元

### 应覆盖的 Action（P1 完备性）

5. 所有 setup-* 插件（setup-jdk/node/python/go/gradle/yarn/pnpm）— 语言 CI 的基础依赖
6. `official_docker_login` + `official_build_push` — 镜像构建链
7. `official_obs_upload/download` — 对象存储集成
8. `official_swr` — 容器镜像仓库集成

### 已知缺陷关注的 Action

| Action | 已知问题 | 编号 |
|---|---|---|
| `official_checkout` | PR 预合并不可用 | #25, #71 |
| `official_checkout` | uses 不支持 `${{atomgit.repository}}` | #82 |
| `setup-jdk` | 不支持 Java 21 | #59 |
| `setup-python` | 指定版本异常 | #26 |
| `setup-node` | 自定义资源池+自定义镜像场景不生效 | #69 |
| `setup-*` 系列 | 版本说明缺失，下载失败 | #50, #98 |
| `official_cache` | 插件找不到 | #90 |
| `official_obs_upload` | 目录/变量路径上传问题 | #15, #16 |

---

*本文件作为 `history/` 输入，在 `/phase01-gen` 时由 spec-analyst、case-writer 消费，确保所有必测 Action 有对应 intent/用例覆盖。*
