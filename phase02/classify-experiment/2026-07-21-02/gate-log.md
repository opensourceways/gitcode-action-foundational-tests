# Gate Log · STOP① 门禁 · Run 2026-07-21-02

> 角色：评审门禁 (review-gate) + orchestrator 联合把关。阶段A(发散 160 条 intent) → 阶段B(展开) 之间的准入闸门。
> 输入：`intent-library.md`(160) + 五维度 intent 详情 + L0 基线 + `case-base-detail.md`(631 评估/260 KEEP) + `cases.md` + business-context 历史问题。
> 产出：本文件 + 回标 `intent-library.md` 门禁列。

---

## ⚠️ 关键前提（覆盖优先级纪律 rules §2）

三份 L0 基线（parity-matrix / risk-register / quality-gate）当前仍为**模板+示例态**（RISK-SEC-01 等为示例行，Parity 能力项为示例）。因此本门禁：

1. **优先级为门禁临时裁定**，依据 = testing-focus 风险语义 + business-context 历史问题实证（cases.md「问题」22 条 + NEEDS-UPDATE 25 类 bug）+ spec.md 缺口严重度。**待 risk-register 刷新为真实风险项后，所有 Pn 需回归复核。** 每条 P0 均注明血缘依据。
2. **Parity Matrix 事实左列**取自 spec.md 的 **133 条能力项（C-* 前缀）+ 36 条缺口（G-01~G-36）**，因官方 parity-matrix 为模板。盲区检测对照此事实左列。
3. 本裁定不写回 risk-register（rules §37「不自造风险项」），仅在本 gate-log 显式标注临时性。

---

## 0. 门禁结论摘要

| 指标 | 数值 |
|---|---|
| 输入 intent 总数 | 160 |
| **准入（可展开）** | **121** |
| 合并为变体/母 intent（不独立展开） | 21 |
| 已有基底充分覆盖（复用，不新展开） | 14 |
| 打回/待补 | 4 |
| 准入优先级分布 | P0 = 27 / P1 = 66 / P2 = 28 |
| 五维度准入是否齐全 | ✅ 五维度均有 P0/P1（security 27 条准入含 9 P0） |
| 覆盖盲区 | 11 项（详见 §6） |

> 说明：合并的 21 条不是「打回」，而是归入母 intent 作变体（-Vn）；已有覆盖 14 条为复用旧用例。真正「不予展开且需回炉」的仅 4 条。准入 121 + 合并 21 + 已有覆盖 14 + 打回 4 = 160。

---

## 1. 去重记录（160 条聚类）

> 聚类判据：同义(标题/验证点等价) / 包含(A ⊇ B) / 变体(同母场景不同参数)。变体标 `-Vn` 关联母 intent。与已有 631 基底(case-base-detail.md 260 KEEP)已覆盖者标 `已有覆盖` + 关联 TC。

### 1.1 跨维度重叠聚类（同一风险语义被多维度重复挖）

门禁发现 5 处**跨维度同题**，统一保留「主维度代表」，其余关联为跨维引用（不各自独立展开，但保留原 ID 作维度视角标注）：

| 聚类 | 成员 intent | 主代表 | 决定 |
|---|---|---|---|
| CL-A `permissions:{}` 语义冲突(G-21) | INTENT-COMP-006 / INTENT-COMPAT-055 / INTENT-SEC-016 / INTENT-USE-013 | **INTENT-SEC-016**（安全主口径，含权限实测） | COMP-006/COMPAT-055/USE-013 关联为同一实测，各保留本维度断言视角；准入 SEC-016，其余标「合并→INTENT-SEC-016」 |
| CL-B fork PR token 降权(C-SEC-09) | INTENT-SEC-002 / INTENT-COMPAT-052 | **INTENT-SEC-002**（安全命脉主口径） | COMPAT-052 为「与 GitHub 同向一致性」视角，合并→SEC-002 作变体 -V1 |
| CL-C pull_request_target base 上下文(C-SEC-10) | INTENT-SEC-004 / INTENT-COMPAT-053 | **INTENT-SEC-004** | COMPAT-053 合并→SEC-004 作变体 -V1 |
| CL-D secret 脱敏变形覆盖(G-16) | INTENT-SEC-006/007/008 / INTENT-COMPAT-054 / INTENT-USE-021 | **INTENT-SEC-006**(base64)为母，007/008 为变体 | COMPAT-054(与 GitHub 对齐视角)合并→SEC-006；USE-021(可观测视角)独立保留(易用性断言不同) |
| CL-E RUN_ID 重跑语义冲突(G-22) | INTENT-COMP-007 / INTENT-USE-014 | **INTENT-COMP-007**（规格实测主口径） | USE-014 合并→COMP-007，保留 usability 文档勘误断言视角 |

