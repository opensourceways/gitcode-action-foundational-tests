# Reliability Test Intents

> Agent: reliability | Run: 2026-07-20-01 | Dimensions: [reliability]
> 来源输入: `phase01/inputs/gitcode-spec/` (全量)、`phase01/inputs/platform-config/` (缺失，见下文)、`phase01/inputs/existing-cases/cases.md` (631 条去重参照)
> 输入版本: gitcode-spec fetched 2026-07-20 | platform-config NOT AVAILABLE

---

## 输入缺失声明

`platform-config/` 目录仅有 README 模板，**无实际配额/上限数值**。以下维度依赖 platform-config 但无法获取具体值：

| 缺失维度 | 影响 | 缓解措施 |
|---------|------|---------|
| max_concurrent_workflows | 并发洪泛 intent 无法设定绝对上限值 | 用行为模式（排队/限流/公平性）替代绝对上限 |
| max_concurrent_jobs_per_workflow | 单 workflow 内并发 job 上限不明 | 用矩阵 max-parallel 间接覆盖 |
| max_matrix_size | 大规模矩阵 exact 边界值不明 | 用中等规模 (16-64 组合) 覆盖展开正确性 |
| max_job_timeout_minutes | 官方值 360min 已在 spec 中，此项已知 | — |
| max_log_size / max_artifact_size / max_cache_size | 制品/日志边界值不明 | 仅覆盖行为模式，不覆盖绝对边界 |
| max_secrets_per_repo | 非本维度核心关注 | 不覆盖 |

所有边界 intent 若需「超出上限」判定，显式标注「无法精确定义越界值——依赖未提供的 platform-config」。

---

## 1. 并发洪泛

### INTENT-REL-001
```
意图 ID:    INTENT-REL-001
维度标签:   [reliability]
标题:       同一 workflow 在 10s 内被 push 事件连续触发 20 次，排队与执行行为可预测

风险点:     高频 push 触发洪泛时，系统可能 (a) 丢失触发、(b) 无序执行、(c) 耗尽 Runner 池导致后续合法触发长时间阻塞。GitCode spec 未声明去抖/合并策略。
预期系统行为: 20 次触发全部产生 Run，按触发时间顺序排队，无 Run 被静默丢弃；若启用 concurrency max=N，超过 N 的 Run 按 exceed-action 策略处理 (QUEUE/IGNORE/CANCEL)。
Oracle 来源: GitCode 规格（concurrency 字段文档声明 exceed-action 行为）+ GitHub Actions 默认行为（不合并 push 触发）

验证要点:
  - [正向] 所有 20 次触发均产生可追踪的 Run ID
  - [正向] Run 按 FIFO 顺序进入执行（按 run_number 严格递增对应触发顺序）
  - [负向] 无 Run 被静默丢弃（未被记录在 Run 列表中即视为丢弃）
  - [非功能] 第 1 次触发的 Run 在 120s 内进入 in_progress（若 Runner 可用）

故障/压力参数: 并发度=20（同 workflow 同分支，10s 窗口内连续 push）；触发事件=push；判据=所有 Run ID 可枚举且 run_number 连续
优先级线索: RISK-REL-01
破坏级别:   none（不破坏实例，仅观察调度行为）
来源输入:   gitcode-spec/core-concepts/workflow-job-step-action.md、gitcode-spec/writing-pipelines/configure-jobs.md (concurrency)；platform-config 缺失致无法设定绝对上限阈值
```

### INTENT-REL-002
```
意图 ID:    INTENT-REL-002
维度标签:   [reliability]
标题:       concurrency max=2 且 exceed-action=QUEUE 时，5 个同时触发的 workflow_dispatch 按排队语义执行

风险点:     排队语义若失效，可能出现同时执行数超过 max 限制（并发槽泄漏）或排队 Run 被饿死。
预期系统行为: 任意时刻最多 2 个 Run 处于 in_progress，其余 Run 保持 queued 直到 slot 释放；被排队 Run 最终全部执行完成。
Oracle 来源: GitCode 规格（concurrency.exceed-action=QUEUE 文档声明）

验证要点:
  - [正向] 任意快照时刻 in_progress Run 数 <= 2
  - [正向] 5 个 Run 全部到达 completed(success) 终态
  - [负向] 无 Run 被静默丢弃
  - [非功能] 首个 Run 完成到下一个 Run 被调度之间的间隔 <= 30s

故障/压力参数: 并发度=5（同 workflow，workflow_dispatch 手动连续触发）；concurrency.max=2；exceed-action=QUEUE
优先级线索: RISK-REL-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-jobs.md (concurrency)
```

