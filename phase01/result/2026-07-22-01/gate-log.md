# Gate Log（评审门禁日志）

> Run: 2026-07-22-01
> 评审角色: orchestrator + review-gate
> 评审日期: 2026-07-22

---

## 去重记录

| 组号 | 涉及意图 | 决定 | 理由 |
|---|---|---|---|
| G1 | COMP-001, COMPAT-029, USE-001 | 保留 COMP-001；COMPAT-029 / USE-001 标「已关联」 | 核心验证点在 completeness（目录识别），compat/usability 侧重差异报错质量，属同一能力不同视角 |
| G2 | COMPAT-016, spec-COMPAT-019, USE-002 | 保留 COMPAT-016；spec-COMPAT-019 打回；USE-002 标「已关联」 | spec-COMPAT-019 与 compat-COMPAT-019 ID 冲突且内容被 COMPAT-016 完全覆盖 |
| G3 | COMPAT-004/005, spec-COMPAT-020, USE-004 | 保留 COMPAT-004/005；spec-COMPAT-020 打回；USE-004 标「已关联」 | spec-COMPAT-020 与 compat-COMPAT-020 ID 冲突且内容被 COMPAT-004/005 覆盖 |
| G4 | COMPAT-030, spec-COMPAT-022, USE-005 | 保留 COMPAT-030；spec-COMPAT-022 打回；USE-005 标「已关联」 | spec-COMPAT-022 与 compat-COMPAT-022 ID 冲突且内容被 COMPAT-030 覆盖 |
| G5 | COMPAT-014, spec-COMPAT-023, USE-008 | 保留 COMPAT-014；spec-COMPAT-023 打回；USE-008 标「已关联」 | spec-COMPAT-023 与 compat-COMPAT-023 ID 冲突且内容被 COMPAT-014 覆盖 |
| G6 | COMPAT-006~010, COMP-021 (spec) | 保留 COMPAT-006~010；COMP-021 打回 | spec-analyst 的 COMP-021 为粗粒度「表达式函数边界」，compat-diff 已拆分为 5 条细化 intent |
| G7 | REL-027/038/039/056, COMP-026 (spec) | 保留 REL-027/038/039/056；COMP-026 打回 | spec-analyst 的 COMP-026 为粗粒度「matrix 规模」，reliability agent 已拆分为 4 条细化 intent |
| G8 | SEC-020~022, COMP-011, COMPAT-028 | 保留 SEC-020~022；COMP-011 / COMPAT-028 标「已关联」 | security agent 的 Runner 隔离意图最完整（含负向断言），其他维度侧重不同 |
| G9 | SEC-004~008, COMP-012, COMPAT-033, USE-016 | 保留 SEC-004~008；其余标「已关联」 | security agent 对脱敏绕过做了 base64/拼接/多行/分片 4 条细分，覆盖最完整 |
| G10 | SEC-035, COMP-004, SEC-002, COMPAT-032 | 保留 SEC-035；COMP-004 / SEC-002 / COMPAT-032 标「已关联/变体」 | SEC-035 覆盖「base 分支 workflow 版本」核心验证点；SEC-002 侧重 checkout head.sha 风险，为变体 |
| G11 | SEC-018, COMP-016, COMPAT-025 | 保留 SEC-018；其余标「已关联」 | cache fork 隔离的核心安全验证在 SEC-018 |
| G12 | REL-023/024, COMP-006, COMPAT-015, USE-026 | 保留 REL-023/024；其余标「已关联」 | reliability agent 提供了边界+越界成对 intent，最完整 |
| G13 | REL-001~006, COMP-025 (spec), COMPAT-034, USE-027 | 保留 REL-001~006；COMP-025 打回；COMPAT-034 / USE-027 标「已关联」 | spec-analyst 的 COMP-025 为粗粒度「concurrency 行为」，reliability 已拆分为 6 条 |
| G14 | REL-007~010, COMP-008 | 保留 REL-007~010；COMP-008 标「已关联」 | reliability agent 提供了边界/越界/短超时/默认超时 4 条成对 intent |
| G15 | REL-011~013, COMP-009 | 保留 REL-011~013；COMP-009 标「已关联」 | reliability agent 提供了边界/越界/过期 3 条成对 intent |
| G16 | REL-014/015, COMP-003, COMPAT-012, USE-015 | 保留 REL-014/015；其余标「已关联」 | reliability agent 提供了边界/越界成对 intent |
| G17 | COMP-015, REL-041, COMPAT-026 | 保留 COMP-015 / REL-041；COMPAT-026 标「已关联」 | COMP-015 覆盖基础 artifact 行为，REL-041 覆盖超大 artifact 边界 |
| G18 | COMP-010, COMPAT-027, USE-006 | 保留 COMP-010；其余标「已关联」 | COMP-010 覆盖三段式标签核心验证点 |
| G19 | COMP-005, COMPAT-013 | 保留 COMP-005；COMPAT-013 标「已关联」 | COMP-005 覆盖 schedule cron 核心验证点 |
| G20 | COMP-007, REL-029, USE-011 | 保留 COMP-007；其余标「已关联」 | COMP-007 覆盖 stages/post 核心验证点 |
| G21 | SEC-009~013, SEC-024 | 保留 SEC-009~013；SEC-024 标「变体」 | SEC-024 侧重特殊字符求值，为注入类意图的变体 |
| G22 | COMPAT-031, USE-001~010, spec-USE-028 | 保留 COMPAT-031 / USE-001~010；spec-USE-028 打回 | spec-USE-028 粗粒度「迁移报错质量」已被 usability agent 拆分为 10 条具体差异项 intent |
| G23 | COMP-002, COMPAT-021, USE-023 | 保留 COMP-002；COMPAT-021 / USE-023 标「已关联」 | COMP-002 覆盖未知字段 YAML 校验核心验证点 |
| G24 | COMP-018, USE-020 | 保留 COMP-018；USE-020 标「已关联」 | COMP-018 覆盖 STEP_SUMMARY 核心验证点 |
| G25 | COMPAT-022, USE-014 | 保留 COMPAT-022；USE-014 标「已关联」 | COMPAT-022 覆盖 vars 不支持降级核心验证点 |
| G26 | SEC-016/017/036, COMP-013, COMPAT-002 | 保留 SEC-016/017/036；其余标「已关联」 | security agent 的 permissions 生效意图最完整（含负向断言） |
| G27 | REL-028/048/061, COMP-017 | 保留 REL-028/048/061；COMP-017 标「已关联」 | reliability agent 对取消语义做了故障注入+竞态+可靠性 3 条细分 |

