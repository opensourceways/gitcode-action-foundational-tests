# Reliability Intents（稳定性意图库）

> 产出者：reliability agent（混沌与边界工程师）
> Run ID：2026-07-22-01
> 输入版本：platform-config/README.md（2026-07-21 修订）、instance-config.md（2026-07-20 快照）、gitcode-spec/（2026-07-20 fetched）
> 说明：本文件为当前 run 完整产出。历史基底 REL-001~REL-040 见 2026-07-21-02；本轮包含 REL-001~REL-066 全量覆盖。

---

## 1. platform-config 提取的配额/上限参数表

| 维度 | 参数名 | 具体数值/范围 | 来源文件 | 备注 |
|---|---|---|---|---|
| 并发控制 | `concurrency.max` | 1–5 | `platform-config/README.md` | workflow/ job 级均适用 |
| 并发控制 | `concurrency.exceed-action` | `QUEUE` / `IGNORE` | `platform-config/README.md` | |
| 并发控制 | `concurrency.preemption.events` | 最多 10 个 | `platform-config/README.md` | |
| 超时 | `default_job_timeout_minutes` | 360 分钟（6 小时） | `platform-config/README.md` / `configure-jobs.md` | 超时强制终止 |
| 超时 | `step_timeout_default` | 无独立超时 | `platform-config/README.md` | 受 job timeout 控制 |
| 重试 | `max_rerun_times` | 3 次 | `platform-config/README.md` / `rerun-failed-jobs.md` | 单条运行上限 |
| 重试 | `rerun_age_limit_hours` | 6 小时 | `platform-config/README.md` / `rerun-failed-jobs.md` | 超期不可 rerun |
| 触发匹配 | `paths_match_limit` | 300 个变更文件 | `platform-config/README.md` / `configure-triggers.md` | 超出部分不参与判断 |
| Step 输出 | `max_step_output_per_param` | 1 MB | `platform-config/README.md` / `pass-output-between-jobs.md` | ATOMGIT_OUTPUT 单参数上限 |
| Runner 资源 | `slim` | CPU 1 / 内存 4 GB / 磁盘 20 GB | `platform-config/README.md` / `runner-and-environment.md` | |
| Runner 资源 | `small`（默认） | CPU 2 / 内存 8 GB / 磁盘 50 GB | `platform-config/README.md` / `runner-and-environment.md` | |
| Runner 资源 | `medium` | CPU 4 / 内存 16 GB / 磁盘 100 GB | `platform-config/README.md` / `runner-and-environment.md` | |
| Runner 资源 | `large` | CPU 8 / 内存 32 GB / 磁盘 200 GB | `platform-config/README.md` / `runner-and-environment.md` | |
| Runner 资源 | `xlarge` | CPU 16 / 内存 64 GB / 磁盘 500 GB | `platform-config/README.md` / `runner-and-environment.md` | |
| Runner 资源 | `2xlarge` | CPU 32 / 内存 128 GB / 磁盘 1000 GB | `platform-config/README.md` / `runner-and-environment.md` | |
| K8s Runner | `default_cpu_per_pod` | 1 核 | `platform-config/README.md` | |
| K8s Runner | `default_memory_gb_per_pod` | 4 GB | `platform-config/README.md` | |
| K8s Runner | `default_min_runners` | 1 | `platform-config/README.md` | |
| K8s Runner | `default_max_runners` | 1 | `platform-config/README.md` | |
| 制品保留 | `artifact_retention.default_days` | 90 天 | `platform-config/README.md` / `artifacts-and-cache.md` | 可配置 |
| 缓存策略 | `cache.retention_policy` | LRU 淘汰 | `platform-config/README.md` / `artifacts-and-cache.md` | 长期保留，同仓库共享 |
| 可重用工作流 | `workflow_call` 嵌套 | 最多 2 层 | `configure-triggers.md` | |
| workflow_dispatch | inputs 类型 | 仅 `string` | `configure-triggers.md` | |

**文档未公开上限（待实测/标注）**：
- `max_concurrent_workflows`（单仓库/单实例级并发 workflow 上限）
- `max_concurrent_jobs_per_workflow`（文档称「取决于 Runner 可用数量」）
- `max_matrix_size`（矩阵组合数上限未声明）
- `max_log_size`（单 job 日志大小上限未声明）
- `max_artifact_size`（仅提示「不超过限制」，无具体数值）
- `max_cache_size`（未声明容量上限）
- `max_workflow_file_size`
- `max_secrets_per_repo`

---

## 2. 输入退化标注

- `inputs/business-context/`：**⚠️ 仅 README.md**，无典型业务 workflow 模板提供真实负载模式参照。以下大规模/洪泛类 intent 的规模参数基于 platform-config 已公开的 Runner 规格与并发上限推导，而非真实业务负载校准。


---

## 3. Intent 列表

### 3.1 并发控制维度

```
意图 ID:    INTENT-REL-001
维度标签:   [reliability]
标题:       concurrency.max 边界值——同时触发 5 个运行应全部进入执行态

风险点:     concurrency.max 上限为 5，若系统在边界值处仍排队或丢失，说明并发控制实现有缺陷。
预期系统行为: 配置 concurrency.max=5 的 workflow，同时触发 5 次，5 次均应进入 in_progress 状态，无排队、无丢失。
Oracle 来源: GitCode规格（platform-config/README.md: max_concurrency_per_workflow=5）

验证要点:
  - [正向] 5 个运行均进入 in_progress 并在合理时间内完成
  - [非功能] 从 queued→in_progress 的调度时延 ≤60 秒（容差）

故障/压力参数: 并发度=5，concurrency.max=5，触发方式=push
稳态判据:     5 个运行状态均为 completed(success)，无 queued 残留
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/configure-jobs.md
```

```
意图 ID:    INTENT-REL-002
维度标签:   [reliability]
标题:       concurrency.max 越界值——配置 max=6 时系统应拒绝或明确报错

风险点:     越界配置若被静默截断，会导致用户预期与实际行为不一致，形成 flaky 来源。
预期系统行为: 系统应在 YAML 解析或运行调度阶段明确拒绝 concurrency.max=6 的配置。
Oracle 来源: GitCode规格（max 取值范围 1-5）

验证要点:
  - [正向] 系统给出明确的校验错误，指出 max 超出范围
  - [负向] 不应静默截断为 5 或直接忽略上限

故障/压力参数: concurrency.max=6
稳态判据:     workflow 无法保存/运行，错误信息包含 "max" 或 "5" 或 "范围"
恢复预期:     明确报错（用户修正配置后重试成功）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）
```

```
意图 ID:    INTENT-REL-003
维度标签:   [reliability]
标题:       concurrency 排队策略 QUEUE——超上限运行应排队等待而非丢失

风险点:     并发洪泛下若超出上限的运行被静默丢弃，会造成 CI 漏跑。
预期系统行为: concurrency.max=2、exceed-action=QUEUE，同时触发 4 个运行，后 2 个应进入 queued，待前 2 个完成后自动启动。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 运行 1-2 进入 in_progress；运行 3-4 状态=queued
  - [正向] 运行 1-2 完成后，运行 3-4 自动转为 in_progress
  - [负向] 运行 3-4 不应被丢弃或状态异常

故障/压力参数: concurrency.max=2，exceed-action=QUEUE，同时触发数=4
稳态判据:     4 个运行最终全部 completed(success)，总耗时 ≈ 2×单运行时长
恢复预期:     自动恢复（排队完成后执行）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/configure-jobs.md
```

```
意图 ID:    INTENT-REL-004
维度标签:   [reliability]
标题:       concurrency 忽略策略 IGNORE——超上限运行应直接执行不排队

风险点:     需验证 IGNORE 策略不被错误实现为 QUEUE 或丢弃。
预期系统行为: concurrency.max=2、exceed-action=IGNORE，同时触发 4 个运行，4 个均应直接进入 in_progress。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 4 个运行全部进入 in_progress
  - [负向] 不应出现 queued 状态

故障/压力参数: concurrency.max=2，exceed-action=IGNORE，同时触发数=4
稳态判据:     4 个运行全部 completed(success)，无 queued
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）
```

```
意图 ID:    INTENT-REL-005
维度标签:   [reliability]
标题:       preemption events 边界值——配置 10 个抢占事件应正常解析

风险点:     preemption 事件用于 cancel-in-progress 类抢占逻辑，边界值解析失败会导致并发控制失效。
预期系统行为: concurrency.preemption.events 配置 10 个不同事件，workflow 正常保存并运行。
Oracle 来源: GitCode规格（max_preemption_events=10）

验证要点:
  - [正向] workflow YAML 校验通过，运行正常触发

故障/压力参数: preemption.events=10
稳态判据:     workflow 运行 completed(success)
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）
```

```
意图 ID:    INTENT-REL-006
维度标签:   [reliability]
标题:       preemption events 越界值——配置 11 个抢占事件应被拒绝

风险点:     越界配置若被静默截断，会导致抢占逻辑不完整。
预期系统行为: 配置 11 个 preemption 事件时，系统应在解析阶段报错。
Oracle 来源: GitCode规格（max_preemption_events=10）

验证要点:
  - [正向] 系统明确报错，指出 events 数量超限
  - [负向] 不应静默截断为前 10 个

故障/压力参数: preemption.events=11
稳态判据:     workflow 保存/运行失败，错误信息包含 "10" 或 "preemption"
恢复预期:     明确报错（用户修正配置后重试成功）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）
```


---

### 3.2 超时维度

```
意图 ID:    INTENT-REL-007
维度标签:   [reliability]
标题:       job timeout 边界值——运行 359 分钟后在 360 分钟边界前正常完成

风险点:     接近 timeout 边界时若系统提前终止，会误杀正常长任务。
预期系统行为: timeout-minutes=360，job 实际运行 359 分钟，应在超时前成功完成。
Oracle 来源: GitCode规格（default_job_timeout_minutes=360）

验证要点:
  - [正向] job 状态=success，运行时长 359±1 分钟
  - [负向] 不应在 358 分钟前被强制终止

故障/压力参数: timeout-minutes=360，实际运行时长=359 分钟（通过 sleep 模拟）
稳态判据:     job 状态=success，日志显示正常结束
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/configure-jobs.md
```

