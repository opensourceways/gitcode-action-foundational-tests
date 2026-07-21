# Report Builder（report-builder）

## 类型
确定性脚本（Bash + jq / Python）

## 职责
在所有用例执行完成后，聚合结果、生成分维度报告、对照 Phase 01 quality-gate 做门禁判定、生成回归 diff、标记 flaky。

> ★ **本组件负责「内部判定 → 对外结论」的映射**（`phase02/rules.md` §11.3）。报告须区分两个正交的轴：
> - **可测性结论**（每场景一个）：`通过 / 未发现问题 / 不可测试`（对齐 `test-strategy.md` §5）。
> - **问题发现**（叠加层，0..N 个）：确认的平台缺陷，附最小复现 + 实际vs预期 + 证据 + 严重度 + 受影响场景。
>
> 纪律：`不可测试` / `未发现问题` **不计入失败率**；`未发现问题` 绝不可表述为「通过」或「风险已消除」。分维度通过率的分母应剔除 `不可测试`。

## 依赖
- 用例执行结果：`runs/<run-id>/results/*.json`
- Phase 01 基线：`phase01/baseline/quality-gate.md`、`risk-register.md`、`parity-matrix.md`
- 上次 run 的 `summary.json`（用于回归 diff）
- `jq` / Python

## 输入
- `runs/<run-id>/results/` 下所有 `.json` 文件
- `runs/<run-id>/queue.md`（执行队列）
- Phase 01 三份基线

## 处理逻辑

### 1. 汇总统计

```bash
# 扫描所有结果文件，汇总
TOTAL=0; PASS=0; FAIL=0; FLAKY=0; TIMEOUT=0; ENV_ERROR=0

for result_file in runs/<run-id>/results/*.json; do
  TOTAL=$((TOTAL + 1))
  VERDICT=$(jq -r '.verdict' "$result_file")
  case "$VERDICT" in
    PASS)    PASS=$((PASS + 1)) ;;
    FAIL)    FAIL=$((FAIL + 1)) ;;
    FLAKY)   FLAKY=$((FLAKY + 1)) ;;
    TIMEOUT) TIMEOUT=$((TIMEOUT + 1)) ;;
    ENV_ERROR) ENV_ERROR=$((ENV_ERROR + 1)) ;;
  esac
done

PASS_RATE=$(echo "scale=1; $PASS * 100 / $TOTAL" | bc)
```

### 2. 分维度聚合

```python
# 按 dimension 分组统计
dimensions = {}
for result in all_results:
    dim = result["dimension"]
    if dim not in dimensions:
        dimensions[dim] = {"total": 0, "pass": 0, "fail": 0, "p0_fail": 0}
    dimensions[dim]["total"] += 1
    if result["verdict"] == "PASS":
        dimensions[dim]["pass"] += 1
    elif result["verdict"] == "FAIL":
        dimensions[dim]["fail"] += 1
        if result["priority"] == "P0":
            dimensions[dim]["p0_fail"] += 1

# 输出分维度统计表
for dim, stats in dimensions.items():
    rate = stats["pass"] / stats["total"] * 100
    print(f"| {dim} | {stats['total']} | {stats['pass']} | {stats['fail']} | {rate:.1f}% | {stats['p0_fail']} |")
```

### 3. 门禁判定

```python
# 对照 Phase 01 baseline/quality-gate.md 的分维度阈值
# 假设 quality-gate 定义：
#   completeness: >= 95%
#   compatibility: >= 90%
#   reliability:   >= 85%
#   security:      >= 90% (P0 100%)
#   usability:     >= 80%

GATE = load_quality_gate("phase01/baseline/quality-gate.md")
BLOCKED_DIMS = []
for dim, stats in dimensions.items():
    threshold = GATE[dim]["min_pass_rate"]
    if stats["pass"] / stats["total"] < threshold:
        BLOCKED_DIMS.append(dim)

# P0 失败 → 整体 BLOCKED
if any(r["priority"] == "P0" and r["verdict"] == "FAIL" for r in all_results):
    OVERALL = "BLOCKED"

# 生成门禁判定
```

### 4. 回归 diff

```python
# 与上次 run 对比
prev_summary = load_json(f"reports/{prev_run_id}/summary.json")
curr_summary = build_summary(all_results)

regressions = []
for case_id in curr_summary:
    if case_id in prev_summary:
        if prev_summary[case_id]["verdict"] == "PASS" and curr_summary[case_id]["verdict"] == "FAIL":
            regressions.append(case_id)

# 输出回归清单
```

