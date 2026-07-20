# Reliability Test Intents

> Agent: reliability | Run: 2026-07-21-01 | Dimensions: [reliability]
> 来源输入: `phase01/inputs/gitcode-spec/` (全量 runner-management + writing-pipelines + core-concepts)、`phase01/inputs/history/issues-encountered.md` (101 条历史缺陷)、`phase01/inputs/github-reference/reference/workflow-syntax.md` (oracle)、`phase01/inputs/existing-cases/cases.md` (629 条去重参照)、`phase01/testing-focus.md` §3/§4/§12
> 输入版本: gitcode-spec fetched 2026-07-20 | history fetched 2026-07-20 | existing-cases generated 2026-07-20

---

## 输入缺失声明

`platform-config/` 目录仅有 README 模板，**无实际配额/上限数值**。以下维度依赖 platform-config 但无法获取具体值：

| 缺失维度 | 影响 | 缓解措施 |
|---------|------|---------|
| max_concurrent_workflows | 并发洪泛 intent 无法设定绝对上限值 | 用行为模式（排队/限流/公平性）替代绝对上限 |
| max_concurrent_jobs_per_workflow | 单 workflow 内并发 job 上限不明 | 用矩阵 max-parallel 间接覆盖 |
| max_matrix_size | 大规模矩阵 exact 边界值不明 | 用中等规模 (16-64 组合) 覆盖展开正确性，已从 history #101 获取实证缺陷 |
| max_log_size / max_artifact_size / max_cache_size | 制品/日志边界值不明 | 仅覆盖行为模式，不覆盖绝对边界 |
| max_secrets_per_repo | 非本维度核心关注 | 不覆盖 |

所有边界 intent 若需「超出上限」判定，显式标注「无法精确定义越界值——依赖未提供的 platform-config」。

---

## 1. 并发控制边界与越界

### INTENT-REL-001
```
意图 ID:    INTENT-REL-001
维度标签:   [reliability]
标题:       concurrency.max=1 时同一 workflow 连续触发 5 次，仅 1 个 Running，其余按 exceed-action 处理

风险点:     并发控制是防止 Runner 池耗尽的屏障。若 exceed-action 不生效（QUEUE 变并发执行 / IGNORE 不丢弃），可能导致资源过载或触发丢失。
预期系统行为: 当 max=1 且 exceed-action=QUEUE 时，5 次触发中 1 个 Running，其余 4 个按 FIFO 排队；exceed-action=IGNORE 时，1 个 Running，其余 4 个被忽略并产生明确状态标记。
Oracle 来源: GitCode 规格（workflow-file-location-structure.md concurrency 字段: max 范围 1-5; exceed-action=QUEUE/IGNORE）

验证要点:
  - [正向] 同一时刻 Running 数严格 ≤ max
  - [正向] QUEUE 模式: 排队 Run 在前一个完成后自动调度，run_number 连续
  - [正向] IGNORE 模式: 被忽略的 Run 有明确状态标记
  - [负向] 无「排队中 Run 被静默丢弃」

场景/参数: max=1, exceed-action=QUEUE / IGNORE, 5 次 push 触发（间隔 2s）
稳态判据: Running 数始终 ≤ 1，排队 Run 在 5min 内被调度
恢复预期: N/A（非破坏性）
破坏级别: none
优先级线索: RISK-REL-01
来源输入: gitcode-spec/writing-pipelines/workflow-file-location-structure.md (concurrency); history #10 (停止指定 record 不管用)
关联已有用例: TC-289 (concurrency.max), TC-290 (concurrency.enable), TC-293 (concurrency.exceed-action)
```

### INTENT-REL-002
```
意图 ID:    INTENT-REL-002
维度标签:   [reliability]
标题:       concurrency.max 越界值（max=0 / max=6 / max=100）被正确拒绝

风险点:     GitCode spec 声明 max 范围 1-5。越界值若被静默接受可能导致非预期的并发行为（0=死锁/永不执行，超上限=资源耗尽）。
预期系统行为: max=0、max=6、max=100 在 YAML 解析阶段报错，workflow 无法保存/触发。
Oracle 来源: GitCode 规格（max 范围 1-5）

验证要点:
  - [正向] max=0 报错：并发数不能为 0
  - [正向] max=6 报错：超过上限 5
  - [正向] max=100 报错：超过上限 5

场景/参数: max ∈ {0, 6, 100}
稳态判据: YAML 保存/触发阶段明确报错，workflow 未进入排队
恢复预期: N/A（配置校验，非破坏性）
破坏级别: none
优先级线索: RISK-REL-01
来源输入: gitcode-spec/writing-pipelines/workflow-file-location-structure.md
```

### INTENT-REL-003
```
意图 ID:    INTENT-REL-003
维度标签:   [reliability]
标题:       concurrency.exceed-action 非法值被拒绝

风险点:     exceed-action 仅支持 IGNORE/QUEUE。非法值若被静默接受会致并发控制策略不可预测。
预期系统行为: 非法值（如 CANCEL、INVALID）应被 YAML 校验拒绝。
Oracle 来源: GitCode 规格（exceed-action 枚举）

验证要点:
  - [正向] exceed-action=CANCEL 报错（仅 IGNORE/QUEUE 合法）
  - [正向] exceed-action="" 报错（不能为空）

场景/参数: exceed-action ∈ {CANCEL, ""}
稳态判据: YAML 保存/触发阶段明确报错
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/workflow-file-location-structure.md
```

### INTENT-REL-004
```
意图 ID:    INTENT-REL-004
维度标签:   [reliability]
标题:       concurrency.max=5 满载时，第 6 次触发按 exceed-action=QUEUE 排队，观察是否超时排队或被丢弃

风险点:     当并发满载 + 排队队列过长时，新触发是否 (a) 无限排队、(b) 超时失败、(c) 被静默丢弃。历史 #7/#12 报告 job 持续等待/排队，重试也无解。
预期系统行为: 排队 Run 最终被调度执行或明确标记为取消。不应无限排队或静默丢弃。
Oracle 来源: GitCode 规格 + history #7（3 并行 job、2 runner 空闲、1h 后失败仅 1 行日志）、history #12（持续等待、重试无效、资源池已释放）

验证要点:
  - [正向] 所有排队 Run 最终进入终态（success/failure/cancelled），不超过 timeout-minutes
  - [正向] 排队 Run 的 run_number 连续不跳号
  - [负向] 排队超过 10min 的 Run 应有状态说明（不应仅显示 'queued' 无下文）
  - [负向] 排队 Run 不应在 Runner 空闲时仍不被调度

场景/参数: max=5, exceed-action=QUEUE, 8 次触发（5 running + 3 queued）
稳态判据: 8 个 Run 全部进入终态，无静默丢弃
恢复预期: N/A
破坏级别: none
优先级线索: RISK-REL-01 + history #7/#12
来源输入: gitcode-spec + history/issues-encountered.md (#7, #12)
```

---

## 2. 矩阵策略边界与竞态

### INTENT-REL-005
```
意图 ID:    INTENT-REL-005
维度标签:   [reliability]
标题:       fail-fast=true 时，矩阵中 1 个 job 失败后立即取消其余未完成实例

风险点:     fail-fast 是矩阵的最基础稳定性机制。若失效，矩阵中一个实例失败后其他实例白白消耗资源直到完成。
预期系统行为: 第 1 个 job 实例失败后，所有仍在 queued/in_progress 的实例在 30s 内被标记为 cancelled。
Oracle 来源: GitCode 规格（configure-matrix-builds.md: fail-fast: true）

验证要点:
  - [正向] 失败实例发生 30s 内，其余未完成的矩阵实例状态变为 cancelled
  - [正向] 已完成（success）的实例不受影响
  - [负向] 无 cancelled 实例被错误标记为 failure

场景/参数: matrix: os=[ubuntu-latest], retcode=[0,0,1,0,0]（5 个实例，第 3 个故意 exit 1），fail-fast=true
稳态判据: 第 3 个失败后 30s 内，其余 running 实例全部 cancelled
恢复预期: N/A
破坏级别: none
优先级线索: RISK-REL-01
来源输入: gitcode-spec/writing-pipelines/configure-matrix-builds.md
关联已有用例: TC-277 (strategy.fail-fast), TC-329 (fail-fast:false)
```