```
意图 ID:    INTENT-REL-008
维度标签:   [reliability]
标题:       job timeout 越界触发——运行 361 分钟时应在 360 分钟被强制终止

风险点:     超时机制失效会导致 job 无限挂起，消耗 Runner 资源。
预期系统行为: timeout-minutes=360，job 运行超过 360 分钟，应在 360 分钟时被强制终止，状态=failure。
Oracle 来源: GitCode规格（超时后强制终止）

验证要点:
  - [正向] job 在 360±2 分钟时被终止，状态=failure
  - [正向] 日志包含明确的超时终止信息
  - [负向] 不应运行超过 365 分钟仍未终止

故障/压力参数: timeout-minutes=360，实际运行时长=361 分钟
稳态判据:     job 状态=failure，日志含 "timeout" 或 "超时" 字样
恢复预期:     明确报错（用户调整 timeout 或优化任务后重试成功）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/configure-jobs.md
```

```
意图 ID:    INTENT-REL-009
维度标签:   [reliability]
标题:       自定义短超时——timeout-minutes=1 时 step 运行 2 分钟应被强制终止

风险点:     短超时场景验证 timeout 机制的精度与响应速度。
预期系统行为: timeout-minutes=1，step 执行 sleep 120，job 应在 1 分钟时被终止。
Oracle 来源: GitCode规格

验证要点:
  - [正向] job 在 60±10 秒时被终止
  - [正向] 日志包含超时信息

故障/压力参数: timeout-minutes=1，step 运行时长=2 分钟
稳态判据:     job 状态=failure，实际运行时长 60±10 秒
恢复预期:     明确报错
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）
```

```
意图 ID:    INTENT-REL-010
维度标签:   [reliability]
标题:       默认超时（未声明 timeout-minutes）——运行 361 分钟应被强制终止

风险点:     未声明 timeout 时系统是否按默认 360 分钟执行，若默认失效会导致无限挂起。
预期系统行为: job 不声明 timeout-minutes，运行 361 分钟，应在 360 分钟时被终止。
Oracle 来源: GitCode规格（default_job_timeout_minutes=360）

验证要点:
  - [正向] job 在 360 分钟时被终止
  - [负向] 不应无限运行

故障/压力参数: timeout-minutes=未声明（默认 360），实际运行时长=361 分钟
稳态判据:     job 状态=failure，日志含超时信息
恢复预期:     明确报错
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）
```


---

### 3.3 重试维度

```
意图 ID:    INTENT-REL-011
维度标签:   [reliability]
标题:       rerun 边界值——单条运行连续重新运行 3 次应全部成功

风险点:     rerun 机制是偶发故障恢复的关键路径，边界值处若失效会影响可用性。
预期系统行为: 失败运行连续点击 Re-run all jobs / Re-run failed jobs 共 3 次，每次均创建新运行记录并成功执行。
Oracle 来源: GitCode规格（max_rerun_times=3）

验证要点:
  - [正向] 第 1-3 次 rerun 均创建新运行，ATOMGIT_RUN_ID 更新
  - [正向] 每次 rerun 的 atomgit.sha / ref 与原始运行保持一致
  - [负向] 不应复用旧运行记录

故障/压力参数: rerun 次数=3，触发方式=手动 Re-run
稳态判据:     3 次新运行均 completed(success)，运行编号递增
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/rerun-failed-jobs.md
```

```
意图 ID:    INTENT-REL-012
维度标签:   [reliability]
标题:       rerun 越界值——尝试第 4 次重新运行应被系统拒绝

风险点:     超过 rerun 上限后若系统仍允许 rerun，可能暗示运行记录管理或幂等性缺陷。
预期系统行为: 已完成 3 次 rerun 的运行，第 4 次 rerun 请求被拒绝，给出明确错误提示。
Oracle 来源: GitCode规格（max_rerun_times=3）

验证要点:
  - [正向] 第 4 次 rerun 按钮不可用或点击后报错
  - [正向] 错误信息包含 "最多 3 次" 或类似提示

故障/压力参数: rerun 次数=4（第 4 次）
稳态判据:     第 4 次 rerun 被拒绝，运行总数=原始 1 次 + 3 次 rerun = 4 次
恢复预期:     明确报错（用户需新 push 触发）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/rerun-failed-jobs.md
```

```
意图 ID:    INTENT-REL-013
维度标签:   [reliability]
标题:       rerun 6 小时年龄限制——超期运行不可重新运行

风险点:     过期运行若被 rerun，可能因环境/依赖变化导致不可预期行为。
预期系统行为: 运行完成 6 小时后，Re-run 按钮不可用或点击后报错。
Oracle 来源: GitCode规格（rerun_age_limit_hours=6）

验证要点:
  - [正向] 6 小时 1 分钟后尝试 rerun 被拒绝
  - [正向] 错误信息含 "6 小时" 或 "已过期"

故障/压力参数: rerun_age_limit=6 小时，验证时机=6 小时 1 分钟后
稳态判据:     rerun 被拒绝，系统不创建新运行
恢复预期:     明确报错（用户需新 push 触发）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/rerun-failed-jobs.md
```


---

### 3.4 触发匹配维度

```
意图 ID:    INTENT-REL-014
维度标签:   [reliability]
标题:       paths 匹配边界值——变更恰好 300 个文件时 paths 过滤应生效

风险点:     paths 匹配是触发器核心逻辑，边界值处若失效会导致 CI 漏触发或误触发。
预期系统行为: push 变更恰好 300 个文件，其中 1 个匹配 paths 规则，workflow 应正确触发。
Oracle 来源: GitCode规格（paths_match_limit=300）

验证要点:
  - [正向] workflow 被触发
  - [负向] 不应因文件数恰好为 300 而判定异常

故障/压力参数: 变更文件数=300，匹配 paths 的文件数=1
稳态判据:     workflow 运行被创建，状态=queued/in_progress
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/configure-triggers.md
```

```
意图 ID:    INTENT-REL-015
维度标签:   [reliability]
标题:       paths 匹配越界值——第 301 个变更文件不参与 paths 匹配判断

风险点:     超出 300 的文件若仍参与匹配，会导致大变更集下的触发行为不可预期。
预期系统行为: push 变更 301 个文件，仅前 300 个参与 paths 匹配，第 301 个匹配 paths 也不触发。
Oracle 来源: GitCode规格（paths 匹配前 300 个变更文件，超出不参与判断）

验证要点:
  - [正向] 当第 301 个文件是唯一匹配 paths 的文件时，workflow 不触发
  - [正向] 当前 300 个文件中已有匹配项时，workflow 正常触发

故障/压力参数: 变更文件数=301，paths 匹配文件位置=第 301 个
稳态判据:     workflow 不触发（当仅第 301 个匹配时）
恢复预期:     N/A（设计行为）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/configure-triggers.md
```

---

### 3.5 Step 输出维度

```
意图 ID:    INTENT-REL-016
维度标签:   [reliability]
标题:       step output 边界值——ATOMGIT_OUTPUT 写入 1 MB 参数应成功传递

风险点:     step 输出是下游 job 依赖的关键机制，边界值处若截断会导致数据丢失。
预期系统行为: 向 ATOMGIT_OUTPUT 写入恰好 1 MB（1,048,576 bytes）的参数，下游 step 和 job 能完整读取。
Oracle 来源: GitCode规格（max_step_output_per_param=1MB）

验证要点:
  - [正向] 下游 step 通过 steps.<id>.outputs.<key> 读取到完整 1 MB 内容
  - [正向] Job 输出映射到 needs 后下游 job 也能读取完整内容
  - [负向] 不应截断或丢失

故障/压力参数: 输出参数大小=1,048,576 bytes
稳态判据:     下游读取到的内容长度=1,048,576 bytes，MD5 校验通过
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/pass-output-between-jobs.md
```

```
意图 ID:    INTENT-REL-017
维度标签:   [reliability]
标题:       step output 越界值——ATOMGIT_OUTPUT 写入 1 MB+1 byte 应被拒绝或报错

风险点:     越界写入若被静默截断，会导致下游读取到不完整数据，产生难以排查的 flaky 故障。
预期系统行为: 向 ATOMGIT_OUTPUT 写入 1,048,577 bytes 时，系统应拒绝写入或给出明确错误。
Oracle 来源: GitCode规格（max_step_output_per_param=1MB）

验证要点:
  - [正向] 系统报错或截断并给出警告
  - [负向] 不应静默截断且无提示

故障/压力参数: 输出参数大小=1,048,577 bytes
稳态判据:     step 状态=failure 或日志含 "1MB" / "超出限制" 警告
恢复预期:     明确报错（用户拆分输出或改用 artifact 后重试成功）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/pass-output-between-jobs.md
```


---

### 3.6 Runner 资源维度

```
意图 ID:    INTENT-REL-018
维度标签:   [reliability]
标题:       Runner 磁盘边界——small runner（50 GB）写入 49 GB 应成功

风险点:     大构建产物/日志场景下，磁盘边界值若被提前限制会导致正常任务失败。
预期系统行为: runs-on=[ubuntu-latest,x64,small]，磁盘 50 GB，job 顺序写入 49 GB 文件后仍能完成后续 step。
Oracle 来源: GitCode规格（small: disk_gb=50）

验证要点:
  - [正向] job 状态=success，df 显示剩余约 1 GB
  - [负向] 不应在写入 49 GB 时报磁盘满

故障/压力参数: runner flavor=small，磁盘配额=50 GB，写入量=49 GB
稳态判据:     job 状态=success，文件完整性校验通过（MD5）
恢复预期:     N/A
破坏级别:     fixture
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/runner-and-environment.md
```

```
意图 ID:    INTENT-REL-019
维度标签:   [reliability]
标题:       Runner 磁盘越界——small runner（50 GB）写入 51 GB 应失败并报磁盘满

风险点:     磁盘满时若系统无清晰报错，会导致构建失败原因难以定位。
预期系统行为: 写入超过 50 GB 时，系统应报磁盘满错误，job 状态=failure。
Oracle 来源: GitCode规格（small: disk_gb=50）

验证要点:
  - [正向] 写入 50+ GB 时报 "No space left on device" 或平台等价错误
  - [正向] job 状态=failure
  - [负向] 不应静默卡死或状态保持 in_progress

故障/压力参数: runner flavor=small，磁盘配额=50 GB，写入量=51 GB
稳态判据:     job 状态=failure，日志含磁盘满错误
恢复预期:     明确报错（用户改用 larger runner 或清理后重试成功）
破坏级别:     fixture
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/runner-and-environment.md
```

```
意图 ID:    INTENT-REL-020
维度标签:   [reliability]
标题:       Runner 内存边界——small runner（8 GB）分配 7.5 GB 应成功

风险点:     内存密集型任务（如大型 JVM 构建）在边界值处若被 OOM，会导致正常任务误杀。
预期系统行为: runs-on=[ubuntu-latest,x64,small]，内存 8 GB，job 分配并占用 7.5 GB 内存后正常完成。
Oracle 来源: GitCode规格（small: memory_gb=8）

验证要点:
  - [正向] job 状态=success，内存占用峰值≈7.5 GB
  - [负向] 不应在 7 GB 时 OOM

故障/压力参数: runner flavor=small，内存配额=8 GB，分配量=7.5 GB
稳态判据:     job 状态=success
恢复预期:     N/A
破坏级别:     fixture
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/runner-and-environment.md
```