### 1.2 维度内变体聚类（同母场景不同参数 → -Vn）

| 母 intent | 变体成员 | 决定 |
|---|---|---|
| INTENT-SEC-006（脱敏 base64） | SEC-007（拼接分片）、SEC-008（多行） | 007→SEC-006-V1，008→SEC-006-V2（同一脱敏机制不同变形输入） |
| INTENT-REL-001（concurrency.max 边界 1/5） | REL-002（越界 0/6/非整数） | 002→REL-001-V1（同 concurrency.max 校验，正向+负向合一展开） |
| INTENT-SEC-001（fork 读 secret） | INTENT-SEC-028（多项目共享 runner secret 隔离） | 保留独立：028 为 runner 层横向隔离，攻击面不同，**不合并** |
| INTENT-COMPAT-031（env 文件变量前缀） | INTENT-COMPAT-032（系统环境变量映射全集） | 保留独立：031 是写协议前缀、032 是读取全集覆盖度，断言集不同 |
| INTENT-USE-002（github.* 迁移报错） | INTENT-COMPAT-025（前缀替换完备性） | 保留独立：USE-002 测报错质量，COMPAT-025 测替换正确性，oracle 不同 |

### 1.3 与已有基底(260 KEEP)已覆盖 → 复用不新展开

以下 intent 的核心验证点已被基底用例有效覆盖（PASS 或已在 KEEP），门禁标 `已有覆盖`，建议 case-writer 复用旧 ID / 加 intent_ref，不重复生成：

| intent | 已有覆盖 TC | 说明 |
|---|---|---|
| INTENT-COMP-003 / INTENT-REL-009（paths 前300文件边界） | TC-422 / TC-514 / TC-515 / TC-516 | 300/301/空变更边界基底已覆盖；本轮仅补「第301+命中不触发」负向断言差异 → 降为变体补充 |
| INTENT-COMP-002 / INTENT-REL-001（concurrency.max 1-5 与越界） | TC-289 / TC-290 / TC-524(D) | max/enable 基底覆盖；越界校验 TC-524 为 D 测不动，本轮负向仍有价值 → 部分已有覆盖 |
| INTENT-REL-027（strategy.fail-fast 语义） | TC-277 / TC-329(SKIP) | fail-fast 字段基底覆盖但 TC-329 失败观察 SKIP；本轮确定性展开有增量 → 部分覆盖 |
| INTENT-REL-028（stages.fail_fast 传播） | TC-403 / TC-404 | true/false 基底覆盖；本轮跨 stage 传播为增量 |
| INTENT-COMP-004（workflow_call 2层嵌套） | TC-426(C 难真测) | 基底仅语法声明 PASS；本轮超限拒绝为增量 |
| INTENT-SEC-015（permissions 收窄生效） | TC-351/352/353/408/409/410/411-416 | 权限声明语法基底大量覆盖；但**「收窄真实生效/越权被拒」的负向执行未覆盖** → 本轮 P0 有独立价值，非纯复用 |
| INTENT-SEC-005（secret 基础脱敏） | TC-354 / TC-011(SKIP) | 脱敏声明基底覆盖但 C 难真测 SKIP；本轮执行验证有增量 |
| INTENT-COMPAT-047（checkout 等价性） | TC-304 | 基底语法 PASS；本轮参数集等价性为增量 |
| INTENT-COMPAT-048（cache 语义/隔离） | TC-301/302/303/305 | 基底语法 PASS；fork 隔离(SEC-019)为独立安全增量 |
| INTENT-COMPAT-049（artifact 等价性） | TC-294~300/306/307 | 基底语法 PASS；本轮上限/命名为增量 |
| INTENT-USE-024（PR 状态回写可见性） | TC-350(rerun) 邻近 | 部分观测基底覆盖；PR Checks 回写为增量 |
| INTENT-COMPAT-036（runs-on 三段式） | TC-571/572/573 | 边界基底覆盖；GitHub 单标签迁移降级为增量 |
| INTENT-COMPAT-050（setup-* 参数） | TC-310(FAIL setup-java) | 历史 bug 已在 NEEDS-UPDATE；复用跟踪 |
| INTENT-COMPAT-017（PR types 命名 open vs opened） | TC-064(P2 问题) / TC-234(FAIL) | 历史问题已实证；本轮兼容差异确认复用历史证据 |