### INTENT-REL-003
```
意图 ID:    INTENT-REL-003
维度标签:   [reliability]
标题:       concurrency max=1 且 exceed-action=CANCEL 时，新触发的 Run 应取消正在进行中的旧 Run

风险点:     抢占取消逻辑若不可靠，可能出现新旧 Run 同时运行并发冲突（如部署竞态）；或旧 Run 取消不完全（步骤卡死、资源泄漏）。
预期系统行为: 新 Run 触发时，旧 in_progress Run 被立即标记为 cancelled → 其正在执行的 step 收到 SIGTERM 并终止；旧 Run 中 if: always() 的清理步骤仍有最多 60s 执行机会；新 Run 被调度启动。
Oracle 来源: GitCode 规格（concurrency.exceed-action=CANCEL 文档声明 + GitHub Actions cancel-in-progress 语义）

验证要点:
  - [正向] 旧 Run 状态变更为 cancelled
  - [正向] 新 Run 在旧 Run 被取消后的 60s 内进入 in_progress
  - [负向] 新旧 Run 不同时处于 in_progress 状态
  - [非功能] 旧 Run 中被取消的 step 在 10s 内收到终止信号（step 日志显示 "Cancelled" 标记）

故障/压力参数: 并发度=2（同 workflow，workflow_dispatch 先后触发）；concurrency.max=1；exceed-action=CANCEL；旧 Run 内布置一个 sleep 180 的长步骤作为抢占目标
优先级线索: RISK-REL-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-jobs.md (concurrency)
```

### INTENT-REL-004
```
意图 ID:    INTENT-REL-004
维度标签:   [reliability]
标题:       concurrency max=1 且 exceed-action=IGNORE 时，并发超限的触发被直接拒绝

风险点:     IGNORE 策略下多余的触发若未正确拒绝，可能 (a) 实际执行了、(b) 排队而非拒绝、(c) 没有给出可诊断的状态/信息。
预期系统行为: 在已有 1 个 in_progress Run 时触发的新 Run 立即被标记为 skipped 或等价终态（不被排队、不被执行）。
Oracle 来源: GitCode 规格（exceed-action=IGNORE 文档声明）

验证要点:
  - [正向] 新 Run 不进入 queued 或 in_progress
  - [正向] 新 Run 状态为 skipped 或 cancelled（有明确终态，非 pending）
  - [负向] 新 Run 无任何 job 被调度

故障/压力参数: 并发度=2（同 workflow，先触发一次使 Run1 in_progress，立即再触发 Run2）；concurrency.max=1；exceed-action=IGNORE
优先级线索: RISK-REL-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-jobs.md (concurrency)
```

---

## 2. 大规模矩阵

### INTENT-REL-005
```
意图 ID:    INTENT-REL-005
维度标签:   [reliability]
标题:       二维矩阵生成 16 个 job 实例时，所有实例正确展开并独立执行

风险点:     矩阵展开逻辑 Bug 会导致 (a) 部分组合被跳过、(b) 重复生成、(c) `runs-on` 动态解析在某实例上失败。已知 TC-486 报告 needs 指向 matrix 父 job 导致初始化错误。
预期系统行为: 4×4=16 个 job 实例全部生成，各自独立分配 runner 并执行；每个实例的 matrix 上下文值正确注入。
Oracle 来源: GitCode 规格（configure-matrix-builds.md 声明：每个变量值组合生成一个 job 实例）

验证要点:
  - [正向] Run 中可见 16 个 job（API/steps 日志可枚举）
  - [正向] 每个 job 中 ${{ matrix.os }} 和 ${{ matrix.node }} 的值与生成组合一致
  - [负向] 无 "任务初始化错误" 或类似 TC-486 的失败
  - [非功能] 所有 16 个 job 的 steps 日志各自独立、无交叉污染

故障/压力参数: 矩阵规模=4(os) × 4(node-version) = 16 job 实例；os 维度=[ubuntu-latest,ubuntu-24,ubuntu-22] 中取 3 + 1 个预期的 runner 标签；strategy.max-parallel=8
优先级线索: (无直接风险项，但大规模矩阵展开是 quality-gate 中稳定性门禁的关键场景)
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-matrix-builds.md；platform-config 缺失致无法设定 max_matrix_size 边界
```

### INTENT-REL-006
```
意图 ID:    INTENT-REL-006
维度标签:   [reliability]
标题:       matrix include 追加 3 个额外组合时，总实例数 = 基础组合 + include - exclude

风险点:     include 追加的组合可能在 (a) 基础矩阵同名组合上覆盖而非追加、(b) 变量未定义时报错或静默跳过、(c) include 中的额外变量未注入对应实例。
预期系统行为: 基础矩阵 os=[ubuntu, windows] × node=[18, 20] = 4 实例；include 追加 3 个组合（含一个额外变量 experimental），exclude 排除 1 个 → 总 4 + 3 - 1 = 6 实例。include 中定义的额外变量 experimental 仅对 include 实例可见。
Oracle 来源: GitCode 规格（configure-matrix-builds.md include/exclude 文档声明）

验证要点:
  - [正向] 总 job 数 = 6
  - [正向] include 追加的 experimental 变量仅在其所属实例的 shell 中可读
  - [负向] 被 exclude 的组合无对应 job 生成

故障/压力参数: 矩阵配置=os×node 基础 2×2=4, include 3, exclude 1 → 预期 6 实例
优先级线索: (无直接风险项)
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-matrix-builds.md
```