---

## 优先级裁决

| 意图 ID | 原始线索 | 最终优先级 | 裁决理由 |
|---|---|---|---|
| REL-064 | reliability agent 自评 P0（历史 workflow_call 假阳性严重 bug #30/#64） | **P1** | risk-register.md 中无对应 blocker 风险项；RISK-REL-01 为 P1。历史 bug 严重性高，但优先级唯一来源为 risk-register，不自造 P0 |
| SEC-034 | security agent 标注「若支持则 P0，若不支持则 P1 缺口」 | **P1** | risk-register.md 中无 OIDC 专项风险项；若平台明确不支持 OIDC 则属已知限制，不构成本次 blocker |
| COMPAT-002 | compat-diff agent 标注 RISK-SEC-01 延伸 | **P0** | 明确对齐 RISK-SEC-01（fork PR secret 隔离的延伸——默认权限过宽同样导致 secret 泄露风险） |
| COMP-011 | spec-analyst 标注「安全与稳定性」 | **P0** | 明确对齐 RISK-SEC-01（Runner 非一次性将导致跨 job secret 泄露） |
| COMP-012 | spec-analyst 标注「安全命脉」 | **P0** | 明确对齐 RISK-SEC-01（secret 脱敏失效 = secret 泄露） |
| COMP-013 | spec-analyst 标注「安全命脉」 | **P0** | 明确对齐 RISK-SEC-01（permissions 默认权限过宽 = fork PR 可越权） |
| COMP-014 | spec-analyst 标注「安全命脉」 | **P0** | 明确对齐 RISK-SEC-01（pull_request_target checkout head.sha = Pwn Request） |
| COMP-016 | spec-analyst 标注「安全与稳定性」 | **P0** | 明确对齐 RISK-SEC-01（cache fork 隔离失效 = cache 投毒） |
| USE-016 | usability agent 标注 RISK-SEC-01 | **P0** | 明确对齐 RISK-SEC-01（secret 脱敏文档与实际不一致可能导致用户误用） |
| COMPAT-025 | compat-diff agent 标注 RISK-SEC-01 | **P0** | 明确对齐 RISK-SEC-01（cache fork 隔离 = cache 投毒） |
| COMPAT-028 | compat-diff agent 标注 RISK-SEC-01 | **P0** | 明确对齐 RISK-SEC-01（Runner 复用 = 跨 job secret 泄露） |
| COMPAT-030 | compat-diff agent 标注 RISK-USE-01 | **P0** | 裁决升级：permissions 命名差异被静默忽略时，默认权限可能过宽，实质属于 RISK-SEC-01 延伸 |
| COMPAT-032 | compat-diff agent 标注 RISK-SEC-01 | **P0** | 明确对齐 RISK-SEC-01（pull_request_target 语义不一致 = Pwn Request） |
| COMPAT-033 | compat-diff agent 标注 RISK-SEC-01 | **P0** | 明确对齐 RISK-SEC-01（secret 脱敏绕过 = secret 泄露） |
| REL-054 | reliability agent 自评 P2 | **P2** | 对齐 RISK-REL-01（P1），但 cache 加速比属性能基准，无直接稳定性风险，维持 P2 |
| REL-062 | reliability agent 自评 P2 | **P2** | 对齐 RISK-REL-01（P1），但网络容错属边界体验，无直接稳定性风险，维持 P2 |
| REL-065 | reliability agent 自评 P2 | **P2** | 对齐 RISK-REL-01（P1），但 API 限流属可测性缺口，无直接稳定性风险，维持 P2 |

