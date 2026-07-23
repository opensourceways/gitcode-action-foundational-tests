---
name: validate-yaml
description: Validate GitCode workflow YAML files against the platform API. Use when validating workflow syntax, checking for schema errors, or running schema checks on case-generated YAML.
---

# GitCode Workflow YAML Validator

Validate workflow YAML files using the GitCode platform's `POST /api/v2/projects/{project}/actions/valid` endpoint.

## Prerequisites

- `GITCODE_COOKIE` in project root `.env` (browser cookie, not v8 API token)
- `GITCODE_OWNER` and `GITCODE_REPO` configured

## Usage

### Batch validate a run's cases

```bash
set -a && source <(grep -v '^#' .env | grep '=' | sed 's/ #.*//') && set +a
./phase02/scripts/extract-workflows.sh phase01/runs/<run-id>/cases/yaml/ tmp/
```

### Single file validate

```bash
python phase02/scripts/validate_workflow.py tmp/<case>.yml
```

## Common Fixes

| # | Error | Fix |
|---|-------|-----|
| 1 | `on:` array format `on:\n- push` | Change to map: `on:\n  push:` |
| 2 | Duplicate key `name:` | One `name:` per job/step |
| 3 | Step name contains `[` `]` | Replace with `(` `)` |
| 4 | `${{ }}` in unquoted `run:` | Wrap entire value in double quotes, escape inner `"` as `\"` |
| 5 | `if:` bare keyword `always` | Use `${{ always() }}` |
| 6 | `runs-on` multiline list | Use inline array `[ubuntu-latest, x64, small]` |
| 7 | `permissions` with `contents`/`pull-requests` | Delete the entire `permissions` block |
| 8 | `on.<event>.types` illegal value | See allowed values table |
| 9 | `on.<event>` branches empty or >32 | At least 1, max 32 |

## Allowed `on.<event>.types`

| Event | Allowed |
|-------|---------|
| `pull_request_comment` | `created`, `deleted`, `edited` |
| `merge_requests` | `close`, `merge`, `open`, `reopen`, `update` |

## Full Rules

See `phase01/schema/VALIDATION-RULES.md` for complete platform validation rules.
