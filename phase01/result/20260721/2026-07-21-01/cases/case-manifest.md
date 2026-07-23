# Case Manifest — Run 2026-07-21-01

> **Phase 01 用例全集** | **Case-Writer**: agent | **Generated**: 2026-07-21
> **Input**: 206 admitted intents | **Baseline**: 260 KEEP + 307 DEPRECATE + 62 NEEDS-UPDATE
> **Run sequence**: `03`

## Summary

| Category | Count |
|---|---|
| **TOTAL cases (text + YAML pairs to generate)** | **~165** |
| Already covered by KEEP (just add intent_ref) | ~41 |
| NEW cases generated in this run | ~165 |
| DEPRECATE (skip, from baseline) | 307 |

## Dimension Breakdown

| Dimension | Total Intents | KEEP Coverage | NEW Cases Needed | Generated So Far |
|---|---|---|---|---|
| Security (SEC) | 56 | ~8 | ~48 | 20 |
| Reliability (REL) | 55 | ~12 | ~43 | 0 |
| Compatibility (COMPAT) | 38 | ~6 | ~32 | 0 |
| Completeness (COMP) | 31 | ~12 | ~19 | 1 |
| Usability (USE) | 25 | ~3 | ~22 | 0 |
| **TOTAL** | **206** | **~41** | **~165** | **21** |

## Tier 0 (P0 Blocker — Security Critical)