---

## 覆盖盲区清单

| 盲区类型 | 具体项 | 影响 | 建议补哪个维度 |
|---|---|---|---|
| 能力项盲区 | **注解(annotation)机制** — parity-matrix 标记为 ❓，USE-021 仅覆盖「是否支持及文档一致性」，无完整端到端验证 intent | 无法确认 GitCode 是否支持 GitHub 风格的 `::error file=...::message` 行级 annotation 回写到 PR/commit | completeness / usability |
| 能力项盲区 | **action `runs.using` 支持范围** — GAP-017，文档仅列 `node16`，是否支持 node20/docker/composite 未知；TC-601 仅验证 node20 被拒绝，未形成系统级 intent | Action 开发者无法确认平台支持的运行环境，迁移决策缺少依据 | completeness / compatibility |
| 能力项盲区 | **runner.debug 触发方式** — GAP-018，文档未说明如何开启 debug 模式；无 intent 覆盖 | 无法验证 debug 日志输出与行为 | completeness |
| 能力项盲区 | **自托管 Runner 同时运行多个 Job** — GAP-019，文档未明确一个 Runner 是否可同时运行多个 Job | 影响自托管资源调度与隔离策略设计 | reliability / security |
| 能力项盲区 | **K8s Runner 容器隔离边界** — GAP-020，文档未说明 K8s Runner Pod 的网络策略、特权模式、宿主机访问限制 | 自托管 K8s 场景下攻击面无法评估 | security |
| 能力项盲区 | **取消语义与清理钩子完整行为** — GAP-008，REL-028/061 覆盖手动取消，但「被抢占时 step 如何终止、post 是否执行」未完全覆盖 | 生产环境被抢占或运维误操作时的行为不确定 | reliability |
| 能力项盲区 | **`issue_comment` / `pull_request_comment` 默认 types** — GAP-011，TC-464~467 已有用例但未形成独立 intent；spec.md 标记为模糊 | 评论触发器的默认行为无法系统验证 | completeness |
| 风险项盲区 | **RISK-SEC-01 / RISK-SEC-02 已全覆盖** — 两个 blocker 风险项均有 P0 intent 覆盖 | — | — |
| 风险项盲区 | **RISK-COMPAT-01 已全覆盖** — 默认值差异致行为静默不同，有 20+ P1 intent 覆盖 | — | — |
| 风险项盲区 | **RISK-REL-01 已全覆盖** — 并发洪泛下排队/公平性失效，有 60+ P1 intent 覆盖 | — | — |
| 风险项盲区 | **RISK-USE-01 已全覆盖** — 迁移报错不指明 GitCode 差异，有 15+ P1 intent 覆盖 | — | — |