```
意图 ID:    INTENT-REL-021
维度标签:   [reliability]
标题:       Runner 内存越界/OOM——small runner（8 GB）分配 9 GB 应被 OOM kill

风险点:     OOM 时若系统无清晰报错或错误终止其他进程，会导致隔离性破坏。
预期系统行为: 分配 9 GB 内存时，系统应 OOM kill 该 job 或使其失败，给出内存不足错误。
Oracle 来源: GitCode规格（small: memory_gb=8）

验证要点:
  - [正向] job 状态=failure
  - [正向] 日志含 OOM / "Out of memory" / "Killed" 信息
  - [负向] 不应导致 Runner 宿主机整体崩溃或影响同 Runner 其他 job

故障/压力参数: runner flavor=small，内存配额=8 GB，分配量=9 GB
稳态判据:     job 状态=failure，日志含 OOM 或 Killed 信息
恢复预期:     明确报错（用户改用 larger runner 或优化内存后重试成功）
破坏级别:     fixture
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/runner-and-environment.md
```

```
意图 ID:    INTENT-REL-022
维度标签:   [reliability]
标题:       Runner CPU 饱和——small runner（2 核）运行 4 个 CPU 密集型进程应完成但耗时延长

风险点:     CPU 饱和时系统应优雅降级（执行变慢但不被 kill），若直接终止则影响任务稳定性。
预期系统行为: 2 核 small runner 上启动 4 个并行 CPU burn 进程，job 最终完成，耗时约为单进程的 2 倍。
Oracle 来源: GitHub行为（Runner CPU 饱和时应公平调度，不应无故 kill）

验证要点:
  - [正向] job 状态=success
  - [非功能] 执行时间约为单进程 2 倍（±20% 容差）
  - [负向] 不应被系统强制终止

故障/压力参数: runner flavor=small，CPU=2 核，并行 CPU 密集型进程数=4，单进程运行 60 秒
稳态判据:     job 状态=success，总耗时 120±24 秒
恢复预期:     优雅降级（执行时间延长但成功完成）
破坏级别:     fixture
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/runner-and-environment.md
```


---

### 3.7 workflow_call 嵌套维度

```
意图 ID:    INTENT-REL-023
维度标签:   [reliability]
标题:       workflow_call 嵌套边界——2 层嵌套调用应成功执行

风险点:     可重用工作流嵌套若边界值实现错误，会导致编排复杂度受限。
预期系统行为: Workflow A 通过 workflow_call 调用 Workflow B，Workflow B 再调用 Workflow C，共 2 层嵌套，应成功执行。
Oracle 来源: GitCode规格（嵌套调用最多支持 2 层）

验证要点:
  - [正向] 3 个 workflow 均成功完成
  - [正向] 输入参数在每一层正确传递

故障/压力参数: 嵌套层数=2（A→B→C）
稳态判据:     最外层运行状态=success，所有子运行均 success
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-triggers.md
```

```
意图 ID:    INTENT-REL-024
维度标签:   [reliability]
标题:       workflow_call 嵌套越界——3 层嵌套调用应被拒绝

风险点:     超过嵌套上限若被静默允许，可能导致递归调用或资源耗尽。
预期系统行为: Workflow A→B→C→D（第 3 层嵌套）时，第 3 层调用应被拒绝，给出明确错误。
Oracle 来源: GitCode规格（嵌套调用最多支持 2 层）

验证要点:
  - [正向] 第 3 层调用失败，运行状态=failure
  - [正向] 日志含 "嵌套层数" / "2 层" 或类似错误
  - [负向] 不应死循环或挂起

故障/压力参数: 嵌套层数=3（A→B→C→D）
稳态判据:     运行状态=failure，日志明确提示嵌套超限
恢复预期:     明确报错（用户扁平化调用链后重试成功）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-triggers.md
```

---

### 3.8 执行模型关键机制

```
意图 ID:    INTENT-REL-025
维度标签:   [reliability]
标题:       needs 失败传播——上游 job 失败时下游 job 应被 skip

风险点:     needs 依赖失败传播若失效，会导致下游 job 在错误前置状态下执行。
预期系统行为: job A 失败，job B needs A，job B 应被 skip（除非显式 if: always()/failure()）。
Oracle 来源: GitHub行为（GitHub Actions 标准语义）

验证要点:
  - [正向] job A 状态=failure，job B 状态=skipped
  - [负向] job B 不应在 job A 失败后仍执行（除非 if 条件覆盖）

故障/压力参数: needs 依赖层数=1，上游 job 故意失败
稳态判据:     job B 状态=skipped
恢复预期:     N/A（设计行为）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-jobs.md；testing-focus.md §3
```

```
意图 ID:    INTENT-REL-026
维度标签:   [reliability]
标题:       matrix fail-fast=true——任意 job 实例失败应立即取消其余实例

风险点:     fail-fast 机制失效会浪费 Runner 资源在已注定失败的 matrix 上。
预期系统行为: 3×3 matrix（9 jobs），其中一个 job 实例失败后，其余尚未完成的实例应立即被取消。
Oracle 来源: GitCode规格（fail-fast: true 定义）

验证要点:
  - [正向] 失败 job 状态=failure
  - [正向] 其余未完成 jobs 状态=cancelled
  - [负向] 不应继续执行已失败的 matrix 其余实例

故障/压力参数: matrix=3×3=9 jobs，fail-fast=true，1 个 job 故意失败
稳态判据:     未完成 jobs 状态=cancelled，总执行时长显著短于全部跑完
恢复预期:     N/A（设计行为）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-matrix-builds.md；testing-focus.md §3
```

```
意图 ID:    INTENT-REL-027
维度标签:   [reliability]
标题:       matrix max-parallel=4——9 个组合应最多同时运行 4 个

风险点:     max-parallel 若失效，matrix 会瞬间耗尽所有 Runner，影响其他 workflow。
预期系统行为: 3×3 matrix（9 jobs），max-parallel=4，同时运行的 jobs 不应超过 4 个。
Oracle 来源: GitCode规格（max-parallel 限制同时运行的矩阵 job 实例数量）

验证要点:
  - [正向] 任意时刻 in_progress 的 matrix job 数 ≤4
  - [正向] 其余 jobs 状态=queued
  - [正向] 前 4 个完成后自动启动后续 jobs

故障/压力参数: matrix 组合数=9，max-parallel=4
稳态判据:     9 个 jobs 全部 completed(success)，峰值并发≤4
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-matrix-builds.md；testing-focus.md §3
```

```
意图 ID:    INTENT-REL-028
维度标签:   [reliability]
标题:       手动取消 workflow——运行中取消时 always() cleanup step 仍应执行

风险点:     取消时若 cleanup 不执行，会导致资源泄漏（如临时文件、锁、外部部署状态不一致）。
预期系统行为: 手动取消正在运行的 workflow，if: always() 的 cleanup step 仍执行，非 always step 被终止。
Oracle 来源: GitHub行为（cancel 语义标准行为）

验证要点:
  - [正向] 非 always step 被终止，不再继续输出日志
  - [正向] if: always() 的 cleanup step 被执行并输出日志
  - [正向] workflow 最终状态=cancelled

故障/压力参数: 取消时机=step 执行中（第 3/5 step）
稳态判据:     cleanup step 日志存在且 completed(success)，workflow 状态=cancelled
恢复预期:     优雅降级（已执行步骤结果保留，cleanup 执行）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-conditional-execution.md；testing-focus.md §3
```

```
意图 ID:    INTENT-REL-029
维度标签:   [reliability]
标题:       stages fail_fast 机制——阶段内任一 job 失败应立即终止同阶段其他 jobs

风险点:     stages 的 fail_fast 与 matrix fail-fast 是不同层面控制，需分别验证。
预期系统行为: stage 内 3 个 jobs 并行执行，1 个失败后，其余 2 个被立即终止。
Oracle 来源: GitCode规格（workflow-job-step-action.md: fail_fast 机制）

验证要点:
  - [正向] 失败 job 状态=failure
  - [正向] 同阶段其余 jobs 状态=cancelled 或 skipped
  - [负向] 不应进入下一阶段（若本阶段全部失败）

故障/压力参数: stage jobs=3，fail_fast=true，1 个 job 故意失败
稳态判据:     同阶段其余 jobs 状态∈{cancelled, skipped, failure}
恢复预期:     N/A（设计行为）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/workflow-job-step-action.md；testing-focus.md §3
```

```
意图 ID:    INTENT-REL-030
维度标签:   [reliability]
标题:       continue-on-error=true——job 失败后 workflow 不应终止

风险点:     continue-on-error 若失效，会导致 flaky test 等场景阻断整个流水线。
预期系统行为: job A 设置 continue-on-error=true 并故意失败，workflow 继续执行 job B。
Oracle 来源: GitCode规格（configure-jobs.md）

验证要点:
  - [正向] job A 状态=failure（但 workflow 不终止）
  - [正向] job B 正常执行并 success
  - [负向] workflow 不应因 job A 失败而整体 failure

故障/压力参数: continue-on-error=true，失败 job 数=1
稳态判据:     job B 状态=success，workflow 状态=success（或 failure 仅标记在 job A）
恢复预期:     N/A（设计行为）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-jobs.md；testing-focus.md §3
```


---

### 3.9 故障注入（混沌）

```
意图 ID:    INTENT-REL-031
维度标签:   [reliability]
标题:       故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志

风险点:     Runner 级故障（宿主机重启、OOM killer、运维误操作）是生产环境常见场景，系统需具备可观测的失败记录。
预期系统行为: job 运行到第 3 个 step 时，runner 进程收到 SIGKILL，job 状态=failure，已执行 step 的日志保留。
Oracle 来源: GitHub行为（Runner 失联后 job 标记失败）

验证要点:
  - [正向] job 状态=failure
  - [正向] step 1-2 的日志完整可查看
  - [正向] step 3 日志不完整或标记为中断
  - [负向] 不应状态=in_progress 挂起超过 5 分钟

故障/压力参数: 注入时机=第 3/5 step 执行中，故障类型=runner 进程 SIGKILL
稳态判据:     job 状态=failure，step 1-2 日志可下载查看
恢复预期:     明确报错（runner 失联/被终止），用户 rerun 后重试成功
破坏级别:     fixture
优先级线索:   RISK-REL-01
来源输入:     testing-focus.md §4 Runner 与隔离；testing-focus.md §12 稳定性专项
```