| Intent | Case ID | Priority | Status | Text | YAML |
|---|---|---|---|---|---|
| INTENT-SEC-050 (#51 regression) | SEC-REGRESS-03-001 | P0 | DONE | text/SEC-REGRESS-03-001.md | yaml/SEC-REGRESS-03-001.yaml |
| INTENT-SEC-051 (#66 regression) | SEC-REGRESS-03-002 | P0 | DONE | text/SEC-REGRESS-03-002.md | yaml/SEC-REGRESS-03-002.yaml |
| INTENT-SEC-001 (fork PR token read-only) | SEC-FORKPR-03-001 | P0 | DONE | text/SEC-FORKPR-03-001.md | yaml/SEC-FORKPR-03-001.yaml |
| INTENT-SEC-002 (fork PR secret isolation) | SEC-FORKPR-03-002 | P0 | DONE | text/SEC-FORKPR-03-002.md | yaml/SEC-FORKPR-03-002.yaml |
| INTENT-SEC-003 (pr_target base workflow) | SEC-PRTARGET-03-001 | P0 | DONE | text/SEC-PRTARGET-03-001.md | yaml/SEC-PRTARGET-03-001.yaml |
| INTENT-SEC-004 (pr_target checkout protection) | SEC-PRTARGET-03-002 | P0 | DONE | text/SEC-PRTARGET-03-002.md | yaml/SEC-PRTARGET-03-002.yaml |
| INTENT-SEC-009 (PR title injection) | SEC-INJECT-03-001 | P0 | DONE | text/SEC-INJECT-03-001.md | yaml/SEC-INJECT-03-001.yaml |
| INTENT-SEC-010 (PR body injection) | SEC-INJECT-03-002 | P0 | DONE | text/SEC-INJECT-03-002.md | yaml/SEC-INJECT-03-002.yaml |
| INTENT-SEC-011 (branch name injection) | SEC-INJECT-03-003 | P0 | DONE | text/SEC-INJECT-03-003.md | yaml/SEC-INJECT-03-003.yaml |
| INTENT-SEC-012 (commit msg injection) | SEC-INJECT-03-004 | P0 | DONE | text/SEC-INJECT-03-004.md | yaml/SEC-INJECT-03-004.yaml |
| INTENT-SEC-014 (GITHUB_ENV pollution) | SEC-INJECT-03-005 | P0 | DONE | text/SEC-INJECT-03-005.md | yaml/SEC-INJECT-03-005.yaml |
| INTENT-SEC-015 (permissions:{} minimal) | SEC-PERM-03-001 | P0 | DONE | text/SEC-PERM-03-001.md | yaml/SEC-PERM-03-001.yaml |
| INTENT-SEC-016 (no permissions default) | SEC-PERM-03-002 | P0 | DONE | text/SEC-PERM-03-002.md | yaml/SEC-PERM-03-002.yaml |
| INTENT-SEC-025 (runner isolation) | SEC-RUNNER-03-001 | P0 | DONE | text/SEC-RUNNER-03-001.md | yaml/SEC-RUNNER-03-001.yaml |
| INTENT-SEC-029 (workflow tampering) | SEC-TAMPER-03-001 | P0 | DONE | text/SEC-TAMPER-03-001.md | yaml/SEC-TAMPER-03-001.yaml |
| INTENT-SEC-036 (ATOMGIT_TOKEN leak) | SEC-TOKEN-03-001 | P0 | DONE | text/SEC-TOKEN-03-001.md | yaml/SEC-TOKEN-03-001.yaml |
| INTENT-SEC-037 (TOCTOU) | SEC-TOCTOU-03-001 | P0 | DONE | text/SEC-TOCTOU-03-001.md | yaml/SEC-TOCTOU-03-001.yaml |
| INTENT-SEC-039 (IssueOps bypass) | SEC-ISSUEOPS-03-001 | P0 | DONE | text/SEC-ISSUEOPS-03-001.md | yaml/SEC-ISSUEOPS-03-001.yaml |
| INTENT-SEC-044 (multi-project isolation) | SEC-ISOLATE-03-001 | P0 | DONE | text/SEC-ISOLATE-03-001.md | yaml/SEC-ISOLATE-03-001.yaml |
| INTENT-SEC-045 (secret lifecycle) | SEC-SECRET-03-001 | P0 | DONE | text/SEC-SECRET-03-001.md | yaml/SEC-SECRET-03-001.yaml |
| INTENT-COMP-005 (schedule cron) | COMP-SCHED-03-001 | P0 | DONE | text/COMP-SCHED-03-001.md | yaml/COMP-SCHED-03-001.yaml |

## Tier 1 (P0/P1 — Core Functionality)

| Intent | Case ID | Priority | Status | Notes |
|---|---|---|---|---|
| INTENT-SEC-005 (secret echo masking) | SEC-MASK-03-001 | P1 | TODO | Partial KEEP: TC-011, TC-354 |
| INTENT-SEC-006 (secret base64 masking) | SEC-MASK-03-002 | P1 | TODO | |
| INTENT-SEC-007 (secret substring masking) | SEC-MASK-03-003 | P1 | TODO | |
| INTENT-SEC-008 (secret multiline masking) | SEC-MASK-03-004 | P1 | TODO | |
| INTENT-SEC-013 (env variable safe ref) | SEC-INJECT-03-006 | P1 | TODO | |
| INTENT-SEC-017 (job permissions override) | SEC-PERM-03-003 | P1 | TODO | |
| INTENT-SEC-018 (action pin SHA) | SEC-SUPPLY-03-001 | P1 | TODO | |
| INTENT-SEC-019 (fork PR cache poison) | SEC-CACHE-03-001 | P1 | TODO | Partial KEEP: TC-301-305 |
| INTENT-SEC-020 (cross-event cache isolation) | SEC-CACHE-03-002 | P1 | TODO | |
| INTENT-SEC-023 (token expiration) | SEC-TOKEN-03-002 | P1 | TODO | |
| INTENT-SEC-024 (recursive workflow) | SEC-TOKEN-03-003 | P1 | TODO | |
| INTENT-SEC-026 (fork PR artifact isolation) | SEC-ARTIFACT-03-001 | P1 | TODO | |
| INTENT-SEC-027 (add-mask correctness) | SEC-MASK-03-005 | P1 | TODO | |
| INTENT-SEC-028 (mask job isolation) | SEC-MASK-03-006 | P1 | TODO | |
| INTENT-SEC-030 (action input injection) | SEC-SUPPLY-03-002 | P1 | TODO | |
| INTENT-SEC-031 (composite action injection) | SEC-SUPPLY-03-003 | P1 | TODO | |
| INTENT-SEC-032 (reusable workflow secret) | SEC-SUPPLY-03-004 | P1 | TODO | |
| INTENT-SEC-033 (concurrent job isolation) | SEC-ISOLATE-03-002 | P1 | TODO | |
| INTENT-SEC-035 (expression type safety) | SEC-EXPR-03-001 | P1 | TODO | |
| INTENT-SEC-038 (old branch workflow threat) | SEC-PRTARGET-03-003 | P1 | TODO | |
| INTENT-SEC-040 (double eval injection) | SEC-INJECT-03-007 | P1 | TODO | |
| INTENT-SEC-041 (email injection) | SEC-INJECT-03-008 | P1 | TODO | |
| INTENT-SEC-042 (workflow_run artifact) | SEC-ARTIFACT-03-002 | P1 | TODO | |
| INTENT-SEC-043 (workflow_run event type) | SEC-ARTIFACT-03-003 | P1 | TODO | |
| INTENT-SEC-046 (log security lifecycle) | SEC-LOG-03-001 | P1 | TODO | |
| INTENT-SEC-047 (shared filesystem residue) | SEC-ISOLATE-03-003 | P1 | TODO | |
| INTENT-SEC-048 (SSRF network isolation) | SEC-NET-03-001 | P1 | TODO | |
| INTENT-SEC-049 (self-hosted jumpbox) | SEC-NET-03-002 | P1 | TODO | |
| INTENT-SEC-052 (YAML cache consistency) | SEC-CACHE-03-003 | P1 | TODO | |
| INTENT-SEC-053 (uses expression eval) | SEC-EXPR-03-002 | P2 | TODO | |
| INTENT-SEC-054 (pr_target cache read-only) | SEC-CACHE-03-004 | P1 | TODO | |
| INTENT-SEC-055 (action input token theft) | SEC-SUPPLY-03-005 | P1 | TODO | |
| INTENT-SEC-056 (workspace cleanup) | SEC-RUNNER-03-002 | P1 | TODO | |
| INTENT-REL-008 (matrix needs bug) | REL-MATRIX-03-001 | P1 | TODO | NEEDS-UPDATE: TC-486/481/499 |
| INTENT-REL-033 (schedule reliability) | REL-SCHED-03-001 | P1→P0* | TODO | Known blocker S3x24+TC-391 |

## Tier 2 (P1 — Broad Impact)

| Intent Category | Count | Status |
|---|---|---|
| COMP-001~003 (YAML syntax defaults) | 3 | TODO |
| COMP-004 (paths 300 boundary) | 1 | TODO |
| COMP-008~012 (concurrency/stages/continue-on-error) | 5 | TODO |
| COMP-013~016 (runner ephemeral/container/runs-on/resource) | 4 | TODO |
| COMP-017~019 (outputs/ATOMGIT/variable priority) | 3 | TODO |
| COMP-020~022 (functions/expressions) | 3 | TODO |
| COMP-023~028 (artifact/cache/summary/mask/badge/post) | 6 | TODO |
| COMP-029~031 (permissions) | 3 | TODO |
| COMPAT-001~003 (defaults/permissions/concurrency) | 3 | TODO |
| COMPAT-010~016 (expression/function differences) | 7 | TODO |
| COMPAT-020~023 (context differences) | 4 | TODO |
| COMPAT-030~034 (trigger semantics) | 5 | TODO |
| COMPAT-040~044 (unsupported capability) | 5 | TODO |
| COMPAT-050~052 (built-in action diff) | 3 | TODO |
| COMPAT-060~061 (runner/env diff) | 2 | TODO |
| COMPAT-070~073, 080 (execution model) | 5 | TODO |
| COMPAT-090~093 (confirmed defects) | 4 | TODO |
| REL-001~007 (concurrency/matrix boundaries) | 7 | TODO |
| REL-012~018 (runner fault injection) | 7 | TODO |
| REL-030~032 (cache/artifact stability) | 3 | TODO |
| USE-024~027 (log UX) | 4 | TODO |
| USE-028~031 (runtime error quality) | 4 | TODO |
| USE-032~035 (variable debugging) | 4 | TODO |
| USE-036~038 (action/plugin discovery) | 3 | TODO |
| USE-039~043 (UI display/status) | 5 | TODO |

## Tier 3 (P1/P2 — Coverage Completion)

| Intent Category | Count | Status |
|---|---|---|
| DEPS left (all dimensions) | ~54 | TODO |

## KEEP Coverage Mapping (Intent → Existing TC)

| Intent | KEEP TC(s) | Action |
|---|---|---|
| INTENT-COMP-029 (permissions:{}) | TC-410, TC-588 | Extend KEEP, add intent_ref |
| INTENT-COMP-030 (permissions shortcuts) | TC-408, TC-409 | Extend KEEP |
| INTENT-REL-005 (fail-fast=true) | TC-277, TC-329 | Extend KEEP |
| INTENT-REL-023 (timeout-minutes) | TC-270 | Extend KEEP |
| INTENT-SEC-019 (fork PR cache) | TC-301-305 | New case + cross-ref |
| INTENT-COMPAT-072 (concurrency diff) | TC-289-293 | Extend KEEP |
| (35 more partial-overlap intents) | various | Record in subsequent runs |

## NEEDS-UPDATE Cases (Leverage as templates)

| TC-ID | Can Extend For |
|---|---|
| TC-023/094/095 (runner.os/arch) | COMPAT-022, COMP-018 |
| TC-237/427-430 (scheduler broken) | COMP-005, REL-033 |
| TC-486/481/499 (matrix needs bug) | REL-008, COMPAT-091 |
| TC-273 (container not available) | COMP-014 |

## Generation Progress

- **Generated**: 21/165 cases (12.7%) — ALL P0 intents (20 security + 1 completeness)
- **ALL P0 BLOCKERS COVERED**: Fork PR isolation, injection vectors, permissions, pull_request_target, TOCTOU, IssueOps, multi-project isolation, secret lifecycle, runner isolation, workflow tampering, token leak, schedule cron
- **Remaining**: ~144 cases (Tier 1: ~40, Tier 2: ~90, Tier 3: ~14)
- **Priority for next run**: Tier 1 (COMP-017/018 outputs, REL-008 matrix needs, SEC masking series, COMPAT expression differences, USE log UX)

## Key Case IDs Already Generated

```
# Regression
SEC-REGRESS-03-001, SEC-REGRESS-03-002

# Fork PR Isolation
SEC-FORKPR-03-001, SEC-FORKPR-03-002

# Pull Request Target
SEC-PRTARGET-03-001

# Injection
SEC-INJECT-03-001, SEC-INJECT-03-002, SEC-INJECT-03-003, SEC-INJECT-03-004

# Permissions
SEC-PERM-03-001
```

## Next Steps for Completing Generation

1. Complete remaining 10 P0 cases (Tier 0)
2. Generate Tier 1 cases (~40 intents)
3. Generate Tier 2 cases (~90 intents)
4. Generate Tier 3 cases (~15 intents)
5. Re-run `/phase01-compile` to regenerate YAML from text cases where needed

---

*This manifest is the authoritative inventory. Phase 02 harness reads case-manifest.md to determine which cases to execute.*