> 注：上述多为「部分已有覆盖」——基底覆盖了**语法声明**，本轮 intent 补的是**执行/负向/差异**断言，仍有独立展开价值。仅标注供 case-writer diff 复用，避免重复生成语法层用例。真正「完全已有覆盖、零增量」的为 0 条——因基底 260 KEEP 中大量为 C 难真测/语法声明 PASS，本轮执行导向 intent 普遍有增量。故摘要中「已有覆盖 14」指**建议优先复用旧用例作基底、仅生成 delta** 的 intent 数。

---

## 2. 优先级裁决（临时裁定 · 待 risk-register 刷新回归）

> 纪律：P0 仅授予 **blocker 级风险语义**——安全命脉（secret 泄露/权限越界/注入/隔离逃逸）、迁移直接断点（CI 静默不触发/不运行）、数据损坏/不可恢复。每条 P0 注明血缘。P1=影响大有 workaround；P2=体验/边角。

### 2.1 P0 授予（27 条）及依据

| intent | 维度 | P0 依据（血缘） |
|---|---|---|
| INTENT-SEC-001 | security | 安全命脉：fork PR 读取 secret = RISK-SEC-01 语义；testing-focus §5；issues.md §1 |
| INTENT-SEC-002 | security | 安全命脉：fork token 强制降只读；C-SEC-09；越权=blocker |
| INTENT-SEC-004 | security | 安全命脉：pull_request_target base 上下文防篡改；C-SEC-10 |
| INTENT-SEC-018 | security | 安全命脉：_target + checkout head 高权限跑不可信代码；G-17 明确弱点 |
| INTENT-SEC-009 | security | 安全命脉：PR 标题/正文注入命令执行 = RISK-SEC-02；Actions 高频漏洞 |
| INTENT-SEC-010 | security | 安全命脉：head_ref/commit msg 非显性注入面；最易漏防 |
| INTENT-SEC-005 | security | 安全命脉：secret 日志脱敏基础；issues.md §3 |
| INTENT-SEC-006（母,含V1/V2） | security | 安全命脉：脱敏变形(base64/拼接/多行)绕过；G-16 文档自承弱点 |
| INTENT-SEC-015 | security | 安全命脉：permissions 收窄失效=提权 blocker；执行层未被基底覆盖 |
| INTENT-SEC-019 | security | 安全命脉：fork PR 缓存投毒主分支；G-19 明确缺口 |
| INTENT-SEC-025 | security | 安全命脉：runner 跨 job 敏感残留；G-15；issues.md §1/§4 |
| INTENT-SEC-028 | security | 安全命脉：多项目共享 runner secret 横向泄露；issues.md §1 |
| INTENT-COMPAT-008 | compatibility | 迁移直接断点：状态函数括号 success() 静默失效 → CI 逻辑反转 |
| INTENT-COMPAT-017 | compatibility | 迁移直接断点：PR types open/opened 差异致 CI 静默不触发；**TC-064/TC-234 历史实证** |
| INTENT-COMPAT-036 | compatibility | 迁移直接断点：runs-on 单标签→三段式，不改则每 workflow 排不到 runner |
| INTENT-COMP-005 | completeness | 安全相关：inputs 非 string 静默按字符串致布尔条件判真（安全语义误判） |
| INTENT-COMPAT-052 | 合并→SEC-002 | （见 CL-B）—作 SEC-002-V1，继承 P0 |
| INTENT-COMPAT-053 | 合并→SEC-004 | （见 CL-C）—作 SEC-004-V1，继承 P0 |

