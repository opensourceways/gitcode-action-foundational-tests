# 稳定性维度 Test Intent 增补 · BLIND-07 schedule/cron 回归验证

> 产出 Agent：reliability（混沌与边界工程师）
> Run：2026-07-21-02（增量更新，不修改历史结论）
> 目标盲区：coverage.md BLIND-07 `C-TRIG-08 schedule/cron 完整语义`
> 背景：历史记录显示 Scheduler 整体不工作（NEEDS-UPDATE E 类，cases.md 问题 §S3×24，TC-391/TC-427-474/TC-505-512），本轮 160 条 intent 未覆盖 schedule 回归验证。COMPAT-SCHEDULE-02-001 已覆盖「时区差异/默认分支/最短间隔」兼容差异，但未覆盖 cron 运算符边界、最小间隔 enforcement、调度真正触发及取消收敛。
> 遵循：rules.md §5(破坏性纪律)/§8(确定性·恢复预期)/§1(ID)/§11(维度标注)；intent 模板。

---

```
意图 ID:    INTENT-REL-034
维度标签:   [reliability, completeness]
标题:       cron 表达式运算符边界——标准运算符（`*/5` `L` `W` `#`）生效、静默忽略或报错

风险点:     历史记录显示 Scheduler 整体不工作（S3×24、TC-391），导致文档已声明的运算符 `*` `,` `-` `/`（TC-471~474）及 8 组特殊符号（TC-505-512）全部无法验证；此外标准 cron 扩展运算符 `L`（最后日）、`W`（最近工作日）、`#`（第N个星期几）在 GitCode 规格中未声明支持与否。修复后若部分运算符被静默忽略或解析错误，用户配置的定时规则将与预期严重偏离，产生漏触发或误触发。
预期系统行为: 文档已声明的 `*` `,` `-` `/` 按 POSIX cron 语义解析并触发；`L`/`W`/`#` 要么生效要么在校验/调度阶段明确报错，绝不静默降级为 `*` 或忽略；不支持的 6-field 格式或 `?` 给出确定拒绝。
Oracle 来源: GitCode规格（syntax-reference/trigger-events.md:266-275 声明 `*` `,` `-` `/` 及最短间隔 5min；C-TRIG-08）；历史 NEEDS-UPDATE（TC-471~474、TC-505-512）实证缺陷；GitHub Actions 标准 5-field cron 语义作参照。

验证要点:
  - [正向] `*/5`（步长）、`1,3,5`（列表）、`1-5`（范围）、`*`（任意）在修复后于预期 UTC 时刻触发运行；运行日志中 `atomgit.event.schedule` 包含原 cron 表达式。
  - [负向] 不应复现历史「配置合法 cron 但运行历史永远空白」故障；`L`/`W`/`#` 不应被静默当作 `*` 处理导致高频误触发。
  - [非功能] 不支持的运算符（如 `?` 或 6-field 格式）在 YAML 保存或调度首触阶段给出明确报错，而非解析通过但调度层忽略。

故障/压力参数: 构造 8 组 cron 表达式变体，部署于默认分支，观察 30 分钟窗口：
  1. `*/5 * * * *` — 步长（文档已声明）
  2. `0 0 L * *` — 最后日（标准扩展，未声明）
  3. `0 0 * * 1W` — 最近工作日（标准扩展，未声明）
  4. `0 0 * * 1#2` — 第 2 个周一（标准扩展，未声明）
  5. `0 2,14 * * *` — 列表（文档已声明）
  6. `0 9-17 * * 1-5` — 范围（文档已声明）
  7. `? * * * *` — 不支持符号（应拒绝）
  8. `0 * * * * *` — 6-field（应拒绝）
  稳态判据：组 1/5/6 在 30min 内按声明时刻触发（容差 ±3min，含文档声明的「数分钟调度延迟」）；组 2/3/4 要么触发要么明确拒绝；组 7/8 在校验阶段明确拒绝。
恢复预期: 不适用（配置边界与回归验证类；若某运算符被误拒，修正 cron 后重部署即可恢复）。
破坏级别: none
来源输入: baseline/case-base-detail.md（TC-471~474、TC-505-512 NEEDS-UPDATE）；inputs/gitcode-spec/syntax-reference/trigger-events.md:266-275；coverage.md BLIND-07
优先级线索: BLIND-07（高严重度盲区），历史 bug 回归，建议 P1
```

```
意图 ID:    INTENT-REL-035
维度标签:   [reliability]
标题:       schedule 最小调度间隔 enforcement——低于 5 分钟的拒绝/排队/降级行为

风险点:     GitCode 规格声明 schedule 最短间隔为 5 分钟（trigger-events.md:275；TC-429 历史 FAIL 未验证）。若修复后平台仍不支持 <5min 却未拒绝，可能静默降级为 5min（用户无感知）、直接忽略部分触发（漏跑），或不受限地每分钟触发导致 Runner 资源被无限占用。历史 Scheduler 完全不工作时该 enforcement 从未被实测。
预期系统行为: cron 间隔低于 5 分钟（如 2min、1min）时，在 YAML 校验阶段或调度首触阶段明确拒绝/提示；若被静默降级，实际触发间隔不得 <5min 且日志应有明确标记。绝不出现「配置通过但永不触发」或「无限制高频触发」的未定义行为。
Oracle 来源: GitCode规格（syntax-reference/trigger-events.md:275「schedule 的最短间隔为 5 分钟」；C-TRIG-08）；历史 TC-429 NEEDS-UPDATE。