### INTENT-REL-007
```
意图 ID:    INTENT-REL-007
维度标签:   [reliability]
标题:       strategy.fail-fast=true 时，矩阵中 1 个 job 实例失败应立即取消其余未完成实例

风险点:     fail-fast 取消信号可能 (a) 延迟过长、(b) 部分实例未收到取消、(c) 和 stages.fail_fast 交互产生意外行为。
预期系统行为: 当任一矩阵 job 实例的 step 失败后，所有其他尚未 completed 的矩阵 job 实例在 30s 内收到取消信号并转为 cancelled。
Oracle 来源: GitCode 规格（configure-matrix-builds.md fail-fast 文档声明）

验证要点:
  - [正向] 矩阵中首个 job 失败后，其余尚未完成的 job 在 30s 内全部转为 cancelled
  - [正向] 已完成的 job 状态不受影响
  - [负向] 无 job 卡死在 in_progress 超过 60s 未响应取消

故障/压力参数: 矩阵规模=6 实例；其中 1 个实例布置必然失败的 step（exit 1），其余 5 个实例布置 sleep 120 或正常步骤；fail-fast=true
优先级线索: (无直接风险项，但 cancel-in-progress 传播是 concurrency 体系基石)
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-matrix-builds.md
```

### INTENT-REL-008
```
意图 ID:    INTENT-REL-008
维度标签:   [reliability]
标题:       strategy.max-parallel=3 时，6 实例矩阵的并发峰值不超过 3

风险点:     max-parallel 限制若未生效，矩阵 job 全部同时启动 → Runner 池耗尽 → 同 workflow 内其他 job 或同组织其他 workflow 饿死。
预期系统行为: 任意快照时刻，该矩阵的 in_progress job 数 ≤ 3；第 4 个 job 在某个 slot 释放后才被调度。
Oracle 来源: GitCode 规格（configure-matrix-builds.md max-parallel 文档声明）

验证要点:
  - [正向] 同时 in_progress 的矩阵 job 数 <= 3
  - [正向] 6 个 job 全部到达 completed 终态
  - [负向] 无 job 因 slot 不足而永久卡在 queued

故障/压力参数: 矩阵规模=6 实例；max-parallel=3
优先级线索: (无直接风险项)
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-matrix-builds.md
```

---

## 3. 长时运行与超时

### INTENT-REL-009
```
意图 ID:    INTENT-REL-009
维度标签:   [reliability]
标题:       job 设置 timeout-minutes=5 时，超过 5 分钟的 step 被强制终止

风险点:     超时机制未触发 → job 永久挂起占用 Runner；超时触发但不输出可诊断信息 → 用户无法定位原因；超时时间不精确 → 实际超时阈值远大于声明值。
预期系统行为: job 从 in_progress 起计时，5 分钟后系统发送 SIGTERM 给 step 进程；若 10s 内进程未退出则 SIGKILL；job 终态为 cancelled（或 failure，视具体平台设计）；日志中明确标注 timeout 原因。
Oracle 来源: GitCode 规格（configure-jobs.md timeout-minutes: 360min 默认，声明超时后强制终止）

验证要点:
  - [正向] job 在 5min ± 30s 内终止（允许 scheduler 轮询延迟）
  - [正向] job 日志末尾包含 timeout 相关标记（如 "The job was canceled because it exceeded the timeout of 5 minutes" 或等价信息）
  - [负向] job 不会持续运行超过 10 分钟
  - [非功能] timeout 后的 Runner 被正常回收，不影响下一个 job 的执行

故障/压力参数: timeout-minutes=5；布置一个 sleep 600 的 step 确保超时触发
优先级线索: (无直接风险项，但超时是唯一的防死循环机制)
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-jobs.md
```

### INTENT-REL-010
```
意图 ID:    INTENT-REL-010
维度标签:   [reliability]
标题:       多个 job 设置不同 timeout-minutes（5/30/360），各自按独立时钟超时

风险点:     多 job 间 timeout 时钟可能 (a) 共享、非独立、(b) 从 workflow 开始计时而非 job 开始计时、(c) 在 matrix 场景下未独立展开。
预期系统行为: 每个 job 的超时从「该 job 进入 in_progress」起计，互不影响。job A (5min) 先超时被终止，不影响 job B (360min) 继续运行。
Oracle 来源: GitCode 规格（configure-jobs.md: timeout-minutes 是 jobs.<id>.timeout-minutes 字段）

验证要点:
  - [正向] job A（5min）在 5min ± 30s 内终止
  - [正向] job B（360min, 但 step 执行 30s 即完成）正常成功
  - [负向] job A 的超时不触发 job B 的取消

故障/压力参数: 2 个独立 job 无 needs 依赖；job A: timeout=5, step=sleep 600；job B: timeout=360, step=echo done
优先级线索: (无直接风险项)
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-jobs.md
```

### INTENT-REL-011
```
意图 ID:    INTENT-REL-011
维度标签:   [reliability]
标题:       timeout-minutes=0 或负数的非法值被配置校验拒绝

风险点:     非法超时值若被接受，(a) timeout=0 意味着立即终止——job 不可能成功、(b) 负数可能导致整形溢出或未定义行为。
预期系统行为: 配置校验阶段（workflow 解析/保存时）报错，拒绝无效 timeout 值。具体拒绝方式可能是 YAML lint 错误或保存时校验错误。
Oracle 来源: GitCode 规格（未明确声明合法范围，但任何合理系统不应接受 <= 0 的超时值）

验证要点:
  - [正向] workflow 文件含 timeout-minutes: 0 时，系统拒绝（保存失败 / 触发时解析报错 / job 标记为配置错误）
  - [负向] 无 job 以 timeout=0 被实际调度执行

故障/压力参数: timeout-minutes=0（非法值）
优先级线索: (无直接风险项)
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-jobs.md
```

---

## 4. Runner 资源耗尽

