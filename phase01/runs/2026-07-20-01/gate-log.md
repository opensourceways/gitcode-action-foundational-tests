# Gate Log · Run 2026-07-20-01

> 评审门禁记录。review-gate agent + orchestrator 联合产出。
> 状态：GATE PASSED → 进入阶段B。

---

## 1. Review-Gate Agent Assessment

> Agent: review-gate | Date: 2026-07-20
> Inputs audited: intent-library.md (144 intents), 5 raw intent files (spec.md, compat.md, security.md, reliability.md, usability.md), risk-register.md, parity-matrix.md, quality-gate.md, rules.md, existing-cases/cases.md (629 cases)

### 1.1 Dedup Results

**Total duplicates merged: 1**
**Variant/overlap relationships established: 8**

| Pair | Relationship | Verdict | Rationale |
|---|---|---|---|
| **COMP-012 ↔ COMPAT-003** (status function syntax) | Variant | Keep both, link | COMP-012 asks "does GitCode's own `${{ success }}` syntax work?" (completeness); COMPAT-003 asks "does `${{ success }}` equal GitHub's `${{ success() }}`?" (compatibility). Different oracle sources, overlapping test assertions. |
| **COMP-014 ↔ COMPAT-001** (atomgit context attributes) | Strong overlap | Keep both, COMP-014 = subset | COMP-014 covers 20 documented attributes; COMPAT-001 additionally covers GitHub-only attributes absent from atomgit (action_path, actor_id, etc). COMP-014's scope is a subset. |
| **COMPAT-021 → COMP-016** (workflow_call 2-layer nesting) | **Subset → MERGE** | Merge COMPAT-021 into COMP-016 | COMPAT-021's only unique contribution (2-layer pass / 3-layer reject) is already in COMP-016's verification points. Merge the compat cross-ref into COMP-016. |
| **COMPAT-028 ↔ SEC-005/006/007/008** (secret masking) | Superset (summary) | Demote COMPAT-028 to cross-ref | SEC-005 through SEC-008 cover echo/env/base64/concatenation masking in greater detail. COMPAT-028 adds no unique assertions. Mark COMPAT-028 as `superseded-by SEC-005~008`, retain cross-ref. |
| **COMPAT-019 ↔ COMP-002** (paths 300-file limit) | Partial overlap | Keep both, link | COMP-002 already covers 300-file behavior; COMPAT-019 adds the GitHub 3000-file threshold comparison. |
| **USE-010 ↔ COMPAT-024** (workflow commands) | Heavy overlap | Keep both, link | USE-010 tests from debugging-experience perspective (does log fold?); COMPAT-024 tests from compatibility perspective (GitCode vs GitHub equivalence). Verification points nearly identical. |
| **COMPAT-016 ↔ USE-018** (inputs type limitation) | Partial overlap | Keep both, link | COMPAT-016 verifies rejection; USE-018 verifies error message quality. Complementary. |
| **COMPAT-008 ↔ SEC-003/004** (pull_request_target semantics) | Subset | Keep all; SEC intents are drill-downs | COMPAT-008 covers broad semantics; SEC-003 (base branch execution) and SEC-004 (checkout head.sha risk) are focused security drill-downs with stronger negative assertions. |
| **USE-014 ↔ COMPAT-027** (migration friction) | Complementary | Keep both | USE-014 = empirical test (copy-paste error path); COMPAT-027 = theoretical checklist (10 friction points). |

**Existing case coverage (0 intents suppressed):** All 144 intents add value beyond existing 629 cases — existing cases verify "does the feature work?" atomically; new intents verify "does the feature work *systematically*?" and "is it *secure/compatible/usable under stress*?"

### 1.2 Priority Audit

**Risk register baseline:** Only 5 risk items (RISK-SEC-01 P0, RISK-SEC-02 P0, RISK-COMPAT-01 P1, RISK-REL-01 P1, RISK-USE-01 P1), explicitly marked as template. With only 2 blocker risks, the 34 P0 intents in the library exceed justified P0 count.

**P0s correctly tracing to blocker risks (keep P0): 19 intents**