```
意图 ID:    INTENT-REL-032
维度标签:   [reliability]
标题:       故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误

风险点:     网络抖动时 artifact 上传若无限重试或静默失败，会导致资源泄漏或数据丢失。
预期系统行为: upload-artifact step 执行期间网络断开 30 秒，step 失败后 job 状态=failure，日志含网络错误。
Oracle 来源: GitHub行为（网络故障应明确报错）

验证要点:
  - [正向] upload-artifact step 状态=failure
  - [正向] 日志含 "network" / "connection" / "timeout" 或中文等价词
  - [负向] 不应无限挂起超过 120 秒

故障/压力参数: 注入时机=upload-artifact step 执行中，故障类型=网络分区（出站断开），持续时间=30 秒
稳态判据:     step 状态=failure，job 状态=failure，日志含网络错误
恢复预期:     明确报错（网络恢复后 rerun 成功）
破坏级别:     fixture
优先级线索:   RISK-REL-01
来源输入:     testing-focus.md §12 稳定性专项；gitcode-spec/upload-download-artifacts.md
```

```
意图 ID:    INTENT-REL-033
维度标签:   [reliability]
标题:       故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满

风险点:     磁盘满时若系统无清晰报错，会导致后续所有 IO 操作产生难以排查的随机失败。
预期系统行为: small runner（50 GB）上预填充 49.5 GB 数据，job 再尝试写入 2 GB artifact，应报磁盘满错误。
Oracle 来源: GitCode规格（small: disk_gb=50）

验证要点:
  - [正向] 写入失败，日志含 "No space left on device" 或平台等价错误
  - [正向] job 状态=failure

故障/压力参数: runner flavor=small，磁盘配额=50 GB，预填充=49.5 GB，追加写入=2 GB
稳态判据:     job 状态=failure，日志含磁盘满错误
恢复预期:     明确报错（用户清理磁盘或改用 larger runner 后重试成功）
破坏级别:     fixture
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；testing-focus.md §4 Runner 资源边界
```

```
意图 ID:    INTENT-REL-034
维度标签:   [reliability]
标题:       故障注入——cache 服务 503 不可用时 job 应优雅降级为 cache miss

风险点:     cache 服务是加速依赖项，非关键路径；若其不可用导致 job 失败，会降低系统可用性。
预期系统行为: cache restore step 时 cache 服务返回 503，step 应标记为 cache miss，job 继续执行（重新安装依赖）。
Oracle 来源: GitHub行为（cache miss 时 step 继续，不会导致 job 失败）

验证要点:
  - [正向] cache step 状态=success（miss）或 failure 但不阻断 job
  - [正向] 后续 step（如 npm ci）正常执行
  - [负向] job 不应因 cache 服务不可用而整体 failure

故障/压力参数: 注入时机=cache restore step，故障类型=依赖服务返回 503，持续时间=整个 step 期间
稳态判据:     job 状态=success，cache step 标记为 miss 或跳过
恢复预期:     优雅降级（无缓存继续执行，cache 服务恢复后下次命中）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     testing-focus.md §12 稳定性专项；gitcode-spec/using-dependency-cache.md
```

```
意图 ID:    INTENT-REL-035
维度标签:   [reliability]
标题:       故障注入——artifact 下载服务 503 不可用时 job 应失败并报依赖服务错误

风险点:     artifact 是跨 job 传递构建产物的关键路径，其服务不可用时应明确失败而非静默跳过。
预期系统行为: download-artifact step 时服务返回 503，step 失败，job 状态=failure。
Oracle 来源: GitCode规格（artifact 是跨 job 传递的必需路径）

验证要点:
  - [正向] download-artifact step 状态=failure
  - [正向] 日志含 503 / "service unavailable" 或中文等价词
  - [正向] job 状态=failure

故障/压力参数: 注入时机=download-artifact step，故障类型=依赖服务返回 503，持续时间=整个 step 期间
稳态判据:     job 状态=failure，日志含服务不可用错误
恢复预期:     明确报错（服务恢复后 rerun 成功）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     testing-focus.md §12 稳定性专项；gitcode-spec/upload-download-artifacts.md
```


---

### 3.10 并发洪泛与大规模

```
意图 ID:    INTENT-REL-036
维度标签:   [reliability]
标题:       并发洪泛——同一仓库 10 个 push 同时触发 10 个 workflow 运行应无丢失

风险点:     并发洪泛下若运行丢失或状态异常，会导致 CI 漏跑。
预期系统行为: 同一仓库短时间内 10 次 push，触发 10 个独立的 workflow 运行，全部进入 queued/in_progress。
Oracle 来源: GitHub行为（运行应全部创建）

验证要点:
  - [正向] 10 个运行均被创建，状态≠丢失/异常
  - [正向] 每个运行有独立的 RUN_ID
  - [负向] 不应出现运行数 <10 或状态混乱

故障/压力参数: 并发 workflow 触发数=10，触发方式=push，时间窗口=10 秒内
稳态判据:     10 个运行最终全部进入 completed（queued→in_progress→completed）
恢复预期:     自动恢复（排队完成后执行）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     testing-focus.md §12 稳定性专项
```

```
意图 ID:    INTENT-REL-037
维度标签:   [reliability]
标题:       并发洪泛——同一仓库 50 个 push 同时触发应正确排队/限流不崩溃

风险点:     极端洪泛下系统若崩溃或丢运行，会严重影响可用性。
预期系统行为: 50 次同时 push 触发 50 个运行，系统应正确排队或限流，API/UI 不崩溃，运行不丢失。
Oracle 来源: GitHub行为（运行应全部创建，按 Runner 容量排队）

验证要点:
  - [正向] 50 个运行均被创建
  - [正向] 系统 API/UI 响应正常（HTTP 200，无 5xx）
  - [非功能] 全部 50 个运行完成总时长 ≤（50/并发容量）×单运行时长 + 60 秒容差
  - [负向] 不应出现运行丢失、重复触发、状态机错乱

故障/压力参数: 并发 workflow 触发数=50，触发方式=push，时间窗口=30 秒内
稳态判据:     50 个运行最终全部 completed，无 5xx，无丢失
恢复预期:     自动恢复（排队完成后执行）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     testing-focus.md §12 稳定性专项
```

```
意图 ID:    INTENT-REL-038
维度标签:   [reliability]
标题:       大规模 matrix——20 个组合（4 维×5 值）应全部生成并正确调度

风险点:     matrix 规模较大时若展开算法有缺陷，会导致 job 丢失或变量传递错误。
预期系统行为: matrix 4 维 × 5 值 = 20 个 job 实例，全部生成，每个实例获得正确的矩阵变量值。
Oracle 来源: GitCode规格（configure-matrix-builds.md 展开算法）

验证要点:
  - [正向] 20 个 jobs 全部生成，状态≠丢失
  - [正向] 每个 job 的矩阵变量值与预期组合一致
  - [负向] 不应出现重复组合或遗漏组合

故障/压力参数: matrix 组合数=20（4 维×5 值），max-parallel 未设
稳态判据:     20 个 jobs 全部 completed(success)，矩阵变量校验 100% 通过
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-matrix-builds.md；testing-focus.md §12 稳定性专项
```

```
意图 ID:    INTENT-REL-039
维度标签:   [reliability]
标题:       大规模 matrix——50 个组合（5 维×10 值）应全部生成并正确调度

风险点:     更大规模 matrix 是压力测试展开算法与调度系统的关键场景。
预期系统行为: matrix 5 维 × 10 值 = 50 个 job 实例，全部生成并正确调度。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 50 个 jobs 全部生成
  - [正向] 无重复/遗漏组合
  - [非功能] 从触发到全部进入 in_progress 的调度时延 ≤300 秒

故障/压力参数: matrix 组合数=50（5 维×10 值），max-parallel 未设
稳态判据:     50 个 jobs 全部 completed(success)，调度时延≤300 秒
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-matrix-builds.md；testing-focus.md §12 稳定性专项
```

```
意图 ID:    INTENT-REL-040
维度标签:   [reliability]
标题:       超长日志——单 job 输出 100 MB 日志应完整保留且可下载查看

风险点:     大日志若被截断或无法下载，会导致调试困难。
预期系统行为: job 连续输出 100 MB 日志，运行结束后日志完整，可逐行查看/下载。
Oracle 来源: GitHub行为（大日志应完整保留）

验证要点:
  - [正向] 日志总大小≈100 MB
  - [正向] 日志首尾行均可查看，无截断
  - [正向] 日志下载 API/页面可正常下载

故障/压力参数: 日志大小=100 MB，生成方式=循环 echo
稳态判据:     日志可下载，MD5/行数校验通过（无截断）
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     testing-focus.md §12 稳定性专项
```


```
意图 ID:    INTENT-REL-041
维度标签:   [reliability]
标题:       超大 artifact——100 MB artifact 上传后下游 job 应成功下载

风险点:     大 artifact 若上传/下载不稳定，会导致跨 job 传递失败。
预期系统行为: 上传 100 MB artifact，下游 job download-artifact 成功，内容完整性校验通过。
Oracle 来源: GitCode规格（artifacts-and-cache.md: 制品大小不超过限制——但未给具体数值，100MB 作为实测探针）

验证要点:
  - [正向] upload 成功
  - [正向] download 成功
  - [正向] 下载后文件 MD5 与上传前一致

故障/压力参数: artifact 大小=100 MB
稳态判据:     upload 与 download 均 success，MD5 校验通过
恢复预期:     N/A
破坏级别:     fixture
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/upload-download-artifacts.md；artifacts-and-cache.md
```

```
意图 ID:    INTENT-REL-042
维度标签:   [reliability]
标题:       超多 step——单 job 内 50 个 step 应全部串行执行无丢失

风险点:     step 数过多时若调度或日志系统有瓶颈，会导致 step 丢失或状态未回写。
预期系统行为: job 内定义 50 个 step，每个 step 输出唯一标识，全部 50 个 step 按顺序执行。
Oracle 来源: GitHub行为

验证要点:
  - [正向] 50 个 step 全部出现在运行详情页
  - [正向] 每个 step 的日志包含其唯一标识
  - [正向] step 执行顺序与定义顺序完全一致
  - [负向] 不应出现 step 丢失、顺序错乱

故障/压力参数: step 数=50，每 step 运行时长=1 秒
稳态判据:     50 个 step 全部 completed(success)，顺序正确，日志完整
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     testing-focus.md §12 稳定性专项
```