### INTENT-REL-006
```
意图 ID:    INTENT-REL-006
维度标签:   [reliability]
标题:       fail-fast=false 时，矩阵中 1 个 job 失败后其余实例继续执行至完成

风险点:     fail-fast=false 与 =true 语义相反。若实现错误（误触发 fail-fast），将中断不应中断的并行测试。
预期系统行为: 某个矩阵实例失败后，其余实例继续执行直到各自完成，不触发取消。
Oracle 来源: GitCode 规格（fail-fast: false）

验证要点:
  - [正向] 失败实例发生后，其余实例继续执行并各自产生 success/failure 结果
  - [负向] 其余实例的状态不应为 cancelled

场景/参数: matrix: os=[ubuntu-latest], retcode=[0,0,1,0,0]（5 个实例），fail-fast=false
稳态判据: 5 个实例全部完成，2 个 success + 1 个 failure（非 cancelled），其余 success
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-matrix-builds.md
关联已有用例: TC-329 (fail-fast:false)
```

### INTENT-REL-007
```
意图 ID:    INTENT-REL-007
维度标签:   [reliability]
标题:       max-parallel=2 时，5 实例矩阵任意时刻并发数 ≤ 2

风险点:     max-parallel 限制防止矩阵瞬时占满所有 Runner。若失效，大矩阵会导致其他 workflow 饥饿。
预期系统行为: 任意时刻 Running 的矩阵实例数 ≤ max-parallel=2，其余排队。
Oracle 来源: GitCode 规格（configure-matrix-builds.md: max-parallel）

验证要点:
  - [正向] 通过 run API 轮询，任意时刻 ≥ 2 个实例同时 running
  - [负向] 任意时刻从未出现 > 2 个实例同时 running

场景/参数: matrix: os=[ubuntu-latest], task=[1,2,3,4,5]，max-parallel=2，每个 task sleep 30s
稳态判据: 轮询采样全程，concurrent_running ≤ 2
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-matrix-builds.md
关联已有用例: TC-278 (strategy.max-parallel), TC-330 (max-parallel:3)
```

### INTENT-REL-008
```
意图 ID:    INTENT-REL-008
维度标签:   [reliability]
标题:       needs 指向 matrix job 后非 matrix job 能正确解析依赖——针对已知缺陷 #101 的回归

风险点:     history #101 明确记录: 「jobA needs matrix jobB, jobB 成功但 jobA 仍然初始化失败」。这是已被实证的稳定性缺陷，需要显式回归验证。
预期系统行为: matrix job 的所有实例完成后，needs 该 matrix job 的下游 job 应正常启动并执行。
Oracle 来源: history #101 + GitHub Actions 语义（needs 以 job 名为粒度，对应整组 matrix）

验证要点:
  - [正向] matrix job（如 test）所有实例 success 后，下游 job deploy 启动并执行成功
  - [负向] deploy 不出现「任务初始化错误」
  - [非功能] deploy 日志中引用 `needs.test.result` 应返回 'success'

场景/参数: matrix job test（3 实例: node=[18,20,22]）+ job deploy（needs: test）
稳态判据: deploy 正常执行并 success
恢复预期: N/A
破坏级别: none
优先级线索: history #101
来源输入: history/issues-encountered.md (#101: matrix needs 依赖bug)
关联已有用例: TC-486/481/499 (needs 指向 matrix 父 job 导致初始化错误)
```

### INTENT-REL-009
```
意图 ID:    INTENT-REL-009
维度标签:   [reliability]
标题:       大矩阵（64 实例，8×8）正确展开且全部实例可追踪

风险点:     大矩阵展开失败（部分实例丢失、编号跳号）、或因资源不足导致部分实例永久 pending。history #101 暴露 matrix needs 解析错误，大矩阵放大了此类风险。
预期系统行为: 64 个矩阵实例全部在 Run 列表中可枚举，每个实例有独立状态，最终全部完成。
Oracle 来源: GitCode 规格 + GitHub Actions 语义

验证要点:
  - [正向] Run 列表显示 64 个 matrix 子 job
  - [正向] 所有 64 个实例最终进入 success/failure 终态
  - [负向] 无「缺失实例」（matrix 组合有对应 job 但未创建）
  - [非功能] 展开到第一个实例 running 的时间 ≤ 120s

场景/参数: matrix: size=[1..8] × variant=[1..8]，每个实例 sleep 5s + echo
稳态判据: 全部 64 实例终态 = success
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec + history #101
```

### INTENT-REL-010
```
意图 ID:    INTENT-REL-010
维度标签:   [reliability]
标题:       matrix include 追加组合后展开正确，不破坏原始矩阵

风险点:     include 追加组合若与原始组合重复导致重复实例或冲突。GitCode spec 未明确 include 重复时的去重行为。
预期系统行为: include 追加 2 个额外组合后，矩阵总实例 = 原始组合数 + 2（无重复），每个实例有独立 `matrix.*` 上下文。
Oracle 来源: GitCode 规格（configure-matrix-builds.md: include）+ GitHub Actions 语义

验证要点:
  - [正向] 实例总数 = N + 2
  - [正向] include 追加的实例的 matrix.extra 上下文正常可读
  - [负向] 无因为 include 产生的重复实例

场景/参数: matrix: os=[ubuntu-latest,windows-latest], node=[18,20] (4 实例) + include: [{os: macos-latest, node:20}, {os: ubuntu-latest, node:22}]
稳态判据: 6 个实例全部 success
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-matrix-builds.md
关联已有用例: TC-327 (matrix include)
```

### INTENT-REL-011
```
意图 ID:    INTENT-REL-011
维度标签:   [reliability]
标题:       matrix exclude 正确排除组合，且被排除组合不生成实例

风险点:     exclude 若部分生效（排除不完整），会生成预期之外的实例，浪费资源且混淆结果。
预期系统行为: 被 exclude 的组合无对应 job 实例产生。
Oracle 来源: GitCode 规格（configure-matrix-builds.md: exclude）

验证要点:
  - [正向] 实例总数 = 原始组合数 - 排除数
  - [负向] 被排除组合的 job 实例不存在于 Run 列表中

场景/参数: matrix: os=[ubuntu-latest,windows-latest], node=[18,20] (4) + exclude: [{os: windows-latest, node:18}]
稳态判据: 3 个实例 success，无 windows-latest+node18 实例
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-matrix-builds.md
关联已有用例: TC-328 (matrix exclude)
```

---

## 3. 故障注入：Runner 层

### INTENT-REL-012
```
意图 ID:    INTENT-REL-012
维度标签:   [reliability]
标题:       job 执行中被 kill runner 后，Run 状态正确标记为 failure 而非 hanging

风险点:     runner 被 kill 后，若调度器未感知（心跳超时），Run 可能永久显示 in_progress，阻塞后续排队 job。history #78 报告「runner 显示运行中但无任务执行，流水线一直转圈」。
预期系统行为: runner 失联后，调度器在心跳超时窗口内（建议 ≤5min）将 Run 标记为 failure，释放资源给后续排队 job。
Oracle 来源: GitHub Actions 语义（job failure on runner disconnect）+ history #78

验证要点:
  - [正向] runner kill 后 ≤5min Run 状态变为 failure
  - [正向] 被释放的 runner slot 可被排队中的下一个 job 使用
  - [负向] Run 状态不永久停留在 in_progress/queued
  - [非功能] Run 日志中应有「runner disconnected」或等价提示

场景/参数: 1 个 job running (sleep 600s)，kill runner 进程（SIGKILL），观察 Run 状态变化
稳态判据: Run 在 5min 内变为 failure，后续排队 job 被正常调度
恢复预期: runner kill → Run 标记 failure + 资源释放 + 新 job 正常调度
破坏级别: full_instance
优先级线索: history #78 (#55: 全量完成但状态一直显示运行中)
来源输入: history/issues-encountered.md (#78, #55, #39)
```

