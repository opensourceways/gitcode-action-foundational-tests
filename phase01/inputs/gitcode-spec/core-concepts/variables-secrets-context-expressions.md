<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/core-concepts/variables-secrets-context-expressions | fetched: 2026-07-20 -->
<!-- 注意：本页 WebFetch 返回为英文（模型转译），内容忠实但语言待统一为中文，勘误时可重抓。 -->

# Variables, Secrets, Context and Expressions

AtomGit Action provides a four-level variable system using `env`, `vars`, `secrets`, and `inputs`, enabling flexible workflow configuration through context (primarily `atomgit`) and expressions (`${{ expression }}`).

## Four-Level Variable System

| Type | Suitable For | Sensitive | Reference Method |
|------|-------------|-----------|-------------------|
| `env` | Temporary variables within workflow | No | `$VAR_NAME` or `${{ env.VAR }}` |
| `vars` | Repository/organization-level regular variables | No | `${{ vars.VAR }}` |
| `secrets` | Passwords, tokens, private keys | Yes | `${{ secrets.NAME }}` |
| `inputs` | Workflow input parameters | No | `${{ inputs.NAME }}` |

## Variable Priority

```
Step env  >  Job env  >  Workflow env
```

## Context

AtomGit Action supports 12 contexts, with the core context being **`atomgit`**:

| Context | Description | Typical Properties |
|---------|-------------|-------------------|
| `atomgit` | Core workflow run information | `atomgit.sha`, `atomgit.ref`, `atomgit.event_name` |
| `env` | Environment variables | `env.VAR_NAME` |
| `vars` | Configuration variables | `vars.VAR_NAME` |
| `secrets` | Secrets | `secrets.NAME` |
| `job` | Current job information | `job.status` |
| `steps` | Step information and outputs | `steps.id.outputs.result` |
| `runner` | Runner information | `runner.os`, `runner.arch` |
| `inputs` | Input parameters | `inputs.NAME` |
| `matrix` | Matrix parameters | `matrix.os` |
| `strategy` | Matrix strategy information | `strategy.fail-fast` |

## Expressions

Expressions embed into YAML values using `${{ expression }}` syntax:

**Operators**: `==`, `!=`, `!`, `&&`, `||`

**Status Functions**:

| Function | Description |
|----------|-------------|
| `success` | Previous steps succeeded |
| `always` | Execute regardless of success or failure |
| `cancelled` | Workflow was cancelled |
| `failed` | Previous steps failed |

**String Functions**: `contains`, `startsWith`, `endsWith`, `format`, `substring`, `replace`

**Special Functions**: `hashFiles`, `toJson`
