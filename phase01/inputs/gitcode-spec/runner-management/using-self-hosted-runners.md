<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/runner-management/using-self-hosted-runners | fetched: 2026-07-20 -->

# 使用自托管 Runner

## 配置说明

AtomGit Action支持主机和Kubernetes两类自定义Runner，配置方式如下。

### 主机Runner的配置安装

#### 步骤一：进入 Runner 管理页面

1. 进入目标项目/组织页面，点击顶部导航栏的 **项目设置/组织设置**。
2. 在左侧边栏中，展开 **Actions** 分组，点击 **Runners**。
3. 进入"Runners"页面，页面顶部有两个标签页：**主机 Runner** 和 **Kubernetes Runner**，默认选中"主机 Runner"。

> **说明**：首次进入时页面显示"暂无数据"，表示该仓库/组织尚未配置任何 Runner。

#### 步骤二：创建主机 Runner

1. 点击页面右上角的 **"+ 新增自定义 Runner"** 按钮。
2. 在弹出的下拉菜单中选择 **"新增主机 Runner"**，进入 Runner 配置表单。

#### 步骤三：填写 Runner 配置

| 字段 | 是否必填 | 说明 |
|------|--------|------|
| **Runner 名称** | 必填 | 自定义 Runner 的标识名称，如 `CI-runner`，用于在管理页面区分不同 Runner |
| **安装准备** | — | 环境前置条件及自动安装选项（见下方说明） |
| **Runner 工作目录** | 必填 | Runner 在主机上的工作目录路径，系统会自动生成默认值（如 `/opt/runner_1783325952`），可按需修改 |
| **Runner 环境镜像** | 必选 | 选择 Runner 运行的操作系统镜像，支持 **Ubuntu** 和 **EulerOS** |
| **CPU 架构** | 必选 | 选择主机的 CPU 架构，支持 **x64** 和 **arm64** |
| **自定义标签** | 选填 | 为 Runner 添加自定义标签，用于在 workflow 中精确匹配（见下方说明） |

**安装准备选项：**

页面提示："您的主机需要有访问外网权限，并且有安装 Java 8、Git 和 Docker 环境。"

系统提供以下 4 个复选框，默认全部勾选：

| 选项 | 默认 | 说明 |
|------|------|------|
| ☑ 自动安装 JDK | 勾选 | 安装脚本自动检测并安装 JDK 环境 |
| ☑ 自动安装 Git | 勾选 | 安装脚本自动检测并安装 Git |
| ☑ 自动安装 Docker | 勾选 | 安装脚本自动检测并安装 Docker |
| ☑ 重启免注册 | 勾选 | 主机重启后 Runner 自动恢复注册状态，无需重新执行注册脚本 |

> **提示**：如果主机上已预装了部分环境，可以取消对应选项，安装脚本将跳过已安装的组件。建议保持"重启免注册"勾选，以确保 Runner 服务持久可用。

**自定义标签配置：**

自定义标签用于在 workflow 的 `runs-on` 中精确匹配目标 Runner。标签表格包含标签名称（key）、默认值（value）、标签颜色、操作四列。系统会根据所选的环境镜像和 CPU 架构自动生成默认标签行（如 `os=euler`、`arch=x64`），可点击 **"+ 新增自定义标签"** 添加更多标签。

#### 步骤四：获取并执行安装脚本

1. 完成表单配置后，点击左下角的 **"获取执行脚本"** 按钮。
2. 系统根据配置自动生成 Shell 安装脚本，显示在"执行脚本"区域。
3. 点击复制图标，一键复制完整脚本。

生成的脚本示例结构：

```bash
export RUNNER_INSTALL_URL=...
export RUNNER_INSTALL_FILE=install-octopus-runner.sh
# 使用自托管 Runner
if [ -f 'which curl' ]; then
  curl -# -k -o ${RUNNER_INSTALL_FILE} ${RUNNER_INSTALL_URL}
else
  wget ... ${RUNNER_INSTALL_URL}
fi
```

4. 登录目标主机，粘贴脚本执行（自动完成：下载 Runner → 安装依赖 → 注册到平台 → 启动服务）。

> **重要**：
> - 目标主机必须有访问外网的权限。
> - 脚本需要 `sudo` 权限执行。
> - 安装脚本中包含一次性注册 Token，请勿泄露或重复使用。

#### 步骤五：验证 Runner 状态

脚本执行成功后，返回 **项目设置 → Runners** 页面，确认新 Runner 状态为 **在线**（绿色）。离线则检查主机网络连通性和脚本执行日志。

#### 步骤六：在 workflow 中使用自托管 Runner

```yaml
# .gitcode/workflows/gpu-build.yml
stages:
  - name: gpu-test
    jobs:
      - name: cuda-compile
        runs-on: [self-hosted, euler, x64, gpu]
        steps:
          - run: nvcc -o myapp myapp.cu
```

```yaml
# 使用自定义标签精确匹配
jobs:
  - name: backend-deploy
    runs-on: [self-hosted, env-prod, server-backend]
    steps:
      - run: ./deploy.sh
```