SEC-001, SEC-002, SEC-003, SEC-004, SEC-005, SEC-009, SEC-010, SEC-011, SEC-012, SEC-014, SEC-015, SEC-016, SEC-018, SEC-019, SEC-025, SEC-029, SEC-030, SEC-036, COMPAT-008, COMPAT-009, COMP-015 — all trace to RISK-SEC-01 (fork PR isolation, permissions, token scope) or RISK-SEC-02 (injection, information leak).

**P0s NOT tracing to blocker risks → DEMOTE to P1: 15 intents**

| Intent | Current | Proposed | Reason |
|---|---|---|---|
| COMP-009 (stages) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). Stages is GitCode-only, no compat blocker. |
| COMP-016 (workflow_call) | P0 | P1 | No blocker risk trace. Workaround exists (inline workflow). |
| COMP-022 (action ref) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). Workaround (use full path). |
| COMP-023 (fail-fast) | P0 | P1 | No blocker risk trace. Matrix fail-fast is standard GitHub behavior. |
| COMPAT-001 (context attributes) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). |
| COMPAT-003 (status function syntax) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). Syntax difference documented. |
| COMPAT-007 (PR types naming) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). Naming difference documented. |
| COMPAT-011 (runner context) | P0 | P1 | No blocker risk trace. Already FAIL-documented (TC-094/095). |
| COMPAT-012 (builtin actions) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). Workaround (use short names). |
| COMPAT-014 (default shell) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). |
| COMPAT-015 (concurrency model) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). Model difference documented. |
| COMPAT-019 (paths filter) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). 300-file limit documented. |
| COMPAT-020 (schedule) | P0 | P1 | Traces to RISK-COMPAT-01 (P1). Schedule broken is known (S3×24+TC-391 FAIL). |
| REL-007 (matrix fail-fast) | P0 | P1 | No blocker risk trace. |
| REL-015 (kill runner) | P0 | P1 | Traces to RISK-REL-01 (P1). |
| REL-022 (needs chain) | P0 | P1 | Traces to RISK-REL-01 (P1). |
| REL-024 (needs + matrix) | P0 | P1 | Traces to RISK-REL-01 (P1). Known P1 bug TC-486. |
| USE-014 (e2e migration) | P0 | P1 | Traces to RISK-USE-01 (P1). |
| USE-015 (runs-on error) | P0 | P1 | Traces to RISK-USE-01 (P1). |

**Exception:** USE-016 (permissions naming error) is retained as P0 — while its primary focus is error message quality (P1), the risk note states "静默忽略权限差异 = 安全/行为风险". The behavioral assertion (must not silently ignore unknown permission names) IS a P0 security concern.

**Blocker risks without P0 coverage: 0.** Both RISK-SEC-01 and RISK-SEC-02 have sufficient P0 intent coverage.

**Revised priority distribution:**

| Dimension | P0 (before) | P0 (after) | P1 (before) | P1 (after) |
|---|---|---|---|---|
| completeness | 5 | 1 | 20 | 24 |
| compatibility | 9 | 2 | 22 | 28 |
| security | 14 | 16 | 22 | 20 |
| reliability | 3 | 0 | 26 | 29 |
| usability | 3 | 1 | 20 | 22 |
| **Total** | **34** | **20** | **110** | **123** |

**Reliability P0 gap:** After demotion, reliability has 0 P0 intents. The quality-gate requires "P0 稳定性用例全过" — with no P0 stability intents, this gate is vacuously satisfied. **Recommendation:** Either promote REL-015 (runner kill recovery, data loss risk) back to P0, or add a new P0 reliability intent.

### 1.3 Coverage Blind Spots

#### Uncovered Spec-Analyst Capability Gaps

From the spec-analyst's 94-item capability catalog (spec.md Part B), the following gaps have no intent coverage:

| Gap ID | Description | Severity | Suggested Dimension |
|---|---|---|---|
| **G14** | `container.image` — doc says supported, TC-273 shows non-functional | P1 | completeness |
| **G15** | `environment` field YAML syntax — doc mentions approval, TC-010 shows unknown property | P1 | completeness or usability |
| **G19** | Multi-workflow same-trigger execution order — undefined when multiple .yml match same event | P1 | reliability |
| — | **OIDC / short-lived credentials** — no doc, no intent; critical for cloud auth | **P0** | security |
| — | `services:` field (service containers) — GitHub supports, GitCode unknown | P1 | compatibility |
| — | `ACTIONS_STEP_DEBUG` / `ACTIONS_RUNNER_DEBUG` debug logging — existence unverified | P2 | usability |
| — | Self-hosted runner security model — registration token, network boundary | P1 | security |
| — | Webhook event payload validation — malformed payload handling | P2 | reliability |

#### Under-Covered Areas (by feature domain)

| Area | Current Coverage | Gap |
|---|---|---|
| Composite actions | SEC-031 only (security) | No completeness intent for definition, inputs/outputs, nesting |
| Docker container actions | None | `runs.using: docker` not tested |
| OIDC / cloud credentials | None | Unknown if GitCode supports OIDC |
| Workflow dispatch UI | USE-018 only (inputs type) | Manual trigger UX not covered |
| Rate limiting / DoS | REL-001/002 (concurrency side) | Fork PR spam DoS not covered |
| Action registry / marketplace | None | Discovery, verified creator, deprecation |
| Log retention / export | None | Availability after run, download limits |
| PR Checks API integration | None | Status checks on PRs |
| Notifications | None | Email/webhook/slack on run events |

#### Dimension Label Audit

All cross-dimensional intents have correct `dimensions` arrays with ONE exception:

- **USE-016**: Currently `[usability, compatibility]`. Should additionally include `[security]` — the behavioral assertion "must not silently ignore unknown permission names" is a P0 security concern per the intent's own risk note.

---

## 2. Orchestrator Strategic Assessment

### 2.1 Traceability Chain Status

**风险登记册 blocker 项 → P0 intent 覆盖验证：**

| Blocker 风险 | 覆盖的 P0 Intent | 状态 |
|---|---|---|
| RISK-SEC-01 (fork PR 读到仓库 secrets) | SEC-001 (token 只读), SEC-002 (secret 隔离), SEC-019 (cache 投毒), SEC-025 (runner 残留隔离), SEC-029 (workflow 篡改), SEC-036 (内置 token 安全) | ✅ 已覆盖 |
| RISK-SEC-02 (不可信输入注入命令执行) | SEC-009 (PR标题), SEC-010 (PR正文), SEC-011 (分支名), SEC-012 (commit message), SEC-014 (GITHUB_ENV 污染), SEC-015 (permissions 空声明), SEC-016 (默认权限审计) | ✅ 已覆盖 |

两条 blocker 风险均有充足的 P0 intent 覆盖。溯源链闭合。

**Parity Matrix「部分/不支持/未知」项 → intent 覆盖验证：**

Parity Matrix（`baseline/parity-matrix.md`）当前仅含 8 行模板数据，全部标记为 ❓ 未知。逐一验证：

| Parity 能力项 | 覆盖 Intent | 状态 |
|---|---|---|
| `push` 触发 + branches 过滤 | COMP-001, COMP-002 | ✅ |
| `pull_request_target` | SEC-003, SEC-004, COMPAT-008 | ✅ |
| `${{ contains() }}` | COMP-012, COMP-013, COMPAT-003~006 | ✅ |
| `concurrency` + cancel-in-progress | COMP-005, REL-001~004, COMPAT-015 | ✅ |
| 默认 `permissions` | COMP-015, SEC-015, SEC-016, COMPAT-009, COMPAT-014 | ✅ |
| secret 日志 masking | SEC-005~008, COMPAT-028 | ✅ |
| `actions/checkout` 等价实现 | COMP-022, COMPAT-012 | ✅ |
| `runs-on` 标签 | COMP-017, COMPAT-010 | ✅ |

Parity Matrix 全部 8 行均有 intent 覆盖。但 Parity Matrix 本身严重欠填充（仅模板行），需人工补全真实能力项后才能做完整的覆盖闭合审计。

---

### 2.2 Completeness by Dimension

**按维度 × P0 分布：**