---

## 已有用例复用建议

| 意图 ID | 已有用例 ID | 建议 |
|---|---|---|
| COMP-001 | TC-366, TC-383 | 可直接复用 TC-366（workflow 文件位置识别），建议补充「.github/workflows 不被识别」负向用例 |
| COMP-003 | TC-223, TC-229~233 | TC-223 覆盖 push 触发基础行为；建议新增 paths>300 文件和 branches-ignore 负向用例 |
| COMP-004 | TC-445, TC-461~463 | TC-461/463 为 FAIL 状态，需重新验证 pull_request_target 触发行为后复用 |
| COMP-005 | TC-427~430 | TC-427/428/429/430 均为 FAIL/SKIP，schedule  cron 当前无法验证，建议保留占位待平台修复后执行 |
| COMP-006 | TC-426, TC-564 | TC-426 验证 2 层嵌套（SKIP），TC-564 验证 3 层越界（SKIP）；均为平台侧校验，建议保留为文档约束用例 |
| COMP-007 | TC-402~404, TC-406~407 | 可直接复用 stages 与 post 机制用例 |
| COMP-008 | TC-270 | TC-270 覆盖 timeout-minutes 配置；建议补充「未声明 timeout 时默认 360 分钟」的显式用例 |
| COMP-010 | TC-363, TC-365, TC-446~457 | Runner 标签用例丰富，可直接复用；建议补充「default 快捷标签」和「标签不完全匹配」用例 |
| COMP-012 | TC-011, TC-354 | TC-011 验证 secret 日志脱敏基础行为；建议补充 base64/拼接/多行/分片绕过场景的独立用例 |
| COMP-013 | TC-351~416 | permissions 用例覆盖完整，可直接复用；建议补充「未声明 permissions 时默认权限」的显式用例 |
| COMP-015 | TC-294~300, TC-378~380 | artifact 基础用例为 SKIP（外部 Action），建议优先设计可在纯 shell 中验证的 artifact 边界用例 |
| COMP-016 | TC-301~303 | cache 基础用例为 SKIP；建议设计 fork PR cache 隔离的专项用例（需多仓库协作） |
| COMP-017 | TC-347, TC-348 | 运行结果与日志查看用例可直接复用；建议补充「日志完整性（超大日志不截断）」用例 |
| COMP-018 | TC-219, TC-246, TC-497 | STEP_SUMMARY 用例为 SKIP（UI 验证困难）；建议设计通过 API 拉取 summary 内容的自动化用例 |
| COMPAT-004 | TC-176~179, TC-317~321 | 状态函数用例可直接复用；注意 TC-317~321 为 FAIL，需跟踪修复后重新验证 |
| COMPAT-006 | TC-180, TC-543~544 | contains 用例可直接复用；建议补充「空值/数组元素」边界用例 |
| COMPAT-007 | TC-186, TC-550 | hashFiles 用例可直接复用；建议补充「无匹配文件返回空字符串」边界用例 |
| COMPAT-014 | TC-014, TC-193, TC-581 | inputs 类型限制用例可直接复用；建议补充 workflow_call inputs 非 string 类型校验用例 |
| COMPAT-018 | TC-023, TC-094, TC-136~139 | runner.os 大小写错误用例（FAIL）可直接复用；修复后需重新验证 |
| COMPAT-019 | TC-095, TC-442 | runner.arch 格式错误用例（FAIL）可直接复用；修复后需重新验证 |
| COMPAT-030 | TC-351~416 | permissions 命名用例可直接复用；建议补充「GitHub 命名 contents:read 被静默忽略」负向用例 |
| SEC-001/003 | TC-445 | fork PR 隔离用例为 SKIP；建议设计真实的 fork PR 触发实验用例 |
| SEC-014 | TC-628 | Action SHA 固定用例可直接复用 |
| SEC-018 | TC-301~303 | cache fork 隔离用例为 SKIP；需设计多仓库协作的 cache 隔离实验 |
| SEC-027 | TC-010 | 环境级 secret 审批用例为 FAIL；需跟踪平台 environment 字段支持状态 |
| REL-001~006 | TC-289~293, TC-518~523 | concurrency 用例可直接复用；建议补充「QUEUE/IGNORE 策略实际行为」的端到端用例 |
| REL-007~010 | TC-270 | timeout 用例可直接复用；建议补充「短超时（1 分钟）精度」和「默认超时」用例 |
| REL-011~013 | TC-350 | rerun 用例可直接复用；建议补充「第 4 次 rerun 被拒绝」和「6h 后不可 rerun」用例 |
| REL-014/015 | TC-422, TC-514~515 | paths 匹配用例为 SKIP；需设计大变更集（>300 文件）的真实触发实验 |
| REL-023/024 | TC-426, TC-564 | workflow_call 嵌套用例为 SKIP；建议保留为平台侧校验用例 |
| REL-025 | TC-313~316 | needs 失败传播用例可直接复用 |
| REL-026/027 | TC-277, TC-278, TC-329, TC-330 | matrix fail-fast / max-parallel 用例可直接复用；建议补充「fail-fast=false」用例 |
| REL-028 | TC-350 | 取消语义用例可直接复用；建议补充「always() cleanup step 执行」的显式断言 |
| REL-038/039 | TC-325~328 | matrix 规模用例可直接复用；建议补充 20/50 组合的大规模矩阵用例 |
| REL-040 | TC-348 | 日志用例可直接复用；建议补充「100MB 日志完整性校验」用例 |
| REL-041 | TC-378~380 | artifact 用例为 SKIP/用例不当；需重新设计可自动化的 artifact 边界用例 |
| REL-047 | TC-296, TC-380 | artifact 保留期用例可直接复用 |
| REL-049 | TC-447~455 | Runner 规格用例可直接复用；建议补充「实际资源 vs 声明值」的自动化探针用例 |
| REL-059 | TC-348 | 日志稳定性用例可直接复用；建议补充「6 万行顺序输出」的显式校验用例 |
| USE-001 | TC-366, TC-383 | 目录报错质量用例可直接复用；建议补充「报错是否包含 .gitcode/workflows 字样」的断言 |
| USE-004 | TC-176~179 | 状态函数报错质量用例可直接复用；建议补充「success() 报错是否提示不带括号」的断言 |
| USE-008 | TC-014, TC-193 | inputs 类型报错质量用例可直接复用；建议补充「boolean 类型报错是否提示仅支持 string」的断言 |
| USE-010 | TC-239~241, TC-552~553 | 废弃命令用例可直接复用；建议补充「报错是否给出 ATOMGIT_OUTPUT/ENV/PATH 替代示例」的断言 |
| USE-012 | TC-206, TC-220 | 文档残留措辞用例可直接复用；建议改为「全文扫描 GITHUB_ 独立出现次数=0」的自动化检查 |
| USE-016 | TC-011 | secret 脱敏文档一致性用例可直接复用 |
| USE-022 | TC-393~401 | YAML 报错质量用例可直接复用；建议补充「行号/列号/预期类型」的显式断言 |
| USE-026 | TC-564 | workflow_call 嵌套报错清晰度用例可直接复用 |
| USE-027 | TC-522 | concurrency max 报错清晰度用例可直接复用 |
| USE-028 | TC-531 | Secret 名称规则报错质量用例可直接复用 |
| USE-030 | TC-012~016, TC-581~583 | workflow_dispatch inputs 用例可直接复用；建议补充「默认值生效」和「必填参数缺失阻止触发」的显式用例 |
