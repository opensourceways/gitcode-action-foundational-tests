# Case Base · 已有用例基底评估

> 对 `phase01/inputs/existing-cases/cases.md` 中 631 条已有用例的**一次性评估结果**。
> 本文件是后续所有 run 的加速器——case-writer 不再每次重新评估 631 条，而是读取本文件直接做 diff。
> 评估日期: 2026-07-21

## 评估维度

每条已有用例按以下矩阵评估：

| 维度 | 评估项 | 取值 |
|---|---|---|
| 状态 | 测试结果 | PASS / FAIL / SKIP / UNKNOWN |
| 可测性 | 真测可达性 | A(可真测) / B(API字段) / C(难真测) / D(测不动) |
| 价值 | 是否有独立验证价值 | HIGH(行为级断言) / MEDIUM(规格覆盖) / LOW(纯文档抄录/参数横扫) |
| 风险 | 是否关联已知风险 | P0 / P1 / P2 / NONE |
| 处置 | 保留/淘汰/待更新 | KEEP / DEPRECATE / NEEDS-UPDATE |

## 淘汰标准（`rules.md` §9b）

满足以下**任一**的淘汰：
1. 真测可达性 = D（测不动）
2. 测试结果 = SKIP 且 skip 原因长期有效
3. 价值 = LOW 且测试结果 = PASS（纯文档抄录型，已确认过，无需保留）
4. 测试结果 = PASS + 价值 = LOW + 有 3+ 条同类型 PASS（参数横扫冗余）

## 处置分类

| 处置 | 含义 | Case-writer 行为 |
|---|---|---|
| `KEEP` | 保留为 Phase 01 用例 | 保持已有 ID，补充 `intent_ref` 和 `dimensions` 标签 |
| `DEPRECATE` | 淘汰 | 记录淘汰原因，不产出 Phase 01 用例 |
| `NEEDS-UPDATE` | 需更新 | 保留但需更新断言/预期（如 FAIL→待修后重验） |

---

*详细评估见 `case-base-detail.md`（按 TC-ID 逐条列出）。
*本文件由 case-writer 在首次全集评估时生成，后续 `/phase01-gen` 直接读取。