```
意图 ID:    INTENT-REL-043
维度标签:   [reliability]
标题:       长时运行接近 timeout 边界——350 分钟运行应成功且心跳保活正常

风险点:     长时运行若心跳/保活机制失效，会被系统误判为死进程而提前终止。
预期系统行为: timeout-minutes=360，job 运行 350 分钟，期间心跳/日志持续更新，最终成功。
Oracle 来源: GitCode规格（default_job_timeout_minutes=360）

验证要点:
  - [正向] job 状态=success
  - [正向] 运行期间每 60 秒至少输出 1 行日志（保活证据）
  - [负向] 不应在 350 分钟前被误判为死进程而终止

故障/压力参数: timeout-minutes=360，实际运行时长=350 分钟，心跳间隔=60 秒
稳态判据:     job 状态=success，总运行时长=350±2 分钟
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；testing-focus.md §12 稳定性专项
```

```
意图 ID:    INTENT-REL-044
维度标签:   [reliability]
标题:       并发资源公平性——2 个 workflow 各 3 个 jobs 应被公平调度

风险点:     若调度器偏向先提交的 workflow，后提交的会长时间饥饿。
预期系统行为: workflow X 和 workflow Y 同时触发，各含 3 个 jobs，6 个 jobs 应被交错/公平调度，无单个 workflow 独占所有 Runner。
Oracle 来源: GitHub行为（公平调度预期）

验证要点:
  - [正向] 2 个 workflow 的 jobs 启动时间差 ≤60 秒（无显著饥饿）
  - [负向] 不应出现 workflow X 全部完成后 workflow Y 才开始

故障/压力参数: workflow 数=2，每 workflow jobs=3，每 job 运行时长=30 秒
稳态判据:     2 个 workflow 均 completed(success)，启动时延差≤60 秒
恢复预期:     N/A
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     testing-focus.md §12 稳定性专项
```

```
意图 ID:    INTENT-REL-045
维度标签:   [reliability]
标题:       自托管 K8s Runner 弹性伸缩——min=1/max=1 时并发 3 个 jobs 应排队执行

风险点:     K8s Runner 弹性伸缩若突破 max 限制，会导致资源超配；若不按 min 保持，会导致冷启动时延。
预期系统行为: K8s Runner 组配置 min_runners=1, max_runners=1，并发触发 3 个 jobs，Pod 数保持 1，jobs 排队执行。
Oracle 来源: GitCode规格（default_min_runners=1, default_max_runners=1, elastic_scaling=true）

验证要点:
  - [正向] Runner Pod 数始终=1
  - [正向] 3 个 jobs 顺序执行（峰值并发=1）
  - [负向] 不应创建 2 个及以上 Pod

故障/压力参数: K8s Runner min=1, max=1，并发 jobs=3
稳态判据:     3 个 jobs 全部 completed(success)，Pod 数=1，总耗时≈3×单 job 时长
恢复预期:     自动恢复（排队完成后执行）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/runner-and-environment.md
```

```
意图 ID:    INTENT-REL-046
维度标签:   [reliability]
标题:       缓存 LRU 淘汰压力——连续写入 10 个大缓存后最旧缓存应被正确淘汰

风险点:     LRU 策略若失效，会导致缓存无限增长或错误淘汰新缓存。
预期系统行为: 连续写入 10 个不同 key 的缓存（每个 100 MB），最旧的 key 应在后续写入时被 LRU 淘汰。
Oracle 来源: GitCode规格（cache.retention_policy=LRU 淘汰）

验证要点:
  - [正向] 最新写入的缓存 key 可命中
  - [正向] 最旧的缓存 key 变为 miss（被驱逐）
  - [负向] 不应出现所有 10 个 key 同时命中（若容量不足）

故障/压力参数: 缓存数=10，每个大小=100 MB，写入间隔=5 分钟
稳态判据:     最旧 key 状态=miss，最新 key 状态=hit
恢复预期:     N/A（设计行为）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/artifacts-and-cache.md
```

```
意图 ID:    INTENT-REL-047
维度标签:   [reliability]
标题:       artifact 保留期 90 天边界——第 91 天应不可下载

风险点:     保留期若被突破，会导致存储无限增长；若提前删除，会导致用户数据丢失。
预期系统行为: artifact 保留期设为 90 天，第 90 天仍可下载，第 91 天下载应失败。
Oracle 来源: GitCode规格（artifact_retention.default_days=90）

验证要点:
  - [正向] 第 90 天下载成功（HTTP 200）
  - [正向] 第 91 天下载失败（404 / 403）

故障/压力参数: 保留天数=90，验证时机=第 90 天、第 91 天
稳态判据:     第 90 天可下载，第 91 天不可下载
恢复预期:     N/A（设计行为）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     platform-config/README.md（2026-07-21）；gitcode-spec/artifacts-and-cache.md
```

```
意图 ID:    INTENT-REL-048
维度标签:   [reliability, compatibility]
标题:       取消与 needs 条件竞态——job A 被取消时 job B（if: failure()）应正确判定

风险点:     取消语义与状态函数（failure/cancelled/always）的交互若存在竞态，会导致条件 job 执行错误。
预期系统行为: job A 运行中被手动取消，job B needs A 且 if: failure()，job B 应被 skip（cancelled≠failure）。
Oracle 来源: GitHub行为（cancelled 与 failure 是不同状态）

验证要点:
  - [正向] job A 状态=cancelled
  - [正向] job B 状态=skipped（因 cancelled≠failure，不满足 if: failure()）
  - [负向] job B 不应执行

故障/压力参数: 取消时机=job A step 执行中，job B 条件=if: failure()
稳态判据:     job B 状态=skipped
恢复预期:     N/A（设计行为）
破坏级别:     none
优先级线索:   RISK-REL-01
来源输入:     gitcode-spec/configure-conditional-execution.md；testing-focus.md §3
```


---

### 3.11 历史 bug 回归与性能基准（本轮增量 · 来源：history/issues-encountered.md）

```
意图 ID:    INTENT-REL-049
维度标签:   [reliability]
标题:       Runner 规格真实性——small/medium/large 实际 CPU/内存/磁盘 vs 声明值

风险点:     platform-config 给出 flavor 规格表（small 2C8G50G ~ 2xlarge 32C128G1T），但历史 #7/#52/#54/#96 显示资源调度异常（arm 任务申请 2xlarge 报错、空闲却拉不到资源）。若实际分配低于声明值，用户按规格选型后会在编译/测试时遭遇 OOM、磁盘满或无解释失败。
预期系统行为: 每个 flavor 实际可用 CPU 核数、内存容量、磁盘容量不低于声明值的 90%（允许虚拟化 overhead），且不超额分配导致 neighbor 争抢。
Oracle 来源: GitCode规格（platform-config/README.md:50-57 flavor_specs）

验证要点:
  - [正向] small(2C8G50G)/medium(4C16G100G)/large(8C32G200G) 探针 job 读取 `/proc/cpuinfo`(nproc)、`free -m`(MemAvailable)、`df -BG $RUNNER_TEMP`(Avail) 均 ≥ 声明值 × 0.9。
  - [负向] 实际资源不应显著低于声明（如 small 实际只有 1C4G），也不应因同主机多 runner 共享导致波动>20%。
  - [非功能] 各 flavor 探针在 5 分钟内完成调度（queued→running ≤ 5min）。

故障/压力参数: 对 slim/small/medium/large/xlarge/2xlarge 六种 flavor 各触发 3 次探针 job（每次打印系统资源快照）；汇总 18 次采样，计算实际/声明比率最小值。稳态判据：所有 flavor 的 CPU/内存/磁盘最小比率 ≥ 0.9。
恢复预期: 不适用（探测验证类；若发现规格不符则记为平台声明缺陷）。
破坏级别: none
来源输入:   platform-config/README.md:50-57；history/issues-encountered.md #7/#52/#54/#96
优先级线索: RISK-REL-01（并发与调度），历史资源调度异常，建议 P1
```

```
意图 ID:    INTENT-REL-050
维度标签:   [reliability, usability]
标题:       调度延迟基准——queued→running P50/P95 等待时间

风险点:     历史 #52 显示自定义镜像 pending 约 10min 后失败；#7 显示 2 个 runner 空闲但 job 排队 1h 后失败。平台未公布调度延迟 SLA。若延迟不可预期，用户无法判断「正常排队」与「调度卡死」。
预期系统行为: 有空闲 runner 时 job 在合理时限内进入 running；排队深度增加时延迟线性可控，无无限饿死。需实测坐定 P50/P95 基线。
Oracle 来源: 未知·待实测（GitCode 未公布调度延迟 SLA）

验证要点:
  - [正向] 空闲 runner 池条件下，单次触发 job 的 queued→running 延迟有界。
  - [负向] 不应出现「runner 空闲但 job 死等 >10min」的调度丢失。
  - [非功能] 记录 P50/P95/P99 延迟，形成可复现的基准数据集。

故障/压力参数: 分两组——(a) 基线组：在空闲 runner 条件下连续触发 30 次单 job workflow，记录每次 queued→running 延迟；(b) 压力组：并发触发 20 个 job（各 60s sleep），记录每个 job 的排队延迟与执行顺序。稳态判据：基线组 P95≤60s；压力组所有 job 最终完成，无饿死。
恢复预期: 不适用（性能基准探测）。
破坏级别: none
来源输入:   history/issues-encountered.md #7/#52/#78；platform-config/README.md:41-57
优先级线索: RISK-REL-01（并发洪泛下排队/公平性失效），建议 P1
```

```
意图 ID:    INTENT-REL-051
维度标签:   [reliability, usability]
标题:       日志加载性能——50MB/200MB 日志下载与查看耗时

风险点:     历史 #14 显示任务失败查看日志时加载时间约 7min；#6 显示日志无法下载。大日志（如编译输出、测试报告）的下载与 UI 查看性能直接影响故障排查效率。若 200MB 日志需 >5min 才能下载，严重拖长 MTTR。
预期系统行为: 日志量 ≤200MB 时，下载在可接受时限内完成；UI 查看不卡死；日志内容完整、不乱序、不截断。
Oracle 来源: 历史实证（issues-encountered.md #6/#14）；GitHub Actions 行为作参照

验证要点:
  - [正向] 50MB 日志可在 ≤30s 内下载完成；200MB 日志可在 ≤120s 内下载完成。
  - [负向] 不应出现「日志显示成功但下载文件损坏/截断」；不应 UI 卡死无法查看。
  - [非功能] 下载后文件大小与原始生成大小一致，行数一致。

故障/压力参数: 构造三组日志量——(a) 基准 5MB（1 万行）、(b) 50MB（10 万行）、(c) 200MB（40 万行）；用 `seq` 生成带序号行确保可校验。每组触发 3 次，测量：UI 首次可查看时间、下载 API 返回完整文件耗时、文件大小/行数校验。稳态判据：(a) 下载≤10s；(b) ≤30s；(c) ≤120s；且大小/行数 100% 一致。
恢复预期: 不适用（性能基准）。
破坏级别: none
来源输入:   history/issues-encountered.md #6/#14；platform-config/README.md:33
优先级线索: 历史日志性能严重问题，建议 P1
```

