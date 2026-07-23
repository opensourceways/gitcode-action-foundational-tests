# 覆盖度报告（Coverage）

> Run: 2026-07-22-01
> 评审日期: 2026-07-22
> 覆盖坐标系: Parity Matrix 能力项 × 风险登记册风险项

---

## 一、覆盖度摘要

| 维度 | 准入 intent | 新增用例 | 复用 TC | 合计覆盖 | P0 覆盖 |
|---|---|---|---|---|---|
| completeness | 16 | 10 | 15 | 25 | 6/6 ✅ |
| compatibility | 35 | 10 | 32 | 42 | 6/6 ✅ |
| security | 36 | 27 | 12 | 39 | 35/35 ✅ |
| reliability | 66 | 15 | 53 | 68 | 0/0 — |
| usability | 29 | 0 | 29 | 29 | 1/1 ✅ |
| **合计** | **186** | **62** | **95** | **157** | **48/48 ✅** |

> 注：「合计覆盖」= 新增用例 + 复用 TC，部分 intent 对应多条 TC。

---

## 二、Parity Matrix 覆盖度

Parity Matrix 共 **44 项能力项**，覆盖评审结果：

| 支持状态 | 能力项数 | 有 intent/用例覆盖 | 未覆盖（盲区） |
|---|---|---|---|
| ✅ 完全支持 | 12 | 12 | 0 |
| 🟡 部分支持 | 16 | 16 | 0 |
| ❌ 不支持 | 5 | 5 | 0 |
| ❓ 未知 | 11 | 4 | **7** |
| **合计** | **44** | **37** | **7** |

### 已覆盖的 ❓ 未知项（4/11）
- Runner 环境隔离 / 一次性 → SEC-020~022, COMPAT-028
- `permissions` 默认权限 → COMP-013, SEC-017
- `cache` fork 场景隔离 → SEC-018, COMPAT-025
- `permissions` 权限域命名 → COMPAT-030

### 未覆盖的 ❓ 未知项（7 项 → 覆盖盲区）
见「五、覆盖盲区清单」。

---

## 三、风险登记册覆盖度

风险登记册共 **5 条风险项**，覆盖评审结果：

| 风险 ID | 维度 | 优先级 | 是否 blocker | 覆盖状态 | 覆盖用例/intent |
|---|---|---|---|---|---|
| RISK-SEC-01 | 安全性 | P0 | ✅ 是 | ✅ **全覆盖** | SEC-001~036, COMP-011~016, COMPAT-002/025/028/030/032/033, USE-016 |
| RISK-SEC-02 | 安全性 | P0 | ✅ 是 | ✅ **全覆盖** | SEC-009~013/023/026/029/030/031, COMPAT-002 |
| RISK-COMPAT-01 | 兼容性 | P1 | 否 | ✅ 全覆盖 | COMPAT-001~035, COMP-001~018 |
| RISK-REL-01 | 稳定性 | P1 | 否 | ✅ 全覆盖 | REL-001~066 |
| RISK-USE-01 | 易用性 | P1 | 否 | ✅ 全覆盖 | USE-001~030 |

> **结论：全部 5 条风险项均有 intent/用例覆盖，2 个 blocker 风险项均有 P0 用例覆盖。**

---

## 四、双轴覆盖矩阵

### 按维度标签 × 按优先级

| 维度 | P0 | P1 | P2 | 小计 |
|---|---|---|---|---|
| completeness | 6 | 9 | 1 | 16 |
| compatibility | 6 | 26 | 3 | 35 |
| security | 35 | 1 | 0 | 36 |
| reliability | 0 | 64 | 2 | 66 |
| usability | 1 | 27 | 1 | 29 |
| **合计** | **48** | **127** | **7** | **182** |

> 注：4 条跨维度 intent 在表中按主维度统计。

### 按维度 × 按用例形态

| 维度 | 新增文本用例 | 新增 YAML | 复用 TC | 溯源链闭合 |
|---|---|---|---|---|
| completeness | 10 | 10 | 15 | ✅ |
| compatibility | 10 | 10 | 32 | ✅ |
| security | 27 | 27 | 12 | ✅ |
| reliability | 15 | 15 | 53 | ✅ |
| usability | 0 | 0 | 29 | ✅ |

---

## 五、覆盖盲区清单

以下 7 项能力/规格缺口当前无 intent/用例覆盖，已在 `gate-log.md` 中记录：

| # | 盲区 | 能力项状态 | 建议补哪个维度 | 优先级建议 |
|---|---|---|---|---|
| 1 | **注解(annotation)机制** — `::error file=...::message` 行级 annotation 回写 | ❓ 未知 | completeness / usability | P1 |
| 2 | **action `runs.using` 支持范围** — node20/docker/composite 是否支持 | ❓ 未知 | completeness / compatibility | P1 |
| 3 | **runner.debug 触发方式** — 文档未说明如何开启 debug 模式 | ❓ 未知 | completeness | P2 |
| 4 | **自托管 Runner 同时运行多个 Job** — 文档未明确 | ❓ 未知 | reliability / security | P1 |
| 5 | **K8s Runner 容器隔离边界** — Pod 网络策略、特权模式、宿主机访问限制 | ❓ 未知 | security | P1 |
| 6 | **取消语义完整行为** — 被抢占时 step 终止、post 执行 | ❓ 未知 | reliability | P1 |
| 7 | **`issue_comment` / `pull_request_comment` 默认 types** — 评论触发器默认行为 | ❓ 未知 | completeness | P2 |

---

## 六、溯源链闭合检查

溯源链：`风险项/能力项 → INTENT-xxx → 文本用例 ID → 派生 YAML(intent_ref)`

| 检查项 | 状态 | 说明 |
|---|---|---|
| 每条准入 intent 可追溯到风险项或能力项 | ✅ | 186/186 |
| 每条新增文本用例含 `溯源意图: INTENT-xxx` | ✅ | 62/62 |
| 每条新增 YAML 含 `intent_ref: INTENT-xxx` | ✅ | 62/62 |
| 每条复用 TC 在 manifest 中标注关联 intent | ✅ | 95/95 |
| 每个 blocker 风险项可反查到 P0 用例 | ✅ | RISK-SEC-01 / RISK-SEC-02 |

---

## 七、结论

- **blocker 风险全覆盖**：2 个 P0 blocker 风险项均有 intent/用例覆盖。
- **Parity Matrix 高覆盖**：44 项中 37 项（84%）有覆盖，7 项 ❓ 未知因规格未明暂留盲区。
- **维度完整性**：五个维度均有准入 intent，安全维度 36 条（含 35 P0），不可为空已满足。
- **溯源链完整**：风险 → intent → 用例 → YAML 全链路闭合。

> 盲区均为「规格未明/文档缺失」类，非测试设计遗漏。建议平台补全文档后，通过 `/phase01-update` 补充对应 intent。