| 维度 | P0 | P1 | P2 | P0 不足？ | 评估 |
|---|---|---|---|---|---|
| completeness | 5 | 20 | 0 | 否 | stages/permissions/reusable workflow/action 引用/matrix 策略的核心路径已 P0 |
| compatibility | 9 | 22 | 0 | 否 | context/表达式/PR types/permissions 命名/runner 格式/内置 action/默认值差异均已 P0 |
| security | 14 | 22 | 0 | **充足** | 6 个攻击面全覆盖，fork PR/注入/脱敏/权限/供应链每一类都有多个 P0 |
| reliability | 3 | 26 | 0 | **偏轻** | 仅 3 个 P0（fail-fast 级联 / kill runner 恢复 / needs 失败传播），其余 26 条全 P1——但质量门禁要求 P0 全过才上线 |
| usability | 3 | 20 | 0 | 否 | 迁移摩擦 3 个核心路径 P0（端到端迁移 / runs-on 映射 / permissions 映射），其余为错误质量与文档一致性 |

**按 testing-focus.md §章节的覆盖检查：**

| 章节 | 覆盖状态 | 缺口 |
|---|---|---|
| §1 语法解析 | ✅ | — |
| §2 触发器语义 | ✅ | — |
| §3 执行模型 | ✅ | — |
| §4 Runner 环境隔离 | ⚠️ | 缺少网络出站策略验证、预装工具链版本确认、容器逃逸测试 |
| §5 Secrets 与权限 | ✅ | — |
| §6 表达式注入 | ✅ | — |
| §7 复用与供应链 | ✅ | Dependabot 等价机制未知，暂无法覆盖 |
| §8 Artifact/Cache | ✅ | — |
| §9 可观测性 | ✅ | — |
| §10 兼容性差异 7 类 | ✅ | 全部 7 类有对应 COMPAT intent |
| §11 迁移摩擦 | ✅ | — |
| §12 稳定性专项 | ⚠️ | CPU 饱和注入缺（可靠性 agent 自承）；自托管 runner 离线恢复缺 |

**安全维度攻击面 6 类覆盖（testing-focus.md §2,5,6,7）：**

| 攻击面 | 覆盖 Intent | 状态 |
|---|---|---|
| fork PR 权限降级 | SEC-001, SEC-002 | ✅ |
| secret 脱敏（含绕过变形） | SEC-005, SEC-006, SEC-007, SEC-008 | ✅ |
| 表达式注入（PR标题/正文/分支/commit/ENV文件） | SEC-009, SEC-010, SEC-011, SEC-012, SEC-013, SEC-014 | ✅ |
| 权限模型 | SEC-015, SEC-016, SEC-017 | ✅ |
| 供应链（SHA pin / cache 投毒 / artifact / workflow 篡改） | SEC-018, SEC-019, SEC-020, SEC-026, SEC-029, SEC-030, SEC-031, SEC-032 | ✅ |
| token 生命周期 | SEC-023, SEC-024, SEC-036 | ✅ |

**兼容性维度 7 类热点覆盖（testing-focus.md §10）：**

| 热点类别 | 覆盖 Intent | 状态 |
|---|---|---|
| 默认值差异 | COMPAT-014, COMPAT-015 | ✅ |
| 表达式函数差异 | COMPAT-003, 004, 005, 006 | ✅ |
| 触发过滤语义差异 | COMPAT-007, 008, 019, 020 | ✅ |
| 上下文对象差异 | COMPAT-001, 011, 025 | ✅ |
| 不支持能力降级 | COMPAT-022 | ✅ |
| 内置 action 差异 | COMPAT-012, 031 | ✅ |
| runner 标签/环境差异 | COMPAT-010, 011 | ✅ |

---

### 2.3 Cross-cutting Themes

以下主题跨越多个维度，intent 间存在内在联系，展开用例时应保持交叉引用：