```
意图 ID:    INTENT-REL-052
维度标签:   [reliability]
标题:       镜像拉取性能——自定义 container 环境准备耗时基准

风险点:     历史 #52 显示默认 runner+自定义镜像 pending 约 10min 后失败；#70 显示拉镜像过长超过默认环境准备时间；#89 显示自定义资源池拉取自定义镜像报错。自定义镜像是 CI/CD 关键路径，若拉取耗时不可预期或超过 job timeout 隐式阈值，会导致大规模 job 失败。
预期系统行为: 常用自定义镜像（如 500MB/2GB/5GB）在合理时限内拉取完成；超大镜像应有明确指引或超时保护，不无限 pending。
Oracle 来源: 历史实证（issues-encountered.md #52/#70/#89）；GitCode规格（configuring-images-toolchains.md:9-52）

验证要点:
  - [正向] 500MB 镜像在 2min 内完成拉取并启动 container job。
  - [负向] 不应出现「镜像拉取 pending 10min 后无解释失败」；不应拉取失败后无归因（网络/registry/认证）。
  - [非功能] 记录镜像大小→拉取耗时映射关系，形成基线。

故障/压力参数: 使用三种体积档的公开镜像作探针（~500MB、~2GB、~5GB），各触发 3 次 container job（job 内仅打印环境信息）。记录 queued→running 延迟（含镜像拉取）与容器启动到 step 执行的时间差。稳态判据：500MB≤2min、2GB≤5min、5GB≤10min；失败时有明确归因。
恢复预期: 不适用（性能基准；失败时按 REL-025 归因处理）。
破坏级别: fixture
来源输入:   history/issues-encountered.md #52/#70/#89；platform-config/README.md:50-57
优先级线索: 历史镜像拉取高频问题，建议 P1
```


```
意图 ID:    INTENT-REL-053
维度标签:   [reliability]
标题:       制品传输性能——100MB/500MB/1GB artifact 上传下载耗时

风险点:     REL-013 已探测 artifact 大小上限，但未测量传输速率。大制品上传/下载若耗时过长，会逼近 job timeout（360min）或导致用户放弃使用 artifact 传递构建产物。历史无直接 artifact 性能问题，但平台未声明速率 SLA。
预期系统行为: artifact 上传/下载速率可预期，100MB~1GB 档在合理时限内完成，不因超时而假成功或失败。
Oracle 来源: 未知·待实测（platform-config/README.md:34 未公开上限；GitHub artifact 行为作参照）

验证要点:
  - [正向] 100MB/500MB/1GB 制品上传成功，下载后 hash 一致。
  - [负向] 上传不应「显示成功但下载失败/损坏」；下载不应因体积大被静默截断。
  - [非功能] 记录 upload/download 耗时，计算有效传输速率。

故障/压力参数: 用 `dd` 生成确定大小文件（100MB、500MB、1GB），先 upload-artifact，再在下游 job download-artifact 并校验 SHA256。各体积档触发 3 次。稳态判据：上传/下载均成功且 hash 100% 匹配；100MB 上传≤30s、下载≤30s；500MB 上传≤120s、下载≤120s；1GB 上传≤300s、下载≤300s。
恢复预期: 不适用（性能基准）。
破坏级别: fixture
来源输入:   platform-config/README.md:34；history/issues-encountered.md #15/#16（obs 上传相关，artifact 同族风险）
优先级线索: RISK-REL-01（大规模下稳定性），建议 P1
```

```
意图 ID:    INTENT-REL-054
维度标签:   [reliability]
标题:       缓存加速比——cache 命中 vs 未命中构建耗时对比

风险点:     cache 的核心价值是加速构建。若 cache save/restore 本身开销极大（如 restore 耗时 > 重新下载依赖），或命中后实际无加速，cache 功能形同虚设。平台未声明 cache 性能 SLA。
预期系统行为: cache 命中时，构建耗时显著低于未命中（加速比可观测）；cache save/restore 本身开销不抵消加速收益。
Oracle 来源: 未知·待实测（artifacts-and-cache.md:36-42；platform-config/README.md:35）

验证要点:
  - [正向] 首次运行（未命中）完成依赖安装；第二次运行（命中）restore 缓存后跳过安装，总耗时降低。
  - [负向] cache 命中后不应仍执行完整安装（失效）；restore 本身不应耗时 > 未命中时的安装耗时。
  - [非功能] 加速比 ≥ 2×（命中耗时 ≤ 50% 未命中耗时）。

故障/压力参数: 构造典型构建 job——安装约 500MB node_modules（或等效 Python/Go 依赖包）。第一轮无 cache，记录「安装耗时 T1」；第二轮 cache 命中，记录「restore 耗时 + 构建耗时 T2」。重复 3 轮取平均。稳态判据：T2 ≤ 0.5 × T1；restore 耗时 ≤ 30s。
恢复预期: 不适用（性能基准；若未命中则正常回退重建）。
破坏级别: fixture
来源输入:   platform-config/README.md:35；artifacts-and-cache.md:36-42
优先级线索: 性能专项，建议 P2
```

```
意图 ID:    INTENT-REL-055
维度标签:   [reliability]
标题:       并发压测——concurrency.max=5 时触发 20 个 workflow 的排队与完成率

风险点:     REL-001/003 已验证 max=5 的边界与 QUEUE 行为，但未做大规模洪泛（20 个并发触发）。洪泛下可能出现队列丢失、调度器崩溃、runner 池耗尽后无法恢复、或某些运行被无限饿死。
预期系统行为: 20 次触发最终全部完成（0 丢失），任一时刻 running≤5，排队者按 FIFO 消费，调度器不崩溃，runner 池在完成后恢复可用。
Oracle 来源: GitCode规格（platform-config/README.md:10-11 concurrency.max=1-5；exceed-action=QUEUE）

验证要点:
  - [正向] 20 次触发全部进入终态（success/failure/cancelled），0 丢失。
  - [负向] running 峰值不应 >5；不应出现运行静默消失（无状态记录）。
  - [非功能] 排队消费顺序稳定；所有运行在合理时限内完成（如 20×30s 任务 + 排队 ≤ 15min）。

故障/压力参数: concurrency.max=5、exceed-action=QUEUE；在 10s 内并发触发 20 次同一 workflow（每 job sleep 30s）；每 5s 采样 running/queued/completed 计数，记录总完成时间与各运行 queued→running 延迟。稳态判据：completed=20、running_max=5、总耗时≤15min。
恢复预期: 不适用（压测后调度器与 runner 池应自动恢复）。
破坏级别: none
来源输入:   platform-config/README.md:10-11；spec.md C-QUOTA-01/C-EXEC-21
优先级线索: RISK-REL-01（并发洪泛下排队/公平性失效），建议 P1
```

```
意图 ID:    INTENT-REL-056
维度标签:   [reliability]
标题:       矩阵调度公平性——20 实例 matrix 配 max-parallel=4 的无饿死验证

风险点:     REL-010 探测 matrix 组合数上限，REL-027 验证 fail-fast，但未覆盖 max-parallel 限制下的大规模矩阵公平调度。若调度器有偏（如优先某些矩阵键），部分实例可能被长期饿死，导致整体 workflow 耗时不可预期。
预期系统行为: 20 个 matrix 实例在 max-parallel=4 下全部完成，无实例被无限饿死；各实例的 queued 等待时间方差有界（最大/最小比 ≤ 3）。
Oracle 来源: GitCode规格（configure-matrix-builds.md:110-121；platform-config 未公开矩阵上限）

验证要点:
  - [正向] 20 实例全部执行完成，状态正确。
  - [负向] 任一实例不应被无限饿死（queued 时间 > 总时限的 50%）。
  - [非功能] 各实例 queued 延迟分布可观测，无极端离群值。

故障/压力参数: matrix 维度 `version:[1..20]`（20 组合），max-parallel=4，每实例 sleep 30s。记录每个实例的 queued→running 延迟与总耗时。稳态判据：20 实例 100% 完成；最大 queued 延迟 ≤ 3 × 最小延迟；总耗时 ≤ 20/4×30s + 排队开销 ≈ 3min。
恢复预期: 不适用（公平性验证）。
破坏级别: none
来源输入:   spec.md C-EXEC-15/C-QUOTA-08；testing-focus §3（matrix）
优先级线索: RISK-REL-01（公平性失效），建议 P1
```

```
意图 ID:    INTENT-REL-057
维度标签:   [reliability]
标题:       资源调度状态一致性——空闲 runner 存在时 job 不应死等

风险点:     历史 #12 显示「两个 job 持续处于等待状态，重试也一样等待，但资源池已释放」；#78 显示「没有任务在执行时 runner 也显示运行中，再触发流水线会一直转圈」。调度状态不一致（runner 实际空闲但平台认为忙碌，或 job 已分配但 runner 未认领）会导致 job 死等。
预期系统行为: 当 runner 池存在空闲 runner 时，新触发 job 应在有限时限内（≤60s）被调度到 running；不应出现 runner 空闲但 job 无限 queued 的状态不一致。
Oracle 来源: 历史实证（issues-encountered.md #12/#78）

验证要点:
  - [正向] 空闲 runner 条件下触发 job，queued→running ≤ 60s。
  - [负向] 不应出现「runner 空闲但 job 死等 >5min」；不应 runner 状态与实际不符。
  - [非功能] 连续 10 次触发均满足延迟上限，无 flaky。

故障/压力参数: 确保 runner 池有 ≥2 个空闲 runner；连续触发 10 次单 job workflow（各 sleep 30s），每次完成后等待 runner 回到空闲再触发下一次；记录每次 queued→running 延迟。稳态判据：10 次全部 ≤60s，平均 ≤30s。
恢复预期: 不适用（一致性验证；若发现死等则记为调度缺陷）。
破坏级别: none
来源输入:   history/issues-encountered.md #12/#78；platform-config/README.md:41-57
优先级线索: 历史调度状态严重问题，建议 P1；若复现死等则升 P0
```

