# Gate Log — Run 2026-07-21-01

> **Auditor**: review-gate | **Date**: 2026-07-21
> **Input**: 206 intents across 5 dimensions (COMP 31 / COMPAT 38 / SEC 56 / REL 56+1 / USE 25)
> **Baseline**: risk-register.md (5 risks), parity-matrix.md (8 ❓ items), quality-gate.md, case-base-detail.md (260 KEEP / 307 DEPRECATE / 62 NEEDS-UPDATE)
> **Verdict**: PASS (with 3 observations)

---

## 1. Dedup: Cross-Reference Against KEEP List (260 TCs)

### 1.1 Category-Level Dedup Summary

The 206 intents were cross-referenced against the 260 KEEP cases in `case-base-detail.md`. Three tiers of overlap were found:

| Overlap Tier | Count | Action |
|---|---|---|
| **No overlap** — intent covers territory untested by any KEEP case | ~145 | Admit as-is |
| **Partial overlap** — KEEP case covers basic path, intent adds boundary/negative assertion | ~55 | Admit; note KEEP association for case-writer |
| **Significant overlap** — intent largely re-covers what KEEP already validates | ~6 | Flag for case-writer: prefer extending KEEP over generating new |

### 1.2 Specific Overlap Findings

**Tier 3 (Significant overlap — case-writer MUST prefer KEEP extension):**

| Intent | Overlapping KEEP TC(s) | Recommendation |
|---|---|---|
| INTENT-COMP-029 (`permissions: {}` 最小权限) | TC-410 (`permissions:{}`), TC-588 (`permissions空对象`) | Extend TC-410/588 with the negative assertions (403 on write ops) rather than creating a new case. KEEP already validates the `{}` syntax. |
| INTENT-COMP-030 (`permissions` 快捷语法) | TC-408 (`read-all`), TC-409 (`write-all`) | Extend TC-408/409 with explicit per-domain read/write verification. |
| INTENT-REL-005 (fail-fast=true 取消) | TC-277 (`strategy.fail-fast`), TC-329 (`fail-fast:false`) | Extend TC-277 with timing assertions (30s cancellation window). |
| INTENT-REL-023 (timeout-minutes 精确) | TC-270 (`jobs.<id>.timeout-minutes`) | Extend TC-270 with ±30s precision assertion. |
| INTENT-SEC-019 (fork PR cache 投毒) | TC-301-305 (cache 系列) | The KEEP cache cases don't cover fork PR isolation. INTENT-SEC-019 adds a security dimension that TC-301-305 lack. Recommend: new case with `intent_ref: INTENT-SEC-019` + cross-ref TC-301 for cache mechanics. |
| INTENT-COMPAT-072 (concurrency 字段语义差异) | TC-289-293 (concurrency 系列) | KEEP covers basic concurrency fields. EXTEND with GitHub-vs-GitCode semantic mapping verification. |

**Tier 2 (Partial overlap — admit, note KEEP for cross-ref):**

This is the majority category (~55 intents). Key examples:

| Intent | Related KEEP | Why Not a Dup |
|---|---|---|
| INTENT-SEC-001 (fork PR token 只读) | TC-345 (fork 触发事件) | TC-345 verifies event triggering; SEC-001 verifies token permission downgrade — different oracle |
| INTENT-SEC-005 (secret echo 脱敏) | TC-011, TC-354 | TC-011 tests basic masking; SEC-005 adds multi-step consistent masking assertion |
| INTENT-SEC-009-012 (injection vectors) | None | No KEEP case covers script injection from PR title/body/branch/commit — **net new territory** |
| INTENT-COMP-005 (schedule cron) | TC-237, TC-427-430, S3×24 | KEEP cases exist but schedule is known broken; COMP-005 adds end-to-end oracle (API-verifiable event_name) |
| INTENT-COMP-017 (job.outputs 三级链) | TC-486, TC-481, TC-499 (NEEDS-UPDATE, known FAIL) | KEEP tracks the bug; COMP-017 adds the full 1MB + multi-line + matrix regression test |
| INTENT-REL-008 (matrix needs 依赖) | TC-486/481/499 (NEEDS-UPDATE) | Same pattern — known FAIL cases exist; REL-008 is the regression intent |
| INTENT-USE-024 (日志下载) | TC-022, TC-258 | KEEP verifies log display exists; USE-024 verifies download completeness (500+ lines) |
| INTENT-USE-039 (PR Checks 展示) | TC-561 (PR checks 不展示) | TC-561 is NEEDS-UPDATE (known bug); USE-039 adds full positive-path verification |
| INTENT-SEC-037 (TOCTOU) | TC-336 (pull_request_target 语法) | TC-336 covers syntax; SEC-037 covers a timing attack pattern not in KEEP |

### 1.3 Dedup Verdict

**No intent is a pure duplicate of a KEEP case.** The 6 Tier-3 intents have partial overlap but add assertions (negative, boundary, regression) that KEEP cases lack. Recommendation to case-writer: for these 6, prefer mutating the existing KEEP TC rather than creating a new top-level case, to keep the case base compact.

---

## 2. Priority Audit Against Risk Register

### 2.1 Risk Register Coverage