| 主题 | 涉及 Intent | 维度交叉 | 展开建议 |
|---|---|---|---|
| **pull_request_target** | SEC-003, SEC-004, COMPAT-008 | security × compatibility | 作为联合用例展开：同一次执行同时验证「base 分支执行」（security 视角）和「语义与 GitHub 对齐」（compat 视角） |
| **permissions 模型** | COMP-015, COMPAT-009, COMPAT-014, SEC-015, SEC-016, SEC-017, USE-016 | completeness × security × compatibility × usability | 已有 7 条 intent 从不同角度覆盖，展开时注意：(a) 功能性正确定性 (COMP-015)，(b) 安全验证 (SEC-015~017)，(c) GitHub 命名差异报错 (COMPAT-009, USE-016)，(d) 默认值对齐 (COMPAT-014)。可复用同一套 fixture |
| **cache 隔离** | SEC-019, SEC-020, COMP-007, COMPAT-031 | security × completeness × compatibility | fork PR 缓存投毒 (SEC-019) 和跨事件隔离 (SEC-020) 是安全核心，COMP-007 和 COMPAT-031 验证基础正确性。应作为同一测试组展开 |
| **并发控制** | COMP-005, REL-001~004, REL-021, COMPAT-015, USE-023 | completeness × reliability × compatibility × usability | 并发模型是 GitCode 独有（与 GitHub group 模型不同），从功能完备 (COMP-005)、稳定性 (REL-001~004)、兼容性 (COMPAT-015)、易用性 (USE-023) 四个维度覆盖，应联动设计 |
| **表达式系统** | COMP-012, COMP-013, COMPAT-003~006, SEC-009~014, SEC-035 | completeness × compatibility × security | 表达式既是完备性验证点（函数行为），也是兼容性差异高发点（语法/大小写），还是注入攻击面。展开时优先设计一组合并用例 |
| **stages + post** | COMP-009, COMP-010, COMPAT-017, COMPAT-018, REL-020 | completeness × compatibility × reliability | GitCode 独有机制，无 GitHub 对等物。展开需要以 GitCode 规格为唯一 oracle |

---

### 2.4 Input Gap Impact Assessment

以下三个输入目录缺失，对覆盖置信度的影响评估：

**`workflow-samples/` 缺失：**
- **impact on compat-diff** (COMPAT-005, COMPAT-023, COMPAT-027)：差异发现的「真实常用性」基于文档推断而非实际 workflow 样本。无法确认 startsWith 大小写敏感性影响面、pull_request_comment 的真实使用率、端到端迁移清单的完整性。降级程度：中等——GitHub 文档和 GitCode spec 可覆盖大部分常见模式，但边缘使用场景可能遗漏。
- **impact on usability** (USE-014, USE-019)：迁移摩擦场景选择偏通用，无法验证非标准 GitHub workflow（如 matrix + concurrency + reusable workflow 组合）的迁移路径。降级程度：中等偏高——真实迁移最痛的往往是组合场景而非单字段替换。

**`security-knowledge/` 缺失：**
- **impact on security**：缺少 OWASP CI/CD Top 10 对照、GitCode 特有 CVE 模式、公开漏洞知识库。安全 agent 已在自检中列出 7 项未覆盖领域（GitCode 独有漏洞模式、自托管 runner 内网攻击面、OIDC、全量 workflow 命令注入面、容器逃逸、Dependabot 等价、速率限制）。降级程度：中等偏高——基于通用威胁模型 + GitCode/GitHub 规格文档的推导覆盖面较广（6 类攻击面均有 coverage），但缺少平台特有漏洞模式可能遗漏特定攻击向量。
- **关键盲区**：若 GitCode 在 fork PR 隔离 / ATOMGIT_TOKEN 权限 / expression evaluation 的实现细节与开源 Actions 运行时有实质差异，当前安全 intent 的 oracle（以 GitHub 行为为主）可能不适用。

**`platform-config/` 缺失：**
- **impact on reliability**：所有边界值测试的阈值均为推断值。max_concurrent_workflows、max_matrix_size、artifact/cache 配额、调度延迟 SLO——均无实际数字。受影响的 intent：REL-001（并发洪泛上限）、REL-002（排队上限）、REL-005（矩阵规模边界）、REL-008（max-parallel 上限）、REL-012/013（资源配额边界值）。降级程度：中等——行为模式验证（排队/限流/公平性/故障恢复）仍有效，但绝对边界的「超限即拒绝」断言无法精确设定。
- **关键盲区**：若实际配额远小于推断值（如 max_concurrent_workflows=3 而非推测的 20），部分 intent 的场景设计需要调整。

