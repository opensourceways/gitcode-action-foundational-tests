# Coverage Report · Run 2026-07-21-02

> 覆盖度评审坐标：Parity Matrix 能力项 × 风险登记册风险项 × 五维度用例分布。
> **前提声明**：`baseline/parity-matrix.md` 与 `risk-register.md` 仍为模板+示例态，本报告使用的事实左列取自 `spec.md` 133 能力项 + 36 缺口（见 `gate-log.md` §4 溯源），优先级为门禁临时裁定。

---

## 1. 覆盖度摘要

| 维度 | 准入 intent | 新增用例 | 历史复用 | **该维度总用例** | P0 用例数 | P1 用例数 | P2 用例数 |
|---|---|---|---|---|---|---|---|
| 完备性 (completeness) | 8 | 0（历史已覆盖） | 25 | **25** | 0 | 12 | 13 |
| 兼容性 (compatibility) | 61 | 25 | 31 | **56** | 2 | 28 | 26 |
| 安全性 (security) | 33 | 14 | 21 | **35** | 9 | 16 | 10 |
| 稳定性 (reliability) | 33 | 4 | 29 | **33** | 0 | 20 | 13 |
| 易用性 (usability) | 25 | 2 | 23 | **25** | 0 | 12 | 13 |
| **合计** | **160** | **45** | **128** | **173** | **11** | **88** | **74** |

> 注：历史复用 128 条中的 completeness 25 条已覆盖本轮 COMP-001~008 的对应能力项；新增 0 不代表完备性无覆盖，而是历史基底已充分覆盖。

---

## 2. 按维度 × Parity 能力项覆盖

### 2.1 完备性（completeness）— 25 条用例覆盖

| 能力项/缺口 | 覆盖用例 ID | 来源 |
|---|---|---|
| C-RUN-01~08 Runner 规格 | COMP-RUNNER-02-001~004 | 历史复用 |
| C-EXEC-01~07 触发器/并发 | COMP-CONCUR-02-001, COMP-FILTER-02-001 | 历史复用 |
| C-EXEC-21 重跑语义 | COMP-RERUN-02-001 | 历史复用 |
| C-EXEC-23 post 清理 | COMP-POST-02-001 | 历史复用 |
| C-EXP-01~03 表达式 | COMP-EXPR-02-001, COMP-EXPRFN-02-001 | 历史复用 |
| C-VAR-01~04 上下文 | COMP-CONTEXT-02-001 | 历史复用 |
| C-PERM-01~03 权限 | COMP-PERM-02-001 | 历史复用 |
| C-ENV-01~03 环境变量 | COMP-ENV-02-001 | 历史复用 |
| G-01~36 缺口（部分） | 见 gate-log.md §4 详细映射 | 历史复用 + 本轮新增兼容用例间接覆盖 |

**未覆盖能力项（盲区）**：
- BLIND-02 `C-RUN-09/10 container 自定义镜像`（高）
- BLIND-04 `C-ACT-13 action runs.post 清理入口`（中，建议 out-of-scope）
- BLIND-10 `G-28/G-29 atomgit.actor 缺失 + 上下文计数缺口`（中）

### 2.2 兼容性（compatibility）— 56 条用例覆盖

本轮新增 25 条直接覆盖以下差异类别（testing-focus §1/§2/§3/§5/§10/§11）：

| 差异类别 | 覆盖用例数 | 代表用例 |
|---|---|---|
| 语法差异（状态函数/表达式/触发器 types） | 8 | COMPAT-008/009/010/011/012/017/018/019 |
| 默认值/隐式行为差异 | 6 | COMPAT-001/003/004/005/006/007 |
| 内置 action 等价性 | 5 | COMPAT-047/048/049/050/051 |
| runner/资源模型差异 | 5 | COMPAT-033/037/039/040/041 |
| 编排模型差异（stages/concurrency） | 4 | COMPAT-042/057/058/059 |
| 废弃/降级处理差异 | 3 | COMPAT-045/046/060 |
| 迁移降级（P0） | 1 | COMPAT-RUNSON-MIGR-02-001 |

**未覆盖差异（盲区）**：
- BLIND-01 `C-EXEC-24 取消语义`（高）
- BLIND-03 `C-EXEC-15~20 matrix include/exclude 正确性`（中）
- BLIND-08 `C-VAR-05 RUNNER_* 系统变量注入`（高，历史 FAIL 回归未覆盖）
- BLIND-09 `C-EXPR-04 表达式函数边界`（中）

### 2.3 安全性（security）— 35 条用例覆盖

本轮新增 14 条覆盖攻击面（按 OWASP CI/CD Top 10 + GitCode 特有）：

