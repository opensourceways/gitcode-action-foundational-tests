# inputs/platform-config/ （建议）

放 **平台规格与容量参数**。这些是稳定性/可靠性 agent 设计边界与并发用例的源头数据，也是规格分析 agent 验证平台声明的依据。

## 平台规格与容量参数

### 基础资源规格
```yaml
# 并发控制（workflow 级 concurrency.max）
max_concurrency_per_workflow: 5          # concurrency.max 取值范围 1-5
concurrency_exceed_action: QUEUE         # 超出并发时策略：IGNORE 忽略 / QUEUE 排队
max_preemption_events: 10                # concurrency.preemption.events 最多配置 10 个

# 超时
default_job_timeout_minutes: 360         # job 默认超时 360 分钟（6 小时），超时强制终止
step_timeout_default: none               # step 默认无独立超时，受 job 的 timeout-minutes 控制


# 重新运行（rerun）限制
max_rerun_times: 3                       # 单条运行最多重新运行 3 次
rerun_age_limit_hours: 6                 # 超过 6 小时的运行不可重新运行

# 触发路径匹配
paths_match_limit: 300                   # paths 匹配「前 300 个变更文件」，超出不参与判断

# Step 输出
max_step_output_per_param: 1MB           # ATOMGIT_OUTPUT 每个参数最大 1MB

# max_concurrent_workflows: 200
# max_concurrent_jobs_per_workflow: <文档未公开·待实测>   （matrix 的 max-parallel 未设时「取决于 Runner 可用数量」，无固定上限；见 configure-matrix-builds.md:129）
# max_matrix_size: <文档未公开·待实测>                   （文档仅示例展开算法，未声明矩阵组合数上限）
# max_log_size: <文档未公开·待实测>
# max_artifact_size: <文档未公开·待实测>                 （upload-download-artifacts.md:10 仅称「已确认制品大小不超过限制」，未给具体数值）
# max_cache_size: <文档未公开·待实测>                    （artifacts-and-cache.md 仅称缓存「长期保留，LRU 淘汰」，未给容量上限）
# max_workflow_file_size: <文档未公开·待实测>
# max_secrets_per_repo: <文档未公开·待实测>
```

### Runner 资源池
```yaml
# 官方托管 Runner —— 三段式标签 {os-version},{arch},{flavor}

hosted_runner:
  label_format: "{os-version},{arch},{flavor}"
  os: [ubuntu-latest, ubuntu-24, ubuntu-22, euler-25]  # 注：using-hosted-runners 列 ubuntu-latest/24/22；
                                                       #     runner-and-environment 列 ubuntu-24/euler-25，合并取并集
  arch: [x64, arm64]
  flavors: [slim, small, medium, large, xlarge, 2xlarge]
  # 规格详表（CPU/内存/磁盘）
  flavor_specs:
    slim:    {cpu: 1,  memory_gb: 4,   disk_gb: 20}    # 轻量检查：lint、静态分析
    small:   {cpu: 2,  memory_gb: 8,   disk_gb: 50}    # 常规构建与测试（默认）
    medium:  {cpu: 4,  memory_gb: 16,  disk_gb: 100}   # 中等规模编译
    large:   {cpu: 8,  memory_gb: 32,  disk_gb: 200}   # 大规模构建
    xlarge:  {cpu: 16, memory_gb: 64,  disk_gb: 500}   # 重型计算
    2xlarge: {cpu: 32, memory_gb: 128, disk_gb: 1000}  # 极重型计算
  default: {os: ubuntu-latest, arch: x64, flavor: small}  # runs-on: default 等效值


# 自托管 Runner —— 支持主机 / Kubernetes 两类

self_hosted_runner:
  supported: true
  supported_types: [host, kubernetes]
  host:
    os_images: [Ubuntu, EulerOS]        
    arch: [x64, arm64]                  
    prereqs: [外网访问权限, Java 8, Git, Docker]   
    elastic_scaling: false              # 每台主机固定运行一个 Runner，不支持伸缩
                                        
  kubernetes:
    default_image: Ubuntu               
    arch: [x64, arm64]                  # x64 默认
    default_cpu_per_pod: 1              # 每 Pod 请求 CPU 核数，默认 1
    default_memory_gb_per_pod: 4        # 每 Pod 请求内存，默认 4GB
    default_min_runners: 1              # 弹性伸缩下限默认 1
    default_max_runners: 1              # 弹性伸缩上限默认 1
    elastic_scaling: true               # 支持按 min/max 扩缩容
  registration_levels: 项目级
```

### 存储与网络
```yaml
# 制品与日志保留
artifact_retention:
  configurable: true                    # 制品「可设定保留天数」
  env_var: ATOMGIT_RETENTION_DAYS       # 工作流运行日志和工件的保留天数，运行时环境变量暴露
  default_days: 90    

# 缓存
cache:
  retention_policy: "LRU 淘汰"  
  scope: "同仓库的所有运行"

# 网络出口
# network_egress_policy: 有访问外网权限
```

### 格式

Markdown / YAML 均可。**数字平铺，不要套在不可解析的 PDF/截图里**——agent 需要能读到具体数值才能设计边界用例。

## 消费方

- **reliability agent**（最直接消费者）：所有配额维度都是边界值·越界·恢复类 intent 的源头
- **spec-analyst**：验证平台规格文档是否与真实容量一致（「规格说支持 X，但实际能否跑满」）
- **compat-diff**：对照 GitHub Actions 的 limits（如 matrix max、job timeout、artifact size 等）

## 刷新时的影响

更新本目录后，reliability agent 在下次 `/phase01-gen` 或 `/phase01-update dim:reliability` 时会基于新参数**重新审视**边界类 intent（如配额改了，旧的越界值可能已不适用，需更新或新增）。
---

**已补充 / 2026-07-21**


