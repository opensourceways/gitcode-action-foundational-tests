<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/core-concepts/runner-and-environment | fetched: 2026-07-20 -->

# Runner 和运行环境

AtomGit Action 支持官方资源池和自托管资源池两种 Runner 运行环境。

## 官方资源池

官方资源池标签采用三段式格式 `{os-version},{arch},{flavor}`：

| 段位 | 说明 | 可选值 |
|------|------|-------|
| `os-version` | 操作系统及版本 | `ubuntu-24`、`euler-25` |
| `arch` | CPU 架构 | `x64`、`arm64` |
| `flavor` | 资源规格 | `slim`、`small`、`medium`、`large`、`xlarge`、`2xlarge` |

默认资源池标签为 `default=[ubuntu-latest, x64, small]`。

**资源规格详表**：

| 规格 | CPU（核） | 内存（GB） | 磁盘（GB） | 适用场景 |
|------|-----------|-----------|-----------|---------|
| `slim` | 1 | 4 | 20 | 轻量检查：Lint、静态分析 |
| `small` | 2 | 8 | 50 | 常规构建与测试（**默认**） |
| `medium` | 4 | 16 | 100 | 中等规模编译 |
| `large` | 8 | 32 | 200 | 大规模构建 |
| `xlarge` | 16 | 64 | 500 | 重型计算 |
| `2xlarge` | 32 | 128 | 1000 | 极重型计算 |

## 自托管资源池

自托管 Runner 配置采用三段式 `type/group/labels`：

```yaml
jobs:
  self-hosted-build:
    runs-on: [self-hosted, dev-group, linux, x64, gpu]
    steps:
      - run: nvidia-smi
```
