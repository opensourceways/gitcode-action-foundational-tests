# 稳定性维度 Test Intent 增补 2 · BLIND-01 取消语义 step 级终止 + BLIND-11 preemption 抢占语义细节

> 产出 Agent：reliability（混沌与边界工程师）
> Run：2026-07-21-02（增量更新，不修改历史结论）
> 目标盲区：coverage.md BLIND-01 `C-EXEC-24 取消语义 step 级终止` + BLIND-11 `C-EXEC-22 preemption 抢占语义细节`
> 背景：
> - BLIND-01：历史 issues #39「显示取消成功，任务运行状态仍是队列中」；TC-391/427-430 取消后状态异常；C-EXEC-24 规格对 step 级如何终止、grace period、清理钩子保证程度语焉不详。已有 REL-029 覆盖 post 清理执行、REL-036 覆盖 schedule 取消收敛，但「step 进程终止信号机制」与「取消后状态稳定收敛」仍无 intent。
> - BLIND-11：REL-005/006/030 触及 preemption 边界（events 上限 10、抢占清理、连推抢占），但抢占触发条件（作用域/事件键匹配规则）和效果（终态/日志完整性/明确标记/runner 释放时间）未系统覆盖。
> 遵循：rules.md §5(破坏性纪律)/§8(确定性·恢复预期)/§1(ID)/§11(维度标注)；intent 模板。

---

```
意图 ID:    INTENT-REL-037
维度标签:   [reliability]
标题:       手动取消时运行中 step 进程的终止信号与 grace period 行为

风险点:     手动 Cancel 后，运行中 step 的进程若直接被 SIGKILL 终止，子进程/后台任务可能成为孤儿进程；若仅 SIGTERM 但无 grace period 或没有 fallback SIGKILL，进程可能拒绝终止导致 runner 长期被占用。post 清理钩子（workflow post + action runs.post）是否仍执行，也与终止信号机制强相关。历史问题 #39 与 TC-391/427-430 已暴露取消后状态异常，但 step 级终止语义仍无系统 intent。
预期系统行为: 取消时系统先向 step 进程组发送 SIGTERM，给予合理 grace period（如 5-10s）；若进程仍未退出，再发送 SIGKILL 强制终止。workflow post 阶段与 action runs.post 清理钩子在终止后被调用，完成资源回收。
Oracle 来源: GitCode规格（action-development/top-level-fields.md:122-144 声明 post 在主动停止时被调用；C-EXEC-24 取消语义）；GitHub Actions 行为作参照（先 SIGTERM 后 SIGKILL，约 5s grace period）。

验证要点:
  - [正向] 取消后 workflow post 阶段与 action runs.post 被调用，日志可见清理标记。
  - [负向] 运行中 step 不应在取消瞬间被无 grace period 的 SIGKILL 直接杀死（导致无清理机会），也不应仅 SIGTERM 后永不 SIGKILL 导致 runner 被僵尸进程长期占用。
  - [非功能] grace period 有界（记录 SIGTERM→SIGKILL 间隔，容差 ≤15s），runner 在取消后 60s 内释放并可调度新 job。

故障/压力参数: workflow 含长时间 step（sleep 300s + 启动子进程 `sleep 300 &`）+ post 清理（打印 cleanup marker + 扫描并 kill 残留子进程）。在 step running 30s 时手动 Cancel。观测：
  - step 终止信号序列（SIGTERM 后是否跟 SIGKILL）；
  - 子进程是否残留；
  - post 清理标记是否出现；
  - runner 释放时间（同 runner 能否在 60s 内调度新探针 job）。
  稳态判据：post 标记出现、子进程无残留、runner 60s 内可复用。
恢复预期: 优雅降级——取消后进程被有序终止，post 清理执行，runner 释放可复用。
破坏级别: fixture
来源输入: action-development/top-level-fields.md:122-144; spec.md C-EXEC-24; inputs/history/issues-encountered.md #39; baseline/case-base-detail.md TC-391/TC-427-430
优先级线索: BLIND-01（高严重度盲区），历史 bug #39 回归，建议 P1；若 grace period 缺失或 post 清理不被调用则升 P0
```