> P0 实际独立展开条数 = 15（SEC 12 + COMPAT 3 + COMP 1，含 SEC-006 母合并 007/008）。加上继承 P0 的合并变体统计口径为 27（含各维度视角计数）。**独立可展开 P0 = 15**，摘要「P0=27」为含变体视角的宽口径。以 **15 独立 P0** 为交付基准。

**修正摘要口径**：独立展开计数下 P0 = 15 / P1 = 66 / P2 = 28（合计 109 独立）+ 变体 12 = 121 准入。

### 2.2 P1 授予要点（66 条，摘录高价值依据）

- **迁移摩擦高频**（P1）：INTENT-COMPAT-001(默认shell)/009(default函数)/010(缺失函数)/016(identifier)/021(PR checkout ref)/024(inputs类型)/025(github→atomgit前缀)/026(actor缺失)/031(env文件前缀)/032(系统变量映射)/039(无Win/mac)/042(concurrency模型)/043(node16限制)/044(uses引用)/047(checkout)/057(stages)/059(stage特有字段)/060(报错质量)/061(workflow_call)。依据 testing-focus §10/§11 + business-context 维度3 兼容性核心资产。
- **安全 P1**（有 workaround 或非命脉）：SEC-003/012/013/014/016/017/020/022/023/024/026/027/029/030/031/032/033/036。依据 testing-focus §5-§8。
- **稳定性 P1**：REL-003/005/006/007/008/018/019/020/021/022/026/027/028/029/030/033。依据 testing-focus §12 + platform-config 配额。
- **易用性 P1**：USE-001/002/003/004/005/007/010/013/014/020/021/022。依据 business-context 维度1/2 文档+实操易用性。
- **规格 P1**：COMP-006(权限冲突)/007(RUN_ID冲突)。

### 2.3 P2 授予要点（28 条）

体验/边角/低频：COMPAT-004/006/011/012/013/014/019/022/023/027/028/030/033/034/035/037/038/040/045/046/048/049/050/051；USE-012/015/016/023；REL-004/010~017(探测类多为 P2，无上限声明的容量探测)。依据：无历史实证、非命脉、有 workaround。

### 2.4 优先级质疑（无法对齐，标注存疑）

- **全部 spec 类 INTENT-COMP-001~008**：源标注即「无法对齐 risk-register 模板态」。门禁临时裁定：COMP-005→P0（安全语义）、COMP-006/007→P1（文档冲突致误用）、COMP-001/002/003/004/008→P2（规格坐实，除 008 迁移断点升 P1... 见修正）。
  - **修正**：COMP-008（状态函数唯一合法形式）与 COMPAT-008 同题，随 COMPAT-008 升 **P0**（迁移断点）。COMP-002/003 与 REL/已有基底重叠，降 P2。

---

## 3. 可测性审查（四要素齐 + oracle 明确 + 三线断言）

> 最小标准（testing-focus 附）：① 四要素(YAML+触发身份+仓库前置+环境) ② oracle 明确(GitCode规格/GitHub行为/差异声明) ③ 三线断言(状态/日志/副作用 → positive/negative/nonfunctional)。

### 3.1 通过可测性审查（121 条准入均满足或可补齐）

- 安全类 33 条：oracle 明确（多为 negative「不应发生」），四要素在 intent 详情中已布置（fork 身份/PR 前置/隔离环境）。✅
- 兼容类 61 条：oracle 均标「一致性(对齐GitHub)/差异确认(对齐GitCode声明)」，符合 rules §4。✅
- spec 8 条：oracle=GitCode 规格或差异声明，三线断言在详情「验证要点」齐备。✅

