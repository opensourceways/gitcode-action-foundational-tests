<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/syntax-reference/runner-images-tools | fetched: 2026-07-20 -->

# Runner 镜像与预装工具（语法参考）

AtomGit Action Runner 使用**三段式标签**格式：`{os-version},{arch},{flavor}`

| 标签段 | 说明 | 取值示例 |
|--------|------|---------|
| os-version | 操作系统与版本 | `ubuntu-24`, `windows-2022` |
| arch | CPU 架构 | `x64`, `arm64` |
| flavor | 资源规格 | `slim`, `small`, `medium`, `large`, `xlarge`, `2xlarge` |

## 常用标签示例

| 标签 | 说明 |
|------|------|
| `{ubuntu-24,x64,small}` | Ubuntu 24.04 / x64 / 2核8G50G |
| `{ubuntu-24,x64,medium}` | Ubuntu 24.04 / x64 / 4核16G100G |
| `{ubuntu-24,x64,large}` | Ubuntu 24.04 / x64 / 8核32G200G |
| `{ubuntu-24,arm64,medium}` | Ubuntu 24.04 / ARM64 / 4核16G100G |

## 6.1 资源规格表

| 规格 | CPU | 内存 | 系统盘 | 适用场景 |
|------|-----|------|--------|---------|
| `slim` | 1核 | 4GB | 20GB | 轻量检查、lint、小型脚本 |
| `small` | 2核 | 8GB | 50GB | 常规 CI 构建、单元测试 |
| `medium` | 4核 | 16GB | 100GB | 中型项目构建、集成测试 |
| `large` | 8核 | 32GB | 200GB | 大型项目构建、性能测试 |
| `xlarge` | 16核 | 64GB | 500GB | 大规模并行构建、重型计算 |
| `2xlarge` | 32核 | 128GB | 1TB | 极重型计算、大数据处理 |

> **规格选择建议：** 默认推荐 `small` 规格（2核8G50G），可满足大多数 CI/CD 场景。仅在有明确性能需求时选择更高规格。

## 6.2 Ubuntu 24.04 预装工具

| 类别 | 工具 | 版本/说明 |
|------|------|----------|
| **语言与运行时** | Python | 3.10, 3.11, 3.12 |
| | Node.js | 18, 20, 22 |
| | Go | 1.21, 1.22, 1.23 |
| | Java (JDK) | 8, 11, 17, 21 |
| | Ruby | 3.1, 3.2, 3.3 |
| | PHP | 8.1, 8.2, 8.3 |
| | Rust | latest stable (via rustup) |
| | .NET | 6.0, 7.0, 8.0 |
| **构建工具** | Maven | 3.9.x |
| | Gradle | 8.x |
| | npm | bundled with Node.js |
| | pip | bundled with Python |
| | yarn | 1.22+ |
| | pnpm | 8.x |
| **CI 工具** | Git | 2.x |
| | curl / wget | latest |
| | jq | 1.7+ |
| | yq | 4.x |
| | shellcheck | 0.9+ |
| **云工具** | kubectl | latest |
| | helm | 3.x |
| | aws-cli | 2.x |
| **包管理** | apt | Ubuntu 24.04 默认 |
| | brew | Linuxbrew (可选) |

## 6.3 自托管 Runner（self-hosted）

除云托管 Runner 外，AtomGit Action 支持**自托管 Runner**，使用 `runs-on` 中的 `self-hosted` 标签组合指定：

```yaml
runs-on:
  - self-hosted
  - linux
  - x64
  - my-group          # Runner 分组名
  - custom-label      # 自定义标签
```

### 自托管标签组合规则

- 必须包含 `self-hosted` 标签
- 可附加 `group`（Runner 分组名，用于区分不同团队/环境的 Runner）
- 可附加自定义 `labels`（如 `gpu`, `high-mem`, `arm64` 等）
- Runner 匹配规则：Job 的 `runs-on` 标签列表必须是 Runner 注册标签的**子集**

```yaml
# 匹配 self-hosted + linux 的 Runner
runs-on: [self-hosted, linux]

# 匹配 self-hosted + my-group + gpu 的 Runner
runs-on: [self-hosted, my-group, gpu]

# 匹配特定分组中的特定规格
runs-on: [self-hosted, group-deploy, x64, large]
```