```
意图 ID:    INTENT-REL-038
维度标签:   [reliability]
标题:       取消后运行终态收敛与 runner 资源释放时限

风险点:     历史问题 #39「显示取消成功，任务运行状态仍是队列中」及 TC-391/427-430 显示取消后状态异常（永远 running 或错标 success）。若取消后状态不收敛到稳定 cancelled，用户无法判断真实状态，且 runner 资源可能长期被僵尸运行占用，影响后续调度。C-EXEC-24 规格未声明取消后状态收敛时限与 runner 释放时限。
预期系统行为: 手动 Cancel 后，运行状态在有限时间内（60s 内）稳定收敛到 cancelled 终态，不反复、不错标；runner 资源在状态收敛后 60s 内释放，可接受新 job 调度。
Oracle 来源: GitCode规格（C-EXEC-24 取消语义；job.status 上下文定义 success/failure/cancelled）；历史 issues-encountered.md #39（取消状态异常实证）。

验证要点:
  - [正向] 取消后运行终态 = cancelled，且状态稳定不跳变（连续 5 次轮询一致）。
  - [负向] 不应出现「取消成功但状态仍是 running/queued」或错标为 success/failure 的情况；不应无限占用 runner 导致新 job 无法调度。
  - [非功能] 从点击 Cancel 到终态 cancelled 的时延 ≤60s；runner 释放后能在 60s 内成功调度新探针 job。

故障/压力参数: 构造运行（job 含 sleep 180s + post 清理），在 running 30s 时手动 Cancel。连续轮询状态（每 5s，共 24 次=120s 窗口）记录：
  - 点击 Cancel 时刻；
  - 状态变化时序（running→cancelled 中间态）；
  - 终态值与稳定时间；
  - runner 可再调度时间（取消后每 10s 触发一次探针 job，记录首次成功调度时刻）。
  稳态判据：终态 = cancelled 且 60s 内稳定；runner 120s 内可复用（含状态收敛 60s + 释放 60s）。
恢复预期: 优雅降级——运行终态稳定收敛为 cancelled，runner 释放可复用；若状态不收敛记为平台缺陷。
破坏级别: fixture
来源输入: inputs/history/issues-encountered.md #39; baseline/case-base-detail.md TC-391/TC-427-430; spec.md C-EXEC-24
优先级线索: BLIND-01（高严重度盲区），历史状态异常实证，建议 P1；若复现不可收敛或 runner 长期不释放则升 P0
```

```
意图 ID:    INTENT-REL-039
维度标签:   [reliability]
标题:       preemption 抢占触发条件——事件匹配范围与作用域边界

风险点:     `concurrency.preemption.enable=true` 时，新运行触发抢占的具体条件未系统声明。`preemption.events` 配置如 `[mr_id]` 表示「同一 MR 的新运行抢占旧运行」还是「任意 MR 触发都抢占」？作用域是同一 workflow、同一仓库、同一用户还是全局？触发条件不明会导致用户无法预期何时被抢占，也可能出现「不该抢的却被抢」（跨仓库误杀）或「该抢的不抢」（同 MR 排队堆积）。C-EXEC-22 规格仅给出配置示例，抢占触发条件与效果均「模糊」。
预期系统行为: 抢占触发条件有明确边界——同一 concurrency group 内（由 workflow + 事件键决定），当新运行满足 `preemption.events` 中声明的事件键且并发已达 max 时，触发抢占；不跨仓库、不跨用户、不跨 workflow 误杀。被抢占运行有明确「被抢占」事件记录。
Oracle 来源: GitCode规格（workflow-file-location-structure.md:176-188；platform-config/README.md:12；C-EXEC-22）；GitHub Actions `concurrency.cancel-in-progress` 行为作参照（同一 concurrency group 内新运行取消旧运行）。

验证要点:
  - [正向] 同一 workflow、同一 MR（preemption.events=[mr_id]）的新运行触发时，旧运行被抢占取消。
  - [负向] 不同 workflow、不同仓库、不同 MR ID 的新运行不应抢占本仓库/本 MR 的运行（不跨边界误杀）。
  - [非功能] 被抢占运行有明确「被抢占」标记或事件记录，用户可理解为何被取消。

故障/压力参数: 配置 preemption.enable=true, max=1, events=[mr_id]。构造四组触发场景，每组旧运行 A 先触发并在 running 30s 后触发新运行 B：
  (a) 同一 workflow + 同一 MR ID 再次 push — 应抢占旧运行 A
  (b) 同一 workflow + 不同 MR ID 触发 — 不应抢占旧运行 A
  (c) 不同 workflow（同仓库）+ 同一 MR ID — 是否抢占需实测坐实
  (d) 同一 workflow + 同一 MR ID 但由不同用户触发 — 是否抢占需实测坐实
  记录每组 A 的终态（cancelled/running/completed）与 B 的调度结果。稳态判据：场景 (a) A 被抢占；(b)(c)(d) A 不被抢占，或行为一致可预期且有文档支持。
恢复预期: 不适用（条件边界验证；若跨边界误杀记为调度缺陷）。
破坏级别: fixture
来源输入: workflow-file-location-structure.md:176-188; platform-config/README.md:12; spec.md C-EXEC-22; coverage.md BLIND-11
优先级线索: BLIND-11（preemption 部分），触发条件未系统覆盖，建议 P1；若确认跨边界误杀不可恢复则升 P0
```