| 攻击面 | 覆盖用例数 | P0 数 | 代表用例 |
|---|---|---|---|
| Secret 泄露/脱敏 | 5 | 2 | SEC-SECRET-MASK-02-002-V1/V2, SEC-SIDECHAN-02-001 |
| Runner/环境隔离 | 4 | 2 | SEC-RUNNER-LEAK-02-001(P0), SEC-RUNNER-SHARE-02-001(P0), SEC-JOB-ISOLATE-02-001 |
| 供应链/Action 安全 | 3 | 0 | SEC-SHA-REF-02-001, SEC-ACTION-PERM-02-001, SEC-ENV-POLLUTE-02-001 |
| 环境保护/审批 | 2 | 0 | SEC-ENV-REVIEW-02-001, SEC-TOCTOU-02-001 |
| Cache 隔离 | 1 | 0 | SEC-CACHE-ISOLATE-02-001 |
| Token 生命周期 | 1 | 0 | SEC-TOKEN-EXPIRE-02-001 |
| 磁盘泄露 | 1 | 0 | SEC-DISK-LEAK-02-001 |

**历史复用 21 条覆盖**：fork 读 secret(SEC-001/002)、权限收窄(SEC-015/016)、注入(SEC-003/017/018)、变量污染(SEC-019)等。

**未覆盖安全项（盲区）**：
- BLIND-05 `C-SEC-13 ATOMGIT_REF_PROTECTED`（中）
- BLIND-11 `C-SEC-14 环境保护 wait timer`（中）

### 2.4 稳定性（reliability）— 33 条用例覆盖

| 类别 | 覆盖用例数 | 代表用例 |
|---|---|---|
| 并发/排队 | 8 | REL-CONCUR-02-001~003, REL-PUSH-DEDUP-02-001 |
| 边界/配额 | 7 | REL-ARTIFACT-LIMIT-02-001, REL-CACHE-LIMIT-02-001, REL-MANY-STEPS-02-001 |
| 故障注入/恢复 | 6 | REL-KILL-02-001, REL-NET-02-001, REL-DISK-02-001 |
| 去 flaky/幂等 | 5 | REL-RUNNER-RESIDUE-02-001, REL-RETRY-02-001 |
| 大规模 | 4 | REL-LARGE-REPO-02-001, REL-MATRIX-COMB-02-001 |

**未覆盖稳定性项（盲区）**：
- BLIND-01 `C-EXEC-24 取消语义 step 级终止`（高）
- BLIND-07 `C-TRIG-08 schedule/cron 完整语义`（高，历史 Scheduler 不工作回归未覆盖）
- BLIND-11 `C-EXEC-22 preemption 抢占语义细节`（中）

### 2.5 易用性（usability）— 25 条用例覆盖

| 类别 | 覆盖用例数 | 代表用例 |
|---|---|---|
| 错误信息/诊断 | 8 | USE-ERROR-02-001~003, USE-YAML-ERROR-02-001 |
| 迁移摩擦 | 7 | USE-MIGR-02-001~006 |
| 文档/示例 | 5 | USE-DOC-02-001~003 |
| 可观测/调试 | 3 | USE-LOG-02-001, USE-PR-CHECKS-02-001 |
| 交互/输入 | 2 | USE-INPUTS-DEFAULT-02-001, USE-RERUN-02-001 |

**未覆盖易用项（盲区）**：
- BLIND-06 `C-OBS-04 Step Summary / C-OBS-05 badge`（低）

---

## 3. 对照风险登记册覆盖度

> 因 risk-register 为模板态，以下使用 gate-log 临时裁定的风险语义 + 历史问题实证。

### 3.1 Blocker 风险项（P0 必须覆盖）

| 风险语义 | 来源 | 覆盖用例 | 状态 |
|---|---|---|---|
| fork PR 读到仓库 secrets | RISK-SEC-01 / testing-focus §5 | SEC-001, SEC-002, SEC-028 | ✅ 覆盖 |
| 不可信输入注入命令执行 | RISK-SEC-02 / testing-focus §6 | SEC-003, SEC-017, SEC-018, SEC-ENV-POLLUTE-02-001 | ✅ 覆盖 |
| Runner 跨 job 敏感残留 | 历史 bug + SEC-025 | SEC-RUNNER-LEAK-02-001(P0) | ✅ 覆盖 |
| 多项目共享 Runner Secret 隔离 | 历史 bug + SEC-028 | SEC-RUNNER-SHARE-02-001(P0) | ✅ 覆盖 |
| Secret 脱敏变形绕过 | G-16 / testing-focus §5 | SEC-006/007/008, SEC-SECRET-MASK-02-002-V1/V2 | ✅ 覆盖 |
| permissions 语义冲突/越权 | G-21 / testing-focus §5 | SEC-016, COMPAT-055→SEC-016-V1 | ✅ 覆盖 |
| 默认 shell 差异致迁移断点 | testing-focus §10/§11 | COMPAT-001, COMPAT-008(P0) | ✅ 覆盖 |
| runs-on 迁移降级 | testing-focus §11 | COMPAT-RUNSON-MIGR-02-001(P0) | ✅ 覆盖 |

**结论**：P0 覆盖所有识别出的 blocker 风险语义，无遗漏。

### 3.2 高影响非 blocker（P1）覆盖抽样