### 3.2 可测性打回/待补（4 条，见 §7 打回清单）

- **INTENT-REL-011**（账户/仓库级全局并发上限探测）：G-11 规格未声明上限，**oracle 缺失**——无「预期值」可断言，只能观测。打回待补：需先向平台确认是否存在该上限，否则退化为无 oracle 的探索，不满足确定性断言(rules §8)。
- **INTENT-REL-013 / REL-014 / REL-016 / REL-017**（artifact/cache/workflow文件/secret数 容量上限探测）：G-07/08/09 均「未公开」，**同样 oracle 缺失**。门禁裁决：**其中 REL-013(artifact)、REL-014(cache) 保留为 P2 准入**（有 LRU/超限行为可作 nonfunctional 断言），**REL-016(workflow文件大小)、REL-017(secret数) 打回**——纯找数字上限、无行为契约、无恢复预期，不满足最小可测标准。

> 打回总数收敛为 **4**：REL-011、REL-016、REL-017，加 **INTENT-USE-018**（示例可直接复刻验证——范围过宽，「所有 quick-start 示例开箱可跑」非单一 oracle，需拆分为具体示例用例后重提）。

---

## 4. 准入意图清单（可展开）

> 格式：ID | 维度 | 优先级 | 覆盖的风险/能力项（血缘）。合并变体列出母 ID。已复用基底者标 ⟳。

### 4.1 安全性（准入 31 / 打回 0 · 含 9 独立 P0）

| ID | 维度 | 优先级 | 覆盖能力项/缺口 |
|---|---|---|---|
| SEC-001 | security | P0 | C-SEC-05 fork secret 隔离 / RISK-SEC-01 |
| SEC-002（含 COMPAT-052-V1） | security,compatibility | P0 | C-SEC-09 fork token 降权 |
| SEC-003 | security | P1 | C-SEC-05 fork 攻击范围受限 |
| SEC-004（含 COMPAT-053-V1） | security,compatibility | P0 | C-SEC-10 _target base 上下文 |
| SEC-005 | security | P0 | ⟳TC-354 C-SEC-03 基础脱敏 |
| SEC-006（母,含 007-V1/008-V2/COMPAT-054） | security | P0 | G-16 脱敏变形绕过 |
| SEC-009 | security | P0 | RISK-SEC-02 脚本注入 |
| SEC-010 | security | P0 | testing-focus §6 非显性注入面 |
| SEC-012 | security | P1 | C-TRIG-04/05 评论注入 |
| SEC-013 | security | P1 | 中间变量防御模式 |
| SEC-014 | security,compatibility | P1 | G-18 双重求值+正则过滤注入面 |
| SEC-015 | security | P0 | C-SEC-07 permissions 收窄执行生效 |
| SEC-016（母,含 COMP-006/COMPAT-055/USE-013） | security,usability | P1 | G-21 permissions:{} 冲突 |
| SEC-017 | security | P1 | G-06 默认权限不宽于仓库设置 |
| SEC-018 | security | P0 | G-17 _target+checkout head 注入 |
| SEC-019 | security,reliability | P0 | G-19 fork 缓存投毒 |
| SEC-020 | security | P1 | C-ART-06 cache 跨仓隔离 |
| SEC-021 | security | P1 | C-ACT-07 SHA 不可变引用/tag 重写 |
| SEC-022 | security | P1 | C-ACT-14 第三方 action 最小权限 |
| SEC-023 | security | P1 | C-SEC-06 token 运行后失效 |
| SEC-024 | security | P1 | C-ACT-02 写协议污染提权 |
| SEC-025 | security,reliability | P0 | G-15 runner 跨 job 残留 |
| SEC-026 | security | P1 | 共享盘跨 job 泄露 |
| SEC-027 | security,reliability | P1 | G-14 网络出站/SSRF |
| SEC-028 | security | P0 | 多项目共享 runner secret 隔离 |
| SEC-029 | security | P1 | artifact 投毒防护 |
| SEC-030 | security,usability | P1 | G-20 环境保护规则未审批 |
| SEC-031 | security | P1 | TOCTOU 审批后推送绕过 |
| SEC-032 | security | P1 | secret 侧信道外泄 |
| SEC-033 | security,reliability | P1 | 同主机并发 job 隔离 |
| SEC-036 | security | P1 | token 默认权限+job级覆盖 |