验证要点:
  - [正向] `*/5 * * * *`（5 分钟间隔）在 15 分钟窗口内触发约 3 次，行为稳定可预期。
  - [负向] `*/2 * * * *`（2 分钟）与 `* * * * *`（1 分钟）不应不受限地产生每分钟一次运行；不应静默无触发。
  - [非功能] 若拒绝，报错文案应指明「cron 间隔不得小于 5 分钟」或类似信息；若降级，运行日志/调度记录应有「间隔被调整为 5 分钟」的明确标记。

故障/压力参数: 三组 cron 部署于默认分支，观察 15 分钟窗口：
  (a) `*/5 * * * *` — 基准 5min（应触发 3 次）
  (b) `*/2 * * * *` — 2min，低于声明阈值
  (c) `* * * * *` — 1min，极限高频
  记录实际触发次数、触发时刻间隔、校验阶段是否报错。稳态判据：(a) 触发次数≈3，间隔≈5min；(b)(c) 要么在保存/校验阶段被拒绝，要么实际最小触发间隔≥5min 且有降级标记。
恢复预期: 不适用（配置边界类；修正 cron 间隔≥5min 后重部署恢复）。
破坏级别: none
来源输入: baseline/case-base-detail.md（TC-429 NEEDS-UPDATE）；inputs/gitcode-spec/syntax-reference/trigger-events.md:275；coverage.md BLIND-07
优先级线索: BLIND-07（高严重度盲区），历史 bug 回归，建议 P1
```

```
意图 ID:    INTENT-REL-036
维度标签:   [reliability, completeness]
标题:       schedule 触发收敛与取消语义——Scheduler 修复后调度运行可达终态

风险点:     历史 observed 为「Scheduler 整体不工作」——配置 cron 后从未产生 Schedule Run（S3×24、TC-391/TC-427-430）。修复后必须验证：调度任务不仅被登记，还要在到达触发时刻后真正触发运行；运行触发后若手动取消，状态必须从 running 收敛到 cancelled，runner 资源释放，而非永远卡在 running 或错标为 success（类似历史问题 #39「显示取消成功，任务运行状态仍是队列中」的变体）。
预期系统行为: cron 到达触发时刻后，在合理延迟内（含文档声明的「数分钟调度延迟」，观测上限 5min）产生 schedule 事件运行；运行正常执行 step；用户在 running 阶段手动 Cancel 后，运行状态收敛为 cancelled，post 清理钩子被执行，runner 资源在 60s 内释放并可接新 job。
Oracle 来源: GitCode规格（C-TRIG-08 schedule 触发；C-EXEC-24 取消语义；configure-triggers.md:137-138「数分钟调度延迟」）；历史 TC-391/TC-427-430/TC-562-563 NEEDS-UPDATE；inputs/history/issues-encountered.md #39（取消状态异常）。

验证要点:
  - [正向] 配置 `*/5 * * * *` 后，在 15 分钟窗口内至少触发 1 次 schedule 运行；运行日志可查看；`atomgit.event_name == 'schedule'`；`atomgit.event.schedule` 包含原表达式。
  - [负向] 不应复现历史「cron 配置正确但运行历史永远空白」故障；取消后不应无限停留在 running，也不应错标为 success/failure。
  - [非功能] 触发延迟可观测（记录计划 UTC 时刻与实际 running 时刻差，上限 5min）；取消后 runner 在 60s 内释放并可调度新 job。

故障/压力参数: 部署 schedule workflow（默认分支，cron=`*/5 * * * *`），job 内含 sleep 180s + 写标记文件 step + post 清理（删除标记文件并打印 cleanup log）。在运行进入 running 后 30s 执行手动 Cancel。观测：
  - 15min 内触发次数 ≥1；
  - 计划时刻与实际 running 时刻差 ≤5min；
  - 取消后终态 = cancelled；
  - post 清理日志出现且标记文件被删除；
  - 取消后 60s 内同 runner 可成功调度新探针 job。
  稳态判据：触发可达、取消可收敛、资源可释放。
恢复预期: 优雅降级——取消后运行判 cancelled 并完成清理（post 执行、runner 释放），runner 可复用；若 15min 内零触发则记为 Scheduler 未修复（回归失败）。
破坏级别: fixture
来源输入: baseline/case-base-detail.md（TC-391/TC-427-430/TC-562-563 NEEDS-UPDATE）；inputs/history/issues-encountered.md #39；inputs/gitcode-spec/syntax-reference/trigger-events.md:275；coverage.md BLIND-07
优先级线索: BLIND-07（高严重度盲区），历史 bug 回归，建议 P1；若平台确认 Scheduler 仍不可恢复则升 P0
```

---

## 增补说明

- **ID 接续**：REL-033 为已有最后一条，本增补从 REL-034 起编，共 3 条。
- **与已有 intent 不重复**：COMPAT-SCHEDULE-02-001（INTENT-COMPAT-020）覆盖「UTC 时区/默认分支/最短间隔」兼容差异，属于差异确认视角；本增补从 reliability 视角覆盖运算符边界、间隔 enforcement、触发收敛与取消语义，与 COMPAT-020 互补而非重复。
- **参数具体化**：每条 intent 的 cron 表达式、观测窗口（15min/30min）、延迟上限（5min）、取消后释放时限（60s）均为具体数值，符合 rules §8 确定性纪律。
- **破坏级别**：REL-034/035 为 none（仅配置验证，不破坏共享状态）；REL-036 为 fixture（取消后需清理运行残留）。
- **优先级建议**：3 条均关联 BLIND-07 高严重度盲区及历史 NEEDS-UPDATE bug，建议门禁裁为 P1；若平台确认 Scheduler 修复失败或取消后状态不可收敛，REL-036 可升 P0。