### INTENT-REL-012
```
意图 ID:    INTENT-REL-012
维度标签:   [reliability]
标题:       step 尝试分配超过 runner 可用内存（8GB 的 small runner 上尝试分配 12GB）时，进程被 OOM kill 且 job 标记为失败

风险点:     OOM kill 发生后若 job 不报失败而标记为成功（退出码传播错误），或 runner 宿主机因 OOM 连带崩溃影响其他 job。
预期系统行为: 内存分配失败的进程被内核 OOM killer 终止（exit code 137 / SIGKILL）；step 失败 → job 标记为 failure；runner 继续存活可调度后续 job。
Oracle 来源: GitCode 规格（runner-and-environment.md 资源规格表：small=2C/8G/50G）+ Linux OOM 行为惯例

验证要点:
  - [正向] OOM 被杀的 step 的 exit code 为非零（137 或等价），job status = failure
  - [正向] runner 本身不崩溃，日志完整可查
  - [负向] job 不为 success
  - [非功能] OOM 事件应出现在 step 日志中（如 "Killed" 或类似信号）

故障/压力参数: 在 `small` (2C/8G) runner 上，step 执行一个逐步分配内存直至超过 8GB 的脚本（如 `node -e 'const a=[];while(true)a.push(Buffer.alloc(1e8))'` 或 `stress --vm 1 --vm-bytes 12G --timeout 10s`）
破坏级别:   none（runner 不受永久损伤，仅本次 job 失败）
来源输入:   gitcode-spec/core-concepts/runner-and-environment.md（资源规格表）
```

### INTENT-REL-013
```
意图 ID:    INTENT-REL-013
维度标签:   [reliability]
标题:       step 填充 runner 磁盘超过 50GB（small runner 的磁盘上限）时，job 失败并给出磁盘空间相关错误

风险点:     磁盘满后 (a) 后续 step 静默失败、(b) runner agent 自身日志无法写入导致心跳丢失、(c) checkout 或 artifact 操作无声失败。
预期系统行为: 磁盘写满后，正在写的 step 收到 ENOSPC 错误并退出非零；job 标记为 failure；日志中包含 "No space left on device" 或等价信息。
Oracle 来源: GitCode 规格（runner-and-environment.md：small runner 磁盘 50GB）+ POSIX ENOSPC 行为惯例

验证要点:
  - [正向] step 因磁盘满失败（exit code != 0），job status = failure
  - [正向] 日志中包含 "No space left" 或 "disk quota exceeded" 等价信息
  - [负向] job 不为 success

故障/压力参数: 在 `small` (50GB disk) runner 上，step = `dd if=/dev/zero of=/tmp/fill bs=1M count=50000`（创建 50GB 文件填充磁盘）
破坏级别:   none
来源输入:   gitcode-spec/core-concepts/runner-and-environment.md
```

### INTENT-REL-014
```
意图 ID:    INTENT-REL-014
维度标签:   [reliability]
标题:       前一个 job 在 runner 上留下的文件残留，不污染下一次调度到同一 runner 的 job

风险点:     runner 若非完全 ephemeral，前一个 job 的工作区文件 (`$ATOMGIT_WORKSPACE`)、环境变量、临时文件可能被后一个 job 读取——隔离逃逸。spec 未明确声明 runner 是否 per-job 全新。
预期系统行为: 每个 job 获得干净的工作区；无法从 job B 访问 job A 创建的文件（`/tmp` 分享除外——本测试确认 workspace 级别隔离）。如果 runner 确实是 per-job ephemeral，则天然满足。
Oracle 来源: GitCode 规格（未明确声明 ephemeral 特性；对标 GitHub Actions hosted runner 每次使用全新 VM）

验证要点:
  - [正向] job B 的 `$ATOMGIT_WORKSPACE` 中不存在 job A 创建的文件 `/tmp/cross-job-marker`
  - [正向] job B 的环境变量中不含 job A 自定义的 job 级 env

故障/压力参数: 同 workflow 内两个串行 job（needs 依赖）；job A 步骤：创建 `marker` 文件 + 写 job 级 env；job B 步骤：检查 marker 不存在、env 不存在
优先级线索: (无直接风险项，但 runner 隔离是安全性维度的前置条件)
破坏级别:   none
来源输入:   gitcode-spec/core-concepts/runner-and-environment.md
```

---

## 5. 故障注入（混沌）

### INTENT-REL-015
```
意图 ID:    INTENT-REL-015
维度标签:   [reliability]
标题:       在 job 执行过程中 kill runner 进程，依赖该 job 的下游 job 应在超时后标记为失败，且被 kill 的 job 可重新运行恢复

风险点:     runner 进程被 kill 后，(a) 调度器可能不感知 → 下游 job 永久等待、(b) job 状态永久 stuck in_progress、(c) 重新运行仍使用同一脏状态导致再次失败。
预期系统行为: runner 被 kill 后，调度器在心跳超时（推定 60-120s）后将该 job 标记为 failure 或 cancelled；needs 依赖该 job 的下游 job 不执行（默认行为）或被跳过；重新运行（Re-run failed jobs）后，job 在干净 runner 上成功执行。
Oracle 来源: GitCode 规格（未明确声明心跳超时值，但 rerun-failed-jobs 文档描述了重新运行恢复能力）+ GitHub Actions runner 心跳惯例

验证要点:
  - [正向] 被 kill 的 job 在 180s 内到达 failure/cancelled 终态（非永久 in_progress）
  - [正向] needs 依赖链下游的 job 不执行（skipped）
  - [正向] Re-run failed jobs 后，workflow 完整成功
  - [负向] 被 kill 的 job 不保持 in_progress 超过 300s

故障/压力参数: 注入时机=job A 进入 in_progress 后 10s；注入类型=kill runner 上的 runner agent 进程（SIGKILL）；恢复预期=重新运行失败 job 成功完成
恢复预期:   Re-run failed jobs → job A 在新 runner 上成功 → 整个 workflow 终态为 success
破坏级别:   full_instance（kill runner 进程可能影响 runner 注册状态）
来源输入:   gitcode-spec/running-pipelines/rerun-failed-jobs.md
```