> **标签匹配规则**：`runs-on` 中列出的所有标签必须同时存在于 Runner 的标签集合中，才视为匹配成功。

### Kubernetes Runner 的配置安装

Kubernetes Runner 以 Pod 形式运行在你的 Kubernetes 集群中，支持弹性伸缩和资源隔离。

配置表单字段：

| 字段 | 是否必填 | 说明 |
|------|--------|------|
| **名称** | 必填 | 自定义 Runner 标识名称，如 `k8s-runner-prod` |
| **集群 URL** | 必填 | Kubernetes API Server 访问地址，如 `https://10.0.0.1:6443` |
| **Kubernetes config 凭证** | 必填 | 集群 kubeconfig 凭证内容，用于连接和认证 |
| **命名空间** | 必填 | Runner Pod 部署的目标命名空间，默认 `default` |
| **镜像名称** | 非必填 | Runner 容器镜像，默认 `Ubuntu` |
| **CPU 架构** | 非必填 | Pod 运行架构，支持 x64（默认）和 arm |
| **CPU** | 必填 | 每个 Pod 请求的 CPU 核数，默认 `1` |
| **内存** | 必填 | 每个 Pod 请求的内存，默认 `4` GB |
| **最小 Runner 数量** | 必填 | 弹性伸缩下限，默认 `1` |
| **最大 Runner 数量** | 必填 | 弹性伸缩上限，默认 `1` |
| **自定义标签** | 选填 | 用于 workflow 精确匹配 |

**弹性伸缩**：当 `最小 = 最大 = 1` 时固定 1 个 Pod，不伸缩；如最小 `1`、最大 `5`，空闲保留 1 个、高峰扩展到 5 个。

> **安全提示**：Kubernetes config 凭证包含集群访问证书和密钥，请妥善保管，避免泄露。

创建后返回 **Runners → Kubernetes-Runner** 标签页确认状态为在线。详情页含 4 个标签：基本信息、标签、Runners 列表（实时 Pod 实例）、执行历史。

```yaml
# .gitcode/workflows/k8s-build.yml
jobs:
  - name: container-build
    runs-on: [self-hosted, k8s, arch-x64]
    steps:
      - uses: checkout
      - run: docker build -t myapp:latest .
```

### 主机 Runner 与 Kubernetes Runner 对比

| 对比维度 | 主机 Runner | Kubernetes Runner |
|---------|-----------|-----------------|
| **运行形态** | 安装在物理机/虚拟机上，以系统服务运行 | 以 Pod 形式运行在 K8s 集群中 |
| **创建方式** | 页面配置后获取安装脚本，手动在主机执行 | 页面填写集群信息和资源配置，系统自动部署 |
| **资源管理** | 依赖主机自身硬件资源 | 通过 CPU/内存字段声明资源请求，受 K8s 调度管理 |
| **弹性伸缩** | 不支持，每台主机固定运行一个 Runner | 支持配置最小/最大 Runner 数量，按需扩缩容 |
| **环境隔离** | 同一主机上多个 Job 共享环境 | 每个 Pod 独立容器环境，天然隔离 |
| **适用场景** | 需要 GPU/NPU 特殊硬件、内网环境、长期运行 | 需要弹性伸缩、容器化执行、环境隔离、快速扩容 |
| **前置要求** | 主机有外网访问权限，预装 Java 8、Git、Docker | 拥有可用 K8s 集群，提供 kubeconfig 凭证 |

### 自托管 Runner 标签规则

- **自动生成标签**：创建时系统根据环境镜像和 CPU 架构自动生成标签（如 `os=euler`、`arch=x64`），并默认加入 `self-hosted` 标签。
- **自定义标签**：通过表格添加，支持名称、默认值、颜色。
- **标签组**：可为 Runner 设置 `group` 属性组织归类。

标签匹配逻辑：workflow 的 `runs-on` 列表中所有标签必须与 Runner 的标签集合匹配，或为 Runner 标签子集。

```yaml
# Runner 标签: self-hosted, os=euler, arch=x64, env=prod, server=backend
# ✅ 可匹配
jobs:
  - name: deploy-prod
    runs-on: [self-hosted, env-prod, server-backend]

# ❌ 不可匹配（缺少 env-prod 标签）
jobs:
  - name: deploy-prod
    runs-on: [self-hosted, server-backend]
```

### 组织级 vs 项目级 Runner

| 级别 | 注册入口 | 可服务范围 |
|------|--------|-----------|
| **组织级** | 组织 Settings → Runners | 该组织下所有项目的流水线，支持对指定项目可用 |
| **项目级** | 项目 Settings → Runners | 仅该项目流水线 |

推荐：通用 Runner 注册为组织级，专用 Runner 注册为项目级。

### Runner 更新

更新需在平台重新获取安装脚本并执行：删除旧 Runner → 重新新增 → 按原配置填写 → 获取执行脚本 → 主机执行。建议更新前停止当前 Runner 服务，更新后验证状态。
