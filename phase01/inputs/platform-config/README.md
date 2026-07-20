# inputs/platform-config/ （建议）

放 **平台规格与容量参数**。这些是稳定性/可靠性 agent 设计边界与并发用例的源头数据，也是规格分析 agent 验证平台声明的依据。

## 请补充

### 基础资源规格
```
# 示例（请替换为真实值）
max_concurrent_workflows: <N>
max_concurrent_jobs_per_workflow: <N>
max_matrix_size: <N>
max_job_timeout_minutes: <N>
max_log_size: <N>
max_artifact_size: <N>
max_cache_size: <N>
max_workflow_file_size: <N>
max_secrets_per_repo: <N>
```

### Runner 资源池
```
# 示例
hosted_runner:
  flavors: [slim, small, medium]
  os: [ubuntu-24]
  arch: [x64, arm64]
  default: {os: ubuntu-24, arch: x64, flavor: small}
self_hosted_runner:
  supported: true
  supported_types: [host, kubernetes]
  max_runners: <N>
```

### 存储与网络
```
artifact_retention_days: <N>
cache_retention_policy: <描述>
network_egress_policy: <描述>
```

### 格式

Markdown / YAML 均可。**数字平铺，不要套在不可解析的 PDF/截图里**——agent 需要能读到具体数值才能设计边界用例。

## 消费方

- **reliability agent**（最直接消费者）：所有配额维度都是边界值·越界·恢复类 intent 的源头
- **spec-analyst**：验证平台规格文档是否与真实容量一致（「规格说支持 X，但实际能否跑满」）
- **compat-diff**：对照 GitHub Actions 的 limits（如 matrix max、job timeout、artifact size 等）

## 刷新时的影响

更新本目录后，reliability agent 在下次 `/phase01-gen` 或 `/phase01-update dim:reliability` 时会基于新参数**重新审视**边界类 intent（如配额改了，旧的越界值可能已不适用，需更新或新增）。

> 补充完成后可在此文件末尾记：`已补充 / 日期`。