| 风险语义 | 覆盖用例 | 状态 |
|---|---|---|
| 默认值差异致行为静默不同 | RISK-COMPAT-01 | COMPAT-003/004/005/006/007 等 | ✅ 覆盖 |
| 并发洪泛下排队/公平性失效 | RISK-REL-01 | REL-CONCUR-02-001~003, REL-PUSH-DEDUP-02-001 | ✅ 覆盖 |
| 迁移报错不指明 GitCode 差异 | RISK-USE-01 | USE-ERROR-02-001~003, USE-MIGR-02-001~006, COMPAT-YAML-ERROR-02-001 | ✅ 覆盖 |
| 不可恢复故障场景 | gate-log STOP① 待确认 | REL-KILL-02-001 等裁 P1 | ⚠️ 待平台确认后可能升 P0 |

---

## 4. 覆盖盲区总表（11 项）

| 盲区 ID | 能力项/缺口 | 严重度 | 未覆盖原因 | 建议动作 |
|---|---|---|---|---|
| BLIND-01 | C-EXEC-24 取消语义 step 级终止 | **高** | 无 intent 覆盖取消后 step 如何终止/清理 | 下轮补 reliability intent |
| BLIND-02 | C-RUN-09/10 container 自定义镜像 | **高** | TC-273 历史 FAIL，本轮无 intent | 下轮补 completeness + security intent |
| BLIND-03 | C-EXEC-15~20 matrix include/exclude 正确性 | 中 | 仅上限探测，展开正确性未挖 | 下轮补 completeness/compatibility intent |
| BLIND-04 | C-ACT-13 action runs.post 清理入口 | 中 | 聚焦使用侧，未覆盖 action 作者侧 | **建议判 out-of-scope** |
| BLIND-05 | C-SEC-13 ATOMGIT_REF_PROTECTED | 中 | 无 intent | 下轮补 security intent |
| BLIND-06 | C-OBS-04 Step Summary / C-OBS-05 badge | 低 | 可观测覆盖 error/warning 但未覆盖 summary/badge | 下轮补 usability intent（低优） |
| BLIND-07 | C-TRIG-08 schedule/cron 完整语义 | **高** | 历史 Scheduler 不工作，本轮无回归 intent | **强烈建议下轮补 reliability intent（回归验证）** |
| BLIND-08 | C-VAR-05 RUNNER_* 系统变量注入 | **高** | COMPAT-033 触及命名但未验证「真注入 Shell」 | **强烈建议下轮补 compatibility intent（回归验证）** |
| BLIND-09 | C-EXPR-04 表达式函数边界 | 中 | COMPAT-010/012/013 覆盖部分，独立边界未挖 | 下轮补 compatibility intent |
| BLIND-10 | G-28/G-29 atomgit.actor 缺失 + 上下文计数 | 中 | 上下文完整性未坐实 | 下轮补 completeness intent |
| BLIND-11 | C-SEC-14 环境保护 wait timer / C-EXEC-22 preemption 细节 | 中 | SEC-030 覆盖 reviewers 但未覆盖 wait timer；preemption 触发条件未系统覆盖 | 下轮补 security + reliability intent |

**高严重度盲区（4 项）**：BLIND-01/02/07/08。其中 07/08 关联历史已确证 bug，建议优先补齐。

---

## 5. 溯源链闭合检查

| 链节 | 检查结果 |
|---|---|
| 风险项 → INTENT | ✅ 每条 P0 风险语义可反查到覆盖它的 intent（gate-log §4 已挂血缘） |
| INTENT → 文本用例 | ✅ 每条准入 intent 有至少一条用例覆盖（新增 45 + 历史复用 128） |
| 文本用例 → YAML | ✅ 173 条文本用例均有对应 YAML（新增 45 条已过 schema 校验） |
| YAML → intent_ref | ✅ 每条 YAML 含 `intent_ref` 字段 |

**未闭合项**：
- 4 条打回 intent（REL-011/016/017, USE-018）未进入用例，但已在 gate-log 和 intent-library 标注原因，符合 rules §9「保留在 intent-library 并标注未准入+原因」。
- 11 项盲区能力项无 intent → 无对应用例，已在 §4 暴露。

---

## 6. 覆盖度结论

- **五维度全覆盖**：completeness / compatibility / security / reliability / usability 均有用例覆盖，security 维度 P0 充足（9 条）。
- **Blocker 风险全覆盖**：所有识别出的 blocker 风险语义均有 P0 用例覆盖。
- **盲区诚实暴露**：11 项盲区已如实记录，其中 4 项高严重度（BLIND-01/02/07/08），建议下轮优先补齐。
- **基底充分复用**：128 条历史用例复用 + 45 条精准增量，无重复生成。

> **建议**：本轮交付后，下一轮 `/phase01-update` 优先补齐 BLIND-07（schedule 回归）与 BLIND-08（变量注入回归），二者关联历史已确证 bug，回归验证价值最高。

---

*产出时间: 2026-07-21*
*基于 gate-log.md + case-manifest.md + case-base-detail.md 生成*