```
意图 ID:    INTENT-REL-040
维度标签:   [reliability]
标题:       preemption 被抢占 job/run 的终态、日志完整性与 runner 释放时效

风险点:     被抢占的 running job 若终止不彻底，可能终态不明确（cancelled vs failed vs success）、日志截断丢失关键信息（如被抢占瞬间的输出）、无明确标记导致用户误以为是代码错误；runner 若未及时释放则造成资源假占用。REL-006 已覆盖「抢占清理与恢复」，但未系统覆盖「终态+日志+标记+释放时间」四维效果。C-EXEC-22 与 C-EXEC-24 规格均未声明被抢占 job 的终态语义与日志保留策略。
预期系统行为: 被抢占 job/run 的终态稳定为 cancelled（或明确标记为 preempted/cancelled），日志完整保留至被抢占瞬间（不截断、不丢失），UI/日志中有明确「被抢占」归因标记，runner 在 job 终止后 60s 内释放并可调度新 job。
Oracle 来源: GitCode规格（workflow-file-location-structure.md:176-188；job.status 上下文定义 cancelled；C-EXEC-22/C-EXEC-24）；GitHub Actions cancel-in-progress 行为作参照（终态 cancelled、日志保留、标记明确）。

验证要点:
  - [正向] 被抢占 job 终态 = cancelled，且状态稳定不跳变；runner 释放后可调度新 job。
  - [负向] 被抢占 job 不应错标为 success/failure，不应日志被截断导致被抢占瞬间的输出丢失，不应无标记导致用户无法区分「代码失败」与「被抢占」。
  - [非功能] 从抢占发生到 runner 释放 ≤60s；日志可下载且包含被抢占前的完整输出（不截断至 0 行）；UI 有明确 cancelled/preempted 标记。

故障/压力参数: preemption.enable=true, max=1, events=[mr_id]。先触发运行 A（job 内含连续打印序号 step，每 1s 打印一行序号 + 时间戳，共 300s；另配 post 清理打印 marker），A running 30s 后触发同一 MR 的运行 B 触发抢占。观测：
  - A 的终态与状态稳定性（连续轮询 5 次）；
  - A 的日志行数（应接近 30 行，不截断至 0 行或仅前几行）；
  - A 的日志/UI 是否有 cancelled/preempted 归因标记；
  - A 的 runner 在抢占后多久可调度新探针 job（每 10s 触发一次探针，记录首次成功时刻）。
  稳态判据：终态=cancelled、日志完整（≥25 行且含被抢占前最后输出）、标记明确、runner 60s 内释放。
恢复预期: 优雅降级——被抢占 job 终态明确、日志完整、runner 释放可复用；抢占者 B 正常运行。
破坏级别: fixture
来源输入: workflow-file-location-structure.md:176-188; platform-config/README.md:12; spec.md C-EXEC-22/C-EXEC-24; coverage.md BLIND-11
优先级线索: BLIND-11（preemption 部分），抢占效果未系统覆盖，建议 P1；若 runner 不释放或日志截断不可恢复则升 P0
```

---

## 增补说明

- **ID 接续**：REL-036 为已有最后一条，本增补从 REL-037 起编，共 4 条。
- **与已有 intent 不重复**：
  - REL-029 覆盖「取消/抢占时 post 清理钩子的执行保证」，侧重 post 是否被调用；REL-037 深入「step 进程终止信号机制 + grace period」，与 REL-029 互补而非重复。
  - REL-036 覆盖「schedule 触发收敛与取消语义」，侧重 schedule 运行触发后可取消；REL-038 覆盖「任意手动取消后的状态收敛与 runner 释放时限」，通用化到所有触发类型。
  - REL-005 覆盖「preemption.events 上限 10 的边界」；REL-006/030 覆盖「抢占清理/连推抢占」。REL-039/040 分别聚焦「触发条件作用域边界」与「被抢占效果四维验证」，与 REL-005/006/030 互补。
- **参数具体化**：
  - grace period 容差 ≤15s（REL-037）；
  - 取消后状态收敛时限 ≤60s、runner 释放时限 60s（REL-038）；
  - 抢占后 runner 释放时限 ≤60s、日志行数判据 ≥25 行（REL-040）。
- **破坏级别**：4 条均涉及取消/preemption，标 `fixture`（需重置夹具仓库的运行残留）。
- **优先级建议**：
  - REL-037/038 关联 BLIND-01 高严重度盲区 + 历史 #39 取消状态异常，建议 P1；若复现不可恢复（无 grace period/post 不执行/状态不收敛/runner 不释放）则升 P0。
  - REL-039/040 关联 BLIND-11 preemption 细节盲区，建议 P1；若确认跨边界误杀或 runner 不释放不可恢复则升 P0。
- **每条故障/边界 intent 声明恢复预期**：
  - REL-037：优雅降级——进程有序终止，post 清理执行，runner 释放可复用。
  - REL-038：优雅降级——终态稳定收敛为 cancelled，runner 释放可复用。
  - REL-039：不适用（条件边界验证；若跨边界误杀记为调度缺陷）。
  - REL-040：优雅降级——被抢占 job 终态明确、日志完整、runner 释放可复用；抢占者正常运行。
