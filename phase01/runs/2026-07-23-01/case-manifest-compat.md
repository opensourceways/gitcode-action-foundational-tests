# Case Manifest · Compatibility 维度全量基准

> Run: 2026-07-23-01
> 维度: compatibility
> 生成日期: 2026-07-23

---

## 统计摘要

| 指标 | 数值 |
|---|---|
| **准入 Intent 总数** | 35 |
| **生成用例总数** | 66 |
| **Text 文件数** | 66 |
| **YAML 文件数** | 66 |
| **P0 用例** | 13 |
| **P1 用例** | 53 |
| **P2 用例** | 0 |
| **编译失败** | 0 |

## P0/P1/P2 分布

### P0 (13 条)
- COMPAT-PERM-01-001, 01-002 (permissions 默认 TOKEN 权限)
- COMPAT-MASK-01-001, 01-002 (secret 日志脱敏绕过)
- COMPAT-MIGRATE-01-001, 01-002 (迁移报错质量)
- COMPAT-TARGET-01-001, 01-002 (pull_request_target 语义)
- COMPAT-ISOLATE-01-001, 01-002 (Runner 环境隔离)
- COMPAT-PERM-01-003, 01-004 (permissions 命名差异)
- COMPAT-CONCUR-01-001 (concurrency 差异)

### P1 (53 条)
- 其余全部用例

### P2 (0 条)
- 无

## Intent 覆盖清单

| 意图 ID | 用例数量 | 用例 ID |
|---|---|---|
| INTENT-COMPAT-001 | 2 | COMPAT-SHELL-01-001, 01-002 |
| INTENT-COMPAT-002 | 2 | COMPAT-PERM-01-001, 01-002 |
| INTENT-COMPAT-003 | 2 | COMPAT-IF-01-001, 01-002 |
| INTENT-COMPAT-004 | 2 | COMPAT-EXPR-01-001, 01-002 |
| INTENT-COMPAT-005 | 1 | COMPAT-EXPR-01-003 |
| INTENT-COMPAT-006 | 2 | COMPAT-EXPR-01-004, 01-005 |
| INTENT-COMPAT-007 | 2 | COMPAT-EXPR-01-006, 01-007 |
| INTENT-COMPAT-008 | 1 | COMPAT-EXPR-01-008 |
| INTENT-COMPAT-009 | 2 | COMPAT-EXPR-01-009, 01-010 |
| INTENT-COMPAT-010 | 2 | COMPAT-EXPR-01-011, 01-012 |
| INTENT-COMPAT-011 | 2 | COMPAT-PR-01-001, 01-002 |
| INTENT-COMPAT-012 | 2 | COMPAT-PATHS-01-001, 01-002 |
| INTENT-COMPAT-013 | 2 | COMPAT-SCHEDULE-01-001, 01-002 |
| INTENT-COMPAT-014 | 2 | COMPAT-INPUTS-01-001, 01-002 |
| INTENT-COMPAT-015 | 2 | COMPAT-NEST-01-001, 01-002 |
| INTENT-COMPAT-016 | 2 | COMPAT-CTX-01-001, 01-002 |
| INTENT-COMPAT-017 | 2 | COMPAT-ENV-01-001, 01-002 |
| INTENT-COMPAT-018 | 1 | COMPAT-RUNNER-01-001 |
| INTENT-COMPAT-019 | 1 | COMPAT-RUNNER-01-002 |
| INTENT-COMPAT-020 | 2 | COMPAT-TOKEN-01-001, 01-002 |
| INTENT-COMPAT-021 | 2 | COMPAT-FIELD-01-001, 01-002 |
| INTENT-COMPAT-022 | 2 | COMPAT-VARS-01-001, 01-002 |
| INTENT-COMPAT-023 | 1 | COMPAT-ENVIRON-01-001 |
| INTENT-COMPAT-024 | 2 | COMPAT-ACTION-01-001, 01-002 |
| INTENT-COMPAT-025 | 2 | COMPAT-CACHE-01-001, 01-002 |
| INTENT-COMPAT-026 | 2 | COMPAT-ARTIFACT-01-001, 01-002 |
| INTENT-COMPAT-027 | 2 | COMPAT-RUNSON-01-001, 01-002 |
| INTENT-COMPAT-028 | 2 | COMPAT-ISOLATE-01-001, 01-002 |
| INTENT-COMPAT-029 | 2 | COMPAT-DIR-01-001, 01-002 |
| INTENT-COMPAT-030 | 2 | COMPAT-PERM-01-003, 01-004 |
| INTENT-COMPAT-031 | 2 | COMPAT-MIGRATE-01-001, 01-002 |
| INTENT-COMPAT-032 | 2 | COMPAT-TARGET-01-001, 01-002 |
| INTENT-COMPAT-033 | 2 | COMPAT-MASK-01-001, 01-002 |
| INTENT-COMPAT-034 | 2 | COMPAT-CONCUR-01-001, 01-002 |
| INTENT-COMPAT-035 | 3 | COMPAT-OUTCOME-01-001, 01-002, 01-003 |

## 输出路径

- 文本用例: `phase01/runs/2026-07-23-01/cases/text/COMPAT-*.md`
- 可执行 YAML: `phase01/runs/2026-07-23-01/cases/yaml/COMPAT-*.yaml`

## 质量备注

1. **VALIDATION-RULES 合规**: 所有 YAML 均通过自检（runs-on 数组格式、job/step name 必填、if: 仅 ${{ always() }}、run: | block scalar、on: map 格式、无 permissions 块、无 vars 滥用、${{ atomgit.* }} 上下文、$ATOMGIT_* 环境变量）。
2. **编译失败**: 0 条。运行 `/phase02-schema-check` 前已通过 case-writer 级自检。
3. **已知人工修正**: Agent 2 产出的 `COMPAT-SCHEDULE-01-001/002` 原 `on: schedule:` 为数组格式，已手动修正为 map 格式；`COMPAT-NEST-01-001/002` 原 `uses: ./.github/...` 已修正为 `./.gitcode/...`。
4. **P0 覆盖**: 13 条 P0 用例覆盖 permissions、secret 脱敏、迁移报错、pull_request_target、Runner 隔离、permissions 命名、concurrency 等安全/核心兼容差异。