| Risk ID | Priority | Covered By | Coverage Quality |
|---|---|---|---|
| RISK-SEC-01 (fork PR secrets) | P0 blocker | SEC-001, SEC-002, SEC-003, SEC-004, SEC-029, SEC-036, SEC-037, SEC-038, SEC-039, SEC-050, SEC-051 | **Strong** — 11 intents, including 2 regression intents (#51, #66) |
| RISK-SEC-02 (injection) | P0 blocker | SEC-009, SEC-010, SEC-011, SEC-012, SEC-013, SEC-014, SEC-030, SEC-031, SEC-035, SEC-040, SEC-041 | **Strong** — 11 intents covering 7 injection vectors + env mitigation |
| RISK-COMPAT-01 (default differences) | P1 | COMPAT-001, COMPAT-002, COMPAT-003, COMP-001, COMP-002, COMP-007, COMP-020, COMP-031 | **Adequate** — 8 intents across two dimensions |
| RISK-REL-01 (concurrency fairness) | P1 | REL-001, REL-002, REL-003, REL-004, REL-043, REL-044, COMP-008, COMP-009, COMP-010, COMP-013, COMP-016 | **Strong** — 11 intents covering boundary, overload, fairness |
| RISK-USE-01 (migration error messages) | P1 | USE-028, USE-029, USE-030, USE-031, USE-032, USE-033, USE-035, USE-044, USE-045, USE-046 | **Adequate** — 10 intents from runtime error + migration friction angles |

**All 5 risk register entries have coverage. No risk is orphaned.**

### 2.2 P0 Calibration

| Intent | Claimed Priority | Risk Alignment | Verdict |
|---|---|---|---|
| INTENT-COMP-005 (schedule cron) | P0 | Direct — known blocker S3×24+TC-391 | **Valid P0** |
| INTENT-SEC-001, 002, 003, 004 | P0 | Direct — RISK-SEC-01 | **Valid P0** |
| INTENT-SEC-009, 010, 011, 012, 014 | P0 | Direct — RISK-SEC-02 (injection) | **Valid P0** |
| INTENT-SEC-015, 016 | P0 | Direct — RISK-SEC-01 (permission boundary) | **Valid P0** |
| INTENT-SEC-025 | P0 | Aligned — RISK-SEC-01 (runner isolation is security boundary) | **Valid P0** |
| INTENT-SEC-029 | P0 | Direct — RISK-SEC-01 (workflow tampering) | **Valid P0** |
| INTENT-SEC-036 | P0 | Direct — RISK-SEC-01 (token leak) | **Valid P0** |
| INTENT-SEC-037 (TOCTOU) | P0 | Direct — RISK-SEC-01 (pull_request_target is blocked by history #66) | **Valid P0** |
| INTENT-SEC-039 (IssueOps bypass) | P0 | Direct — RISK-SEC-01 (approval bypass) | **Valid P0** |
| INTENT-SEC-044 (multi-project isolation) | P0 | Inferred — RISK-SEC-01 (multi-tenant isolation is a blocker-class risk) | **Valid P0** — but note RISK-SEC-01 text is specific to fork PR secrets; multi-project isolation is a distinct risk dimension. Recommend adding RISK-SEC-03 to risk-register for multi-tenancy. |
| INTENT-SEC-045 (secret lifecycle) | P0 | Inferred — RISK-SEC-01 | **Valid P0** — secret lifecycle failure = secret leak |
| INTENT-SEC-050, 051 (regression #51, #66) | P0 | Direct — RISK-SEC-01 (these ARE the risk) | **Valid P0** |
| INTENT-USE-032 (input type conversion) | P0 | Partial — cited as P0 for data integrity | **QUESTION**: This is a data integrity bug (#75), not a security blocker. Reclassify to P1. RISK-USE-01 is P1, not P0. |
| INTENT-REL-008 (matrix needs bug) | Not explicitly P0 | History #101 (P1) | **Recommend P1** — the risk register doesn't have a P0 for this; history #101 is a reliability defect, not a security blocker |

### 2.3 P0/P1/P2 Tally (Adjusted)

| Priority | Original (agent claim) | Gate-Adjusted | Notes |
|---|---|---|---|
| P0 | ~25 intents (mostly SEC + COMP-005 + USE-032) | ~23 intents | USE-032 downgraded P0→P1; REL-008 confirmed P1 |
| P1 | ~120 intents | ~122 intents | Net +2 from P0 downgrades |
| P2 | ~61 intents | ~61 intents | Unchanged |

---

## 3. Coverage Blind Spots

### 3.1 Against Parity Matrix

The parity-matrix has 8 ❓ items. Cross-check against intent library:

| Parity Matrix Item | Covered By | Status |
|---|---|---|
| `push` + branches 过滤 | COMP-004, COMP-007 | **Covered** |
| `pull_request_target` | SEC-003, SEC-004, SEC-037, SEC-038, COMPAT-031, SEC-051 | **Covered** (heavily) |
| `${{ contains() }}` | COMPAT-014 (case sensitivity) | **Covered** |
| `concurrency` + cancel-in-progress | COMP-008, COMP-009, REL-001-004, COMPAT-072 | **Covered** |
| 默认 `permissions` | COMP-029, COMP-030, COMP-031, SEC-015, SEC-016, SEC-017, COMPAT-002, COMPAT-080 | **Covered** |
| secret 日志 masking | SEC-005, SEC-006, SEC-007, SEC-008, SEC-027, SEC-028, SEC-032, SEC-036 | **Covered** |
| `actions/checkout` 等价 | COMPAT-050, COMPAT-051, REL-054 | **Covered** |
| `runs-on` 标签 | COMP-015, COMPAT-060, REL-028, REL-052 | **Covered** |

**Every ❓ parity-matrix item has at least one intent.** No parity blind spots.

### 3.2 Against Risk Register

All 5 risk entries covered (see §2.1). No risk blind spots.

### 3.3 Against Dimension Completeness (rules.md §1.1)

| Dimension | Intent Count | P0 Intents | P0 Present? |
|---|---|---|---|
| completeness | 31 | 1 (COMP-005) | YES |
| compatibility | 38 | 0 standalone P0 (COMPAT-031 is cross-tagged with security) | YES (via cross-tagging) |
| reliability | 57 | 0 standalone P0 | **OBSERVATION** — no pure-reliability P0; REL-033 (schedule) and REL-008 (matrix needs) could be argued as P0 |
| security | 56 | 20 | YES (strong) |
| usability | 25 | 0 (after USE-032 downgrade to P1) | **OBSERVATION** — no P0 in usability after gate adjustment |

### 3.4 Blind Spots Identified

| # | Blind Spot | Severity | Recommendation |
|---|---|---|---|
| BS-01 | **No P0 reliability intent.** REL-033 (schedule cron) is a known blocker (S3×24+TC-391) that could be elevated to P0 — it blocks ALL cron-triggered workflows. The current P1 assignment understates its impact. | MEDIUM | Elevate REL-033 to P0. Schedule is entirely broken per history evidence. |
| BS-02 | **No P0 usability intent** after USE-032 downgrade. While usability is inherently lower-severity than security, the risk-register has RISK-USE-01 at P1 — the dimension itself has no blocker-class risk. This is **by design**, not a gap. | LOW | Accept as-is. Document that usability has no P0 by design (RISK-USE-01 is P1). |
| BS-03 | **Multi-project isolation risk not in risk-register.** SEC-044 (multi-project runner isolation) and SEC-047 (shared filesystem residue) are P0 intents but the risk register has no dedicated entry for multi-tenancy. RISK-SEC-01 text is about fork PR secrets, not cross-project isolation. | LOW | Recommend adding RISK-SEC-03 (multi-tenant isolation) to risk-register for traceability. |
| BS-04 | **Network isolation partially untestable.** SEC-048 (SSRF防护) and SEC-049 (self-hosted runner 内网跳板) depend on runner infrastructure details that may not be accessible to the test harness. The security agent flagged this as "若 runner 细节不可获取，标记为 blocked/by-infra-opacity." | LOW | Accept. Gate cannot resolve infrastructure opacity. If Phase 02 finds these untestable, mark as `SKIP/by-infra-opacity`. |
| BS-05 | **`schedule` timezone support missing from compat.** COMPAT-034 covers timezone absence, but there's no intent verifying that `timezone` field usage produces a clear error (vs. silent ignore). Current oracle is "差异确认" — verify at case-writer time. | LOW | COMPAT-034 already addresses this. No additional intent needed. |

---

## 4. Admitted Intent List

### 4.1 Summary

| Dimension | Admitted | P0 | P1 | P2 | Reclassified |
|---|---|---|---|---|---|
| completeness (COMP) | 31 | 1 | 22 | 8 | 0 |
| compatibility (COMPAT) | 38 | 0* | 28 | 10 | 0 |
| security (SEC) | 56 | 20** | 24 | 12 | 0 |
| reliability (REL) | 56*** | 0 | 39 | 17 | REL-033 flag: consider P0 |
| usability (USE) | 25 | 0 | 18 | 7 | USE-032: P0→P1 |
| **TOTAL** | **206** | **21** | **131** | **54** | **1 downgrade** |

\* COMPAT-031 is cross-tagged `[compatibility, security]` and is effectively P0 via RISK-SEC-01.
\** Includes 14 NEW intents (SEC-037-049, 050-056) from security-knowledge + history inputs.
\*** REL-056 is a registry/summary sheet, not a testable intent.

### 4.2 Full Admitted Intent Registry

**COMPLETENESS (31 intents, all admitted)**

| ID | Title | Priority | Risk Alignment |
|---|---|---|---|
| INTENT-COMP-001 | 未知字段的报错行为 | P1 | RISK-COMPAT-01 |
| INTENT-COMP-002 | defaults.run.shell 默认值 | P1 | RISK-COMPAT-01 |
| INTENT-COMP-003 | defaults.run 三级优先级级联 | P1 | — (new) |
| INTENT-COMP-004 | paths 过滤 300 文件边界 | P1 | — (new) |
| INTENT-COMP-005 | schedule cron 完整链路 | P0 | Direct — known blocker |
| INTENT-COMP-006 | pull_request_comment 正则语义 | P2 | — (new) |
| INTENT-COMP-007 | 触发去抖 | P2 | RISK-COMPAT-01 |
| INTENT-COMP-008 | concurrency workflow 级完整行为 | P1 | RISK-REL-01 |
| INTENT-COMP-009 | concurrency 两级交互 | P2 | RISK-REL-01 |
| INTENT-COMP-010 | stages.fail_fast 独立性 | P1 | — (new) |
| INTENT-COMP-011 | continue-on-error 对状态函数影响 | P1 | — (new) |
| INTENT-COMP-012 | workflow_call 2 层嵌套限制 | P1 | — (new) |
| INTENT-COMP-013 | Runner ephemeral | P1 | RISK-REL-01 |
| INTENT-COMP-014 | container 完整字段可用性 | P1 | — (TC-273) |
| INTENT-COMP-015 | runs-on 多标签匹配语义 | P1 | — (new) |
| INTENT-COMP-016 | 托管 Runner 资源超限 | P1 | RISK-REL-01 |
| INTENT-COMP-017 | job.outputs 三级传递链 | P1 | — (known FAIL) |
| INTENT-COMP-018 | ATOMGIT_* 系统变量完整注入 | P1 | — (known FAIL) |
| INTENT-COMP-019 | 变量优先级完整链 | P1 | — (new) |
| INTENT-COMP-020 | substring/replace 函数行为 | P1 | RISK-COMPAT-01 |
| INTENT-COMP-021 | hashFiles 多文件组合 | P2 | — (new) |
| INTENT-COMP-022 | 含括号表达式嵌套解析 | P2 | RISK-COMPAT-01 |
| INTENT-COMP-023 | 制品保留期边界 | P2 | — (new) |
| INTENT-COMP-024 | cache 恢复-键降级匹配 | P2 | — (new) |
| INTENT-COMP-025 | STEP_SUMMARY Markdown 渲染 | P2 | — (new) |
| INTENT-COMP-026 | ::add-mask:: 脱敏命令 | P1 | RISK-SEC-02 |
| INTENT-COMP-027 | 状态徽章 URL | P2 | — (new) |
| INTENT-COMP-028 | post 阶段 run_always 默认 | P1 | — (new) |
| INTENT-COMP-029 | permissions: {} 最小权限 | P1 | RISK-SEC-01 |
| INTENT-COMP-030 | permissions 快捷语法 | P1 | RISK-SEC-01 |
| INTENT-COMP-031 | 未声明 permissions 默认权限 | P1 | RISK-SEC-01, RISK-COMPAT-01 |

**COMPATIBILITY (38 intents, all admitted)**

All 38 COMPAT intents (001-093, with numbering gaps for categories) are admitted. Full listing omitted for brevity — see `intents/compat.md` for details. Key callouts:

- COMPAT-001 (default shell): P1, RISK-COMPAT-01 — **no KEEP overlap**
- COMPAT-010-016 (expression/function differences): P1 — **high migration friction, net new**
- COMPAT-020-023 (context object differences): P1 — **atomgit.* vs github.* migration hurdle**
- COMPAT-030-034 (trigger semantics): P1 — **PR types naming, fork isolation, paths threshold**
- COMPAT-040-044 (unsupported capability degradation): P1 — **composite action, docker daemon, workflow_call depth**
- COMPAT-050-052 (built-in action differences): P1 — **checkout pre-merge, cache scope**
- COMPAT-060-061 (runner/environment): P1 — **label format, pre-installed toolchain**
- COMPAT-070-073, 080 (execution/permission model): P1 — **stages, post, concurrency, permissions domains**
- COMPAT-090-093 (confirmed defects): P1 — **uses expression, matrix needs, YAML cache, env injection**

**SECURITY (56 intents, all admitted)**

| Category | IDs | Count | New? |
|---|---|---|---|
| Fork PR isolation | SEC-001, 002, 050 | 3 | SEC-050 NEW (regression #51) |
| pull_request_target | SEC-003, 004, 037, 038, 051, 054 | 6 | SEC-037, 038, 051, 054 NEW |
| IssueOps bypass | SEC-039 | 1 | NEW |
| Secret masking | SEC-005, 006, 007, 008, 045 | 5 | SEC-045 NEW (lifecycle) |
| Script injection | SEC-009, 010, 011, 012, 013, 014, 041 | 7 | SEC-041 NEW (email vector) |
| Double eval / template injection | SEC-040 | 1 | NEW |
| Permissions & token | SEC-015, 016, 017, 023, 024, 034, 036, 055 | 8 | SEC-055 NEW (action input default) |
| Action supply chain | SEC-018, 030, 031 | 3 | — |
| Cache poisoning | SEC-019, 020 | 2 | — |
| Artifact poisoning | SEC-026, 042, 043 | 3 | SEC-042, 043 NEW (workflow_run) |
| Runner isolation | SEC-025, 028, 033, 044, 047, 056 | 6 | SEC-044, 047, 056 NEW |
| Network isolation | SEC-048, 049 | 2 | NEW |
| Workflow command safety | SEC-027, 052 | 2 | SEC-052 NEW (YAML cache) |
| Secret naming | SEC-021, 022 | 2 | — |
| Expression type safety | SEC-035, 053 | 2 | SEC-053 NEW (uses expression) |
| Log security | SEC-046 | 1 | NEW |
| Workflow tampering | SEC-029, 032 | 2 | — |

**RELIABILITY (56 intents, all admitted)**

| Category | IDs | Count |
|---|---|---|
| Concurrency boundaries | REL-001, 002, 003, 004 | 4 |
| Matrix strategy & races | REL-005, 006, 007, 008, 009, 010, 011 | 7 |
| Runner fault injection | REL-012, 013, 014, 015, 016, 017, 018 | 7 |
| Scheduling & dependency faults | REL-019, 020, 021, 022 | 4 |
| Timeout & long-running | REL-023, 024, 025 | 3 |
| Self-hosted runner resources | REL-026, 027, 028, 029 | 4 |
| Cache & artifact stability | REL-030, 031, 032 | 3 |
| Schedule trigger reliability | REL-033, 034 | 2 |
| Race conditions & consistency | REL-035, 036, 037, 038, 039 | 5 |
| Resource boundary values | REL-040, 041, 042 | 3 |
| Large-scale & load | REL-043, 044, 045 | 3 |
| Post cleanup | REL-046, 047 | 2 |
| Env var consistency | REL-048, 049, 050 | 3 |
| Error handling & recovery | REL-051, 052, 053 | 3 |
| Third-party action stability | REL-054, 055 | 2 |
| Registry (summary) | REL-056 | 1 |

**USABILITY (25 intents, all admitted)**

| Category | IDs | Count |
|---|---|---|
| Log viewing experience | USE-024, 025, 026, 027 | 4 |
| Runtime error quality | USE-028, 029, 030, 031 | 4 |
| Variable/param debugging | USE-032*, 033, 034, 035 | 4 |
| Action/plugin discovery | USE-036, 037, 038 | 3 |
| UI display & status | USE-039, 040, 041, 042, 043 | 5 |
| Migration friction supplement | USE-044, 045, 046 | 3 |

\* USE-032: downgraded P0→P1 per §2.2.

### 4.3 Reclassified Intents

| Intent | Original | Adjusted | Reason |
|---|---|---|---|
| INTENT-USE-032 | P0 | P1 | Data integrity bug (#75), not a security blocker. RISK-USE-01 is P1. |

### 4.4 Rejected/Demoted Intents

**None.** All 206 intents are admitted. No intent is a pure duplicate, and all add assertions beyond existing KEEP coverage. See §1.3.

---

## 5. Gate Verdict

### PASS

**Rationale:**

1. **Dedup**: All 206 intents are net-new or additive over KEEP cases. Six have partial overlap; case-writer guidance provided in §1.2.
2. **Priority**: All P0 intents align to risk register (RISK-SEC-01, RISK-SEC-02). One P0→P1 downgrade (USE-032). One recommendation to elevate REL-033 to P0 (BS-01).
3. **Coverage**: All 5 risk register entries and all 8 parity-matrix ❓ items have intent coverage. Five dimensions each have at least one admitted intent. Security dimension has 56 intents (strong).
4. **Testability**: All intents satisfy the minimum testable standard — oracle is specified, negative assertions exist where needed, verification points are concrete.
5. **Blind spots**: 5 identified — 1 actionable (elevate REL-033 to P0), 4 accepted as-by-design or infrastructure-dependent.

### Conditions on PASS

1. **Case-writer must prefer KEEP extension over new-case generation for the 6 Tier-3 overlap intents** (§1.2). Generate new cases only where KEEP structure cannot accommodate the added assertions.
2. **REL-033 (schedule cron) should be elevated to P0** — it is a known blocker that blocks all cron-triggered workflows per history evidence (S3×24+TC-391). The current P1 assignment understates the impact on users who rely on scheduled CI.
3. **USE-032 confirmed P1** — the `inputs` type conversion bug (#75) is a data integrity issue, not a security blocker. RISK-USE-01 is P1.
4. **SEC-048 and SEC-049 may be untestable** in Phase 02 due to runner infrastructure opacity. If so, mark as `SKIP/by-infra-opacity` rather than FAIL — this is a test harness limitation, not a product defect.

---

## 6. Quality Checklist (Self-Audit)

- [x] Each admitted intent meets minimum testable standard and has priority evidence.
- [x] Each risk register blocker (RISK-SEC-01, RISK-SEC-02) is covered by admitted intents — no orphaned risks.
- [x] All five dimensions (completeness, compatibility, reliability, security, usability) have at least one admitted intent. Security dimension has 56 intents (well above the non-empty threshold).
- [x] Dedup and variant relationships documented (§1.2, §1.3), traceable back to KEEP TC IDs.
- [x] Blind spots listed (§3.4), none hidden.
- [x] No rejected intent without an actionable reason (§4.4 — zero rejections this run).
- [x] Gate verdict declared (§5) with conditions.

---

## PART C — Orchestrator Strategic Assessment

> **Orchestrator**: Claude Code (orchestrator agent) | **Date**: 2026-07-21
> **Inputs read**: All 5 intent files, risk-register.md, parity-matrix.md, quality-gate.md, case-base-detail.md, rules.md
> **Key question**: Are the NEW inputs (security-knowledge, history) actually improving intent quality, or just adding volume?

### C.1 Strategic Traceability Assessment

#### C.1.1 Input-to-Intent Traceability

This run's defining characteristic is the **introduction of empirical inputs** that were absent in run 2026-07-20-01:

| New Input | Intents Produced | Quality Signal |
|-----------|-----------------|----------------|
| `security-knowledge/github-actions-security-series.md` (4 Parts) | SEC-037 to SEC-043 (7 intents: TOCTOU, template injection, email injection, workflow_run attacks) | **Very High** — direct from GitHub Security Lab research, concrete attack patterns with named CVEs/CWEs |
| `security-knowledge/issues.md` (5 sections) | SEC-044 to SEC-049 (6 intents: multi-project isolation, secret lifecycle, log security, network isolation, disk residue) | **High** — systematic coverage of operational security blind spots not in any spec |
| `history/issues-encountered.md` (101 entries) | SEC-050 to SEC-053 (4 regression intents) + REL-001 to REL-055 (all 55 intents history-backed, ~80% carry specific bug IDs) + USE-024 to USE-046 (all 23 intents carry specific bug IDs) | **Very High** — every usability intent and most reliability intents cite specific confirmed defects |
| Cross-referencing security series + existing gaps | SEC-054 to SEC-056 (3 intents: cache RO enforcement, action input token theft, workspace cleanup) | **Medium-High** — fills gaps between security series insights and reliability concerns |

**Key finding**: 102 of 206 intents (~50%) now carry explicit empirical evidence (history bug ID or security research citation). This is a step-change from run 2026-07-20-01, where most intents were spec-driven (testing what "should" work) rather than evidence-driven (testing what "does" break).

#### C.1.2 Intent-to-Risk Traceability (溯源链闭合)

Per rules.md §7: `风险项 → INTENT-xxx → 文本用例`. The orchestrator's job is to verify this chain.

| Dimension | Intents | Mapped to Risk Register | Chain Quality |
|-----------|---------|------------------------|---------------|
| Security | 56 | 55 mapped to RISK-SEC-01 or RISK-SEC-02 | **Strong** — clear lineage from intents to risk items. SEC-053 (uses expression, P2) is the only intent with a loose mapping. |
| Reliability | 55 | ~20 explicitly mapped to RISK-REL-01; ~35 implicitly mapped | **Adequate but coarse** — RISK-REL-01 is one item for 55 intents spanning runner faults, cache consistency, schedule reliability, and matrix correctness |
| Compatibility | 38 | ~28 explicitly mapped to RISK-COMPAT-01; ~10 need explicit mapping | **Adequate** |
| Completeness | 31 | ~5 mapped to RISK-COMPAT-01; ~26 are "new boundary discovery" | **Weak** — most completeness intents are novel boundaries without risk register lineage. This is acceptable (spec-analyst discovers boundaries that aren't yet in the risk register) but the risk register should absorb them. |
| Usability | 25 | 10 explicitly mapped to RISK-USE-01; 15 mapped implicitly | **Adequate** — the review-gate correctly noted USE-032 downgrade from P0 to P1, aligning with RISK-USE-01's P1 |

**Orchestrator observation on the risk register**: The current 5-item risk register was adequate for run 2026-07-20-01 (~100 intents) but is **too coarse for 206 intents**. The orchestrator confirms the review-gate's finding that no risk is orphaned, but adds that:
- RISK-REL-01 needs decomposition into scheduler reliability, runner fault tolerance, and cache/artifact consistency sub-items
- RISK-USE-01 needs decomposition into log UX, runtime error quality, and migration first-impression sub-items
- New risk items needed: multi-tenant isolation, secret lifecycle management, data integrity (inputs type coercion)

The orchestrator agrees with the review-gate on the need for risk register expansion, without which the P0/P1 calibration for ~30% of intents is inference-based rather than risk-register-anchored.

### C.2 Input Gap Impact: Before vs After

#### C.2.1 What Was Missing Before (Run 2026-07-20-01 estimated state)

Without `security-knowledge/` and `history/`:
- **Security**: Focused on basic token isolation (fork PR), secret masking, and injection vectors (PR title/body/branch). **Missed**: TOCTOU attacks (entire class), template injection, email injection, multi-project isolation, secret lifecycle, network isolation (SSRF), log security lifecycle.
- **Reliability**: Would have been mostly spec-driven — testing documented concurrency/matrix/timeout behaviors without empirical evidence of what actually fails in production.
- **Usability**: Focused on YAML parsing errors (compile-time validation). **Missed**: runtime error quality, log download/performance/noise/ordering, variable debugging friction, UI feedback problems (PR checks display, step status accuracy, re-run identity).

#### C.2.2 What Is Now Covered (This Run)

With the new inputs:
- **Security** added 20 NEW intents (SEC-037 to SEC-056) across 14 distinct attack surface categories, including 4 historical regression tests for confirmed P0 bugs (#51, #66)
- **Reliability** produced 55 intents, enabling fault injection (7 intents), cache/artifact stability (3 intents), and schedule reliability (2 intents) from history evidence
- **Usability** produced 23 NEW intents covering log UX (4 intents), runtime error quality (4 intents), variable/parameter debugging (4 intents), and UI feedback (5 intents) — all history-backed
- **OWASP CI/CD Top 10** coverage improved from estimated ~7/10 to verified 10/10 (mapped in security file)

#### C.2.3 Quantitative Impact

| Metric | Before (est., run 2026-07-20-01) | After (run 2026-07-21-01) | Delta |
|--------|----------------------------------|---------------------------|-------|
| Total intents | ~100 | 206 | ~+100% |
| Intents with empirical evidence | ~15 (mostly security + some compat) | 102 (~50%) | ~+580% |
| Security P0 blockers | ~15 | 20 | +5 |
| OWASP CI/CD Top 10 coverage | ~7/10 (estimated) | 10/10 | +3 categories |
| History defect regression coverage | 0 | 25+ distinct history bugs with associated intents | New category |
| Usability runtime coverage | 0 (YAML parse only) | 23 (runtime error, log, UI, debugging) | New category |

**Verdict**: The new inputs did not just add volume — they shifted the intent library from spec-driven to evidence-driven for ~50% of intents. The remaining ~50% (completeness, compatibility) are appropriately spec-driven because their purpose is systematic coverage of documented behaviors.

### C.3 Quality Difference: Annotated vs Non-Annotated Intents

The review-gate admitted all 206 intents (no rejections). The orchestrator validates this decision but adds a quality stratification for case-writer execution priority:

#### Evidence-Driven Intents (102 intents with security-knowledge or history annotations)

**Strengths**:
- Verification points tied to specific bug reports (e.g., "复现 history #51 场景——fork PR 是否仍可获取主仓密钥")
- Oracle sources are concrete (either "regression: bug #X should be fixed" or "Security Lab Part N describes attack pattern Y")
- Higher negative assertion density — these intents test what should NOT happen
- P0 blocker density: 16 of 20 security P0s are either NEW (from empirical inputs) or have been enriched with empirical cross-references

**Weaknesses**:
- Some history items (#66) report symptoms that the platform hasn't fully addressed yet — intents may be blocked-by-platform
- History-driven intents test the specific symptom, not necessarily the root cause class

#### Spec-Driven Intents (~104 intents without empirical annotations)

**Strengths**:
- Systematic coverage of documented behaviors (essential for parity matrix completeness)
- Reveal documentation gaps (e.g., COMP-001: "未知字段是报错还是静默忽略？")

**Weaknesses**:
- Lower specificity about what failure looks like (e.g., "verify default shell is bash with -eo pipefail" vs "because migration users reported silent pipeline failures")
- Some are exploratory (COMP-007: trigger dedup — probes for undocumented behavior without spec or history backing)
- Weaker justification for P0/P1 status (rely on risk register inference rather than empirical evidence)

**Comparative verdict**: The quality gap is real but expected. Evidence-driven intents have higher specificity and stronger justification. Spec-driven intents serve a different purpose (coverage completeness). The orchestrator's only concern is that **some spec-driven P1 intents may crowd out evidence-driven P1 intents** when case-writer execution resources are constrained. The execution order recommendation (§C.4) addresses this.

### C.4 Recommended Execution Order

Based on priority × risk concentration × dependency chains:

#### Tier 0 — Immediate (P0 Blocker, Security-Critical)
*Any FAIL here is a gate-blocker for platform release.*

| Order | Intent(s) | Rationale |
|-------|-----------|-----------|
| T0-1 | SEC-050 (regression #51 — fork PR secret isolation) | Confirmed P0 security bug. Tests whether the most fundamental security boundary holds. |
| T0-2 | SEC-051 (regression #66 — pull_request_target fork secret isolation) | Confirmed P0 security gap — "开发中, 715". May be blocked-by-platform; verify status first. |
| T0-3 | SEC-001, SEC-002, SEC-003, SEC-004 | Fork PR isolation core — the foundational trust boundary. |
| T0-4 | SEC-037 (TOCTOU), SEC-039 (IssueOps bypass) | Newly discovered attack classes from Security Lab Part 4. |
| T0-5 | SEC-009, SEC-010, SEC-011, SEC-012 (injection vectors) | Classic CI/CD injection — PR title/body/branch/commit. |
| T0-6 | SEC-044, SEC-045 (multi-project isolation, secret lifecycle) | Multi-tenant security + secret lifecycle — operational security blind spots. |

#### Tier 1 — High Priority (P0/P1, Core Functionality)
*FAIL here represents significant risk but with narrower blast radius than Tier 0.*

| Order | Intent(s) | Rationale |
|-------|-----------|-----------|
| T1-1 | COMP-005, REL-033 (schedule cron — known P0 blocker S3×24+TC-391) | Schedule entirely broken per history. Blocks ALL cron-triggered workflows. |
| T1-2 | REL-008 (matrix needs bug #101) | Blocks a common CI pattern (matrix build → summary/merge step). |
| T1-3 | SEC-025, SEC-047, SEC-056 (runner isolation, disk residue, workspace cleanup) | Runner-level isolation — affects all jobs on shared infrastructure. |
| T1-4 | SEC-048, SEC-049 (network isolation, SSRF) | Network attack surface. May be blocked-by-infra-opacity (review-gate condition 4). |
| T1-5 | COMPAT-031 (pull_request_target fork isolation) | Security-sensitive compat verification. |
| T1-6 | COMP-018 (ATOMGIT_* system variables — multiple known FAILs: run_id, repository_owner, runner.os, runner.arch) | Known failures in system variables affect ALL workflows. |
| T1-7 | COMP-017 (job.outputs 三级传递 — known P1 FAIL TC-486/481/499) | Core data flow between jobs. |
| T1-8 | COMP-013 (runner ephemeral — unknown behavior) | Runner reuse behavior affects reliability and security dimensions. |

#### Tier 2 — Important (P1, Broad Impact)
*Standard execution priority.*

| Order | Intent(s) | Rationale |
|-------|-----------|-----------|
| T2-1 | SEC-038, SEC-040-043, SEC-046, SEC-052-056 (remaining security P1 intents) | Complete security coverage. |
| T2-2 | REL-012-018 (runner fault injection) | Runner failure scenarios. |
| T2-3 | REL-001-007 (concurrency/matrix boundaries) | Core execution model boundaries. |
| T2-4 | REL-030-032, REL-037 (cache/artifact stability + YAML cache stale) | Data consistency. |
| T2-5 | COMPAT-010-023 (expression/function/context differences) | High migration friction area. |
| T2-6 | USE-024-027 (log UX — download, performance, noise, ordering) | User's primary debugging tool. |
| T2-7 | USE-032, COMPAT-016 (inputs type coercion — same underlying bug #75 from two angles) | Coordinate execution — both test the same data integrity issue. |

#### Tier 3 — General (P1/P2, Coverage Completion)
*Lower urgency; execute as resources permit.*

| Order | Intent(s) | Rationale |
|-------|-----------|-----------|
| T3-1 | COMP-001-004, 006-012, 014-016, 019-031 (remaining completeness intents) | Systematic coverage of documented boundaries. |
| T3-2 | COMPAT-001-003, 030-034, 040-044, 050-052, 060-061, 070-073, 080, 090-093 (remaining compat intents) | Compatibility diff completion. |
| T3-3 | USE-028-031, 033-038, 039-046 (runtime error quality, variable debugging, UI feedback, migration friction) | Usability experience improvements. |
| T3-4 | REL-009-011, 019-025, 028-029, 034-036, 038-055 (remaining reliability intents) | Reliability coverage completion. |

#### Dependency Notes for Case-Writer
- **SEC-050** and **SEC-001/SEC-002** test the same boundary (fork PR secret isolation) — SEC-050 is the regression-specific variant. Execute together.
- **SEC-051** and **SEC-003** test the same boundary (pull_request_target workflow source) — SEC-051 is the regression-specific variant. Execute together.
- **USE-032** and **COMPAT-016** are the same underlying bug (#75, inputs type coercion) from usability and compatibility angles — coordinate execution.
- **COMP-005** and **REL-033** are the same known bug (schedule completely broken) from completeness and reliability angles — coordinate execution.
- **REL-037** and **SEC-052** both test YAML cache staleness from reliability and security angles — coordinate execution.

### C.5 For Case-Writer: KEEP TC Coverage vs New Cases Needed

The orchestrator independently estimated coverage against the 260 KEEP cases in `case-base-detail.md`:

| Dimension | Total Intents | Covered by KEEP TCs | Need New Cases | Key KEEP TCs |
|-----------|--------------|---------------------|----------------|-------------|
| Security | 56 | ~8 (14%) | ~48 (86%) | TC-351-356 (permissions), TC-354 (masking), TC-408-416 (permissions syntax), TC-530-532 (secret boundaries) |
| Reliability | 55 | ~12 (22%) | ~43 (78%) | TC-289-290 (concurrency), TC-270 (timeout), TC-276-278 (matrix), TC-314-315 (needs), TC-403-404 (stages fail_fast), TC-520-521 (preemption) |
| Compatibility | 38 | ~6 (16%) | ~32 (84%) | TC-408-416 (permissions diff), TC-289-290 (concurrency diff), TC-023/095 (runner context values) |
| Completeness | 31 | ~12 (39%) | ~19 (61%) | TC-197-222 (ATOMGIT_*), TC-240-246 (commands), TC-289-290 (concurrency), TC-403-404 (stages), TC-331 (outputs) |
| Usability | 25 | ~3 (12%) | ~22 (88%) | TC-347-350 (basic UI: view results, logs, manual trigger, rerun) |
| **Total** | **206** | **~41 (20%)** | **~165 (80%)** | |

**The orchestrator's estimate (~165 new cases) is slightly higher than the review-gate's estimate (~145 net-new) because the orchestrator counts partial-overlap intents as "need new cases" where the KEEP case has C 难真测 or SKIP limitations that prevent it from serving as a base.**

#### Critical Caveats for Case-Writer

1. **Many KEEP TCs are C 难真测 or SKIP**: TC-329 (fail-fast:false — SKIP), TC-330 (max-parallel:3 — SKIP), TC-291/292/293 (preemption — SKIP). These provide **zero executable coverage** for the overlapping reliability intents. Case-writer must generate new cases, not extend these.

2. **NEEDS-UPDATE cases (25 bug categories, 62 individual TCs)**: These can be leveraged as case skeletons:
   - TC-023/094/095 (runner.os/arch wrong values) → extend for COMPAT-022, COMP-018
   - TC-237/427-430 (scheduler broken) → extend for COMP-005, REL-033
   - TC-486/481/499 (matrix needs bug) → extend for REL-008, COMPAT-091
   - TC-273 (container not available) → extend for COMP-014
   - For NEEDS-UPDATE cases, case-writer should generate **update assertions** rather than full new cases — the test structure exists, only the expected result needs updating.

3. **Near-zero existing coverage dimensions**:
   - **Usability runtime experience**: ALL 25 usability intents need new cases — the 3 KEEP TCs (TC-347-350) are basic UI smoke tests that don't cover log performance, error quality, or variable debugging.
   - **Security advanced attack surfaces**: ALL 20 NEW security intents (SEC-037 to SEC-056) need new cases — zero KEEP coverage for TOCTOU, template injection, email injection, network isolation, multi-project isolation, or secret lifecycle.

4. **The 6 Tier-3 overlap intents** (from review-gate §1.2): case-writer should prefer extending the KEEP case over creating a new top-level case. Specifically:
   - INTENT-COMP-029 → extend TC-410/588 (permissions:{} 最小权限)
   - INTENT-COMP-030 → extend TC-408/409 (permissions 快捷语法)
   - INTENT-REL-005 → extend TC-277 (fail-fast=true)
   - INTENT-REL-023 → extend TC-270 (timeout-minutes)
   - INTENT-SEC-019 → new case with cross-ref to TC-301-305 (fork PR cache poison is not covered by KEEP)
   - INTENT-COMPAT-072 → extend TC-289-293 (concurrency 字段语义差异)

### C.6 Orchestrator's Gate Verdict

**Verdict: CONDITIONAL PASS — aligned with review-gate's PASS, with extended conditions.**

The orchestrator confirms the review-gate's finding that all 206 intents are admissible and that the intent library represents a significant quality improvement over run 2026-07-20-01.

#### Confirmations (Agreement with Review-Gate)

1. **Dedup**: No intent is a pure duplicate. The 6 Tier-3 overlaps are additive (add negative/boundary assertions), not redundant. → AGREE.
2. **Coverage**: All 5 risk register items and all 8 parity-matrix ❓ items have intent coverage. → AGREE.
3. **Security P0 calibration**: ALL 20 security P0 intents are valid (traceable to RISK-SEC-01 or RISK-SEC-02). → AGREE.
4. **USE-032 downgrade**: P0→P1 is correct — this is a data integrity bug, not a security blocker. → AGREE.

#### Additional Orchestrator Conditions (Beyond Review-Gate)

5. **[Required] Risk register expansion before next run**: The current 5-item risk register cannot provide proper priority lineage for 206 intents. Before the next `/phase01-gen` run:
   - Decompose RISK-REL-01 into at least 3 sub-items (scheduler reliability, runner fault tolerance, cache/artifact consistency)
   - Decompose RISK-USE-01 into at least 3 sub-items (log UX, runtime error quality, migration first-impression)
   - Add RISK-SEC-03 (multi-tenant isolation) to cover SEC-044, SEC-047
   - Add RISK-DATA-01 (data integrity) to cover USE-032, COMPAT-016

6. **[Recommended] REL-033 P0 elevation**: The review-gate identified REL-033 as "should be P0" (BS-01). The orchestrator endorses this — schedule being completely broken (S3×24+TC-391) means ALL cron-triggered CI is non-functional, which is a blocker-class impact. The risk register should reflect this.

7. **[Recommended] Blocked-by-platform intent marking**: Before case-writer execution, identify and mark intents that depend on platform features not yet shipped:
   - SEC-051 (depends on #66 pull_request_target secret isolation — "开发中, 715")
   - COMP-005 / REL-033 (depend on scheduler fix — known P0 blocker)
   - COMP-014 (depends on container support — TC-273 FAIL)
   - SEC-048 / SEC-049 (may be blocked-by-infra-opacity — review-gate condition 4)
   These should be marked `status: blocked-by-platform` in `intent-library.md` so case-writer generates documentation-level cases (asserting expected behavior) rather than executable cases that will fail before the first step.

8. **[Recommended] Compat intent count resolution**: The compat file declares "28 条 intent" but the review-gate found 38 distinct intent IDs across 10 categories. The orchestrator's independent count confirms 38. Resolve this discrepancy (likely: the "28" comes from treating cross-category duplicates as a single count, while the "38" counts intent IDs). For case-writer purposes, the correct count is **38 compat intents**.

9. **[Recommended] Intent format standardization**: For case-writer automation robustness, standardize on a single intent format across dimensions before the next run. Currently: security uses fenced code blocks, reliability uses inline markdown, compat uses tables, completeness uses structured blocks, usability uses mixed format. Recommend: adopt the `fenced code block` format (security's pattern) as the canonical format.

### C.7 Coverage Blind Spot Summary (Orchestrator Addendum)

Beyond the 5 blind spots identified by the review-gate (§3.4), the orchestrator identifies these additional structural blind spots:

| # | Blind Spot | Severity | Why Missed | Proposed Fix |
|---|-----------|---------|-----------|-------------|
| BS-06 | **No end-to-end migration workflow test** | MEDIUM | Not in any single agent's scope — usability covers friction points, compat covers diff items, but no agent owns "take a real GitHub Actions workflow and migrate it end-to-end" | Orchestrator to add a cross-cutting intent in a future run when `workflow-samples/` input becomes available |
| BS-07 | **No performance/throughput baseline** | MEDIUM | `platform-config/` input directory is empty (only README template), so throughput, queue depth, and resource limits cannot be anchored to real numbers | Gather platform-config data when available; add throughput intents then |
| BS-08 | **No `workflow_run` trigger coverage** | LOW | GitCode may not support `workflow_run` trigger yet; security agent mentions it in SEC-042/043 but neither completeness nor reliability agents independently verify trigger existence | Verify platform support; if supported, add to completeness and reliability dimensions |
| BS-09 | **`vars` context entirely DEPRECATE** | LOW | Platform limitation — `vars` context is unsupported (confirmed by case-base-detail: TC-005-007, TC-019, TC-115-119 all DEPRECATE). This is accepted as a known gap. | Accept as platform limitation. Document in parity-matrix as ❌ 不支持. |
| BS-10 | **No cross-dimension orchestration intents** | LOW | The orchestrator's role is strategic assessment, not intent generation. But some risks span dimensions (e.g., YAML cache staleness is both REL-037 and SEC-052; inputs type coercion is both USE-032 and COMPAT-016). These are individually covered but not tested as systemic interactions. | Accept for this run. In a future run, consider adding orchestration-level intents that test cross-dimensional interaction patterns (e.g., "修改子 workflow YAML → 验证安全修复生效 + 日志显示新版本号"). |

### C.8 Final Decision Log

| Decision | Rationale | Date |
|----------|----------|------|
| CONDITIONAL PASS (aligned with review-gate) | 206 intents are quality-grounded, empirically enriched, and traceable to risks. Conditions must be met before case-writer execution. | 2026-07-21 |
| Risk register expansion required before next run | Current 5-item register cannot support 206-intent priority calibration. See conditions 5-6. | 2026-07-21 |
| ~165 new cases needed (~41 can leverage KEEP) | 80% of intents need new cases; 20% can extend existing KEEP TCs. Usability and security NEW intents have near-zero KEEP coverage. | 2026-07-21 |
| Compat intent count = 38 (not 28) | Independent count confirms 38 unique intent IDs. Discrepancy to be resolved. | 2026-07-21 |
| Execution order: Tier 0 (security regression + core isolation) → Tier 1 (schedule + known FAILs) → Tier 2 (remaining P1) → Tier 3 (P2 completion) | Priority calibrated by risk concentration × dependency chains. | 2026-07-21 |

---

*Orchestrator assessment complete. Next step: human reviewer confirms risk register expansion and P0 reclassification per conditions 5-6. Then case-writer proceeds with the 206 admitted intents, ~165 needing new cases, ~41 extending existing KEEP TCs.*
