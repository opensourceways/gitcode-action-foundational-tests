# 稳定性维度 Test Intent 库 · GitCode Action

> 产出 Agent：reliability（混沌与边界工程师）
> Run：2026-07-21-02
> 来源输入：
> - `inputs/platform-config/README.md`（2026-07-21）——配额/上限具体数值源
> - `inputs/gitcode-spec/`（fetched 2026-07-20）——容量规格、runner 架构
> - `inputs/business-context/README.md`（2026-07-21）——真实负载模式
> - 本 run `intents/spec.md`——能力清单 C-QUOTA-*、缺口 G-07~G-14/G-19/G-34
> 遵循：rules.md §5(破坏性纪律)/§8(确定性·恢复预期)/§1(ID)/§11(维度标注)；testing-focus.md §3/§4/§12；intent 模板。

## 破坏性纪律声明（rules §5）
本维度在**独立、可随意破坏/重置的测试实例**上设计。每条 intent 显式声明 `破坏级别`：
- `none`——不破坏共享状态，仅消耗本 run 配额（并发/超时/规模类多为此）。
- `fixture`——需重置夹具仓库（污染缓存/制品/工作区残留）。
- `full_instance`——需重置整个实例（磁盘满、runner 崩溃、资源池耗尽等实例级影响）。
故障注入类 intent 均按 rules §8 声明 `恢复预期 recovery_expectation`，否则无法判定通过。

## 参数纪律（护栏）
所有压力/故障参数均为**具体数值**，引用 platform-config 原值：
`concurrency.max=5` / `preemption.events=10` / `job timeout=360min` / `rerun≤3次·6h` /
`paths 匹配前 300 文件` / `step 输出 1MB/参数` / flavor 规格（slim 1C4G20G ~ 2xlarge 32C128G1T）。
未公开上限项（G-07~G-13）用**探测型 intent**：渐进加压逼近实际上限并验证越限行为清晰。

## 覆盖索引
- 配额边界/越界（已公开值）：REL-001 ~ REL-009
- 探测型（未公开上限，渐进加压）：REL-010 ~ REL-019
- 故障注入（混沌，带恢复预期）：REL-020 ~ REL-026
- 执行模型竞态/大规模/隔离：REL-027 ~ REL-033

---

## 一、配额边界 / 越界 intent（参数源：platform-config 已公开值）

```
意图 ID:    INTENT-REL-001
维度标签:   [reliability]
标题:       concurrency.max 边界值 1 与 5 的并发限制生效性

风险点:     concurrency.max 声明范围 1-5。边界值 max=1（完全串行）与 max=5（上限）若限流器实现有 off-by-one，可能放行第 6 个或错误串行化，导致资源争用或吞吐不达标。
预期系统行为: max=1 时同一 concurrency group 严格串行（同一时刻至多 1 个 running）；max=5 时至多 5 个并行、第 6 个按 exceed-action 处置。
Oracle 来源: GitCode规格（workflow-file-location-structure.md:167-188；platform-config/README.md:10-11）

验证要点:
  - [正向] max=5 并发触发 5 次时 5 个同时 running，无排队。
  - [负向] max=5 时第 6 个并发触发不应同时进入 running（不得越限并行）。
  - [非功能] max=1 触发 3 次，running 数恒为 1，其余 QUEUED，串行完成顺序稳定。

故障/压力参数: max=1（触发 3 次）与 max=5（触发 6 次）两组；同一 concurrency group；每个 job 内含 60s sleep 制造稳定并发窗口观察 running 计数。稳态判据：任一采样时刻 running ≤ max。
恢复预期: 不适用（非故障注入；纯边界）。
破坏级别: none
来源输入:   platform-config/README.md:10-11；spec.md C-QUOTA-01/C-EXEC-21
```

```
意图 ID:    INTENT-REL-002
维度标签:   [reliability]
标题:       concurrency.max 越界值（0 / 6 / 非整数）的校验拒绝

风险点:     platform-config 限定 max∈[1,5]，但未声明 max=0、max=6、max=2.5、max="abc" 的处理。若校验缺失，可能静默取边界（clamp）、放行任意并发或崩溃解析，破坏并发保护。
预期系统行为: 越界值应在校验层被明确拒绝并给出可操作报错，而非静默 clamp 或放行未定义并发。
Oracle 来源: GitCode规格（platform-config/README.md:11 声明范围 1-5）

验证要点:
  - [正向] max=1、max=5 正常受理。
  - [负向] max=6 不应被静默接受产生 6 路并发；max=0 不应导致全部无法调度或无限并行。
  - [非功能] 报错应指明合法范围 1-5，而非泛化 YAML 错误。

故障/压力参数: 分别提交 max∈{0, 6, 2.5, "abc", -1} 五个变体 workflow，各并发触发 6 次；观察实际 running 峰值与报错文案。稳态判据：每个越界值产生确定结果（拒绝或文档化 clamp），无未定义并发。
恢复预期: 不适用（边界校验类）。
破坏级别: none
来源输入:   platform-config/README.md:11；spec.md INTENT-COMP-002 关联
```

```
意图 ID:    INTENT-REL-003
维度标签:   [reliability]
标题:       exceed-action=QUEUE 超额排队的公平性与不丢失

风险点:     concurrency.max=2、exceed-action=QUEUE 时，并发触发 10 次，超出的 8 个应排队而非丢弃。若队列有容量上限（未声明）或调度不公平，可能丢运行、饿死或乱序。
预期系统行为: 10 次触发全部最终执行（0 丢失），任一时刻 running≤2，排队者按 FIFO 或声明顺序被消费。
Oracle 来源: GitCode规格（platform-config/README.md:11 concurrency_exceed_action: QUEUE）

验证要点:
  - [正向] 10 次触发最终全部完成，无丢失。
  - [负向] 任一采样时刻 running 不应 >2。
  - [非功能] 排队消费顺序稳定可预期，无运行被无限饿死（每个在合理时限内被调度）。

故障/压力参数: max=2、exceed-action=QUEUE、同一 group；短时并发触发 10 次（每 job 30s sleep）；记录每次运行的 queued→running→completed 时间线。稳态判据：completed 总数=10 且 running 峰值=2。
恢复预期: 不适用（配额降级行为，非故障）。
破坏级别: none
来源输入:   platform-config/README.md:11；spec.md C-QUOTA-01
```

```
意图 ID:    INTENT-REL-004
维度标签:   [reliability]
标题:       exceed-action=IGNORE 超额忽略的行为一致性

风险点:     exceed-action=IGNORE 时超出 max 的触发应被忽略（不排队、不执行）。若忽略语义不清，可能变成静默丢失且无任何记录，用户无法感知运行未发生。
预期系统行为: 超出 max 的触发被明确忽略，且在运行历史/日志有可观测记录（非静默黑洞）。
Oracle 来源: GitCode规格（platform-config/README.md:11 IGNORE 分支）

验证要点:
  - [正向] max=2、并发触发 5 次时，恰 2 个执行。
  - [负向] 被忽略的 3 次不应进入 running，也不应在无任何痕迹下消失。
  - [非功能] 被忽略的触发应有可观测状态（如标记为 ignored/skipped），可理解。

故障/压力参数: max=2、exceed-action=IGNORE、同一 group、并发触发 5 次（每 job 30s sleep）。稳态判据：running 峰值=2，且被忽略数=3 有记录。
恢复预期: 不适用。
破坏级别: none
来源输入:   platform-config/README.md:11；spec.md C-QUOTA-01
```

