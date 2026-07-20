# 测试报告模板

> 由 report-builder 参照此模板生成 `reports/<run-id>/report.md`。
> 结构固定，数据由 `summary.json` 和 `results/*.json` 填充。

---

# GitCode Actions 测试报告

**执行批次**: <run-id>
**Phase 01 用例来源**: <phase01-run-id>
**执行时间**: <start-time> ~ <end-time> (<duration>)
**执行引擎**: GitCode Actions API v8 · Phase 02 Harness

---

## 一、执行摘要

| 指标 | 数值 |
|---|---|
| 总用例数 | <total> |
| ✅ 通过 | <pass> (<pass_rate>%) |
| ❌ 失败 | <fail> (<fail_rate>%) |
| ⚠️ Flaky | <flaky> |
| ⏱️ 超时 | <timeout> |
| 🔧 环境错误 | <env_error> |
| ⏭️ 跳过 | <skipped> |

---

## 二、门禁判定

**结论**: <GO / ⛔ BLOCKED>

**Blocked 维度**: <列出不达标的维度，无则为「无」>

**P0 失败数**: <count> 条（P0 失败即整体 BLOCKED）

---

## 三、分维度通过率

| 维度 | 总数 | 通过 | 失败 | 通过率 | P0 失败 | 门禁阈值 | 判定 |
|---|---|---|---|---|---|---|---|
| completeness | 40 | 38 | 1 | 95.0% | 0 | ≥95% | ✅ |
| compatibility | 30 | 27 | 1 | 90.0% | 0 | ≥90% | ✅ |
| reliability | 20 | 18 | 1 | 90.0% | 0 | ≥85% | ✅ |
| security | 14 | 11 | 3 | 78.5% | 2 | ≥90% | ⛔ |
| usability | 16 | 14 | 2 | 87.5% | 0 | ≥80% | ✅ |

---

## 四、P0 失败（Blocker）

> 以下用例为 P0 优先级且执行结果 FAIL，视作上线 blocker。

| 用例 ID | 标题 | 维度 | 失败断言 | LLM 根因初判 |
|---|---|---|---|---|
| SEC-FORK-01-001 | fork PR 不应读取 secrets | security | negative: run_logs | 产品 bug — secret 脱敏未生效 |
| SEC-INJ-01-003 | PR 标题注入不应被执行 | security | negative: run_logs | 产品 bug — 表达式注入未防护 |

---

## 五、回归 Diff

> 与上次执行（`<prev-run-id>`）对比。

| 类型 | 数量 | 用例 ID |
|---|---|---|
| 🔴 新增失败 | <count> | <ids> |
| 🟢 已修复 | <count> | <ids> |
| ⚪ 新增用例 | <count> | <ids> |

---

## 六、Flaky 标记

> 以下用例在同一批次内多次执行结果不一致，需人工确认是产品不稳定还是用例不可靠。

| 用例 ID | 执行次数 | PASS/FAIL 分布 | 可能原因 |
|---|---|---|---|
| REL-CONCUR-01-004 | 5 | 3 PASS / 2 FAIL | 并发时序依赖不稳定 |
| REL-TIMEOUT-01-001 | 3 | 1 PASS / 2 FAIL | Runner 资源波动 |

---

## 七、失败详情

### <case-id> — <title>

| 项目 | 值 |
|---|---|
| **判定** | FAIL (<flags>) |
| **维度** | <dimension> |
| **优先级** | <priority> |
| **失败断言** | <assertion type/target/expected/actual> |
| **日志指纹** | `sha256:...` |
| **LLM 根因初判** | <分类 (置信度: 高/中/低)> |
| **分析** | <LLM 分析文本> |

---

<!-- 每条失败用例重复上述块 -->

---

## 八、LLM 辅助产出

### 易用性评分

| 用例 ID | 评分维度 | 分数 | 评语 |
|---|---|---|---|
| USE-ERROR-01-001 | 错误信息可理解性 | 3/5 | 报错信息指出了行号但未说明原因和修复建议 |
| USE-MIGRATE-01-002 | 迁移摩擦 | 2/5 | 直接搬 GitHub workflow 报错，错误信息未提示差异点 |

### 衍生用例建议（回流 Phase 01 评审）

| 触发用例 | 建议衍生 | 理由 |
|---|---|---|
| SEC-FORK-01-001 | 验证组织级 secret 在 fork PR 中的隔离 | fork PR 可能同时暴露仓库级和组织级 secret |
| REL-CONCUR-01-004 | 并发度边界值 +1/-1 变体 | 当前 flaky，需确定稳定并发上限 |

---

## 九、执行环境

| 项目 | 值 |
|---|---|
| API Base URL | `https://api.gitcode.com` |
| Runner 标签 | default |
| 并发执行数 | 4 |
| 单用例超时 | 30 min |
| 环境重置级别 | fixture |

---

*报告由 Phase 02 report-builder 生成 · 2026-07-20*
*基线参照: `phase01/baseline/quality-gate.md` · `risk-register.md` · `parity-matrix.md`*