**`business-context/` 缺失：**
- **impact on usability and risk register**：缺少真实迁移规模、历史踩坑记录、常见改造模式。风险登记册的历史问题驱动优先级机制未充分生效——RISK-USE-01 和 RISK-REL-01 的概率评估只能依赖推测。降级程度：低中等——不影响第一轮基础验证，但在「测什么最重要」的优先级排序上缺少实证锚点。

---

### 2.5 Final Admitted Intent List

**准入判定：144 条 intent 全部准入，0 条打回。**

理由：
1. 每条 intent 均可反查到风险项或 Parity Matrix 能力项（或 testing-focus.md 明确章节），符合「有锚点」的基本准入条件。
2. 去重检查通过：COMP-012/COMPAT-003（表达式函数 vs 兼容语法）、COMP-015/SEC-015（功能完备 vs 安全验证）等相邻 intent 属不同维度视角，非隐性重复。
3. 交叉维度的 intent（如 SEC-019/COMP-007、COMPAT-009/COMPAT-014/SEC-015~017/USE-016）存在内在联系但各自关注不同验证面，展开为用例时建议合并但意图层保留独立。

**需人工裁决的优先级疑点（6 条）：**

| Intent | 当前优先级 | 疑点 | 建议 |
|---|---|---|---|
| REL-005 (matrix 16 实例展开) | P1 | 优先级线索标为「无直接风险项」 | 风险登记册缺大规模矩阵风险项。建议：人工确认是否需要新增 RISK-REL-02 或降级为 P2 |
| REL-006 (matrix include/exclude) | P1 | 同上 | 同上 |
| REL-008 (max-parallel 限额) | P1 | 同上 | 同上 |
| REL-011 (非法 timeout 值拒绝) | P1 | 同上 | 同上 |
| REL-014 (跨 job workspace 隔离) | P1 | 同上 | 同上 |
| REL-021 (跨 workflow 死锁防护) | P1 | 同上 | 同上 |
| REL-028 (continue-on-error 传播) | P1 | 同上 | 同上 |

**策略建议**：上述 P1 intent 的验证价值不低（均涉及执行模型正确性），但缺少风险登记册锚点。建议人工补充对应的风险项到 `risk-register.md`（如「大规模矩阵展开错误导致 CI 覆盖率盲区 → P1」），而非降级 intent 优先级。

**风险登记册欠完整提醒：**

当前 `risk-register.md` 仅含 5 行模板数据（3 个 P0 blocker + 2 个 P1）。这意味着：
- 34 条 P0 intent 中，只有与 RISK-SEC-01/SEC-02 直接关联的十余条有严格的风险锚点
- 其余 P0（如 COMPAT-001 context 属性对齐、COMPAT-003 表达式语法、COMPAT-009 permissions 命名等）的 P0 级别来自 agent 对「兼容性若错则大量 workflow 不可用」的判断，但缺少风险登记册形式化支撑

**建议**：在进入用例展开阶段前，由人补齐风险登记册——至少覆盖：兼容性核心差异（permissions/context/runner/triggers 四大类）、可靠性关键场景（大规模矩阵 / 重复运行的上下文一致性）、易用性阻断性摩擦（迁移路径完全不可用）。

---

### 2.6 Recommended Execution Order (P0 First, by Dimension)

#### Phase 1: Security P0（14 条，直接关联 blocker 风险）

```
SEC-001 (fork PR token 只读)
SEC-002 (fork PR secret 隔离)
SEC-003 (pull_request_target base 分支执行)
SEC-004 (pull_request_target checkout head.sha)
SEC-005 (secret 基础脱敏)
SEC-006 (secret base64 绕过)
SEC-007 (secret 拼接绕过)
SEC-009 (PR 标题注入)
SEC-010 (PR 正文注入)
SEC-011 (分支名注入)
SEC-012 (commit message 注入)
SEC-014 (GITHUB_ENV 污染)
SEC-015 (permissions 空声明)
SEC-016 (默认 permissions 审计)
```