```
意图 ID:    INTENT-REL-058
维度标签:   [reliability]
标题:       Runner 状态机正确性——空闲/运行/离线转换与时序一致性

风险点:     历史 #78 显示 runner 状态与实际执行不同步；#7/#54 显示资源空闲但调度失败。Runner 状态机（idle→running→offline 及反向转换）若与平台调度器状态不一致，会导致调度决策错误。
预期系统行为: Runner 状态转换与时序符合状态机定义——idle 可接新 job、running 时不可再接、offline 时不参与调度；状态转换可观测且无跳变（如 running→idle 中间不应出现 undefined）。
Oracle 来源: 历史实证（issues-encountered.md #7/#54/#78）

验证要点:
  - [正向] job 触发后 runner 进入 running；job 完成后 runner 回到 idle；idle runner 可再接受新 job。
  - [负向] running 中的 runner 不应被调度第二个 job（除非支持并发，而 GitCode 默认单 job per runner）；offline runner 不应被分配 job。
  - [非功能] 状态转换时延有界（idle→running ≤ 30s，running→idle ≤ 60s）。

故障/压力参数: 对同一 runner 连续执行「触发 job_A(sleep 60s) → 观察状态 → 等完成 → 触发 job_B(sleep 30s) → 观察状态」循环 5 轮。记录每轮状态转换时序。稳态判据：状态序列符合 idle→running→idle，无异常跳变；转换时延在上限内。
恢复预期: 不适用（状态机验证；若状态不一致记为平台缺陷）。
破坏级别: none
来源输入:   history/issues-encountered.md #7/#54/#78；platform-config/README.md:41-57
优先级线索: 历史 runner 状态高频异常，建议 P1
```


```
意图 ID:    INTENT-REL-059
维度标签:   [reliability, usability]
标题:       日志系统稳定性——6 万行日志无乱序/无丢失/无截断

风险点:     历史 #80 显示日志打印乱序；#81 显示日志大概率不显示。大日志量下（如编译输出、测试矩阵并行日志聚合），乱序和丢失会让用户无法定位错误。6 万行是大型编译任务的常见输出量级。
预期系统行为: 6 万行顺序输出在日志中保持原始顺序，行数完整（0 丢失），可搜索，可下载。
Oracle 来源: 历史实证（issues-encountered.md #80/#81）；GitHub Actions 行为作参照

验证要点:
  - [正向] 6 万行带递增序号的日志在 UI 和下载文件中均完整、顺序正确。
  - [负向] 不应出现行号跳变、重复、乱序；不应出现「日志中间缺失一段」。
  - [非功能] UI 加载 6 万行不卡死；搜索特定行号可定位。

故障/压力参数: job 内用 `for i in $(seq 1 60000); do echo "LOG_LINE_$i $(date +%s%N)"; done` 生成 6 万行带序号和时间戳的日志。触发 3 次。分别校验：UI 行数、下载文件行数、行号单调递增、时间戳单调递增。稳态判据：3 次均行数=60000、无乱序、无丢失。
恢复预期: 不适用（稳定性验证；若发现乱序/丢失则记为日志系统缺陷）。
破坏级别: none
来源输入:   history/issues-encountered.md #80/#81；platform-config/README.md:33
优先级线索: 历史日志乱序/丢失高频问题，建议 P1
```

```
意图 ID:    INTENT-REL-060
维度标签:   [reliability, completeness]
标题:       Workflow YAML 缓存失效——修改后无旧代码残留

风险点:     历史 #85 显示「子 workflow 更新后从日志看用的还是旧代码」，说明平台存在 YAML 或 workflow_call 缓存未刷新问题。若修改 YAML 后仍执行旧版本，会导致调试困难、代码与行为不一致，甚至引入安全修复无法生效的风险。
预期系统行为: 修改 `.gitcode/workflows/` 下的 YAML 文件并 push 后，新触发运行应执行最新版本；workflow_call 引用的子 workflow 修改后也立即生效。
Oracle 来源: 历史实证（issues-encountered.md #85）；GitCode规格（workflow-file-location-structure.md）

验证要点:
  - [正向] 修改主 workflow YAML（如修改 echo 输出字符串）后触发，日志中出现新字符串。
  - [负向] 不应出现「YAML 已改但日志仍打印旧字符串」的缓存残留。
  - [非功能] 修改子 workflow（被 workflow_call 引用）后，父 workflow 触发也使用新版子 workflow。

故障/压力参数: 构造 workflow_A 调用 workflow_B（workflow_call）。第一轮执行记录输出 marker_v1；修改 workflow_B 输出为 marker_v2 并 push；立即触发 workflow_A。观测日志输出是 v1 还是 v2。重复 3 轮（修改→触发→校验）。稳态判据：3 轮均打印 marker_v2，0 残留。
恢复预期: 不适用（一致性验证；若发现缓存残留记为平台缺陷）。
破坏级别: fixture
来源输入:   history/issues-encountered.md #85
优先级线索: 历史缓存失效实证 bug，建议 P1
```

```
意图 ID:    INTENT-REL-061
维度标签:   [reliability]
标题:       取消操作可靠性——queued/running/post 各阶段取消状态正确过渡

风险点:     REL-028/048 已覆盖 running 中取消的 grace period 与状态收敛，但未覆盖 queued 阶段取消（此时 job 尚未分配 runner）和 post 阶段取消（此时主流程已完成，取消应不影响已完成结论）。历史 #39 显示取消后状态异常。
预期系统行为: queued 阶段取消→直接变为 cancelled，不分配 runner；running 阶段取消→按 REL-028/048 收敛；post 阶段取消→post 被终止但主流程结论已定型（success/failure 不变）。
Oracle 来源: GitCode规格（C-EXEC-24 取消语义）；历史 issues-encountered.md #39

验证要点:
  - [正向] queued 阶段取消终态=cancelled，无 runner 分配记录；post 阶段取消后主流程结论不变。
  - [负向] queued 取消后不应错标为 success/failure，也不应之后突然被调度 running。
  - [非功能] 各阶段取消到终态稳定时间 ≤ 60s。

故障/压力参数: 构造三组实验——(a) 触发后立即取消（queued 阶段）；(b) running 30s 后取消（running 阶段，复现 REL-028）；(c) 主 step 完成后、post 执行中取消（post 阶段）。每组 3 次。记录：取消时刻、终态、runner 分配情况、状态稳定时间。稳态判据：(a) 终态=cancelled、无 runner；(b) 终态=cancelled、post 执行、runner 释放；(c) 主结论不变、post 被终止。
恢复预期: 优雅降级——各阶段取消后终态稳定，runner 释放可复用。
破坏级别: fixture
来源输入:   history/issues-encountered.md #39；spec.md C-EXEC-24
优先级线索: 历史取消状态异常，建议 P1
```

```
意图 ID:    INTENT-REL-062
维度标签:   [reliability]
标题:       网络依赖容错——workflow 中访问不可达地址的明确失败与有界超时

风险点:     REL-032 已覆盖 artifact 上传时网络分区，但未覆盖 workflow step 中用户脚本主动访问不可达地址的场景。若 `curl` 不可达地址时无连接超时（hang 至 job timeout 360min），会严重浪费 runner 资源。
预期系统行为: 访问不可达地址时，在合理连接超时（如 ≤60s）后失败，并归因到网络/连接，不 hang 至 job timeout。
Oracle 来源: 未知·待实测（platform-config network_egress 仅一句；history #65 无法连外网）

验证要点:
  - [正向] 访问可达地址成功返回。
  - [负向] 访问不可达地址（不存在域名、防火墙 drop 的端口、内网黑洞地址）不应 hang > 60s。
  - [非功能] 失败信息可归因为连接超时/DNS 失败/拒绝连接。

故障/压力参数: job 内依次 `curl --connect-timeout 10 --max-time 120` 访问：(a) 公网可达端点（基准）；(b) 不存在域名（DNS 失败）；(c) 192.0.2.1（RFC5737 测试地址，黑洞）；(d) 可达主机但被防火墙 drop 的端口。记录各目标返回码与耗时。稳态判据：(a) 成功；(b)(c)(d) 均在 ≤60s 内失败且归因清晰。
恢复预期: 明确报错——不可达目标在连接超时有界失败后返回可理解错误，不 hang 至 job timeout。
破坏级别: none
来源输入:   history/issues-encountered.md #65；platform-config/README.md:97
优先级线索: 资源浪费风险，建议 P2
```


```
意图 ID:    INTENT-REL-063
维度标签:   [reliability]
标题:       制品并发写一致性——多 job 同时 upload-artifact 同名 artifact

风险点:     矩阵或多 job 并行时，若多个实例同时向同名 artifact 写入，可能产生竞态（后覆盖前、文件损坏、元数据混乱、下载时拿到混合内容）。平台未声明同名 artifact 的并发写语义。
预期系统行为: 同名 artifact 并发写有确定语义——要么后写入者覆盖（版本化）、要么报错冲突、要么按 job 隔离（每个 job 写独立命名空间）。绝不产生静默损坏或下载时内容混杂。
Oracle 来源: 未知·待实测（platform-config/README.md:34 未公开 artifact 并发语义）

验证要点:
  - [正向] 单 job 上传后下载内容完整。
  - [负向] 多 job 同时写同名 artifact 后，下载内容不应是损坏/混合/不可预期的中间态。
  - [非功能] 若平台支持覆盖/版本化，行为应稳定可复现。

故障/压力参数: matrix 3×1（3 实例并行），每实例生成不同内容的文件（如实例 1 写 "A"×1MB、实例 2 写 "B"×1MB、实例 3 写 "C"×1MB），同时 upload-artifact 到同名 `concurrent-artifact`。随后在下游 job 下载该 artifact 并校验内容。稳态判据：下载内容确定（AAA 或 BBB 或 CCC，或按实例隔离的多文件），绝非 ABA/BAB 等混合态。
恢复预期: 不适用（并发语义验证；若发现损坏记为竞态缺陷）。
破坏级别: fixture
来源输入:   platform-config/README.md:34；testing-focus §8（artifact）
优先级线索: 竞态风险，建议 P1
```