### INTENT-REL-016
```
意图 ID:    INTENT-REL-016
维度标签:   [reliability]
标题:       step 级故障：step 运行中网络突然不可用（drop 出站流量 60s），后续 step 应失败但 job 应正常恢复标记

风险点:     网络瞬间不可用导致 `apt-get install` / `npm install` 等 step 失败后，(a) 恢复后 continue-on-error 的 step 状态传播不正确、(b) 网络恢复后的 step 仍使用缓存或脏状态导致误判。
预期系统行为: 网络不可用期间执行的 step（如 `curl` 外部 URL）失败且 exit code 非零；`if: always()` 的后续 step 在 60s 后网络恢复时正常执行成功；job 终态正确反映 step 失败状态。
Oracle 来源: GitCode 规格（continue-on-error + if: always() 文档声明）

验证要点:
  - [正向] 网络不可用期间的 step 失败（curl 非零退出）
  - [正向] 60s 后后续 step `if: always()` 正常完成
  - [正向] job status = failure（因失败 step 未设 continue-on-error）

故障/压力参数: 注入时机=job 运行中（step 2/4 被 `curl https://example.com` 执行期间）；注入类型=iptables drop 出站流量 60s；恢复预期=网络恢复后后续步骤正常执行
恢复预期:   网络恢复后后续 step 正确执行；job 标记为 failure（如实反映失败步骤），不被误标为 cancelled
破坏级别:   fixture（修改 runner 网络规则）
来源输入:   gitcode-spec/writing-pipelines/configure-conditional-execution.md
```

### INTENT-REL-017
```
意图 ID:    INTENT-REL-017
维度标签:   [reliability]
标题:       runner 在执行 checkout 步骤前意外重启（模拟宿主宕机），workflow 可在重新运行后完成

风险点:     runner 在 checkout 前崩溃意味着工作区不存在；重新运行时 checkout 需从零开始——若平台对「未完成 checkout 的 job」有特殊处理可能出错。
预期系统行为: job 最终到达 failure/cancelled（心跳超时）；Re-run all jobs → 全部 job 在干净 runner 上从头执行，成功完成。
Oracle 来源: GitCode 规格（rerun-failed-jobs.md：重新运行整条流水线）

验证要点:
  - [正向] 因 runner 崩溃未执行的 job 最终到达终态（不 stuck）
  - [正向] Re-run all jobs → 所有 job completed(success)
  - [负向] 重新运行的 job 没有因残留状态出错

故障/压力参数: 注入时机=job 启动后、checkout 步骤执行前（5s 内 kill runner）；注入类型=kill runner 进程（模拟宿主宕机）；恢复预期=重新运行整条流水线成功
恢复预期:   Re-run all jobs 后所有 job success
破坏级别:   full_instance（影响 runner 注册状态）
来源输入:   gitcode-spec/running-pipelines/rerun-failed-jobs.md
```

### INTENT-REL-018
```
意图 ID:    INTENT-REL-018
维度标签:   [reliability]
标题:       Post 后处理阶段在 workflow 被取消时仍应执行（run_always: true）

风险点:     Post 阶段用于通知/清理/报告，若 workflow 被取消后 Post 不执行 → 告警缺失、资源泄漏。
预期系统行为: post 阶段（默认 `run_always: true`）在 workflow 到达终态后执行，包括 cancelled 终态。post 内的 step 有独立于主 job 的 runner。
Oracle 来源: GitCode 规格（core-concepts/workflow-job-step-action.md: Post 阶段默认 run_always: true）

验证要点:
  - [正向] 手动取消 in_progress 的 workflow 后，post 阶段的 step 日志可见于 Run 详情
  - [正向] post 阶段的 step 正常完成（不被跳过）
  - [负向] post 阶段不因主 workflow 被取消而跳过

故障/压力参数: workflow 包含 post 阶段（step=echo "cleanup done"）；手动 cancel workflow 在执行中；判据=post 步骤日志出现在运行的详情中
破坏级别:   none
来源输入:   gitcode-spec/core-concepts/workflow-job-step-action.md
```

---

## 6. 取消语义

### INTENT-REL-019
```
意图 ID:    INTENT-REL-019
维度标签:   [reliability]
标题:       手动取消正在执行 sleep 的 step，step 收到 SIGTERM 并在 10s 内终止，if: always() 清理步骤仍执行