```
意图 ID:    INTENT-REL-005
维度标签:   [reliability]
标题:       preemption.events 上限 10 的边界与越界（11 个）

风险点:     preemption.events 最多配置 10 个。配 10 个（边界）应生效；配 11 个（越界）未声明处理。抢占配置错误可能导致该抢占不抢占，运行卡占资源。
预期系统行为: 10 个 preemption 事件全部生效并可触发抢占；第 11 个应被校验拒绝或明确截断并告知，而非静默丢弃部分事件。
Oracle 来源: GitCode规格（platform-config/README.md:12；workflow-file-location-structure.md:176-188）

验证要点:
  - [正向] 配置恰 10 个 preemption 事件时，每个都能正确触发抢占。
  - [负向] 配置 11 个时不应静默只生效前 10 个而无提示。
  - [非功能] 超限报错指明「preemption.events 上限 10」。

故障/压力参数: 两组——preemption.events 数=10 与 =11；分别触发抢占条件，观察抢占是否发生与报错文案。稳态判据：10 个组全部可抢占；11 个组产生确定拒绝或明确告知。
恢复预期: 不适用（配置边界）。
破坏级别: none
来源输入:   platform-config/README.md:12；spec.md C-QUOTA-02/C-EXEC-22
```

```
意图 ID:    INTENT-REL-006
维度标签:   [reliability]
标题:       concurrency 抢占（preemption）取消运行中 job 的清理与恢复

风险点:     preemption.enable=true 时新运行抢占旧运行。被抢占的 running job 若终止不彻底，可能残留进程/占用工作区/未跑 post 清理，污染后续 job；抢占也可能误杀不该杀的运行。
预期系统行为: 被抢占运行的 running step 被终止，post/action.post 清理钩子被调用，资源释放；抢占者正常获得资源运行。
Oracle 来源: GitCode规格（workflow-file-location-structure.md:176-188；top-level-fields.md:110-144 post 清理）

验证要点:
  - [正向] 抢占发生后，抢占者成功 running，被抢占者进入 cancelled 终态。
  - [负向] 被抢占 job 不应留下运行中的孤儿进程或锁住工作区导致下一次运行失败。
  - [非功能] 被抢占 job 的 post/cleanup 钩子应被调用（日志可见清理动作）。

故障/压力参数: preemption.enable=true、max=1；先触发运行 A（job 内 sleep 120s + 注册 post 清理打印），在 A running 30s 时触发满足 preemption 条件的运行 B；观察 A 是否 cancelled、post 是否执行、B 是否顺利 running。
恢复预期: 优雅降级——A 被取消并完成清理（post 执行、进程回收），B 正常运行；实例无残留，无需 full_instance 重置。
破坏级别: fixture
来源输入:   platform-config/README.md:12；spec.md C-EXEC-22/C-EXEC-24/G-15
```

```
意图 ID:    INTENT-REL-007
维度标签:   [reliability]
标题:       job timeout-minutes 边界：接近 360 分钟默认超时与显式短超时的强制终止

风险点:     job 默认 timeout=360min，超时强制终止。若超时计时不准或终止不彻底，长时 job 可能超期仍占用 runner（资源泄漏）或提前被杀（误判）。360min 实测过长，用显式短超时验证机制，并对默认值做声明一致性抽验。
预期系统行为: job 运行至 timeout-minutes 时被强制终止并标记超时失败；未达时限正常完成；终止后 runner 资源释放。
Oracle 来源: GitCode规格（configure-jobs.md:110-121；platform-config/README.md:15）

验证要点:
  - [正向] timeout-minutes=2、job sleep 60s 时正常成功（未超时）。
  - [负向] timeout-minutes=1、job sleep 300s 时不应跑满 300s，应在 ~60s 被终止。
  - [非功能] 超时终止后状态为超时失败（非泛化 failure），且 runner 立即可接新 job。

故障/压力参数: 三组 timeout-minutes∈{1, 2, 5}，job 内 sleep 分别为 {300s, 60s, 30s}；测量实际终止时刻与设定值偏差（容差 ±15s）。默认 360min 仅做声明抽验（不实跑满 6h）。稳态判据：终止时刻在 timeout±15s。
恢复预期: 优雅降级——超时后 job 判失败、runner 释放可复用，无孤儿进程。
破坏级别: fixture
来源输入:   platform-config/README.md:15-16；spec.md C-QUOTA-03/C-EXEC-04
```

```
意图 ID:    INTENT-REL-008
维度标签:   [reliability]
标题:       rerun 次数上限 3 与 6 小时时效边界

风险点:     单条运行最多重跑 3 次、超 6h 不可重跑。若计数错误可能允许第 4 次重跑（资源滥用）或提前锁死；6h 时效边界若判断不准，临界运行的可重跑性不确定。
预期系统行为: 前 3 次重跑受理，第 4 次被拒绝并告知已达上限；运行年龄≤6h 可重跑、>6h 明确拒绝。
Oracle 来源: GitCode规格（platform-config/README.md:19-20；rerun-failed-jobs.md:11-47）

验证要点:
  - [正向] 对一条失败运行连续重跑 3 次均被受理。
  - [负向] 第 4 次重跑不应被受理（不得超限）。
  - [非功能] 达上限/超时效的拒绝信息应指明具体原因（次数用尽 / 超 6h）。

故障/压力参数: 构造一条稳定失败的运行（step 显式 exit 1），连续 Re-run 4 次记录第 4 次结果；6h 时效边界因实测成本高，标注为「若实例支持时钟推进则验证，否则记为待实测」。稳态判据：重跑计数在第 4 次拒绝。
恢复预期: 不适用（配额上限，非故障恢复）。
破坏级别: fixture
来源输入:   platform-config/README.md:19-20；spec.md C-QUOTA-04/C-OBS-06
```