### 4.2 兼容性（准入 59 / 合并 2 / 含 3 独立 P0）

- **P0（3）**：COMPAT-008(状态函数括号)、COMPAT-017(PR types 命名)、COMPAT-036(runs-on 三段式)。
- **合并（2）**：COMPAT-052→SEC-002、COMPAT-053→SEC-004、COMPAT-054→SEC-006、COMPAT-055→SEC-016（共 4 条合并入安全；兼容侧净独立 = 57）。
- **P1（约 33）**：COMPAT-001/002/003/005/007/009/010/015/016/018/020/021/024/025/026/029/031/032/039/041/042/043/044/047/056/057/059/060/061 等（迁移摩擦+安全敏感）。
- **P2（约 21）**：COMPAT-004/006/011/012/013/014/019/022/023/027/028/030/033/034/035/037/038/040/045/046/048/049/050/051。
- ⟳ 基底复用：COMPAT-017(TC-064/234)、036(TC-571-573)、047(TC-304)、048(TC-301-303)、049(TC-294-300)、050(TC-310)。

> 全部 61 条附「对齐方向」已在 intent-library 标注（一致性/差异确认），满足 rules §4「对齐谁」纪律。

### 4.3 稳定性（准入 30 / 打回 3 · REL-011/016/017）

- **P1（约 16）**：REL-003/005/006/007/008/018/019/020/021/022/026/027/028/029/030/033。
- **P2（约 14）**：REL-001(⟳TC-289/290,含 002-V1)/004/009(⟳TC-514-516)/010/012/013/014/015/023/024/025/031/032。
- **打回（3）**：REL-011/016/017（§3.2 oracle 缺失）。
- 说明：探测类(REL-010~017)多为 P2；故障注入类(REL-018~026)P1，均需声明 recovery_expectation(rules §8)。

### 4.4 易用性（准入 24 / 打回 1 · USE-018）

- **P1（约 12）**：USE-001/002/003/004/005/007/010/013(→合并SEC-016视角)/014(→合并COMP-007视角)/020/021/022。
- **P2（约 10）**：USE-006/008/009/011/012/015/016/017/019/023/024/025。
- **打回（1）**：USE-018（范围过宽，§3.2）。
- 说明：USE 全维度无 P0——易用性无 blocker 级（报错缺失有 workaround），符合 quality-gate「核心迁移路径完全不可用且无提示」才 blocker，当前无此条。**但见 §6 盲区：迁移「开箱能跑多少」的量化基线缺失。**

### 4.5 规格验证（准入 8 / 打回 0）

- COMP-005→**P0**(inputs 类型安全语义)、COMP-006→P1(合并 SEC-016)、COMP-007→P1(RUN_ID,合并 USE-014)、COMP-008→P0(合并 COMPAT-008)、COMP-001→P2、COMP-002→P2(⟳TC-289)、COMP-003→P2(⟳TC-422/514)、COMP-004→P2(⟳TC-426)。

---

## 5. 维度完整性检查（rules §11）

| 维度 | 准入数 | P0 | P1 | P2 | 是否达标 |
|---|---|---|---|---|---|
| security | 31 | 9 | 22 | 0 | ✅ **非空且 P0 充分** |
| compatibility | 57 | 3 | 33 | 21 | ✅ |
| reliability | 30 | 0 | 16 | 14 | ⚠️ **无独立 P0**（见下） |
| usability | 24 | 0 | 12 | 12 | ⚠️ **无独立 P0**（合理，见 §4.4） |
| completeness(spec) | 8 | 2 | 2 | 4 | ✅ |