#### Phase 2: Compatibility P0（9 条，兼容性核心差异）

```
COMPAT-001 (atomgit context 属性对齐)
COMPAT-003 (表达式括号语法)
COMPAT-007 (PR types 命名差异)
COMPAT-008 (pull_request_target 语义对齐)
COMPAT-009 (permissions 域命名)
COMPAT-011 (runner context 属性)
COMPAT-012 (内置 actions/checkout 等价)
COMPAT-014 (默认 shell 差异)
COMPAT-015 (默认 permissions 差异)
COMPAT-019 (schedule cron 语义)
COMPAT-020 (pull_request_target 行为对齐)
```

#### Phase 3: Completeness P0（5 条）

```
COMP-009 (stages 阶段依赖)
COMP-015 (permissions 默认值)
COMP-016 (workflow_call 复用)
COMP-022 (第三方 action 引用)
COMP-023 (matrix fail-fast/include/exclude)
```

#### Phase 4: Reliability P0 + Usability P0（6 条）

```
REL-007 (matrix fail-fast 级联)
REL-015 (kill runner 恢复)
REL-022 (needs 链失败传播)
REL-024 (needs→matrix 父级失败)
USE-014 (端到端迁移)
USE-015 (runs-on 标签映射报错)
USE-016 (permissions 命名差异报错)
```

#### Phase 5+ : All P1 intents（110 条）

按 risk-register 补全后的风险优先级排程。建议的批量顺序：security P1 → compatibility P1 → completeness P1 → reliability P1 → usability P1。

---

## 3. Gate Verdict

**GATE: CONDITIONAL PASS — 待人工裁决**

通过条件：
1. ✅ 两条 blocker 风险项均有 P0 intent 覆盖
2. ✅ Parity Matrix 全部 ❓ 项均有 intent 覆盖
3. ✅ 五个维度均有 P0 intent（安全最充足，可靠性偏轻但核心路径已有）
4. ✅ testing-focus.md 12 个章节全部有覆盖（§4 Runner 环境隔离有缺口但可控）
5. ✅ 安全 6 大攻击面、兼容性 7 类热点全覆盖
6. ✅ 无需要打回的 intent
7. ⚠️ 风险登记册欠完整（仅 5 行模板数据），34 条 P0 中部分缺少风险项锚点

**人工裁决事项：**
1. 是否接受当前 risk-register 的完整度进入用例展开，还是先补齐风险登记册？
2. 上述 7 条「优先级无风险项锚点」的 REL intent（REL-005/006/008/011/014/021/028）——维持 P1 还是降级/新增风险项？
3. 可靠性维度仅 3 条 P0——是否需要将关键稳定性场景（如 timeout-minutes 超时终止 REL-009、re-run 限制 REL-026）提升为 P0？
4. 安全维度的 7 项已知缺口（见安全 agent 自检）——是否需要在补充 security-knowledge/ 输入后重跑安全维度？

---

---
## 4. Human Decision Record（2026-07-20）

| # | 事项 | 裁决 |
|---|---|---|
| 1 | 风险登记册欠完整 | **先展开**，后续补风险登记册 |
| 2 | REL-015 升回 P0 | **同意**，可靠性维度 1 P0 |
| 3 | P0 分配 (20 P0 / 121 P1) | **接受** |
| 4 | 8 个覆盖盲区 | **后续 `/phase01-update` 补** |

### 最终准入清单

| 维度 | P0 | P1 | 合计 |
|---|---|---|---|
| completeness | 1 | 23 | 24 |
| compatibility | 2 | 27 | 29 |
| security | 16 | 20 | 36 |
| reliability | **1** (REL-015) | 28 | 29 |
| usability | 1 | 22 | 23 |
| **合计** | **21** | **120** | **141** (+2 cross-ref) |

**变更汇总**：
- 合并 1: COMPAT-021 → COMP-016
- 交叉引用 1: COMPAT-028 → SEC-005~008
- 标签修正 1: USE-016 + [security]
- P0 回退 1: REL-015 (kill runner 恢复)

*下一步：case-writer 展开准入 intent → 文本用例 + 可执行 YAML*
