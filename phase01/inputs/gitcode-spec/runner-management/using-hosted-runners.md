<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/runner-management/using-hosted-runners | fetched: 2026-07-20 -->

# 使用 AtomGit 托管 Runner

**适用场景**：无需自建基础设施，直接使用 AtomGit 提供的官方资源池 Runner 执行流水线任务，适用于大多数构建、测试、轻量部署场景。

## 配置说明

### 官方托管 Runner 标签体系

AtomGit Action 官方资源池 Runner 采用 **三段式标签** 格式：

```
{os-version},{arch},{flavor}
```

| 段位 | 含义 | 可选值 |
|------|------|--------|
| `os-version` | 操作系统 | `ubuntu-latest`、`ubuntu-24`、`ubuntu-22` |
| `arch` | CPU 架构 | `x64`、`arm64` |
| `flavor` | 资源规格 | `slim`、`small`、`medium`、`large`、`xlarge`、`2xlarge` |

### 资源规格详情

| 规格 | CPU | 内存 | 适用场景 | 标签示例 |
|------|-----|------|---------|---------|
| **slim** | 1 核 | 4 GB | 轻量检查（lint、语法校验） | `{ubuntu-24,x64,slim}` |
| **small** | 2 核 | 8 GB | 日常构建、小型项目测试 | `{ubuntu-24,x64,small}` |
| **medium** | 4 核 | 16 GB | 中型项目编译、集成测试 | `{ubuntu-24,x64,medium}` |
| **large** | 8 核 | 32 GB | 大型项目构建、镜像打包 | `{ubuntu-24,x64,large}` |
| **xlarge** | 16 核 | 64 GB | 重度编译、并行测试矩阵 | `{ubuntu-24,x64,xlarge}` |
| **2xlarge** | 32 核 | 128 GB | 极重任务、大规模并行 | `{ubuntu-24,x64,2xlarge}` |

> **注意**：AtomGit托管Runner默认只提供slim,small,medium三种规格的资源，如您需Large及以上规格Runner资源，请咨询AtomGit客服。

### 在 workflow 中指定 Runner

```yaml
# 使用托管 Runner
stages:
  - name: lint
    jobs:
      - name: code-check
        runs-on: {ubuntu-24,x64,slim}       # 轻量任务用 slim
        steps:
          - run: npm run lint
  - name: build
    jobs:
      - name: compile
        runs-on: {ubuntu-24,x64,medium}     # 中型编译用 medium
        steps:
          - run: make build
  - name: package
    jobs:
      - name: docker-build
        runs-on: {ubuntu-24,x64,large}      # 镜像打包用 large
        steps:
          - run: docker build -t myapp .
```

### 使用 default 默认标签

`runs-on: default` 是 AtomGit Action 的快捷标签，等效于：

```
runs-on: [ubuntu-latest, x64, small]
```

即默认使用最新 Ubuntu、x64 架构、small 规格（2核8G）。

```yaml
jobs:
  - name: simple-test
    runs-on: default
    steps:
      - run: pytest
```

### 多标签匹配

`runs-on` 可指定多个标签，Runner 必须同时满足所有标签才被选中：

```yaml
jobs:
  - name: arm64-build
    runs-on: {ubuntu-24,arm64,medium}
    steps:
      - run: make build ARCH=arm64
```

### 托管 Runner 预装工具

| 工具类别 | 预装内容 |
|---------|---------|
| 语言工具链 | Python 3.x, Node.js 18/20, Go 1.21+, Java 11/17/21 |
| 构建工具 | Make, CMake, Maven, Gradle, npm, pip |
| 版本控制 | Git, git-lfs |

> **注意**：预装工具版本随 Runner 镜像更新可能变化，若需固定版本，建议在 step 中显式安装或使用 `container` 字段指定自定义镜像。