```
意图 ID:    INTENT-REL-009
维度标签:   [reliability]
标题:       paths 过滤「前 300 个变更文件」边界与越界（301+ 命中不触发）

风险点:     paths 仅匹配前 300 个变更文件，超出不参与判断。单次 push 变更 >300 文件时，第 301+ 个命中 paths 的文件不触发——「该触发却没触发」的静默边界，CI 可能漏跑。
预期系统行为: 命中文件位于前 300 内正常触发；仅第 301+ 命中（前 300 不命中）按声明不触发，且此截断行为一致、可复现。
Oracle 来源: GitCode规格（configure-triggers.md:181-207；platform-config/README.md:26）

验证要点:
  - [正向] 变更 300 文件、其中含 paths 命中项时正常触发。
  - [负向] 单次 push 变更 350 文件、paths 命中项仅在第 301-350 位（前 300 均不命中）时，不触发。
  - [非功能] 截断边界稳定（多次复现结果一致），评估是否有任何提示。

故障/压力参数: 构造单 push 变更文件数 = {300, 301, 350}；命中 paths 的文件分别精确置于第 300、第 301 位；paths 过滤形如 `**/trigger-target/**`。稳态判据：第 300 位命中触发、第 301 位命中不触发，边界锐利。
恢复预期: 不适用（触发边界）。
破坏级别: fixture
来源输入:   platform-config/README.md:26；spec.md C-QUOTA-05/C-TRIG-10；关联 INTENT-COMP-003
```

---

## 二、探测型 intent（未公开上限 · 渐进加压逼近实际上限并验证越限行为清晰）

> 说明：以下 10 条针对 platform-config「文档未公开·待实测」项与 spec.md 缺口 G-07~G-13。方法：**几何级/阶梯式渐进加压**，记录首个失败点作为实测上限，并验证越限行为是「明确报错」而非「静默截断/挂死/污染」。每条给出加压序列与停止条件。

```
意图 ID:    INTENT-REL-010
维度标签:   [reliability]
标题:       [探测] matrix 组合数上限——渐进加压找实际上限与越限行为

风险点:     文档仅示例矩阵展开算法，未声明组合数上限（G-10）。超大 matrix 可能被平台拒绝、静默截断部分组合（漏跑）、或压垮调度器。用户无从预估安全规模。
预期系统行为: 存在某个可预期的组合数上限；达到上限时给出明确报错（而非静默只展开一部分组合）；上限内全部组合都被调度。
Oracle 来源: 未知·待实测（platform-config/README.md:32 未公开；GitHub 惯例 256 作对比参照）

验证要点:
  - [正向] 小规模矩阵（如 2×2×2=8）全部组合正确展开并各生成一个 job 实例。
  - [负向] 超大矩阵不应静默只展开部分组合而不告知用户（漏跑是最危险的静默失败）。
  - [非功能] 达上限时报错指明「矩阵组合数超限」，并给出实测上限值。

故障/压力参数: 组合数阶梯加压序列 = {8, 64, 256, 512, 1024}（用多维 matrix + include 构造）；每档记录：实际生成 job 实例数是否=声明组合数、是否报错、报错文案。设 max-parallel=2 限制真实并发以控成本。停止条件：出现拒绝/截断即记为实测上限。稳态判据：展开实例数=组合数，或在上限处明确报错。
恢复预期: 不适用（容量探测）。
破坏级别: none
来源输入:   platform-config/README.md:32；spec.md G-10/C-EXEC-15/C-QUOTA-08
```

```
意图 ID:    INTENT-REL-011
维度标签:   [reliability]
标题:       [探测] 账户/仓库级全局并发上限——多 workflow 并发洪泛找实际上限

风险点:     仅有单 workflow 的 concurrency.max=1-5，无账户/仓库级全局并发上限声明（G-11）。大量不同 workflow 同时触发时，是否有全局限流？无上限可能耗尽 runner 池；有隐藏上限则超出者排队/丢失且用户不知。
预期系统行为: 存在可观测的全局调度行为——要么无全局上限（受 runner 池自然限制并公平排队），要么有明确上限且超出者排队不丢失。
Oracle 来源: 未知·待实测（platform-config/README.md:30 明确未公开）

验证要点:
  - [正向] 同时触发 N 个不同 workflow（各 1 job）时，全部最终执行完成，0 丢失。
  - [负向] 超出调度能力的运行不应静默消失（无排队无记录）。
  - [非功能] 并发洪泛下调度公平（无 workflow 被长期饿死），排队时限可观测。

故障/压力参数: 并发触发不同 workflow 数量阶梯 = {10, 30, 50, 100}（各 job 含 30s sleep）；记录同时 running 峰值、queued 深度、总完成数、最长排队等待时间。停止条件：出现丢失或饿死。稳态判据：完成总数=触发总数。
恢复预期: 不适用（容量探测）。
破坏级别: none
来源输入:   platform-config/README.md:30；spec.md G-11/C-QUOTA-07；business-context 真实负载（多仓多 workflow 并发）
```

```
意图 ID:    INTENT-REL-012
维度标签:   [reliability, usability]
标题:       [探测] step 输出超 1MB/参数的行为——截断 vs 报错

风险点:     ATOMGIT_OUTPUT 每参数上限 1MB，但超限行为未声明（G-12）。若静默截断，下游 job 读到不完整数据却无感知，产生错误结果；若崩溃则 job 无端失败。
预期系统行为: 写入超 1MB 的单参数应有确定行为——明确报错或文档化截断并告知，不产生静默的数据损坏。
Oracle 来源: 未知·待实测（platform-config/README.md:29 仅给上限，超限行为未声明）

验证要点:
  - [正向] 写入恰 1MB（1048576 字节）参数，下游经 needs.<job>.outputs 完整读取。
  - [负向] 写入 2MB 参数不应让下游静默读到被截断数据而无任何警告。
  - [非功能] 超限若截断，日志应有明确提示；若报错，应指明「输出超 1MB」。

故障/压力参数: 单参数字节数阶梯 = {1048575(1MB-1), 1048576(1MB), 1048577(1MB+1), 2097152(2MB), 10485760(10MB)}；每档下游 job 校验实际收到字节数与内容 hash。稳态判据：≤1MB 完整传递；>1MB 有确定且可观测的处置。
恢复预期: 不适用（输出边界）。
破坏级别: none
来源输入:   platform-config/README.md:29；spec.md G-12/C-ART-04/C-QUOTA-06
```

```
意图 ID:    INTENT-REL-013
维度标签:   [reliability]
标题:       [探测] 制品（artifact）大小上限——渐进加压找上限与越限行为

风险点:     文档仅称「已确认制品大小不超过限制」，无具体数值（G-07）。上传超大制品可能超时、静默失败（upload 步骤显示成功但 download 拿不到）、或耗尽存储。
预期系统行为: 存在可预期的制品大小上限；超限时 upload-artifact 步骤明确失败并告知，而非「上传假成功、下载失败」。
Oracle 来源: 未知·待实测（upload-download-artifacts.md:10；platform-config/README.md:34）

验证要点:
  - [正向] 上传 100MB 制品后能在另一 job 完整 download 并校验 hash。
  - [负向] 超上限的制品不应 upload 显示成功却 download 失败/损坏（假成功是最坏情形）。
  - [非功能] 超限报错指明制品大小上限值。

故障/压力参数: 制品大小阶梯 = {100MB, 500MB, 1GB, 5GB, 10GB}（用 dd/fallocate 生成确定大小文件）；每档做 upload→另 job download→hash 校验的闭环。注意单文件不得超 runner 磁盘（small=50G，大制品用 medium/large flavor）。停止条件：首个 upload 失败或 download 校验失败。稳态判据：upload 成功 ⇒ download 必然完整。
恢复预期: 不适用（容量探测）。
破坏级别: fixture
来源输入:   platform-config/README.md:34；spec.md G-07/C-ART-04
```

```
意图 ID:    INTENT-REL-014
维度标签:   [reliability]
标题:       [探测] 缓存（cache）容量上限与 LRU 淘汰行为

风险点:     缓存「长期保留、LRU 淘汰」，容量上限未公开（G-08）。写入超容量缓存后，LRU 淘汰边界、被淘汰缓存的 restore 未命中处理若不清晰，会造成缓存抖动、构建忽快忽慢的 flaky。
预期系统行为: 存在容量上限，超出后按 LRU 淘汰最久未用条目；被淘汰后 restore 未命中应正常回退到重新生成（不报错、不卡死）。
Oracle 来源: 未知·待实测（artifacts-and-cache.md:36-42；platform-config/README.md:35）

验证要点:
  - [正向] 单条缓存写入后同仓库另一运行能 restore 命中。
  - [负向] 累计写入超容量后，最久未用缓存被淘汰，其 restore 未命中不应报错而应回退重建。
  - [非功能] LRU 行为可预期，缓存命中率不随机抖动（去 flaky）。

故障/压力参数: 依次写入 N 个不同 key 的缓存（每个 1GB），N 阶梯 = {5, 10, 20, 50}；每轮后回读最早写入 key 是否仍命中，定位淘汰阈值。稳态判据：找到累计容量阈值，且淘汰后 restore 优雅未命中。
恢复预期: 不适用（容量探测；淘汰后回退重建是正常路径）。
破坏级别: fixture
来源输入:   platform-config/README.md:35；spec.md G-08/C-ART-06
```

```
意图 ID:    INTENT-REL-015
维度标签:   [reliability, usability]
标题:       [探测] 单 step 日志量上限——超长日志的截断/落盘/查看

风险点:     max_log_size 未公开（G-09）。step 打印海量日志时，可能拖垮日志采集、UI 卡死、日志被静默截断导致关键错误信息丢失，影响可观测性与调试。
预期系统行为: 存在日志量上限或分页机制；超限时截断应有明确「日志已截断」标记，且不影响 job 成败判定与运行稳定。
Oracle 来源: 未知·待实测（platform-config/README.md:33）

验证要点:
  - [正向] 中等日志量（如 10 万行）完整可查看、可搜索、可下载。
  - [负向] 海量日志不应导致运行卡死/UI 不可用，也不应无标记地丢失尾部关键行。
  - [非功能] 截断时有明确提示，关键的最终错误行仍可见。

故障/压力参数: 单 step 输出行数/字节阶梯 = {1e4 行, 1e5 行, 1e6 行, ~100MB, ~500MB}（用 yes/seq 生成）；每档记录：UI 是否可加载、是否截断及标记、下载日志完整性、job 是否仍正常完成。稳态判据：运行不受日志量影响成败，截断有标记。
恢复预期: 不适用（容量探测）。
破坏级别: none
来源输入:   platform-config/README.md:33；spec.md G-09/C-OBS-03
```

```
意图 ID:    INTENT-REL-016
维度标签:   [reliability, usability]
标题:       [探测] workflow 文件大小上限——超大 YAML 的解析行为

风险点:     max_workflow_file_size 未公开（G-09）。超大 workflow 文件（超多 job/step 或深嵌套）可能解析超时、被拒绝或静默截断，用户无从预估可维护的编排规模。
预期系统行为: 存在文件大小/复杂度上限；超限时明确拒绝并指明原因，不静默解析一部分。
Oracle 来源: 未知·待实测（platform-config/README.md:36）

验证要点:
  - [正向] 含 100 个 job 的合法大文件能被完整解析并调度。
  - [负向] 超限文件不应被静默只解析前若干 job（漏跑）。
  - [非功能] 超限报错指明文件大小/结构上限。

故障/压力参数: workflow 文件规模阶梯——job 数 = {50, 100, 500, 1000}，对应文件体积逐步增大；每档记录是否解析成功、调度 job 数是否=定义数、报错文案。停止条件：首个被拒绝或截断。稳态判据：解析成功 ⇒ 调度 job 数=定义数。
恢复预期: 不适用（解析边界）。
破坏级别: none
来源输入:   platform-config/README.md:36；spec.md G-09/C-STRUCT-02
```

```
意图 ID:    INTENT-REL-017
维度标签:   [reliability]
标题:       [探测] 单仓 secret 数量上限——渐进添加找上限

风险点:     max_secrets_per_repo 未公开（G-09）。大量 secret 的项目达到隐藏上限时，新增 secret 失败若无明确提示，或已配 secret 在运行时解析变慢/失败，影响可用性。
预期系统行为: 存在 secret 数量上限；达上限时新增被明确拒绝并告知；上限内所有 secret 运行时均可正常解析。
Oracle 来源: 未知·待实测（platform-config/README.md:37）

验证要点:
  - [正向] 配置 N 个 secret 后，workflow 能逐个正确解析引用。
  - [负向] 达上限后新增 secret 不应静默失败（看似添加成功实则未生效）。
  - [非功能] 达上限报错指明单仓 secret 数上限。

故障/压力参数: 项目级 secret 数量阶梯 = {10, 50, 100, 200}；每档新增一批后跑一个引用全部 secret 的 workflow 校验解析。停止条件：新增被拒或运行时解析失败。稳态判据：找到上限值且越限有明确反馈。
恢复预期: 不适用（数量探测）。
破坏级别: fixture
来源输入:   platform-config/README.md:37；spec.md G-09/C-SEC-01
```

```
意图 ID:    INTENT-REL-018
维度标签:   [reliability]
标题:       [探测·故障] Runner 内存超限（OOM）行为与恢复

风险点:     flavor 规定内存（slim 4G ~ 2xlarge 128G），但 OOM 行为未声明（G-13）。job 内存超 flavor 上限时，可能被 OOM kill 但状态语义不清（是超时？失败？无解释），或拖垮整个 runner 影响后续 job。
预期系统行为: job 内存超 flavor 上限时被明确终止并标记为资源不足类失败（可理解），runner 在该 job 结束后恢复可用，不影响后续 job。
Oracle 来源: 未知·待实测（runner-and-environment.md:19-28；platform-config/README.md:50-57 flavor 规格；G-13）

验证要点:
  - [正向] small flavor（8G）下分配 6G 的 job 正常完成。
  - [负向] small flavor 下分配 12G（超 8G）的 job 不应静默 hang 或产生无解释的泛化失败。
  - [非功能] OOM 失败信息应可归因到内存超限；runner 事后可正常接新 job。

故障/压力参数: 固定 small flavor（8G）；job 内用 `stress-ng --vm 1 --vm-bytes {6G, 8G, 12G, 16G}` 逐级施压；记录终止时机、退出状态语义、runner 后续可用性。稳态判据：≤8G 内正常，超限被明确终止且可归因。
恢复预期: 优雅降级——超内存 job 被终止判失败并给出可归因信息，runner 事后可复用（无需 full_instance）；若托管 runner 崩溃需重建，则升级 full_instance。
破坏级别: full_instance
来源输入:   platform-config/README.md:50-57；spec.md G-13/C-RUN-14
```

```
意图 ID:    INTENT-REL-019
维度标签:   [reliability]
标题:       [探测·故障] Runner 磁盘写满行为与恢复

风险点:     flavor 规定磁盘（slim 20G ~ 2xlarge 1T），但磁盘满行为未声明（G-13）。checkout 大仓/生成大文件/写制品占满磁盘时，可能 job 无解释失败、工作区损坏、或残留污染同主机后续 job（自托管场景尤甚）。
预期系统行为: 磁盘写满时 job 明确失败并归因到磁盘不足；工作区在 job 结束后被清理，不残留污染后续 job。
Oracle 来源: 未知·待实测（platform-config/README.md:50-57 disk_gb；G-13）

验证要点:
  - [正向] small flavor（50G 磁盘）写 40G 文件正常完成。
  - [负向] 写 60G（超 50G）不应产生无解释失败或损坏工作区残留到下个 job。
  - [非功能] 磁盘满失败可归因；后续同 runner 的 job 有干净工作区（RUNNER_TEMP 清空）。

故障/压力参数: 固定 small flavor（50G）；job 内 `fallocate`/`dd` 逐级写 {40G, 50G, 60G} 直至写满；随后在同 runner（若可复用）调度一个探针 job 检查工作区是否干净。稳态判据：≤容量正常，超容量明确失败且不污染后续。
恢复预期: 优雅降级——磁盘满 job 判失败并归因，工作区清理，后续 job 环境干净；若污染残留则记为隔离缺陷（关联 G-15）。
破坏级别: full_instance
来源输入:   platform-config/README.md:50-57；spec.md G-13/C-RUN-14/G-15
```

---

## 三、故障注入 intent（混沌 · 每条声明恢复预期 recovery_expectation，rules §8）

> 说明：注入维度 = 注入时机（job 前/中/后）× 故障类型（kill runner / 网络分区 / 磁盘满 / CPU 饱和 / 依赖不可用）× 恢复预期（重试成功 / 优雅降级 / 明确报错）。磁盘满已在 REL-019 覆盖，本组补齐其余类型。

```
意图 ID:    INTENT-REL-020
维度标签:   [reliability]
标题:       [故障] job 执行中 kill runner——运行状态收敛与可重跑

风险点:     job 运行到一半时 runner 进程被杀/主机宕机（自托管尤其常见）。若平台侧运行状态不收敛，可能永远卡在 running（僵尸运行），占用并发额度且用户无法感知失败；或状态错标成功。
预期系统行为: runner 失联后，运行在合理时限内被判定为失败/中断（非无限 running），用户可重跑；不产生僵尸运行占用并发。
Oracle 来源: 未知·待实测（GitCode 未系统声明 runner 失联处理；GitHub 行为作参照）

验证要点:
  - [正向] 正常 job 完成后状态收敛为 success。
  - [负向] runner 被 kill 后运行不应无限停留在 running（僵尸），也不应错标为 success。
  - [非功能] 失联到判失败的时限有界（记录实测心跳超时窗口）。

故障/压力参数: job 内 sleep 180s；在 running 到 60s 时对承载该 job 的 runner 进程执行 kill -9（自托管）或强制下线；观察运行多久后被判失败、是否可 Re-run 成功。注入时机=job 中。稳态判据：运行在心跳超时窗口内收敛为失败终态。
恢复预期: 明确报错 + 可重试——运行判为失败/中断并释放并发额度，Re-run 后能在健康 runner 上成功完成。
破坏级别: full_instance
来源输入:   spec.md C-RUN-12/G-15；testing-focus §12（kill runner）；platform-config self_hosted_runner
```

```
意图 ID:    INTENT-REL-021
维度标签:   [reliability]
标题:       [故障] 拉取 action/依赖时网络分区——超时与失败归因

风险点:     job 在 `uses:` 拉取第三方 action、或 setup-* 下载工具链/包时遭遇网络分区。若无超时会无限 hang 直到 job timeout（浪费 6h 额度）；失败若不归因，用户误以为是代码问题。
预期系统行为: 网络不可达时下载步骤在合理超时内失败并归因到网络/拉取失败，不 hang 到 job timeout；瞬时抖动应有重试。
Oracle 来源: 未知·待实测（GitCode 未声明 action 拉取重试/超时策略）

验证要点:
  - [正向] 网络正常时 action 拉取与依赖下载成功。
  - [负向] 网络分区时不应静默 hang 至 360min job timeout 才失败。
  - [非功能] 失败信息归因到网络/下载（非泛化 failure）；瞬时故障有重试痕迹。

故障/压力参数: 两组注入——(a) 永久分区：注入前置阻断对 action registry / 依赖源的出站（防火墙 drop），观察下载步骤失败时限；(b) 瞬时抖动：注入 30s 网络中断后恢复，观察是否重试成功。注入时机=job 中（步骤前）。稳态判据：(a) 有界超时失败并归因；(b) 恢复后重试成功或明确失败。
恢复预期: 瞬时抖动→重试成功；永久分区→有界超时后明确报错（归因网络），不占满 job timeout。
破坏级别: fixture
来源输入:   spec.md C-ACT-06/C-ACT-08；testing-focus §12（网络分区）；platform-config network_egress
```

```
意图 ID:    INTENT-REL-022
维度标签:   [reliability]
标题:       [故障] 平台依赖服务不可用（cache / artifact 服务）时的降级

风险点:     cache 服务或 artifact 服务临时不可用时，若 cache/upload-artifact 步骤硬失败并阻断整个 job，会把「加速/传递」这类非关键路径故障放大为构建失败；理想应可降级。
预期系统行为: cache 服务不可用时 restore/save 应优雅降级（未命中→照常构建，不阻断 job）；artifact 服务不可用时应明确失败并归因，可重试。
Oracle 来源: 未知·待实测（GitCode 未声明后端服务降级策略；cache 语义「未命中则重建」作参照）

验证要点:
  - [正向] 服务正常时 cache 命中、artifact 上传下载成功。
  - [负向] cache 服务故障不应导致整个 job 失败（缓存是优化非依赖）。
  - [非功能] artifact 服务故障时失败归因清晰、支持重跑恢复。

故障/压力参数: 注入 cache/artifact 后端服务不可达（阻断对应服务端点）；分别跑 (a) 含 cache restore+save 的 job，(b) 含 upload/download-artifact 的 job；注入时机=对应 step 执行时。稳态判据：cache 故障→job 仍成功（降级）；artifact 故障→明确失败可重试。
恢复预期: 优雅降级（cache）——未命中照常构建；明确报错 + 可重试（artifact）——恢复后重跑成功。
破坏级别: fixture
来源输入:   spec.md C-ART-05/C-ART-06/C-ART-01；testing-focus §12（依赖不可用）
```

```
意图 ID:    INTENT-REL-023
维度标签:   [reliability]
标题:       [故障] CPU 饱和——同 flavor 下的资源争用与稳态维持

风险点:     job 打满 flavor 的全部 CPU（如 small=2 核跑满）时，运行是否被限流/降速但仍完成，还是被误判超时/杀死。自托管同主机多 job 共享环境时，一个 job 的 CPU 饱和可能拖垮邻居 job（噪声邻居）。
预期系统行为: CPU 饱和使 job 变慢但不被误杀；托管隔离下不影响其他 job；自托管共享主机下的相互影响可观测、有界。
Oracle 来源: 未知·待实测（platform-config flavor CPU 规格；C-RUN-12 共享环境）

验证要点:
  - [正向] small flavor 跑满 2 核 CPU 密集任务能正常完成（只是慢）。
  - [负向] CPU 饱和不应导致 job 被误判为超时/失败（除非真超 job timeout）。
  - [非功能] 托管隔离下饱和 job 不影响同批其他 job 时长；自托管共享主机影响有界可观测。

故障/压力参数: 固定 small flavor（2 核）；job A 用 `stress-ng --cpu 4 --timeout 120s` 超额打满；同时并发 job B 做基准计时任务；对比 B 在 A 饱和 vs 空闲时的耗时差。注入时机=job 中。稳态判据：A 完成不被误杀；托管下 B 耗时不受 A 影响。
恢复预期: 优雅降级——饱和期间降速但完成，饱和解除后恢复正常吞吐；无误杀。
破坏级别: fixture
来源输入:   platform-config/README.md:51-57；spec.md C-RUN-12；testing-focus §12（CPU 饱和）
```

```
意图 ID:    INTENT-REL-024
维度标签:   [reliability, security]
标题:       [故障·探测] 网络出站范围——外网/内网/DNS 可达性与中断行为

风险点:     仅声明「有访问外网权限」，出站范围/内网/DNS/代理未详（G-14）。用户不知能否访问私有制品库/内网服务；出站被限时若无明确报错，表现为神秘 hang。
预期系统行为: 出站可达性有可预期边界（外网可达、内网视策略）；被阻断的出站应快速失败并归因，而非长时 hang。
Oracle 来源: 未知·待实测（platform-config/README.md:97 仅一句；G-14）

验证要点:
  - [正向] 访问公网端点（如 https 公共服务）成功。
  - [负向] 访问不可达/被限制的地址不应无限 hang（应有连接超时）。
  - [非功能] DNS 解析失败、连接超时的报错可归因；探明内网是否可达。

故障/压力参数: 探针 job 依次尝试 = {公网 HTTPS 端点、内网私有地址段 10.x/192.168.x、不存在域名(DNS 失败)、被防火墙 drop 的端口}；记录各自成功/超时/拒绝与耗时。注入时机=job 中。稳态判据：各类目标有确定结果，失败快速归因（连接超时有界）。
恢复预期: 明确报错——不可达目标在连接超时（有界）后失败并归因（DNS/网络/超时），不 hang 至 job timeout。
破坏级别: none
来源输入:   platform-config/README.md:97；spec.md G-14/C-RUN-13；testing-focus §4
```

```
意图 ID:    INTENT-REL-025
维度标签:   [reliability]
标题:       [故障] container 私有镜像 registry 不可用/拉取超时

风险点:     job 用 container 自定义镜像时，若私有 registry 不可用或镜像拉取超时/认证失败，job 在启动阶段（step 执行前）即失败。此类「job 前」故障若归因不清，用户误以为是 workflow 语法问题。
预期系统行为: 镜像拉取失败在 job 启动阶段明确报错并归因（registry 不可达 / 认证失败 / 镜像不存在），瞬时故障有重试。
Oracle 来源: 未知·待实测（configuring-images-toolchains.md:9-52 container 拉取；C-RUN-09/C-RUN-10）

验证要点:
  - [正向] 有效镜像 + 正确 credentials 时 container job 正常启动运行。
  - [负向] registry 不可达时不应静默 hang 或报泛化错误。
  - [非功能] 区分「registry 不可达 / 认证失败 / 镜像 tag 不存在」三类错误并各自归因。

故障/压力参数: 三组注入——(a) registry 端点阻断，(b) credentials 用错误 secret，(c) 引用不存在的 image tag；注入时机=job 前（容器启动阶段）；记录失败时限与归因文案。稳态判据：三类各产生确定且可区分的报错。
恢复预期: 明确报错（三类可区分）；registry 瞬时抖动→重试成功。
破坏级别: fixture
来源输入:   spec.md C-RUN-09/C-RUN-10/C-SEC-12；testing-focus §4/§12
```

```
意图 ID:    INTENT-REL-026
维度标签:   [reliability]
标题:       [故障] needs 依赖 job 失败的传播与 if:always 恢复路径

风险点:     DAG 中上游 job 失败时，下游默认不执行（失败传播）。若传播语义有误——下游被错误执行、或 `if: always` 的恢复/清理 job 未被执行——会导致资源未清理或错误结果被下游消费。
预期系统行为: 上游失败时，未声明 `if: always` 的下游 job 被跳过（不执行）；声明 `if: always` 的下游（清理/通知）仍执行；多依赖汇聚时任一失败即阻断非 always 下游。
Oracle 来源: GitCode规格（configure-jobs.md:74-95；configure-dependencies-order.md:77-144；C-EXEC-02）

验证要点:
  - [正向] 上游成功时下游正常执行；上游失败时 `if: always` 的清理 job 仍运行。
  - [负向] 上游失败时，普通下游 job 不应被执行（不得消费失败上游的产物）。
  - [非功能] 多依赖（B,C→D）中 B 失败 C 成功时，D（非 always）被跳过，状态标注清晰。

故障/压力参数: 构造 DAG：A→B、A→C(cleanup, if:always)、[B,C]→D；注入 A 中 step 显式 exit 1；观察 B/D 是否跳过、C 是否执行。注入时机=job 前（依赖判定）。稳态判据：B 跳过、C 执行、D 跳过，与声明一致。
恢复预期: 优雅降级——失败沿 DAG 正确传播，`if: always` 清理路径保证执行（资源被清理），无孤儿产物被下游消费。
破坏级别: fixture
来源输入:   spec.md C-EXEC-02/C-EXEC-03/C-EXPR-03；testing-focus §3
```
_（本批为最后追加，见下文第四、五节）_

---

## 四、执行模型竞态 / 大规模 / 隔离 intent

```
意图 ID:    INTENT-REL-027
维度标签:   [reliability]
标题:       matrix strategy.fail-fast 语义——一实例失败取消其余的确定性

风险点:     strategy.fail-fast 默认值未声明（G-02，GitHub 惯例为 true）。fail-fast=true 时一实例失败应取消其余；若默认值不明或取消不彻底，用户不知失败时其余组合是否已浪费执行，且被取消实例的清理不确定。
预期系统行为: fail-fast=true 时任一实例失败立即取消其余运行中/待运行实例；fail-fast=false 时其余实例跑完；默认值行为需实测坐实。
Oracle 来源: 差异确认（GitCode 未声明默认值，需实测；GitHub 默认 true 作参照）（configure-matrix-builds.md:110-121；G-02）

验证要点:
  - [正向] fail-fast=true、3×1 矩阵中第 1 个失败时，其余 2 个被取消。
  - [负向] fail-fast=false 时一实例失败不应连带取消其余实例。
  - [非功能] 不显式声明 fail-fast 时的默认行为可复现（实测坐实默认=true 或 false）。

故障/压力参数: 5 组合矩阵（如 version:[1,2,3,4,5]），令 version=3 的 step 显式 exit 1；三组配置 fail-fast∈{true, false, 未声明}；记录其余实例的终态（cancelled/completed/skipped）。稳态判据：true→其余 cancelled；false→其余 completed；未声明→行为一致可复现。
恢复预期: 不适用（执行语义，非故障恢复）。
破坏级别: fixture
来源输入:   spec.md G-02/C-EXEC-18；testing-focus §3
```

```
意图 ID:    INTENT-REL-028
维度标签:   [reliability]
标题:       stages.fail_fast 跨 stage 失败传播语义

风险点:     stages.fail_fast 默认值未声明（G-01）。true=立即终止本 stage 其他 job 并跳过后续所有 stage；false=本 stage 其他 job 继续但后续 stage 不执行。语义复杂且默认不明，易导致「以为后续 stage 会跑」的误判。
预期系统行为: fail_fast=true 时本 stage 其余 job 立即终止 + 后续 stage 全跳过；false 时本 stage 其余 job 跑完但后续 stage 不执行；默认值实测坐实。
Oracle 来源: GitCode规格（configure-dependencies-order.md:150-154；G-01）

验证要点:
  - [正向] fail_fast=false 时，失败 job 所在 stage 的其余 job 仍跑完。
  - [负向] 无论 true/false，失败后的后续 stage 都不应执行。
  - [非功能] 默认值行为可复现坐实。

故障/压力参数: 两 stage（stage1 含 job_a/job_b/job_c、stage2 含 job_d），令 job_a exit 1；三组 fail_fast∈{true, false, 未声明}；记录 job_b/job_c（同 stage）与 job_d（后续 stage）的终态。稳态判据：与声明矩阵一致，默认值坐实。
恢复预期: 不适用（执行语义）。
破坏级别: fixture
来源输入:   spec.md G-01/C-STRUCT-06；testing-focus §3
```

```
意图 ID:    INTENT-REL-029
维度标签:   [reliability]
标题:       取消/抢占时 post 清理钩子的执行保证

风险点:     手动停止或抢占取消运行中 step 时，post 阶段 / action.post 清理钩子是否被调用未系统声明（C-EXEC-24 标模糊）。清理不执行会导致临时资源泄漏（挂载/登录态/临时凭据未回收）。
预期系统行为: 运行被手动取消或抢占时，post 阶段与 action 的 post 清理入口被调用，完成资源回收；清理本身有超时保护不无限挂起。
Oracle 来源: GitCode规格（top-level-fields.md:110-144；workflow-file-location-structure.md:142-165；C-EXEC-24）

验证要点:
  - [正向] 正常完成时 post 清理执行。
  - [负向] 取消/抢占时 post 清理不应被跳过（导致资源泄漏）。
  - [非功能] 清理钩子有自身超时，不因清理挂起阻塞 runner 释放。

故障/压力参数: workflow 含主 job（sleep 120s）+ post（打印清理标记 + 删临时文件）；在主 job running 30s 时手动 Cancel；检查 post 标记是否出现、临时资源是否回收。注入时机=job 中取消。稳态判据：post 清理被执行且有界完成。
恢复预期: 优雅降级——取消后清理钩子执行、资源回收，runner 释放可复用。
破坏级别: fixture
来源输入:   spec.md C-EXEC-24/C-ACT-13/C-STRUCT-07；testing-focus §3（取消语义）
```

```
意图 ID:    INTENT-REL-030
维度标签:   [reliability]
标题:       同一 push 连推的触发去重/幂等与并发触发排队公平性

风险点:     连推去重/幂等行为未声明（G-34）。短时间对同一分支连续推送多次，若每次都触发完整运行且无去重/抢占，会造成运行堆积、资源浪费；用户期望「后推的取代前推的」（类似 cancel-in-progress）但 GitCode 语义未明。
预期系统行为: 连推行为可预期——要么全部触发（配 concurrency 控制），要么按 concurrency+preemption 让新推抢占旧推；无论哪种都不产生失控堆积。
Oracle 来源: 未知·待实测（configure-triggers.md:138；G-34；C-TRIG-13）

验证要点:
  - [正向] 单次 push 触发恰一次运行。
  - [负向] 5 秒内连推 5 次不应产生失控的运行堆积且无任何并发管控。
  - [非功能] 配 concurrency+preemption 时，新推能抢占/排队旧推，行为可预期。

故障/压力参数: 对同一分支在 5s 内连续 push 5 次（每次微小变更）；分别在 (a) 无 concurrency、(b) concurrency.max=1+preemption.enable=true 两组下观察触发运行数、running 峰值、被抢占数。稳态判据：(a) 触发数可预期；(b) 至多 1 running，旧推被抢占/排队。
恢复预期: 不适用（触发调度语义）。
破坏级别: fixture
来源输入:   platform-config/README.md:10-12；spec.md G-34/C-TRIG-13/C-EXEC-22
```

```
意图 ID:    INTENT-REL-031
维度标签:   [reliability]
标题:       [大规模] 超多 step 的单 job 稳定性

风险点:     单 job 含极多 step 时（业务中生成式流水线常见），可能命中 step 数隐藏上限、状态跟踪开销拖慢调度、或日志/UI 渲染退化。step 数上限未公开。
预期系统行为: 大量 step 顺序执行全部完成，step 间 outcome/conclusion 状态正确跟踪，无静默跳过；若有上限则明确报错。
Oracle 来源: 未知·待实测（无 step 数上限声明；C-EXEC-08）

验证要点:
  - [正向] 含 200 个 run step 的 job 全部按序执行完成。
  - [负向] 不应静默跳过中间某些 step 或丢失其状态。
  - [非功能] step 数增大时单 step 调度开销无明显劣化（记录首个 step 到末个 step 的额外开销）。

故障/压力参数: 单 job step 数阶梯 = {50, 200, 500, 1000}，每 step 打印序号；校验实际执行 step 数=定义数、顺序正确。停止条件：出现跳过/上限拒绝。稳态判据：执行数=定义数且有序。
恢复预期: 不适用（规模探测）。
破坏级别: none
来源输入:   spec.md C-EXEC-08；testing-focus §12（超多 step）
```

```
意图 ID:    INTENT-REL-032
维度标签:   [reliability]
标题:       [大规模] 超大仓库 checkout 的磁盘/时间边界

风险点:     checkout 超大仓库（深历史/大二进制）时，可能超 flavor 磁盘（slim 20G/small 50G）、fetch 耗时过长逼近 job timeout，或浅克隆 fetch-depth 行为不符预期导致后续步骤缺历史失败。
预期系统行为: 仓库大小在 flavor 磁盘内时 checkout 成功；超磁盘时明确失败（归因磁盘不足，见 REL-019）；fetch-depth 参数按声明控制克隆深度以规避超限。
Oracle 来源: GitCode规格（C-ACT-09 checkout fetch-depth；platform-config flavor disk_gb）

验证要点:
  - [正向] 仓库 + 历史合计 <50G 时 small flavor 全量 checkout 成功。
  - [负向] fetch-depth=1 浅克隆不应拉全历史导致磁盘超限。
  - [非功能] checkout 耗时可测，超大仓建议用更大 flavor 或浅克隆，边界可给出指引。

故障/压力参数: 夹具仓库大小阶梯 = {5G, 30G, 45G}（含大二进制历史）；small flavor（50G）下分别做 fetch-depth=1 与全量 checkout；记录成功/失败、磁盘占用峰值、耗时。稳态判据：<磁盘容量成功、浅克隆显著降占用。
恢复预期: 不适用（规模边界；超限恢复归 REL-019）。
破坏级别: fixture
来源输入:   spec.md C-ACT-09/C-RUN-14；platform-config flavor_specs；testing-focus §12（超大仓库 checkout）
```

```
意图 ID:    INTENT-REL-033
维度标签:   [reliability, security]
标题:       托管 Runner 跨 job 复用的残留污染——去 flaky 隔离验证

风险点:     托管 Runner 是否 ephemeral、跨 job 残留污染未声明（G-15），仅 RUNNER_TEMP 每 job 清空为线索。若 runner 复用且工作区/环境变量/全局安装/进程未清理，前一 job 的残留会污染后一 job，制造 flaky（时好时坏）与安全隐患（前 job 泄露的凭据被后 job 读到）。
预期系统行为: 每个 job 获得干净环境——工作区无前 job 残留文件、RUNNER_TEMP 清空、无前 job 遗留进程、无前 job 写入的全局状态泄漏。
Oracle 来源: 未知·待实测（using-self-hosted-runners.md:144-153；runtime-environment-variables.md:51；G-15）

验证要点:
  - [正向] job N 在干净工作区启动，无 job N-1 的文件。
  - [负向] job N 不应读到 job N-1 写入工作区/临时目录/全局路径的残留（含敏感数据）。
  - [非功能] 连续 100 次相同 job 结果一致（无因残留导致的 flaky）。

故障/压力参数: 探针序列——job_A 在工作区、RUNNER_TEMP、$HOME、全局 PATH 写入标记文件与哨兵变量并起一个后台进程；紧接调度 job_B 扫描上述位置是否存在 A 的残留；重复 100 轮统计残留出现率。注入时机=job 间（复用点）。稳态判据：残留出现率=0，100 轮结果一致。
恢复预期: 不适用（隔离验证；若发现残留则记为隔离缺陷，关联 security G-15）。
破坏级别: full_instance
来源输入:   spec.md G-15/C-RUN-12；testing-focus §4（runner 生命周期/残留污染）
```

---

## 五、覆盖矩阵（配额维度 × 边界/越界/探测/故障）

| 配额/机制维度 | 已公开值 | 边界 | 越界 | 探测(未公开) | 故障/恢复 | intent |
|---|---|---|---|---|---|---|
| concurrency.max | 1-5 | ✓ | ✓ | — | — | REL-001/002 |
| exceed-action QUEUE/IGNORE | 有 | ✓ | ✓ | — | — | REL-003/004 |
| preemption.events | ≤10 | ✓ | ✓ | — | — | REL-005 |
| preemption 抢占清理 | — | — | — | — | ✓ | REL-006 |
| job timeout-minutes | 360 | ✓ | ✓ | — | ✓ | REL-007 |
| rerun 次数/时效 | 3次/6h | ✓ | ✓ | — | — | REL-008 |
| paths 匹配 | 300 文件 | ✓ | ✓ | — | — | REL-009 |
| matrix 组合数 | 未公开 | — | — | ✓ G-10 | — | REL-010 |
| 全局/账户并发 | 未公开 | — | — | ✓ G-11 | — | REL-011 |
| step 输出 | 1MB | ✓ | ✓ | ✓ G-12 | — | REL-012 |
| artifact 大小 | 未公开 | — | — | ✓ G-07 | — | REL-013 |
| cache 容量 | 未公开 | — | — | ✓ G-08 | — | REL-014 |
| 日志大小 | 未公开 | — | — | ✓ G-09 | — | REL-015 |
| workflow 文件大小 | 未公开 | — | — | ✓ G-09 | — | REL-016 |
| 单仓 secret 数 | 未公开 | — | — | ✓ G-09 | — | REL-017 |
| Runner 内存/OOM | flavor 值 | — | ✓ | ✓ G-13 | ✓ | REL-018 |
| Runner 磁盘满 | flavor 值 | — | ✓ | ✓ G-13 | ✓ | REL-019 |
| kill runner | — | — | — | — | ✓ | REL-020 |
| 网络分区(拉取) | — | — | — | — | ✓ | REL-021 |
| 依赖服务不可用 | — | — | — | — | ✓ | REL-022 |
| CPU 饱和 | — | — | — | — | ✓ | REL-023 |
| 网络出站范围 | 未公开 | — | — | ✓ G-14 | ✓ | REL-024 |
| registry 不可用 | — | — | — | — | ✓ | REL-025 |
| needs 失败传播 | 有 | — | — | — | ✓ | REL-026 |
| matrix fail-fast | 默认未声明 | ✓ | — | ✓ G-02 | — | REL-027 |
| stages.fail_fast | 默认未声明 | ✓ | — | ✓ G-01 | — | REL-028 |
| post 清理钩子 | 模糊 | — | — | — | ✓ | REL-029 |
| 连推去重/幂等 | 未公开 | — | — | ✓ G-34 | — | REL-030 |
| 超多 step | 未公开 | — | — | ✓ | — | REL-031 |
| 超大仓库 checkout | flavor 磁盘 | ✓ | — | — | — | REL-032 |
| Runner 复用残留 | 未声明 | — | — | ✓ G-15 | — | REL-033 |

## 六、交接说明
- **展开归 case-writer**：每条 intent 的「故障/压力参数」已给具体加压序列/注入方式与稳态判据，可直接派生 YAML（含 positive/negative/nonfunctional 三类断言与 `teardown.reset`）。
- **探测型 intent（10 条：REL-010~019 除 018/019 外的 8 条 + REL-024/030/031/033）**：结论应回写 platform-config 未公开项与 spec.md 缺口 G-07~G-14/G-34，坐实实测上限值。
- **破坏级别分布**：`none` 9 条 / `fixture` 15 条 / `full_instance` 4 条（REL-018/019/020/033，实例级影响，需整实例重置）。
- **优先级线索**：risk-register 当前为模板态，各条暂无法对齐具体 RISK-；建议门禁据 testing-focus §12 稳定性专项与 platform-config 配额权威性定级（并发/超时/隔离残留倾向 P0/P1）。
- **输入版本**：platform-config 2026-07-21；gitcode-spec fetched 2026-07-20。若刷新按 rules §12 重审带该来源标注项（尤其未公开上限若被官方补充，探测型 intent 转为边界/越界型）。