### 5. Flaky 检测

```python
# 对同一用例的多次执行（如有），检查结果一致性
case_runs = group_by_case_id(all_results)
flaky_cases = []
for case_id, runs in case_runs.items():
    verdicts = set(r["verdict"] for r in runs)
    if len(verdicts) > 1:  # 时绿时红
        flaky_cases.append(case_id)
```

### 6. 生成报告

按模板（`phase02/templates/test-report.md`）生成最终报告。

## 输出
- `reports/<run-id>/report.md`：完整测试报告
- `runs/<run-id>/summary.json`：结构化汇总（供下次回归 diff）
- `reports/latest/` → 软链到最新报告

## 报告骨架

```markdown
# GitCode Actions 测试报告 · <run-id>

## 执行摘要
- **执行时间**: 2026-07-20 14:30 ~ 15:45 (1h15m)
- **总用例数**: 120
- **通过**: 102 (85.0%) | **失败**: 8 (6.7%) | **超时**: 3 | **环境错误**: 2 | **Flaky**: 5

## 门禁判定: ⛔ BLOCKED

**Blocked 维度**: security (78.5%, 阈值 90%)
**P0 失败**: 2 条

## 分维度通过率
| 维度 | 总数 | 通过 | 失败 | 通过率 | P0 失败 | 门禁 |
|---|---|---|---|---|---|---|
| completeness | 40 | 38 | 1 | 95.0% | 0 | ✅ |
| compatibility | 30 | 27 | 1 | 90.0% | 0 | ✅ |
| reliability | 20 | 18 | 1 | 90.0% | 0 | ✅ |
| security | 14 | 11 | 3 | 78.5% | 2 | ⛔ |
| usability | 16 | 14 | 2 | 87.5% | 0 | ✅ |

## P0 失败（Blocker）
| 用例 ID | 标题 | 维度 | 断言失败 | LLM 根因初判 |
|---|---|---|---|---|
| SEC-FORK-01-001 | fork PR 不应读取 secrets | security | negative: 日志含 DEPLOY_TOKEN | 产品 bug — secret 脱敏未生效 |
| SEC-INJ-01-003 | PR 标题注入不应被执行 | security | negative: 注入代码被 eval | 产品 bug — 表达式注入未防护 |

## 回归 Diff（与上次 run 对比）
| 新增失败 | 用例 ID |
|---|---|
| +2 | COMP-MATRIX-01-007, REL-CONCUR-01-002 |

## Flaky 标记
| 用例 ID | 执行次数 | PASS/FAIL 分布 | 可能原因 |
|---|---|---|---|
| REL-CONCUR-01-004 | 5 | 3 PASS / 2 FAIL | 并发时序依赖不稳定 |
| REL-TIMEOUT-01-001 | 3 | 1 PASS / 2 FAIL | Runner 资源波动 |

## 失败详情
### SEC-FORK-01-001 — fork PR 不应读取 secrets
- **判定**: FAIL (SECURITY_CRITICAL)
- **失败断言**: negative / run_logs — 日志中发现 DEPLOY_TOKEN 明文
- **日志指纹**: `abc123...`
- **LLM 根因初判**: 产品 bug — secret 脱敏未生效（置信度: 高）
- **详情**: 见 `runs/<run-id>/results/SEC-FORK-01-001.json`

<!-- 每条失败用例都有类似的详情块 -->

## LLM 辅助产出
### 易用性评分
| 用例 ID | 评分维度 | 分数 | 评语 |
|---|---|---|---|
| USE-ERROR-01-001 | 错误信息可理解性 | 3/5 | 报错信息未指出具体哪行，需改进 |

### 衍生用例建议（回流 Phase 01 评审）
- 基于 SEC-FORK-01-001 失败 → 建议补充：验证组织级 secret 在 fork PR 中的隔离
- 基于 REL-CONCUR-01-004 flaky → 建议补充：并发度边界值 +1/-1 的变体

---

*报告由 Phase 02 report-builder 生成 · 执行引擎: GitCode Actions API v8*
*基线参照: phase01/baseline/quality-gate.md · risk-register.md · parity-matrix.md*
```

## 质量要求
- 分维度统计不可含混——每个维度独立计算
- 回归 diff 与上次 run 对齐 case_id
- P0 失败必须显式标注 blocker
- 门禁判定必须对照 Phase 01 quality-gate 的实际阈值
