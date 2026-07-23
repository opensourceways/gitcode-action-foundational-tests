# 2026-07-23-01 Validation Results

**Source**: `phase01/runs/2026-07-23-01/cases/yaml/` (284 cases)
**Validator**: `POST /api/v2/projects/ComputingActionTest%2Ffoundational-tests/actions/valid`

## Summary

| Status | Count | % |
|--------|-------|---|
| VALID | **229** | 80.6% |
| INVALID | **43** | 15.1% |
| ERROR (HTTP 418 WAF) | **6** | 2.1% |
| SKIP (no workflow) | **6** | 2.1% |

## INVALID Error Categories (43 cases)

### Top-level unknown properties (7)
| Error | Cases |
|-------|-------|
| `run-name: unknown property` | 3 |
| `unknown_field: unknown property` | 1 |
| `post.steps: unknown property` | 1 |
| `jobs[test].services: unknown property` | 1 |
| `jobs[test].environment: unknown property` | 1 |

### permissions unknown (6)
| Error | Cases |
|-------|-------|
| `jobs[*].permissions: unknown property` | 4 |
| `permissions.contents: unknown property` | 2 |

> GitCode does not support `permissions` at the workflow or job level, nor `contents`/`pull-requests` scopes.

### environment unknown (2)
| Error | Cases |
|-------|-------|
| `jobs[*].environment: unknown property` | 2 |

> GitCode does not support `environment` blocks.

### on: trigger validation (5)
| Error | Cases |
|-------|-------|
| `on.push: paths/paths-ignore sum limit` | 2 |
| `on.merge_requests.types: [opened] not allowed` | 2 |
| `on: 值不能为空` | 1 |

> `opened` → use `open`; paths-ignore + paths sum 1-32.

### schedule/stages deserialization (5)
| Error | Cases |
|-------|-------|
| `schedule: cannot deserialize Object from Array` | 2 |
| `stages: cannot deserialize Map from Array` | 3 |

> `schedule` expects object `{cron: "..."}`, not array. `stages` expects map, not array.

### runs-on format (3)
| Error | Cases |
|-------|-------|
| `runs-on: 数组形式定义` — invalid label | 3 |

### concurrency validation (4)
| Error | Cases |
|-------|-------|
| `concurrency.preemption.events: [push] not allowed` | 2 |
| `concurrency.max: 值不能小于1` | 1 |
| `concurrency.exceed-action: 值不能为空` | 1 |

> `preemption.events` only allows `[mr_id]`; max >= 1.

### if expression errors (3)
| Error | Cases |
|-------|-------|
| `failure()` not supported | 1 |
| `success()` not supported | 1 |
| `unknownFunc()` not supported | 1 |

### uses / plugin errors (3)
| Error | Cases |
|-------|-------|
| `uses: 格式错误 pluginname@version` | 2 |
| `插件 ./...reusable-level1.yml 不存在` | 2 |
| `插件 checkout-action@v1 不存在` | 1 |

### YAML syntax errors (3)
| Error | Cases |
|-------|-------|
| `scanning a simple key` (injection string) | 2 |
| `parsing a block mapping` (indent error) | 1 |

### Other (1)
| Error | Cases |
|-------|-------|
| `jobs[test].steps: 列表长度 0-16` | 1 |

## WAF 418 Blocked (6 cases — false positive)

These workflows contain content that triggers CloudWAF security scanning:
- `COMPAT-TOKEN-01-001`, `COMPAT-TOKEN-01-002`
- `REL-LOG-01-040`
- `REL-OUTPUT-01-017`
- `SEC-NAME-01-002`
- `USE-MASK-01-001`

## SKIP — No workflow field (6 cases)

- `COMP-DIR-01-002`, `USE-DIR-01-002`, `USE-DOC-01-001`, `USE-PATH-01-001`, `USE-RES-01-001`, `USE-VARS-01-001`

---

*Generated: 2026-07-23 | Tool: `extract-workflows.sh` + `validate_workflow.py`*