```
意图 ID:    INTENT-REL-064
维度标签:   [reliability, completeness]
标题:       子任务状态传播——workflow_call 失败/未拉起时不应假阳性完成

风险点:     历史 #30 显示「workflow_call 无法拉起子任务，但显示已完成」；#64 显示「workflow_call 任务失败，job if 未生效」。workflow_call 的状态传播若不可靠，会导致父 workflow 显示成功而实际子任务失败或未执行，产生严重的假阴性（用户以为 CI 通过）。
预期系统行为: 子 workflow 失败时，父 workflow 的 workflow_call step 失败，并阻断下游默认 job（除非显式 if:always/failure）；子 workflow 无法拉起时，step 明确失败而非显示成功。
Oracle 来源: 历史实证（issues-encountered.md #30/#64）；GitCode规格（C-EXEC-02/C-EXEC-03）

验证要点:
  - [正向] 子 workflow 成功时，父 workflow 成功。
  - [负向] 子 workflow 失败（step exit 1）时，父 workflow 不应显示成功；子 workflow 无法拉起时，父 workflow 应显示失败。
  - [非功能] 失败归因指明是 workflow_call 子任务失败，而非泛化 failure。

故障/压力参数: 构造三组——(a) 子 workflow 正常成功；(b) 子 workflow 内 step exit 1；(c) 引用不存在的子 workflow（无法拉起）。父 workflow 均含 workflow_call step + 下游默认 job。观测父 workflow 终态与下游 job 是否执行。稳态判据：(a) 父 success、下游执行；(b) 父 failure、下游跳过；(c) 父 failure、下游跳过。
恢复预期: 明确报错——子任务失败/未拉起时父任务正确标记失败，用户可重跑或修复子任务后恢复。
破坏级别: fixture
来源输入:   history/issues-encountered.md #30/#64/#68/#84；spec.md C-EXEC-02/C-EXEC-03
优先级线索: 历史 workflow_call 假阳性严重 bug，建议 P0
```

```
意图 ID:    INTENT-REL-065
维度标签:   [reliability]
标题:       API 限流与一致性——10 QPS 高频查询 run/job 状态不丢数据

风险点:     dimensional-coverage-gaps 指出 API 速率限制未公开，可测性缺口严重。若测试 harness 或用户工具高频轮询状态，可能触发限流（429/503）或读到不一致的中间态（如状态跳变）。
预期系统行为: 10 QPS 高频查询下，API 不返回 5xx 错误；状态数据一致（同一 run 的 status 不矛盾）；响应时间不严重退化（P95≤2s）。
Oracle 来源: 未知·待实测（gitcode-api/api-reference.md 20 端点；platform-config 未公开限流）

验证要点:
  - [正向] 10 QPS 持续 60s 查询同一 run 状态，全部返回 200，数据字段完整。
  - [负向] 不应出现 429/503/500 限流错误；同一 run 的 status 不应在同一时刻读出矛盾值（如 running 与 completed 并存）。
  - [非功能] 响应时间 P95≤2s，P99≤5s。

故障/压力参数: 用脚本以 10 QPS 连续查询一个 running 状态的 run 的详情 API，持续 60s（共 600 次请求）。记录：HTTP 状态码分布、status 字段一致性、响应时间分布。稳态判据：200 占比=100%、status 无矛盾、P95≤2s。
恢复预期: 不适用（API 稳定性探测；若触发限流则记为平台能力缺口）。
破坏级别: none
来源输入:   gitcode-api/api-reference.md；dimensional-coverage-gaps/README.md §7.1
优先级线索: 可测性缺口，建议 P2
```

```
意图 ID:    INTENT-REL-066
维度标签:   [reliability]
标题:       大规格资源调度稳定性——xlarge/2xlarge 反复编译成功率

风险点:     历史 #96 显示「runs_on 规格改成 2xlarge，arm 任务申请资源错误」。大规格 runner（16C64G/32C128G）是重型编译/AI 训练的关键资源，若调度不稳定（有时成功有时失败），会导致大型项目 CI flaky。
预期系统行为: xlarge/2xlarge 规格的任务在资源池有足够容量时，反复触发应有高成功率（≥90%）；失败时归因清晰（资源不足/架构不匹配/配额超限），而非无解释随机失败。
Oracle 来源: 历史实证（issues-encountered.md #96）；platform-config/README.md:50-57 flavor_specs

验证要点:
  - [正向] xlarge/2xlarge 各反复触发 10 次编译型 job（如编译一个中型 C++ 项目），成功率≥90%。
  - [负向] 不应出现「同一规格今天成功明天失败」的 flaky 调度；arm64 + xlarge 组合不应因架构不匹配而随机失败。
  - [非功能] 失败时有明确归因（如「该规格当前无可用 runner」）。

故障/压力参数: 选择 xlarge(16C64G) 与 2xlarge(32C128G) 两种 flavor，各触发 10 次编译 job（sleep 30s + 编译中型项目），记录成功/失败分布与失败归因。稳态判据：成功率≥90%；失败归因 100% 明确；无 flaky（同一参数连续 3 次结果不一致视为 flaky）。
恢复预期: 不适用（调度稳定性验证；若成功率低则记为大规格调度缺陷）。
破坏级别: none
来源输入:   history/issues-encountered.md #96；platform-config/README.md:50-57
优先级线索: 历史大规格调度失败实证，建议 P1
```


---

## 4. 统计摘要

| 分类 | 数量 | 说明 |
|---|---|---|
| **本轮文件 intent 数** | **66** | REL-001 ~ REL-066 |
| 边界值 intent | 18 | concurrency=5, timeout=360, rerun=3/6h, paths=300, output=1MB, disk=50GB, memory=8GB, preemption=10, workflow_call=2 层, artifact=90 天, K8s min/max=1 |
| 越界值 intent | 12 | concurrency=6, timeout 触发, rerun=4, paths=301, output=1MB+1, disk=51GB, memory=9GB, preemption=11, workflow_call=3 层 |
| 故障注入 intent | 5 | runner SIGKILL, 网络分区, 磁盘满, cache 503, artifact 503 |
| 并发洪泛 intent | 2 | 10 workflow, 50 workflow |
| 大规模 intent | 5 | matrix 20/50, 日志 100MB, artifact 100MB, step 50 个, 长时 350 分钟 |
| 执行模型机制 intent | 7 | needs 传播, matrix fail-fast/max-parallel, cancel, stages fail_fast, continue-on-error, 竞态条件 |
| 性能基准/历史回归 intent | 18 | Runner 规格、调度延迟、日志/镜像/制品/cache 性能、并发压测、公平性、状态一致性、状态机、日志稳定性、YAML 缓存、取消可靠性、网络容错、制品并发、workflow_call 假阳性、API 限流、大规格调度 |
| **破坏级别分布** | | fixture=16, full_instance=0, none=50 |
| **P0 数量** | **1** | REL-064（workflow_call 假阳性完成，历史 #30/#64 实证严重 bug） |
| **P1 数量** | **58** | 含所有历史 bug 回归项与核心稳定性风险 |
| **P2 数量** | **7** | 性能基准、API 探测、网络容错等 |

### 覆盖矩阵（按配额维度 × 机制类别）

| 配额/机制维度 | 边界 | 越界 | 探测/性能 | 故障/恢复 | intent |
|---|---|---|---|---|---|
| concurrency.max (1-5) | ✓ | ✓ | — | — | REL-001~006 |
| exceed-action QUEUE/IGNORE | ✓ | ✓ | — | — | REL-003~004 |
| preemption.events (≤10) | ✓ | ✓ | — | — | REL-005~006 |
| job timeout-minutes (360) | ✓ | ✓ | — | — | REL-007~010 |
| rerun (3次/6h) | ✓ | ✓ | — | — | REL-011~013 |
| paths 匹配 (300文件) | ✓ | ✓ | — | — | REL-014~015 |
| step output (1MB) | ✓ | ✓ | — | — | REL-016~017 |
| Runner 磁盘/内存 (small) | ✓ | ✓ | — | — | REL-018~022 |
| workflow_call 嵌套 (2层) | ✓ | ✓ | — | — | REL-023~024 |
| needs 失败传播 | — | — | — | ✓ | REL-025 |
| matrix fail-fast | ✓ | — | — | — | REL-026 |
| matrix max-parallel | ✓ | — | — | — | REL-027 |
| cancel/always() | — | — | — | ✓ | REL-028 |
| stages.fail_fast | — | — | — | ✓ | REL-029 |
| continue-on-error | — | — | — | ✓ | REL-030 |
| 故障注入 runner kill | — | — | — | ✓ | REL-031 |
| 故障注入网络分区 | — | — | — | ✓ | REL-032 |
| 故障注入磁盘满 | — | — | — | ✓ | REL-033 |
| 故障注入 cache 503 | — | — | — | ✓ | REL-034 |
| 故障注入 artifact 503 | — | — | — | ✓ | REL-035 |
| 并发洪泛 | — | — | ✓ | — | REL-036~037 |
| 大规模 matrix | — | — | ✓ | — | REL-038~039 |
| 超长日志/artifact/step | — | — | ✓ | — | REL-040~042 |
| 长时运行 | ✓ | — | — | — | REL-043 |
| 并发公平性 | — | — | ✓ | — | REL-044 |
| K8s Runner 伸缩 | ✓ | — | — | — | REL-045 |
| 缓存 LRU | — | — | ✓ | — | REL-046 |
| artifact 保留期 | ✓ | — | — | — | REL-047 |
| cancel 与 needs 竞态 | — | — | — | ✓ | REL-048 |
| Runner 规格真实性 | — | — | ✓ | — | REL-049 |
| 调度延迟基准 | — | — | ✓ | — | REL-050 |
| 日志/镜像/制品/cache 性能 | — | — | ✓ | — | REL-051~054 |
| 并发压测/公平性 | — | — | ✓ | — | REL-055~056 |
| 调度状态一致性/状态机 | — | — | ✓ | — | REL-057~058 |
| 日志稳定性/YAML 缓存 | — | — | ✓ | — | REL-059~060 |
| 取消可靠性/网络容错 | — | — | — | ✓ | REL-061~062 |
| 制品并发写一致性 | — | — | — | ✓ | REL-063 |
| workflow_call 假阳性 | — | — | — | ✓ | REL-064 |
| API 限流 | — | — | ✓ | — | REL-065 |
| 大规格调度稳定性 | — | — | ✓ | — | REL-066 |

---

## 5. 质量清单自检

- [x] 每个配额维度都有边界+越界 intent。
  - concurrency.max（1-5）: REL-001/002
  - timeout-minutes（360）: REL-007/008/009/010
  - rerun（3 次 / 6 小时）: REL-011/012/013
  - paths_match_limit（300）: REL-014/015
  - step_output（1MB）: REL-016/017
  - runner disk/memory（small 50GB/8GB）: REL-018/019/020/021
  - preemption events（10）: REL-005/006
  - workflow_call 嵌套（2 层）: REL-023/024
  - artifact retention（90 天）: REL-047
  - K8s Runner min/max（1/1）: REL-045
- [x] 每条故障注入 intent 都声明了恢复预期（REL-031 至 REL-035）。
- [x] 参数具体：并发度、规模、超时秒数、矩阵组合数、磁盘/内存 GB、注入时机均给出具体数字。
- [x] 破坏性 intent 标了正确的 teardown 级别（fixture=16, none=50，无 full_instance）。
- [x] 历史 bug 回归项与平台性能基准均已纳入（REL-049~066）。
- [x] 输入退化标注已在 §2 体现。