风险点:     取消信号只改变了 job 状态机，但 step 进程未被实际终止 → job 卡在 cancelling 状态；清理步骤被跳过 → 资源泄漏（如临时部署未回滚）。
预期系统行为: 取消后 step 进程收到 SIGTERM；若 10s 内未退出则 SIGKILL；if: always() 的后续 step（清理步骤）在 step 被终止后执行；job 终态为 cancelled。
Oracle 来源: GitCode 规格（cancel 语义 + if: always() 文档声明）+ GitHub Actions 取消行为惯例

验证要点:
  - [正向] 被取消的 step 在 10s 内终止（日志不再追加新行）
  - [正向] if: always() 的清理 step 正常执行并完成
  - [正向] job status = cancelled
  - [负向] job 不卡在 in_progress / cancelling 超过 120s

故障/压力参数: step 布置 `sleep 600` 作为取消目标；手动取消运行；判据=清理 step 日志输出可见于详情
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-conditional-execution.md
```

### INTENT-REL-020
```
意图 ID:    INTENT-REL-020
维度标签:   [reliability]
标题:       stages.fail_fast=true 时，stage 内第一个 job 失败后同一 stage 内其他仍在运行的 job 被取消

风险点:     stages.fail_fast 是 AtomGit 特有机制，较 GitHub Actions 无对标。若实现有缺陷：(a) 取消信号漏发、(b) 取消后后续 stage 未跳过、(c) 和 strategy.fail-fast 交互冲突。
预期系统行为: stage 内 job A 失败 → 同 stage 中还在 in_progress 的 job B 收到取消信号 → job B 被 cancelled → 后续 stage 全部跳过 → workflow 终态为 failure。
Oracle 来源: GitCode 规格（core-concepts/workflow-job-step-action.md: stages.fail_fast）

验证要点:
  - [正向] job B 状态变更为 cancelled
  - [正向] 后续 stage 中的所有 job 为 skipped
  - [正向] workflow 终态为 failure（因 job A 失败）
  - [负向] job B 不跑到 completed(success)（否则取消信号未生效）

故障/压力参数: 2-stage workflow；stage1 含 job A（快失败 exit 1）和 job B（sleep 120）；stage2 含 job C；stage1.fail_fast=true
破坏级别:   none
来源输入:   gitcode-spec/core-concepts/workflow-job-step-action.md
```

---

## 7. 并发组与抢占

### INTENT-REL-021
```
意图 ID:    INTENT-REL-021
维度标签:   [reliability]
标题:       job 级 concurrency max=1 且启用抢占时，不同 workflow 的 job 排队不会死锁

风险点:     不同 workflow 间的 job 级 concurrency 若共享全局锁，可能：一个 workflow 的 job A 等待同一 workflow 的 job B，而 job B 等待 concurrency slot——死锁。或抢占事件配置不当导致可被非预期事件取消。
预期系统行为: 多个 workflow 的 job 各自在其 workflow 上下文内的 max=1 约束下排程；不存在跨 workflow 的锁争用导致的死锁。5 分钟内所有 legit 的 job 要么执行要么 queued，无 stuck。
Oracle 来源: GitCode 规格（configure-jobs.md: concurrency 是 job 级配置）

验证要点:
  - [正向] 同一 workflow 内，同一 job 不会出现两个实例同时 in_progress
  - [正向] 所有 job 在 5 分钟内到达终态或 queued
  - [负向] 无 job 永久 stuck in_progress 或 queued

故障/压力参数: 2 个不同 workflow，每个有一个 job 设 concurrency max=1；每个 workflow 各触发 2 次（共 4 个 Run）；判据=无死锁
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-jobs.md
```

---

## 8. Job 依赖失败传播

### INTENT-REL-022
```
意图 ID:    INTENT-REL-022
维度标签:   [reliability]
标题:       needs 链 (A→B→C) 中 job A 失败时，job B 和 C 默认被跳过，job C 中 if: always() 仍可执行

风险点:     失败传播逻辑错误会 (a) 跳过不该跳过的 job、(b) 执行了不该执行的 job（依赖链断裂）、(c) if: always() 在 needs 失败时行为异常。
预期系统行为: job A failure → job B skipped（默认 needs 失败行为）→ job C 也 skipped（因为 B 未成功）。但若 job C 设了 if: always() 则 C 仍被执行。
Oracle 来源: GitCode 规格（configure-dependencies-order.md：依赖 job 失败时下游默认不执行 + configure-conditional-execution.md：always() 强制执行）

验证要点:
  - [正向] job A failure → job B skipped
  - [正向] job C（无 always）skipped
  - [正向] job D（needs: [C], if: always()）正常执行
  - [负向] job B 不被标记为 success

故障/压力参数: 4-job 链 A→B→C→D；A 必然失败（exit 1）；D 设 if: always()
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-dependencies-order.md、configure-conditional-execution.md
```

### INTENT-REL-023
```
意图 ID:    INTENT-REL-023
维度标签:   [reliability]
标题:       多依赖汇聚（fan-in）：job C 依赖 A 和 B，A 成功但 B 失败时 C 被跳过

风险点:     fan-in 汇聚时「全成功才执行」的语义若实现为「任一成功即执行」→ pipeline 在不完整的前置条件下执行危险步骤（如只 build 一半就去 deploy）。
预期系统行为: A success + B failure → C 状态为 skipped。A 和 B 各自独立运行（无 needs 互相依赖）。
Oracle 来源: GitCode 规格（configure-dependencies-order.md：被依赖的 job 完成后才执行；依赖的 job 失败时默认不执行）