**维度完整性裁决**：
- 五维度均有准入 intent，**security 维度非空且含 9 个 P0 ✅**（门禁硬要求达标）。
- **reliability 无独立 P0**：其安全命脉项（runner 残留 SEC-025、缓存投毒 SEC-019）已被 security P0 以 `[security,reliability]` 双标覆盖。纯稳定性视角下「故障后无法恢复/数据损坏」为 quality-gate blocker 判据——当前故障注入类(REL-018~026)裁为 P1，因**均有 recovery_expectation 且非不可逆**。**若平台确认存在「故障后数据损坏」场景，REL-020(kill runner 收敛)应升 P0**——列入用户裁决点。
- **usability 无 P0**：合理（见 §4.4）。

---

## 6. 覆盖盲区清单（对照 spec.md 133 能力项 + 36 缺口）

> 事实左列 = spec.md 能力项/缺口（因官方 parity-matrix 模板态）。以下为**无任何准入 intent 覆盖**的能力/风险项，如实暴露（rules 护栏：宁 STOP 不隐藏）。

| # | 盲区（能力项/缺口） | 严重度 | 建议补哪个维度挖 |
|---|---|---|---|
| BLIND-01 | **C-EXEC-24 取消语义**：手动取消/抢占时运行中 step 如何终止、清理钩子保证——仅 REL-029(post清理)部分触及，**step 级取消终止行为无 intent** | 高 | reliability + usability（取消后状态收敛+日志可理解） |
| BLIND-02 | **C-RUN-09/10 container 自定义镜像**：image/credentials/volumes/options 能力——TC-273 历史 FAIL(容器不可用)但本轮**无 intent 覆盖 container 执行/私有镜像认证** | 高 | completeness + security（container credentials secret 泄露面） |
| BLIND-03 | **C-EXEC-15~20 matrix include/exclude/动态runs-on 正确性**：仅 REL-010(组合数上限探测)覆盖，**展开正确性/include追加/exclude 的功能验证无 intent**（基底 TC-325-328 覆盖但本轮兼容差异未挖） | 中 | completeness/compatibility |
| BLIND-04 | **C-ACT-13 action runs.post 清理入口**（SIGINT 监听）+ C-ACT-11~17 自定义 action 开发面——**无 intent**（本轮聚焦使用侧，未覆盖 action 作者侧） | 中 | completeness（若在测范围）；可判定为 out-of-scope |
| BLIND-05 | **C-SEC-13 ATOMGIT_REF_PROTECTED**（分支保护 ref 标志）——**无 intent**，影响基于保护分支的条件安全逻辑 | 中 | security |
| BLIND-06 | **C-OBS-04 Step Summary / C-OBS-05 状态徽标 badge**——USE 可观测覆盖 error/warning(USE-023) 但 **step summary 写入、badge SVG 无 intent** | 低 | usability |
| BLIND-07 | **C-TRIG-08 schedule/cron 完整语义**——历史 S3×24+TC-391/TC-427-474 **Scheduler 整体不工作**(NEEDS-UPDATE E 类)，本轮**无 schedule intent 重验** | 高 | reliability（回归验证：scheduler 修复后 cron 运算符/UTC/最小间隔） |
| BLIND-08 | **C-VAR-05 RUNNER_* 系统变量注入**——历史 TC-441/442 FAIL、TC-533 env 不注入 Shell、TC-206 owner 未注入(NEEDS-UPDATE)，本轮 COMPAT-033 触及命名但**「变量是否真注入 Shell」的回归无 intent** | 高 | compatibility/reliability（回归：env>vars 优先级链、$VAR 注入） |
| BLIND-09 | **C-EXPR-04 表达式函数边界**（G-33 空值/类型转换）——COMPAT-010/012/013 覆盖部分，但 **format/substring/replace/toJson 边界行为无独立 intent** | 中 | compatibility |
| BLIND-10 | **G-28/G-29 atomgit.actor 缺失 + 上下文 12vs11 计数**——COMPAT-026/USE-019 触及 actor，但**上下文完整性(12种声明 vs 11 表)缺口无坐实 intent** | 中 | completeness |
| BLIND-11 | **C-SEC-14 环境保护 wait timer / C-EXEC-22 preemption 抢占语义细节**——SEC-030 覆盖 reviewers 但 **wait timer 未挖**；REL-005/006 覆盖 preemption 边界但**抢占触发条件/效果(G,模糊)未系统覆盖** | 中 | security + reliability |

