# Summary — 2026-07-24 

All work on automated testing of GitCode workflow triggers and assertions.

---

## 1. Documentation

### Updated
| File | Change |
|------|--------|
| `phase01/schema/VALIDATION-RULES.md` | Added rule 4d: `failure()` vs `failed` naming difference (GitCode uses `failed`, GitHub uses `failure()`) |
| `phase01/inputs/gitcode-api/api-reference.md` | Added 3 API endpoints: `POST /forks`, `POST /pulls`, `POST /comments`; fixed issue path; added fork PR + issue_comment test scenarios |

### Created
| File | Content |
|------|---------|
| `phase02/classify-experiment/2026-07-23/doc-conflict-report.md` | 9 INVALID cases analyzed — 3 doc errors, 3 doc gaps, 2 syntax errors, 1 non-doc issue |
| `phase02/classify-experiment/2026-07-23/not_scriptable-analysis.md` | 32 not-scriptable cases broken down by trigger type, with test strategies |
| `phase02/classify-experiment/demo/README.md` | Demo directory overview, prerequisites, key patterns |
| `phase02/classify-experiment/demo/RESULTS.md` | All demo test results — 6 trigger types tested |

---

## 2. Demo Scripts (8 total)

### Trigger Demos — verifying automation feasibility

| Script | Trigger | Key Finding |
|--------|---------|-------------|
| `demo_pr_trigger.py` | `on: pull_request` same-repo | PR created via API — **not triggered** |
| `demo_fork_pr.py` | `on: pull_request` fork | Full fork→PR pipeline automated — **not triggered** |
| `demo_pull_request_target.py` | `on: pull_request_target` fork | Same API flow — **not triggered** |
| `demo_issue_comment.py` | `on: issue_comment` | Issue + comment APIs work — **not triggered** |
| `demo_schedule.py` | `on: schedule` | Cron pushed, waited 10 min — **not triggered** |
| `demo_push_sanity.py` | `on: push` (control) | **Works** |

### Assertion Demos — verifying assertion engine patterns

| Script | Assertion Kind | Status |
|--------|---------------|--------|
| `demo_artifact_assertion.py` | `artifact_download` | Push→run→log extraction works; upload action name TBD |
| `demo_cache_assertion.py` | `cache_pollution` | Log-based CACHE_HIT/CACHE_MISS scan pattern documented |
| `demo_pr_ui_assertion.py` | `pr_ui` (Playwright) | Pattern documented; blocked on PR trigger |

---

## 3. Core Finding

### Platform Block: API-created events do not trigger workflows

| Trigger | API | Attempts | Result |
|---------|-----|----------|--------|
| `push` | git push | 20+ | ✅ Works |
| `pull_request` | `POST /pulls` | 4 (same-repo + fork) | ❌ No trigger |
| `pull_request_target` | `POST /pulls` (fork) | 1 | ❌ No trigger |
| `issue_comment` | `POST /comments` | 1 | ❌ No trigger |
| `schedule` | cron push + wait | 1 (10 min) | ❌ No trigger |

**Conclusion**: GitCode only fires workflow triggers for git push events. All other event types (`pull_request`, `issue_comment`, `schedule`, `pull_request_target`) do not trigger when the event is created via API (and possibly at all on this platform instance).

### API Reference Verified

| API | Version | Status |
|-----|---------|--------|
| `POST /api/v5/repos/.../forks` | v5 | ✅ Works (rate limit: 1/min) |
| `POST /api/v5/repos/.../pulls` | v5 | ✅ Works (same-repo + cross-repo `head: owner:branch`) |
| `POST /api/v5/repos/.../issues` | v5 | ✅ Works (path: `{owner}/{repo}/issues`) |
| `POST /api/v5/repos/.../issues/:num/comments` | v5 | ✅ Works |
| `PATCH /api/v5/repos/.../pulls/:id` | v5 | ✅ Close PR works |
| `GET /api/v8/.../actions/runs` | v8 | ✅ All runs show `event=Manual` regardless of actual trigger |
| `GET /api/v8/.../runs/:id/jobs/:jid/download_log` | v8 | ✅ Returns zip with per-step log files |
| `GET /api/v8/.../runs/:id/artifacts` | v8 | ⚠️ Not yet confirmed |

---

## 4. Repo State

- `ComputingActionTest/foundational-tests`: **191 workflow files purged → 0**, clean slate for future tests
- PR #5 (`teamfi/foundational-tests → upstream`, `on: pull_request`) still open for manual verification
- Fork `teamfi/foundational-tests` exists for future fork PR tests

---

## 5. Remaining Items

| Priority | Item | File |
|----------|------|------|
| High | Update `not_scriptable-analysis.md` with demo findings | docs |
| Medium | Update `TRIGGER_STATUS` in `workflow_runner.py` with known blockers | code |
| Medium | `artifact_download` assertion kind in `assertion_engine.py` | code |
| Low | `cache_pollution` assertion kind | code |
| Low | Playwright `pr_ui` assertion kind | code |
| Low | Confirm correct artifact action name for platform | investigation |
| Low | Test `workflow_dispatch` trigger via API | investigation |