验证要点:
  - [正向] job C 状态为 skipped
  - [正向] job A 状态为 success
  - [负向] job C 不为 success

故障/压力参数: 3-job fan-in DAG：A（success）、B（exit 1 failure）、C（needs: [A, B]）
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-dependencies-order.md
```

### INTENT-REL-024
```
意图 ID:    INTENT-REL-024
维度标签:   [reliability]
标题:       needs 指向 matrix 父 job 时，下游 job 正确等待所有矩阵实例完成后执行（修复 TC-486 类问题）

风险点:     TC-486 报告了「needs 指向 matrix 父 job 导致任务初始化错误」——这是已知 P1 Bug。若平台未区分「指向父 job（所有实例）」和「指向具体实例」，下游 job 可能不等待全部实例完成即执行。
预期系统行为: 下游 job C（needs: [matrix-job]）在 matrix-job 所有实例全部完成后才被调度执行；C 可通过 `${{ needs.matrix-job.result }}` 获知汇总状态。
Oracle 来源: GitCode 规格（needs 依赖机制）+ GitHub Actions 行为（needs 指向 matrix job 时等待全部实例）

验证要点:
  - [正向] job C 在所有矩阵实例 completed 后才开始执行
  - [正向] job C 的 steps 日志中可见 needs 上下文正确
  - [负向] 无"任务初始化错误"（TC-486 已知问题）

故障/压力参数: 2-job workflow；job A 使用 matrix os=[ubuntu, windows] 生成 2 实例；job C needs=[A]；判据=C 等待 A 的 2 个实例全部完成
优先级线索: TC-486 (P1 Bug, 已知问题复测)
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-dependencies-order.md、existing-cases TC-486
```

---

## 9. 重新运行可靠性

### INTENT-REL-025
```
意图 ID:    INTENT-REL-025
维度标签:   [reliability]
标题:       Re-run failed jobs：仅失败 job 被重新执行，之前成功的 job 状态保留

风险点:     重新运行失败 job 时，(a) 成功的 job 被意外重跑、(b) 失败的 job 未重跑、(c) 上下文变量 (sha/ref) 不一致、(d) 版本冲突。
预期系统行为: 第一次运行：job A success、job B failure。Re-run failed jobs → job B 在新 runner 上重新执行、job A 保持原结果（日志可查看但不再执行）。
Oracle 来源: GitCode 规格（rerun-failed-jobs.md：仅重新执行失败的 job，成功 job 结果保留）

验证要点:
  - [正向] 重新运行后 job A 保持原 success 状态
  - [正向] job B 重新执行并（如果这次成功）状态变为 success
  - [正向] 重新运行使用原始 commit 的 workflow 配置
  - [负向] job A 不被重新执行

故障/压力参数: 2-job workflow（no needs 依赖，独立运行）；job A=快成功，job B 首次故意 `exit 1` 失败、修复后 success
破坏级别:   none
来源输入:   gitcode-spec/running-pipelines/rerun-failed-jobs.md
```

### INTENT-REL-026
```
意图 ID:    INTENT-REL-026
维度标签:   [reliability]
标题:       同一 Run 重新运行超过 3 次（文档声明的最大重试次数）时，第 4 次重新运行被拒绝

风险点:     若平台不限制重试次数，(a) 用户无限重试 flaky job 逃避修复、(b) 资源被重试耗尽。
预期系统行为: 前 3 次 Re-run 允许执行；第 4 次触发 Re-run 时系统拒绝，输出明确提示（如 "Maximum of 3 re-runs exceeded" 或等价信息）。
Oracle 来源: GitCode 规格（rerun-failed-jobs.md：最大重试次数 = 3）

验证要点:
  - [正向] 第 1-3 次 Re-run 均正常执行
  - [正向] 第 4 次 Re-run 被拒绝（UI 按钮禁用 / API 返回错误 / 等价拒绝信号）
  - [负向] 第 4 次 Re-run 不被实际执行

故障/压力参数: 一个注定失败的 workflow Run；连续触发 4 次 Re-run failed jobs
破坏级别:   none
来源输入:   gitcode-spec/running-pipelines/rerun-failed-jobs.md
```

### INTENT-REL-027
```
意图 ID:    INTENT-REL-027
维度标签:   [reliability]
标题:       Re-run all jobs 后，`ATOMGIT_RUN_ID` 和 `ATOMGIT_RUN_NUMBER` 更新为新值，`atomgit.sha` 保持原值

风险点:     重新运行的上下文变量不一致会导致 (a) artifact 冲突、(b) 版本号生成错误、(c) 缓存 key 碰撞。
预期系统行为: Re-run all jobs → 新 Run ID、新 run_number（递增）；`atomgit.sha` 和 `atomgit.ref` 保持与原始运行一致。
Oracle 来源: GitCode 规格（rerun-failed-jobs.md：sha/ref/event_name 保持，RUN_ID/RUN_NUMBER 更新）

验证要点:
  - [正向] 新 Run 的 run_id != 旧 Run 的 run_id
  - [正向] 新 Run 的 run_number > 旧 Run 的 run_number
  - [正向] 新旧 Run 的 atomgit.sha 相同