### INTENT-REL-013
```
意图 ID:    INTENT-REL-013
维度标签:   [reliability]
标题:       job 执行中网络分区（封禁外网出站）后，step 应超时失败而非永久 hang

风险点:     若 step 依赖外网（如 npm install），网络突然断开后 step 可能永久 hang，直到 job timeout 才终止（最长 360min）。history #65 报告「无法连外网下载三方件」。
预期系统行为: 依赖网络的 step（如下载依赖）在网络不可用时应在合理时间内（< 5min）超时失败，而非无限等待。
Oracle 来源: GitHub Actions 语义（网络不可用应导致连接超时而非 hang）

验证要点:
  - [正向] step 在 5min 内因网络错误失败（exit code ≠ 0）
  - [负向] step 不 hang 超过 job timeout-minutes
  - [非功能] 日志应包含可辨识的网络错误信息（如 'could not resolve host' / 'connection refused'）

场景/参数: job 含 `apt-get update && apt-get install -y curl` + `curl https://registry.npmjs.org`；step 开始后 30s 封禁 runner 外网出站
稳态判据: step 在 5min 内 failed，日志含网络错误
恢复预期: step→failed, Run→failure, post 清理钩子仍需执行
破坏级别: fixture
优先级线索: history #65 (#42: 自定义资源池偶现网络问题)
来源输入: history/issues-encountered.md (#65, #42); testing-focus.md §4 网络出站策略
```

### INTENT-REL-014
```
意图 ID:    INTENT-REL-014
维度标签:   [reliability]
标题:       job 执行中磁盘写满后，step 应失败并有明确日志，不静默 hang

风险点:     disk full 时写入操作静默失败或 hang，日志无明确提示，排查困难。
预期系统行为: step 因磁盘满失败，日志含 'No space left on device' 或等价信息，Run 状态 = failure。
Oracle 来源: GitHub Actions 语义 + Linux 文件系统行为

验证要点:
  - [正向] Run 状态 = failure
  - [正向] 日志含磁盘满错误（ENOSPC / 'No space left on device'）
  - [负向] job 不永久 hang 在 writing 操作

场景/参数: step 执行 `dd if=/dev/zero of=/tmp/bigfile bs=1M count=10000` 填满磁盘后触发后续写操作，timeout-minutes=10
稳态判据: Run failure，日志含 'No space left'
恢复预期: job 失败 → post 清理阶段执行（若配置）→ runner 回收重置
破坏级别: fixture
来源输入: testing-focus.md §4 资源边界
```

### INTENT-REL-015
```
意图 ID:    INTENT-REL-015
维度标签:   [reliability]
标题:       CPU 饱和下 job 仍能推进，不会被 OOM killer 误杀

风险点:     runner 在 CPU 100% 下若调度器心跳超时可能被误判为 dead 而 kill。history #91 报告「codearts 资源池资源请求错误」。
预期系统行为: CPU 100% 负载下 job 继续执行（慢但推进），不被系统误 kill。
Oracle 来源: GitHub Actions 语义 + testing-focus.md §4

验证要点:
  - [正向] job 在 timeout-minutes 内完成（虽慢但 execute through）
  - [负向] job 不因 CPU 饱和被系统 kill (status ≠ cancelled/failure due to OOM)
  - [非功能] 日志持续写入（证明 liveness）

场景/参数: step 执行 `stress --cpu 4 --timeout 120s`（CPU 满载 2min），后续执行普通 step；timeout-minutes=10
稳态判据: 所有 step 完成，Run = success
恢复预期: N/A（非破坏，仅施压）
破坏级别: none
来源输入: testing-focus.md §4; history #91
```

### INTENT-REL-016
```
意图 ID:    INTENT-REL-016
维度标签:   [reliability]
标题:       自托管 runner 重启后自动恢复注册（「重启免注册」承诺验证）

风险点:     GitCode 声称自托管 runner 支持「重启免注册」（host 重启后 runner 自动恢复注册态）。若失效，每次 host 重启需人工重新注册。history #78 暗示 runner 状态管理不可靠。
预期系统行为: runner host 重启后，runner 服务自动恢复在线状态，无需人工介入。
Oracle 来源: GitCode 规格（using-self-hosted-runners.md: 「重启免注册」）

验证要点:
  - [正向] 主机重启后 5min 内 runner 状态恢复为在线
  - [正向] 恢复后触发的新 workflow 可调度到该 runner 并执行

场景/参数: 自托管主机 runner 在线 → 重启主机 → 等待 5min → 触发 workflow 验证调度
稳态判据: runner 恢复在线 + 新 workflow 分配到该 runner + 成功执行
恢复预期: 主机重启 → runner 自动恢复 → 可接受新 job
破坏级别: fixture
优先级线索: history #78, #54
来源输入: gitcode-spec/runner-management/using-self-hosted-runners.md
```

### INTENT-REL-017
```
意图 ID:    INTENT-REL-017
维度标签:   [reliability]
标题:       K8s runner 弹性伸缩：从 min=1 触发到 max=5 扩展，Pod 实例正确创建并回收

风险点:     K8s runner 弹性伸缩若失效（不扩展 / 不回收），可能导致高峰资源不足或长期占用集群资源。
预期系统行为: 并发任务数超过当前 Pod 数时，自动扩展至 max；空闲后缩回 min。
Oracle 来源: GitCode 规格（using-self-hosted-runners.md: 弹性伸缩）

验证要点:
  - [正向] 5 个 job 并发触发后，Pod 实例扩展至 5
  - [正向] 所有 job 完成后空闲 5min，Pod 缩回 min=1
  - [负向] 无 Pod 在空闲后长期残留

场景/参数: K8s runner, min=1, max=5, 5 job 并发触发
稳态判据: Pod 在 3min 内扩展至 5 → job 完成 → Pod 在 5min 内缩回 1
恢复预期: 弹性伸缩正确 → 资源回收
破坏级别: fixture
来源输入: gitcode-spec/runner-management/using-self-hosted-runners.md
```

### INTENT-REL-018
```
意图 ID:    INTENT-REL-018
维度标签:   [reliability]
标题:       K8s runner Pod 被意外删除后，调度器应感知失败并标记 Run failure

风险点:     K8s 环境下 Pod 可能因节点驱逐/资源不足被意外删除。若调度器不感知，Run 永久 hanging。
预期系统行为: Pod 被删除后，调度器在心跳超时内感知并将 Run 标记为 failure。
Oracle 来源: GitHub Actions 语义（runner disconnect → job failure）

验证要点:
  - [正向] Pod 删除后 5min 内 Run 状态变为 failure
  - [负向] Run 不永久停留在 in_progress

场景/参数: K8s runner job 执行中 `kubectl delete pod <runner-pod>`，timeout-minutes=30
稳态判据: Run failure 在 5min 内
恢复预期: Pod 删除 → Run failure → 资源释放
破坏级别: full_instance
来源输入: gitcode-spec + testing-focus.md §4
```

---

## 4. 故障注入：调度与依赖层

### INTENT-REL-019
```
意图 ID:    INTENT-REL-019
维度标签:   [reliability]
标题:       needs 依赖链中前序 job 失败时，后续 job 正确跳过（不执行、不卡死）

风险点:     若失败传播逻辑错误，后续 job 可能 (a) 仍执行且不可预期、(b) 卡在 waiting 状态。history #101 报告 matrix needs 初始化错误，普通 job needs 也需验证。
预期系统行为: 前序 job failure → 依赖它的 job 状态 = skipped，不消耗 Runner 资源。
Oracle 来源: GitHub Actions 语义（failure 传播）

验证要点:
  - [正向] 依赖 job 状态 = skipped
  - [负向] 依赖 job 不进入 queued/in_progress
  - [负向] 依赖 job 不错误执行

场景/参数: job-A (exit 1) → job-B (needs: job-A), job-C (needs: job-A)
稳态判据: job-A=failure, job-B=skipped, job-C=skipped
恢复预期: N/A（正常语义验证）
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-dependencies-order.md; history #101
```

### INTENT-REL-020
```
意图 ID:    INTENT-REL-020
维度标签:   [reliability]
标题:       needs 指向不存在/未定义的 job 时，workflow 应解析阶段报错

风险点:     needs 引用不存在的 job 名（拼写错误 / 被删除）若被静默接受，workflow 会在运行时 bug。
预期系统行为: 解析阶段就报错，workflow 不进入排队。
Oracle 来源: GitHub Actions 语义

验证要点:
  - [正向] 触发后立即 failed/parse error，不进入排队

场景/参数: job-A (needs: nonexistent_job)
稳态判据: 触发后 Run 直接 failed，错误信息含 job 名
恢复预期: N/A
破坏级别: none
来源输入: GitHub reference/workflow-syntax.md
```

### INTENT-REL-021
```
意图 ID:    INTENT-REL-021
维度标签:   [reliability]
标题:       手动取消正在运行的 job 后，Run 状态即时变为 cancelled，资源立即释放

风险点:     若取消操作有延迟或无效，用户以为取消了但 job 仍在秘密执行（可能产生副作用）。history #10: 「停止指定 record 时不管用，总是以出栈方式停止最上面的」。history #39: 「取消成功但任务运行状态仍是队列中」。
预期系统行为: 取消操作 30s 内 Run 状态变为 cancelled，job 停止执行，Runner 资源释放。
Oracle 来源: GitHub Actions 语义 + GitCode 规格

验证要点:
  - [正向] 取消 30s 内 Run 状态 = cancelled
  - [正向] 依赖被取消 job 的下游 job 状态 = cancelled/skipped
  - [负向] 被取消 job 的 step 不再产生日志
  - [非功能] 取消后原 Runner slot 可被新 job 使用

场景/参数: job running (sleep 300s)，运行 30s 后手动取消；同时有 job-B (needs: job-A)
稳态判据: Run cancelled, 30s 内 Runner 释放
恢复预期: 取消→资源释放，系统可接受新 workflow
破坏级别: none
优先级线索: history #10, #39
来源输入: history/issues-encountered.md (#10, #39)
关联已有用例: TC-321 (if:cancelled)
```

### INTENT-REL-022
```
意图 ID:    INTENT-REL-022
维度标签:   [reliability]
标题:       抢占（preemption）: 第 2 次触发抢占第 1 次，第 1 次被 cancel 且第 2 次执行

风险点:     preemption 是 GitCode 独有的并发特性。若抢占逻辑错误，可能 (a) 旧 job 未取消导致并发超限、(b) 新 job 未获得资源。preemption.events 字段需明确生效。
预期系统行为: 第 2 次触发（同 preemption events 匹配）抢占第 1 次: 第 1 次 cancel → 第 2 次 running。
Oracle 来源: GitCode 规格（workflow-file-location-structure.md: preemption.enable/events）

验证要点:
  - [正向] 操作完成后，第 1 次 Run = cancelled，第 2 次 Run = success/running
  - [正向] 被抢占的 Run 日志中记录 preempted 原因
  - [负向] 不出现两 Run 同时 running

场景/参数: concurrency.max=1, preemption.enable=true, preemption.events=[mr_id]; 触发 run1 → 30s 后 同 mr_id 触发 run2
稳态判据: run1=cancelled, run2=running
恢复预期: N/A（正常抢占）
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/workflow-file-location-structure.md
关联已有用例: TC-291 (concurrency.preemption.enable), TC-292 (concurrency.preemption.events)
```

---

## 5. 超时与长时间运行

### INTENT-REL-023
```
意图 ID:    INTENT-REL-023
维度标签:   [reliability]
标题:       job timeout-minutes=5 精确触发，job 在恰好 5min 时被强制终止

风险点:     timeout 不精确时，job 可能提前被 kill（误杀）或延后（白白等待）。
预期系统行为: job 在 timeout-minutes ± 30s 内被终止，Run = failure 或 cancelled。
Oracle 来源: GitCode 规格（configure-jobs.md: timeout-minutes 默认 360min）

验证要点:
  - [正向] Run 在 timeout-minutes + 30s 内进入终态
  - [正向] 日志显示 timeout 原因

场景/参数: timeout-minutes=2, step: `sleep 300`
稳态判据: Run 在 120s±30s 内 failure
恢复预期: job timeout → Run failure → 资源释放
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-jobs.md
关联已有用例: TC-270 (jobs.<id>.timeout-minutes)
```

### INTENT-REL-024
```
意图 ID:    INTENT-REL-024
维度标签:   [reliability]
标题:       step timeout-minutes 小于 job timeout-minutes 时，step 超时不影响其他 step

风险点:     step 级 timeout 与 job 级 timeout 的交互需明确: step 超时后是否继续执行后续 step，job 整体是否算失败。
预期系统行为: step 超时后该 step failed，但 job 继续执行后续 step（若 continue-on-error=true 或 step 失败不阻断）。
Oracle 来源: GitHub Actions 语义（step 超时 → step failure, 后续 step 由 if 条件决定）

验证要点:
  - [正向] step-A 超时后 step-B 仍执行
  - [正向] job 最终状态由 step 失败 + continue-on-error 综合决定

场景/参数: step-A (timeout-minutes=1, sleep 120) → step-B (echo done)
稳态判据: step-A failure, step-B success
恢复预期: N/A
破坏级别: none
来源输入: GitHub reference/workflow-syntax.md (jobs.<job_id>.steps[*].timeout-minutes)
```

### INTENT-REL-025
```
意图 ID:    INTENT-REL-025
维度标签:   [reliability]
标题:       长时间 job（接近 timeout）执行中日志持续产生，不因时长而截断

风险点:     长运行 job 的日志可能因缓冲/截断等问题不完整。history #14: 「日志加载时间过长，约 7min 才能完全加载好」。
预期系统行为: 日志完整包含所有 step 输出，无截断、无乱序。
Oracle 来源: GitCode 规格 + history #14, #80, #81

验证要点:
  - [正向] 日志包含所有 30 轮循环的输出（每 10s 一次，共 300s）
  - [正向] 日志行顺序与执行顺序一致
  - [负向] 无日志跳行/缺失（行号连续）

场景/参数: step: `for i in $(seq 1 30); do echo "round $i at $(date)"; sleep 10; done`
稳态判据: 日志完整 30 轮，行号递增
恢复预期: N/A
破坏级别: none
优先级线索: history #14, #80, #81
来源输入: history/issues-encountered.md (#14, #80, #81)
```

---

## 6. 自托管 Runner 资源调度

### INTENT-REL-026
```
意图 ID:    INTENT-REL-026
维度标签:   [reliability]
标题:       自托管 runner + 自定义 image 模式：镜像拉取超时应有明确错误而非 pending 1h 后静默失败

风险点:     history #7/#52/#54: 自定义 runner+image 模式下，job 显示 pending/排队中长达 1h 后失败，日志仅 1 行，完全无法排查。history #70: 「拉镜像时间过长超过默认环境准备时间」。
预期系统行为: 镜像拉取超时时应在合理时间内（10min 内）明确报错: 「image pull timeout」+ 镜像名。不应 pending 1h 才失败。
Oracle 来源: history #7, #52, #54, #70

验证要点:
  - [正向] 镜像拉取失败/超时时 10min 内 Run failed
  - [正向] 日志含镜像拉取错误信息（镜像名 + 失败原因）
  - [负向] 日志不只有 1 行
  - [负向] job 不长期停留在 pending/queued 状态

场景/参数: self-hosted runner, container.image=nonexistent-registry.example.com/nonexistent:99
稳态判据: 10min 内 Run failed，日志含 image pull 错误
恢复预期: Run failure → 资源释放
破坏级别: fixture
优先级线索: history #7, #52, #54, #70
来源输入: history/issues-encountered.md (#7, #52, #54, #70); gitcode-spec/runner-management/configuring-images-toolchains.md
```

### INTENT-REL-027
```
意图 ID:    INTENT-REL-027
维度标签:   [reliability]
标题:       自托管 runner + 自定义 image + 异地镜像仓库：资源充足但拉取不到镜像时不应静默 hang

风险点:     history #54: 「自有资源池+自定义容器镜像，资源空闲但一直拉取不到资源，无日志无报错」。这是一种「资源实际空闲但调度器认为忙」的不一致状态。
预期系统行为: 调度失败时应产生明确错误日志，不应「无日志无报错」。
Oracle 来源: history #54

验证要点:
  - [正向] 终态时日志含失败原因
  - [负向] 日志不为空（至少一行错误信息）

场景/参数: self-hosted runner + container.image=blocked-registry.example.com/image:latest（模拟不可达镜像仓库）
稳态判据: Run failed，日志含错误信息
恢复预期: Run failure → 资源释放
破坏级别: fixture
优先级线索: history #54
来源输入: history/issues-encountered.md (#54, #89)
```

### INTENT-REL-028
```
意图 ID:    INTENT-REL-028
维度标签:   [reliability]
标题:       K8s runner 架构不匹配：runs-on 指定 arm64 但集群只有 x64 节点时，job 应失败而非调度到错误架构

风险点:     history #48: 「kubernetes-Runner 会被调度到 arm 节点上（但不应调度到 arm）」——架构匹配错误。history #96: 「2xlarge 规格 arm job 资源请求错误」。
预期系统行为: 无匹配 runner 时，job 状态 = queued/waiting 并有「no matching runner」提示，而非调度到错误架构的节点。
Oracle 来源: history #48, #96 + GitCode 规格（标签全匹配规则）

验证要点:
  - [负向] job 不应在 arm64 节点上执行（若 runs-on 指定 x64）
  - [正向] 无匹配 runner 时，job 在 reasonable time 内明确报告 no matching runner

场景/参数: K8s runner (仅 x64 节点), runs-on=[self-hosted, arm64, medium]
稳态判据: job 状态为 queued/failed，不错误在 x64 节点执行
恢复预期: N/A
破坏级别: fixture
优先级线索: history #48, #96
来源输入: history/issues-encountered.md (#48, #96)
```

### INTENT-REL-029
```
意图 ID:    INTENT-REL-029
维度标签:   [reliability]
标题:       自托管 runner 在组织级注册后，授权项目可正确调度使用

风险点:     history #37: 「组织下定义了 runner 分组，给代码仓加了权限但代码仓无法使用 runner，调度会失败」。组织级 Runner 权限传播不可靠。
预期系统行为: 组织级 runner 授权给项目后，项目 workflow 可调度到该 runner。
Oracle 来源: GitCode 规格（using-self-hosted-runners.md: 组织级 vs 项目级）+ history #37

验证要点:
  - [正向] 授权项目触发 workflow 后 job 在组织 runner 上执行
  - [负向] 未授权项目无法使用组织 runner

场景/参数: 组织级 runner → 授权项目 A → 项目 A 触发 workflow (runs-on 指向该 runner group)
稳态判据: job 正常执行 success
恢复预期: N/A
破坏级别: fixture
优先级线索: history #37
来源输入: gitcode-spec/runner-management/using-self-hosted-runners.md; history #37
```

---

## 7. 缓存与制品稳定性

### INTENT-REL-030
```
意图 ID:    INTENT-REL-030
维度标签:   [reliability]
标题:       cache 跨 workflow run 可用：第 2 次 run 命中缓存 (cache hit)，第 2 次明显快于第 1 次

风险点:     cache 命中失败导致每次 run 都重复下载依赖，严重影响 CI 效率。history #90: 「cache 插件找不到」。
预期系统行为: 相同 cache key 下，第 2 次 run cache hit 并跳过下载步骤。
Oracle 来源: GitCode 规格（artifacts-and-cache.md: cache 跨运行保留）

验证要点:
  - [正向] 第 1 次 run 输出 cache miss 信息
  - [正向] 第 2 次 run 日志显示 cache hit
  - [非功能] 第 2 次 run 耗时 < 第 1 次 run 耗时的 50%

场景/参数: 2 次 push 触发同一 workflow，step 使用 official_cache（key 基于 hashFiles）
稳态判据: 第 2 次 cache hit + 整体耗时明显缩短
恢复预期: N/A
破坏级别: none
优先级线索: history #90
来源输入: gitcode-spec/core-concepts/artifacts-and-cache.md; history #90
关联已有用例: gitcode-actions-list.md (official_cache)
```

### INTENT-REL-031
```
意图 ID:    INTENT-REL-031
维度标签:   [reliability]
标题:       artifact 跨 job 传递：job-A upload → job-B download，文件完整且内容一致

风险点:     artifact 传递是 job 间通信的核心机制。若失效，后续 job 拿到损坏/不完整的制品。history #16: 「obs 上传插件不支持按照目录上传，目录为变量则无法解析」。
预期系统行为: job-B download 的 artifact 与 job-A upload 的文件完全一致（sha256 校验）。
Oracle 来源: GitCode 规格（artifacts-and-cache.md: 跨 Job 传递）

验证要点:
  - [正向] job-B 下载文件存在且 sha256 匹配
  - [负向] 文件大小与原始一致（无截断）

场景/参数: job-A: `dd if=/dev/urandom of=test.bin bs=1K count=100` + upload; job-B (needs: job-A): download + sha256sum 校验
稳态判据: download 文件 sha256 = upload 文件 sha256
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/core-concepts/artifacts-and-cache.md; history #16
关联已有用例: gitcode-actions-list.md (official_upload_artifact / official_download_artifact)
```

### INTENT-REL-032
```
意图 ID:    INTENT-REL-032
维度标签:   [reliability]
标题:       下载不存在的 artifact 时明确报错而非静默产生空文件

风险点:     若 artifact 名拼写错误或已过期，download 静默成功（空目录）会导致后续 step 在错误数据上运行。
预期系统行为: download nonexitent artifact → step failed + 日志含 'not found' 或等价信息。
Oracle 来源: GitHub Actions 语义

验证要点:
  - [正向] step failed（exit code ≠ 0）
  - [正向] 日志含 artifact 名 + 'not found'

场景/参数: download-artifact name=nonexistent-artifact-2026
稳态判据: step failed + 日志含 not found
恢复预期: N/A
破坏级别: none
来源输入: GitHub reference (actions/download-artifact behavior)
```

---

## 8. schedule 触发可靠性

### INTENT-REL-033
```
意图 ID:    INTENT-REL-033
维度标签:   [reliability]
标题:       schedule cron 触发在配置后首个匹配时间点生效

风险点:     history 批量报告: S3 × 24 + TC-391: 「Scheduler 不工作：两个仓库、多次 cron 配置，从未产生 Schedule Run」。这是已知的严重缺陷。
预期系统行为: 配置有效 cron 后，在匹配时间点 ≤5min 延迟内触发 Run。
Oracle 来源: GitCode 规格（configure-triggers.md: 「可能存在数分钟的调度延迟」）

验证要点:
  - [正向] 至少产生 1 个由 schedule 触发的 Run
  - [正向] Run.event = schedule
  - [非功能] 触发时间与 cron 时间偏差 ≤ 5min

场景/参数: cron='*/15 * * * *'（每 15min 触发）
稳态判据: 在 cron 匹配时间 5min 内产生 schedule Run
恢复预期: N/A（需 scheduler 正常）
破坏级别: none
优先级线索: history S3×24+TC-391
来源输入: gitcode-spec/writing-pipelines/configure-triggers.md; history/issues-encountered.md (S3×24+TC-391)
关联已有用例: TC-237, TC-427-430, S3×24
```

### INTENT-REL-034
```
意图 ID:    INTENT-REL-034
维度标签:   [reliability]
标题:       schedule 仅在默认分支生效，非默认分支的 schedule 配置不触发

风险点:     GitCode spec 声明 schedule 仅在默认分支生效。若平台无此限制（多分支同时触发），可能导致意外的并发高峰。
预期系统行为: 非默认分支上的 schedule 配置不产生 Run；仅默认分支触发。
Oracle 来源: GitCode 规格（configure-triggers.md）

验证要点:
  - [正向] feature-branch 上的 schedule 配置不触发 Run
  - [正向] main 上的 schedule 配置触发 Run

场景/参数: main + feature/schedule-test 各有相同 schedule 配置
稳态判据: main 触发 schedule Run，feature branch 不触发
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-triggers.md
关联已有用例: TC-428 (schedule 仅默认分支生效)
```

---

## 9. 竞态与一致性问题

### INTENT-REL-035
```
意图 ID:    INTENT-REL-035
维度标签:   [reliability]
标题:       同时触发 + 同时取消的竞态：取消不应使后续排队 job 错误取消

风险点:     用户同时手动取消 run1 + 触发 run2，若競态导致 run2 也被取消，影响正常使用。history #10/#39 暴露取消逻辑不靠谱。
预期系统行为: 取消仅作用于指定 Run，不波及其他 Run。
Oracle 来源: GitHub Actions 语义

验证要点:
  - [正向] run1 cancelled, run2 正常执行完成
  - [负向] run2 不被意外 cancelled

场景/参数: run1 running (sleep 120) → 同时发起 cancel run1 + trigger run2
稳态判据: run1=cancelled, run2=success
恢复预期: run2 执行成功后恢复为正常状态
破坏级别: none
优先级线索: history #10, #39
来源输入: history/issues-encountered.md (#10, #39)
```

### INTENT-REL-036
```
意图 ID:    INTENT-REL-036
维度标签:   [reliability]
标题:       对正在运行中 job 的 workflow 文件进行修改后 push，已运行中的 job 不受新配置影响

风险点:     运行中 job 若被新 YAML 影响（如修改了 env/step），可能导致不可预期的执行。应基于触发时的 YAML 快照。
预期系统行为: 已运行中的 job 继续使用触发时的 YAML 快照执行；新触发使用新 YAML。
Oracle 来源: GitHub Actions 语义

验证要点:
  - [正向] run1 按旧 YAML 执行完成（env 不变）
  - [正向] run2 按新 YAML 执行（env 变化体现）

场景/参数: YAML v1（env: VER=1）触发 run1 → run1 运行中修改 YAML v2（env: VER=2）并 push 触发 run2
稳态判据: run1 日志: VER=1; run2 日志: VER=2
恢复预期: N/A
破坏级别: none
来源输入: GitHub reference/workflow-syntax.md
```

### INTENT-REL-037
```
意图 ID:    INTENT-REL-037
维度标签:   [reliability]
标题:       workflow_call 子 workflow 被调用后缓存不更新的回归验证——针对历史 #85

风险点:     history #85: 「子 workflow 更新后从日志看用的还是旧代码（yml 缓存问题）」。这是已验证缺陷，需回归确认已修复。
预期系统行为: 更新子 workflow YAML 后，下次 workflow_call 调用使用最新版本。
Oracle 来源: history #85

验证要点:
  - [正向] 更新子 workflow 后，调用方日志体现新行为（新 echo 文本）
  - [负向] 子 workflow 日志不应出现旧代码行为

场景/参数: caller → reusable workflow（echo "v1"）→ 更新 reusable → echo "v2" → 再次 caller 触发
稳态判据: 第 2 次调用日志显示 "v2"
恢复预期: N/A
破坏级别: none
优先级线索: history #85
来源输入: history/issues-encountered.md (#85, #76, #84)
```

### INTENT-REL-038
```
意图 ID:    INTENT-REL-038
维度标签:   [reliability]
标题:       workflow_call 子 workflow 失败时，父 workflow 正确传播失败而非显示 success

风险点:     history #30: 「workflow_call 无法拉起子任务，但显示已完成」。子 workflow 实际未执行但父 workflow 显示 success——状态不一致。
预期系统行为: 子 workflow failed → 父 workflow 调用 job failed → 父 workflow 整体 failure。
Oracle 来源: GitHub Actions 语义 + history #30, #64

验证要点:
  - [正向] 子 workflow failed → 调用 job failed
  - [负向] 调用 job 不显示 success 当子 workflow 实际 failed

场景/参数: caller (workflow_call: reusable-with-failure) → reusable (故意 exit 1)
稳态判据: 父 workflow = failure
恢复预期: N/A
破坏级别: none
优先级线索: history #30, #64
来源输入: history/issues-encountered.md (#30, #64)
关联已有用例: TC-013 (inputs workflow_call)
```

### INTENT-REL-039
```
意图 ID:    INTENT-REL-039
维度标签:   [reliability]
标题:       workflow_call 嵌套达到 2 层上限：第 3 层应明确报错

风险点:     GitCode spec 声明嵌套最多 2 层。越界时若静默成功（无限制）可能导致无限递归风险。
预期系统行为: 第 3 层调用在 YAML 解析/触发阶段报错。
Oracle 来源: GitCode 规格（configure-triggers.md: 「嵌套调用最多支持 2 层」）

验证要点:
  - [正向] 3 层嵌套时 workflow 触发报错
  - [负向] 第 3 层不实际执行

场景/参数: workflow A → workflow_call B → B → workflow_call C → C → workflow_call D（3 层嵌套）
稳态判据: 触发时报错，不执行到 D
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-triggers.md
```

---

## 10. 资源配置边界值

### INTENT-REL-040
```
意图 ID:    INTENT-REL-040
维度标签:   [reliability]
标题:       slim (1 核 4GB) runner 上执行需要 >4GB 内存的任务，应按 OOM 或退化执行

风险点:     资源不足时 job 可能被 OOM kill 或极其缓慢。若平台不限制，可能抢占其他 job 资源。history #92: 「EulerOS 2.0 不支持」。
预期系统行为: 超内存 job 被 OOM kill 后 Run = failure，或 step 收到分配失败信号。不应 hang。
Oracle 来源: GitCode 规格（using-hosted-runners.md: slim=1核4GB）

验证要点:
  - [正向] Run 终态 = failure
  - [正向] 日志含 OOM/memory 错误
  - [负向] job 不无限 hang

场景/参数: runs-on={ubuntu-24,x64,slim}, step: `stress --vm 1 --vm-bytes 6G --timeout 60s`
稳态判据: Run failure within 5min, 日志含 memory 相关信息
恢复预期: Run failure → runner 回收
破坏级别: fixture
来源输入: gitcode-spec/runner-management/using-hosted-runners.md
```

### INTENT-REL-041
```
意图 ID:    INTENT-REL-041
维度标签:   [reliability]
标题:       container.options --memory 限制生效: 容器内存限制阻止超限分配

风险点:     container.options 中 --memory 限制若未传递到 Docker daemon，容器可能消耗超过声明的内存。
预期系统行为: 容器内进程使用超过 --memory 限制时被 OOM kill。
Oracle 来源: GitCode 规格（configuring-images-toolchains.md: container.options）+ Docker 行为

验证要点:
  - [正向] 超过 --memory=512m 时进程被 kill
  - [正向] 日志含 OOM 信息

场景/参数: container.options: --memory 512m, step: `stress --vm 1 --vm-bytes 1G --timeout 30s`
稳态判据: 容器内进程 OOM killed
恢复预期: N/A
破坏级别: fixture
来源输入: gitcode-spec/runner-management/configuring-images-toolchains.md
```

### INTENT-REL-042
```
意图 ID:    INTENT-REL-042
维度标签:   [reliability]
标题:       paths 过滤前 300 个变更文件边界验证: 301 个文件变更时第 301 个不被匹配

风险点:     GitCode spec 声明 paths 仅匹配前 300 个变更文件（vs GitHub 3000）。此差异可能导致 CI 静默跳过预期匹配的路径变更——兼容性 + 稳定性风险。
预期系统行为: 301 个文件变更时，匹配路径在第 301 个之后的不触发 workflow。
Oracle 来源: GitCode 规格（configure-triggers.md）+ GitHub reference（3000 files）

验证要点:
  - [正向] 变更 299 个 src/ 文件 + 1 个触发文件（第 301 个 = src/trigger.txt）→ 不触发
  - [正向] 变更 300 个文件 + 1 个触发文件（第 1 个 = src/trigger.txt）→ 触发

场景/参数: paths: src/**, 变更 300 个 docs/README.md（占位） + 1 个 src/trigger.txt（第 301 个）
稳态判据: workflow 不触发（因为 trigger.txt 在第 301 个位置，不被扫描）
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-triggers.md (paths 前 300 文件); GitHub reference/workflow-syntax.md (3000 files)
```

---

## 11. 大规模与负载

### INTENT-REL-043
```
意图 ID:    INTENT-REL-043
维度标签:   [reliability]
标题:       单 workflow 含 10 个独立 job（无 needs，全部并行），所有 job 应正确分发到可用 runner

风险点:     大量并行 job 同时竞争 runner，调度器能否公平分发。若某个 job 饥饿，影响整体 workflow 完成时间。
预期系统行为: 所有 10 个 job 在可用 runner 上并行分配，无 job 长时间停留在 queued 而其他后触发 job 已执行。
Oracle 来源: GitHub Actions 语义 + testing-focus.md §12

验证要点:
  - [正向] 所有 10 个 job 最终 success
  - [正向] 任意 job 排队时间 ≤ 5min（若 runner 充足）
  - [非功能] 10 个 job 完成时间接近（无明显饥饿）

场景/参数: 10 个独立 job (sleep 10s each)，runs-on={ubuntu-24,x64,small}
稳态判据: 全部 success，完成时间差异 < 30s
恢复预期: N/A
破坏级别: none
优先级线索: RISK-REL-01
来源输入: testing-focus.md §3 执行模型, §12 稳定性专项
```

### INTENT-REL-044
```
意图 ID:    INTENT-REL-044
维度标签:   [reliability]
标题:       多 workflow 同时洪泛（3 个不同 workflow 各 10 次触发），排队公平性与无死锁

风险点:     多个不同 workflow 同时洪泛时，若调度器有偏向性（如按 workflow 名排序而非 FIFO），可能导致某个 workflow 的所有 Run 被排到最后。history #67: 「流水线频繁触发，每次改动标签都会触发流水线」。
预期系统行为: 所有 Run 按触发时间 FIFO 排队，无某个 workflow 的 Run 被系统性排后。
Oracle 来源: GitHub Actions 语义

验证要点:
  - [正向] 所有 30 个 Run 最终 success/failure
  - [非功能] 3 个 workflow 的 Run 在时间线上交错执行（非一个 workflow 全部完成后再另一个）

场景/参数: 3 个不同 workflow (A/B/C)，各 10 次 push 触发，间隔 1s，交错触发顺序: A1,B1,C1,A2,B2,C2...
稳态判据: 30 个 Run 全部终态，时间线呈现合理交错
恢复预期: N/A
破坏级别: none
优先级线索: RISK-REL-01 + history #67
来源输入: testing-focus.md §12; history #67
```

### INTENT-REL-045
```
意图 ID:    INTENT-REL-045
维度标签:   [reliability]
标题:       大仓库 checkout (>500MB, >1000 commits) 在托管 runner 上稳定完成

风险点:     大仓库 checkout 可能超出 runner 磁盘配额或网络超时，导致 checkout 失败。history #79: 「自定义资源池 checkout 插件运行失败」。
预期系统行为: checkout 在 timeout-minutes 内完成，后续 step 可正常编译。
Oracle 来源: GitCode 规格 + GitHub Actions 行为

验证要点:
  - [正向] checkout 完成，工作区文件总数与仓库一致
  - [正向] 所有 step 正常执行
  - [非功能] checkout 耗时不超过 GitHub Actions 同类 operation 的 2x

场景/参数: runs-on={ubuntu-24,x64,medium}, checkout 一个 ~500MB 测试仓库 (depth=1)
稳态判据: checkout success，后续 step 找到所有文件
恢复预期: N/A
破坏级别: none
优先级线索: history #79
来源输入: testing-focus.md §12; history #79
```

---

## 12. Post 后处理与清理

### INTENT-REL-046
```
意图 ID:    INTENT-REL-046
维度标签:   [reliability]
标题:       post 阶段在 main job 失败时仍执行（run_always=true），完成通知/清理

风险点:     post 是 GitCode 特有机制。若 run_always=true 在失败时不执行，会导致通知丢失和资源泄露。
预期系统行为: main job failure 后 post 阶段仍执行，日志可见 post steps 输出。
Oracle 来源: GitCode 规格（workflow-file-location-structure.md: post.run_always 默认为 true）

验证要点:
  - [正向] main job 失败后 post 阶段步骤执行
  - [正向] post 日志完整可见

场景/参数: main job (exit 1), post (run_always=true, echo "cleanup done")
稳态判据: post 日志含 'cleanup done'
恢复预期: post 完成后 runner 释放
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/workflow-file-location-structure.md
```

### INTENT-REL-047
```
意图 ID:    INTENT-REL-047
维度标签:   [reliability]
标题:       post 阶段 run_always=false 时，main job 失败则 post 不执行

风险点:     run_always=false 语义需与 true 区分，防止两种模式行为一致（都是 always 或都是 never）。
预期系统行为: main job success + post run_always=false → post 执行；main job failure + post run_always=false → post 不执行。
Oracle 来源: GitCode 规格

验证要点:
  - [正向] main job success → post 执行
  - [正向] main job failure → post 不执行

场景/参数: 2 次 run: (1) main: exit 0, post: run_always=false; (2) main: exit 1, post: run_always=false
稳态判据: run1 post 执行; run2 post 不执行
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/workflow-file-location-structure.md
```

---

## 13. 环境变量与上下文一致性

### INTENT-REL-048
```
意图 ID:    INTENT-REL-048
维度标签:   [reliability]
标题:       同一 secret 在两个相邻 step 引用，第二次不应报 bad substitution——历史 #11 回归

风险点:     history #11: 「同一私密参数，在一个 job 的两个相邻 step 引用，第二次报 bad substitution」。这是已被修复的缺陷，需回归验证。
预期系统行为: 两次引用 secret 均正常渲染，不出现 bash 替换错误。
Oracle 来源: history #11

验证要点:
  - [正向] step1 和 step2 均正常 dereference secret 值
  - [负向] step2 不报 'bad substitution'

场景/参数: 2 个相邻 step，各自 echo 同一 secret
稳态判据: 2 个 step 均 success，日志无 bad substitution
恢复预期: N/A
破坏级别: none
优先级线索: history #11
来源输入: history/issues-encountered.md (#11); gitcode-spec/core-concepts/variables-secrets-context-expressions.md
```

### INTENT-REL-049
```
意图 ID:    INTENT-REL-049
维度标签:   [reliability]
标题:       env 变量中带中划线 '-' 时渲染正确——历史 #38 回归

风险点:     history #38: 「使用自定义 ${MindIE-SD_REPOSITORY_NAME} 发生异常，中划线导致参数异常。shell 中 ${aaa-bbb} 的 '-' 后边是默认值」。这是 shell 变量命名规则的已知坑。
预期系统行为: GitCode 应正常处理包含中划线的变量引用（如在 ${{ }} 表达式层渲染），而非在 shell 层暴露 bash 替换歧义。
Oracle 来源: history #38

验证要点:
  - [正向] ${{ env.MY-VAR }} 在表达式层正常渲染
  - [负向] 不触发 bash 替换歧义（不把 MY-VAR 解析为 MY 减去 VAR）

场景/参数: env: MY-VAR: hello, step: echo ${{ env.MY-VAR }}
稳态判据: 日志输出 'hello'
恢复预期: N/A
破坏级别: none
优先级线索: history #38
来源输入: history/issues-encountered.md (#38)
```

### INTENT-REL-050
```
意图 ID:    INTENT-REL-050
维度标签:   [reliability]
标题:       ATOMGIT_OUTPUT 文件写入正常，下游 job 可读取——历史 #87/#94 关注

风险点:     history #84/#87/#94 涉及 outputs 传递、env 传递失败。outputs 是 job 间数据流的核心通道。
预期系统行为: step 写入 `echo "key=value" >> $ATOMGIT_OUTPUT`，下游 job 通过 `needs.<job>.outputs.key` 读取到 value。
Oracle 来源: GitCode 规格（configure-jobs.md: outputs）+ GitHub Actions 语义

验证要点:
  - [正向] 下游 job 的 `needs.<job>.outputs.key` = value
  - [正向] value 在日志中可见（非脱敏场景）

场景/参数: job-A: step id=gen → echo "key=value123" >> $ATOMGIT_OUTPUT; job-B (needs: job-A): echo ${{ needs.job-A.outputs.key }}
稳态判据: job-B 日志: value123
恢复预期: N/A
破坏级别: none
优先级线索: history #87, #94, #84, #76
来源输入: gitcode-spec/writing-pipelines/pass-output-between-jobs.md; history (#87, #94, #84, #76)
```

---

## 14. 错误条件处理与恢复

### INTENT-REL-051
```
意图 ID:    INTENT-REL-051
维度标签:   [reliability]
标题:       continue-on-error=true 的 job 失败后，needs 该 job 的下游 job 仍需判断才能执行

风险点:     continue-on-error 改变失败传播语义。若 downstream job 误认为 needs 已满足，在垃圾输入上执行。
预期系统行为: needs 依赖 continue-on-error job 的下游 job 需要用 `if: always()` 或 `if: failure()` 才能执行；默认 `if: success()` 将被跳过。
Oracle 来源: GitCode 规格（configure-jobs.md: continue-on-error）+ GitHub Actions 语义

验证要点:
  - [正向] 下游 job_A（默认 if）状态 = skipped
  - [正向] 下游 job_B（if: always()）正常执行

场景/参数: job-flaky（continue-on-error:true, exit 1）→ job-A（needs: job-flaky, 无 if）→ job-B（needs: job-flaky, if: always()）
稳态判据: job-A=skipped, job-B=success
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/configure-jobs.md (continue-on-error)
关联已有用例: TC-088 (job.status), TC-317-321 (条件执行函数)
```

### INTENT-REL-052
```
意图 ID:    INTENT-REL-052
维度标签:   [reliability]
标题:       非法 runs-on 标签（不存在的 flavor 如 'tiny'）被拒绝而非 fallback 到 default

风险点:     若非法标签被静默 fallback 到 default runner，用户以为在 large 上执行实际在 small 上，可能导致 OOM。
预期系统行为: 非法标签应导致 job 状态 = queued（无匹配 runner）或 failed，不应静默 fallback。
Oracle 来源: GitCode 规格（标签全匹配规则）

验证要点:
  - [正向] job 状态 = queued/failed
  - [负向] job 不在 default runner 上执行

场景/参数: runs-on={ubuntu-24,x64,tiny}（tiny 不存在）
稳态判据: job 未在 default runner 执行
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/runner-management/selecting-runner-labels.md
```

### INTENT-REL-053
```
意图 ID:    INTENT-REL-053
维度标签:   [reliability]
标题:       stages 中前一个 stage 的 job 失败且 fail_fast=true 时，后续 stage 全部跳过

风险点:     stages.fail_fast 与 strategy.fail-fast 是不同的控制层。两者语义混淆可能导致错误的跳过/继续行为。
预期系统行为: stage1 中 job 失败 + fail_fast=true → stage2 和 stage3 所有 job 不执行（skipped）。
Oracle 来源: GitCode 规格（workflow-file-location-structure.md: stages.fail_fast）

验证要点:
  - [正向] stage2 和 stage3 的 job 状态 = skipped
  - [负向] stage2/stage3 不进入 queued

场景/参数: 3 stages: build (fail_fast=true, 故意 fail) → test → deploy
稳态判据: build=failure, test=skipped, deploy=skipped
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/writing-pipelines/workflow-file-location-structure.md
```

---

## 15. 第三方 Action 与插件稳定性

### INTENT-REL-054
```
意图 ID:    INTENT-REL-054
维度标签:   [reliability]
标题:       official_checkout 在 timeout-minutes 内完成标准仓库 checkout（回归基础可用性）

风险点:     checkout 是 workflow 第一步，不可用则所有后续全断。history #25/#71: PR 预合并不可用，#79: 自定义资源池 checkout 失败，#58: 关闭 PR 后重开 checkout 失败。
预期系统行为: checkout 在标准仓库（<100MB）上 3min 内完成，拉取到正确的 commit SHA。
Oracle 来源: GitCode 规格 + GitHub Actions actions/checkout 行为

验证要点:
  - [正向] checkout 完成后工作区有代码文件
  - [正向] `git rev-parse HEAD` 输出与触发 commit SHA 一致
  - [非功能] checkout 耗时 < 3min (标准小型仓库)

场景/参数: push 触发，runs-on={ubuntu-24,x64,small}, uses: official_checkout
稳态判据: checkout success, HEAD SHA 正确
恢复预期: N/A
破坏级别: none
优先级线索: history #25, #71, #79, #58
来源输入: gitcode-actions-list.md (official_checkout); history (#25, #71, #79, #58)
```

### INTENT-REL-055
```
意图 ID:    INTENT-REL-055
维度标签:   [reliability]
标题:       official_cache 在多 job 引用时 key 唯一性隔离：job-A 的 cache 不污染 job-B

风险点:     若 cache key 作用域不正确，不同 job 可能读到对方的缓存，造成构建污染。
预期系统行为: 不同 key 的 cache 不被其他 job 命中。
Oracle 来源: GitCode 规格（artifacts-and-cache.md）

验证要点:
  - [负向] job-B 不应 hit job-A 的 cache（若 key 不同）

场景/参数: job-A: cache key=cache-A → job-B: cache key=cache-B（不同）
稳态判据: job-B log: cache miss
恢复预期: N/A
破坏级别: none
来源输入: gitcode-spec/core-concepts/artifacts-and-cache.md; gitcode-actions-list.md (official_cache)
关联已有用例: TC-019 (INTENT-SEC-019: cache 投毒)
```

---

## 16. 最终裁决门禁

### INTENT-REL-056
```
意图 ID:    INTENT-REL-056
维度标签:   [reliability]
标题:       注册表：所有 reliability intent 覆盖 summary

汇总 sheet —— 不做单独用例，仅为门禁与覆盖度评审提供索引。

| 覆盖域 | Intent | P0 风险对齐 | 历史缺陷对齐 |
|--------|--------|------------|------------|
| 并发边界与越界 | REL-001~004 | RISK-REL-01 | #7, #10, #12 |
| 矩阵策略与竞态 | REL-005~011 | RISK-REL-01 | #101 |
| Runner 层故障注入 | REL-012~018 | — | #7, #42, #48, #52, #54, #55, #65, #70, #78, #89, #91, #96 |
| 调度与依赖层故障 | REL-019~022 | — | #10, #30, #39, #64, #101 |
| 超时与长运行 | REL-023~025 | — | #14, #80, #81 |
| 自托管 Runner 资源 | REL-026~029 | — | #7, #37, #48, #52, #54, #70, #89, #96 |
| 缓存与制品 | REL-030~032 | — | #16, #90 |
| Schedule 触发 | REL-033~034 | — | S3×24+TC-391 |
| 竞态与一致性 | REL-035~039 | — | #10, #30, #39, #64, #76, #84, #85 |
| 资源边界值 | REL-040~042 | — | #92 |
| 大规模负载 | REL-043~045 | RISK-REL-01 | #67, #79 |
| Post 与清理 | REL-046~047 | — | — |
| 环境变量一致性 | REL-048~050 | — | #11, #38, #76, #84, #87, #94 |
| 错误处理恢复 | REL-051~053 | — | — |
| 第三方 Action | REL-054~055 | — | #25, #58, #71, #79, #90 |

---

## 质量自查清单

- [x] 每个配额维度都有边界+越界 intent: concurrency.max (REL-001~004); matrix (REL-005~011); timeout (REL-023~024); 架构/规格匹配 (REL-026~029, 040~041); workflow_call 嵌套 (REL-039); paths 300 (REL-042)
- [x] 每条故障注入 intent 声明了恢复预期 (REL-012~018, 026~027)
- [x] 参数具体化: 并发=5/10/20, 矩阵=64, 超时=2/5/360 min, 时间=30s/5min/10min
- [x] 破坏性 intent 标了正确的 teardown 级别: fixture / full_instance / none
- [x] 每条 intent 标注了来源输入
- [x] 历史缺陷全覆盖: 101 条 history 中的可靠性相关缺陷 (至少 25+ 条) 被显式关联到对应 intent
- [x] 每条 intent 含 dimensions 标签 [reliability]
- [x] Oracle 来源明确: GitCode 规格 / GitHub Actions 语义 / history 实证