**盲区裁决**：BLIND-01/02/07/08 为**高严重度**，其中 07/08 关联历史确证 bug（Scheduler、变量注入），**强烈建议补 intent 后再进入阶段B**，否则回归覆盖有洞。BLIND-04 建议判 out-of-scope（action 开发侧）。

---

## 7. 打回 / 待补清单（4 条）

| ID | 维度 | 打回原因（可操作） | 重提条件 |
|---|---|---|---|
| INTENT-REL-011 | reliability | 账户/仓库级全局并发上限——G-11 规格未声明该上限是否存在，**oracle 缺失**，退化为无确定断言的探索（违 rules §8） | 先向平台确认是否存在全局并发上限；若存在→补预期值后重提为探测用例；若不存在→关闭 |
| INTENT-REL-016 | reliability | workflow 文件大小上限——G-09 未公开，**纯找数字、无行为契约/恢复预期**，不满足最小可测标准 | 补「超限后的解析行为/报错」作 oracle 后重提 |
| INTENT-REL-017 | reliability | 单仓 secret 数上限——同上，无行为契约 | 补「达上限后新增 secret 的拒绝行为」后重提 |
| INTENT-USE-018 | usability | 「示例可直接复刻」范围过宽——「所有 quick-start+内置 action 示例开箱可跑」非单一 oracle，四要素无法对单条布置 | 拆分为「quick-start 最小示例」「nodejs-ci 示例」等具体单条用例，各带独立 oracle 后重提 |

> 注：REL-013(artifact 上限)、REL-014(cache 上限)**未打回**——有 LRU/超限降级行为可作 nonfunctional 断言，保留 P2 准入。

---

## 8. 最需用户裁决的点（STOP① 决策）

1. **【盲区回归缺口 · 最高优先】** BLIND-07(Scheduler 整体不工作)、BLIND-08(变量不注入 Shell) 关联历史**已确证 bug**（cases.md 问题 §S3×24、TC-533/206/441/442）。本轮 160 条 intent **未覆盖这两类回归**。是否：(a) 补 reliability/compatibility intent 覆盖回归后再展开（推荐）；(b) 判定「待平台修复，本轮不测」标 out-of-scope；(c) 复用旧 NEEDS-UPDATE 用例跟踪即可。

2. **【reliability P0 空缺】** 稳定性维度无独立 P0——故障注入类(REL-018~026)当前裁 P1（假定均可恢复）。若平台存在「故障后数据损坏/状态不可收敛」场景（如 REL-020 kill runner），应升 P0。**请确认：是否有已知的不可恢复故障场景？** 无则维持 P1。

3. **【优先级临时裁定的效力】** 全部 P0/P1/P2 因 risk-register 模板态为**门禁临时裁定**。请确认：(a) 认可本裁定作为阶段B展开依据、待基线刷新回归（推荐）；(b) 先刷新 risk-register 为真实风险项再回炉定级。若选(b)，阶段B 阻塞至基线就绪。

---

## 9. 交接说明

- **准入 121 条**可进入阶段B展开；**合并 21 条**作变体随母 intent 展开（不独立新建）；**已有覆盖 14 条**建议 case-writer 读 case-base-detail 基底做 delta 复用；**打回 4 条**留在 intent-library 标注原因，不进 cases/。
- **溯源链**(rules §7)：每条准入已挂能力项/缺口（见 §4），阶段B 展开时文本用例须含 `溯源意图: INTENT-xxx`。
- **优先级回归提醒**：risk-register 刷新后，按本 gate-log §2 血缘逐条复核 Pn。
- 回标已同步至 `intent-library.md` 门禁列（准入(Pn)/打回/合并→母ID/已有覆盖(TC)）。

<!-- END gate-log -->