故障/压力参数: 先触发一次 Run，Re-run all jobs 一次；比对两次 Run 的 API 返回值中的 run_id, run_number, commit_id
破坏级别:   none
来源输入:   gitcode-spec/running-pipelines/rerun-failed-jobs.md
```

---

## 10. continue-on-error 与 job 状态传播

### INTENT-REL-028
```
意图 ID:    INTENT-REL-028
维度标签:   [reliability]
标题:       job 设 continue-on-error: true 后，即使失败也不阻断 workflow，但 needs 下游 job 中 if: success() 条件不满足

风险点:     continue-on-error 改变了失败传播语义但未改变 job 的实际 conclusion；下游 job 用 `if: success()` 或默认条件时可能误把「continue-on-error 的失败」当成功传下去。
预期系统行为: job A (continue-on-error=true) 失败 → job A status = failure 但 workflow 不因它中止；job B (needs: [A], 默认 if: success()) → B 被 skipped；job C (needs: [A], if: always()) → C 正常执行。
Oracle 来源: GitCode 规格（configure-jobs.md: continue-on-error 不影响后续 job 中 if: success() 判断）

验证要点:
  - [正向] job A failure → workflow 继续执行（不中止）
  - [正向] job B（默认 if）状态为 skipped
  - [正向] job C（if: always()）状态为 success
  - [负向] job B 不被执行（不为 success）

故障/压力参数: 3-job chain；A 失败且 continue-on-error=true；B needs A (默认条件)；C needs A (if: always())
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-jobs.md
```

---

## 11. 制品与缓存韧性

### INTENT-REL-029
```
意图 ID:    INTENT-REL-029
维度标签:   [reliability]
标题:       artifact 上传过程中 workflow 被取消，artifact 状态为 incomplete 且不污染后续下载

风险点:     半上传的 artifact 若标记为可用 → 下游 job 下载损坏的 artifact → 静默错误。
预期系统行为: workflow 被取消时，正在进行的 artifact 上传中断；该 artifact 状态为 incomplete/truncated；下游 job 或后续 Run 无法下载该 artifact（下载时明确报错）。
Oracle 来源: GitCode 规格（core-concepts/artifacts-and-cache.md）

验证要点:
  - [正向] 被取消 Run 的 artifact 不可被后续 Run 下载
  - [负向] 后续 Run 不会使用损坏的 artifact（下载报错或返回空）
  - [非功能] 错误信息包含可操作提示（如 "artifact not found or incomplete"）

故障/压力参数: workload 含上传一个大文件 (100MB) 的 step + 一个 sleep 30 的 step（给取消留窗口）；在上传到一半时手动 cancel
破坏级别:   none
来源输入:   gitcode-spec/core-concepts/artifacts-and-cache.md
```

---

## 覆盖度自检

| 覆盖类别 | 相关 Intent | 状态 |
|---------|------------|------|
| 并发洪泛触发 | REL-001, REL-002 | OK |
| concurrency QUEUE/IGNORE/CANCEL | REL-002, REL-003, REL-004 | OK |
| 大规模矩阵展开 | REL-005, REL-006 | OK |
| strategy.fail-fast | REL-007 | OK |
| strategy.max-parallel | REL-008 | OK |
| timeout-minutes | REL-009, REL-010, REL-011 | OK |
| Runner OOM | REL-012 | OK |
| Runner 磁盘满 | REL-013 | OK |
| Runner 隔离 (per-job clean) | REL-014 | OK |
| Kill runner 恢复 | REL-015, REL-017 | OK |
| 网络故障注入 | REL-016 | OK |
| Post 阶段 run_always | REL-018 | OK |
| 手动取消语义 | REL-019 | OK |
| stages.fail_fast | REL-020 | OK |
| 跨 workflow concurrency 死锁 | REL-021 | OK |
| needs 失败传播 | REL-022, REL-023 | OK |
| needs 指向 matrix 父 job | REL-024 | OK |
| Re-run failed jobs | REL-025, REL-026, REL-027 | OK |
| continue-on-error 传播 | REL-028 | OK |
| Artifact 取消中断 | REL-029 | OK |
| CPU 饱和注入 | — | 缺（需自定义 runner 上执行 `stress` 工具，平台 runner 可能未预装） |
| 缓存投毒/隔离 | — | 归入安全维度 (INTENT-SEC-xxx) |
| 自托管 runner 离线恢复 | — | 需自托管 runner 环境，暂不覆盖 |

**质量清单**：
- [x] 每个有已知配额/上限的维度都有对应 intent（timeout=360min, rerun max=3, runner spec bounded）
- [x] 每条故障注入 intent 声明了恢复预期（REL-015, REL-016, REL-017）
- [x] 参数具体（并发=5/20, 矩阵=16, timeout=5min, sleep=600s, max-parallel=3）
- [x] 破坏性 intent 标注了正确 teardown 级别（REL-015: full_instance, REL-016: fixture, REL-017: full_instance）
- [x] 平台配置缺失已在文档头部声明，受影响 intent 标注了退化（REL-001, REL-005）

**未覆盖的高风险项**：
- CPU 饱和注入：平台 Runner 未预装 `stress-ng`/`cpulimit`，但可通过 `dd if=/dev/zero of=/dev/null` 类 approximate。若有自定义 Runner 环境可补充。
- 自托管 Runner 离线恢复：需自托管环境，不在当前测试实例 scope 内。
- 调度延迟的 SLO 量化：依赖 platform-config 中的调度延迟承诺值（缺失），无法设定绝对阈值。
