# 交付验收清单（Definition of Done）

> Run: 2026-07-22-01
> 验收日期: 2026-07-22
> 依据: `phase01/process.md` §4

---

## DoD 逐项检查

### 1. 完整性/覆盖度评审基于文本用例

- [x] 对照 Parity Matrix 44 项能力项，37 项有覆盖，7 项 ❓ 未知因规格未明记为盲区（见 `coverage.md`）。
- [x] 对照风险登记册 5 条风险项，全部有 intent/用例覆盖。
- [x] `coverage.md` 有据可查，双轴覆盖矩阵已产出。

### 2. 每条文本用例可溯源到某 `intent_ref`，含明确预期结果与验证点

- [x] 新增 62 条文本用例全部含 `溯源意图: INTENT-xxx`。
- [x] 每条文本用例含明确的「预期结果」与「验证点」（正向/负向/非功能）。
- [x] 复用 95 条已有 TC 在 `case-manifest.md` 中标注关联 intent。

### 3. 每条文本用例有对应、且通过 `schema/` 校验的可执行 YAML

- [x] 新增 62 条文本用例均有对应 YAML（`cases/yaml/<ID>.yaml`）。
- [x] 全部 YAML 遵守 `schema/VALIDATION-RULES.md` 编译纪律：
  - `runs-on` 数组格式 ✅
  - job name / step name 必填 ✅
  - step name 无非法字符 ✅
  - `if:` 仅使用 `${{ always() }}`（带括号）✅
  - `run:` 全部使用 `run: |` block scalar ✅
  - `uses:` 裸插件名（非 `actions/checkout@v4`）✅
  - `workflow:` 字段使用 `|` block scalar，未使用 `yaml.dump()` ✅

### 4. 优先级取自风险登记册，P0 覆盖所有 blocker 风险项

- [x] 全部 48 条 P0 优先级均对齐风险登记册（RISK-SEC-01 / RISK-SEC-02）。
- [x] 2 个 blocker 风险项均有 P0 用例覆盖：
  - RISK-SEC-01（fork PR secret 隔离）→ 23 条 P0 intent / 用例
  - RISK-SEC-02（不可信输入注入）→ 12 条 P0 intent / 用例

### 5. 安全用例文本层必含「不应发生」验证点，YAML 层落为 `negative` 断言

- [x] security 维度 36 条 intent 中，35 条 P0 全部含负向验证点。
- [x] 新增 27 条 security YAML 全部含 `type: negative` 断言。
- [x] 典型负向断言覆盖：secret 不泄露、权限不越界、注入不成功、cache 不跨 fork 污染。

### 6. 破坏性用例正确声明 `teardown.reset` 级别

- [x] 全部含破坏性操作（故障注入、Runner 隔离验证等）的用例在文本层声明「清理」级别。
- [x] YAML 层对应 `teardown.reset` 字段取值正确（`fixture` / `full_instance` / `none`）。

### 7. 附带交付：Parity Matrix / 风险登记册 / 质量门禁随用例一并交付

- [x] `baseline/parity-matrix.md` 已交付（44 项能力对标）。
- [x] `baseline/risk-register.md` 已交付（5 条风险项）。
- [x] `baseline/quality-gate.md` 已交付（分维度阈值与 blocker 判定）。

---

## 附加质量检查

| 检查项 | 状态 | 说明 |
|---|---|---|
| 无真实密钥/token/内网地址 | ✅ | 全部用例使用占位符（`DEPLOY_TOKEN` 等） |
| 用例 ID 全局唯一 | ✅ | 格式 `<维度>-<主题>-01-<序号>`，无碰撞 |
| 变体用例关联母 intent/用例 | ✅ | `-Vn` 变体在 manifest 中标注母 intent |
| 主观判据标注 `llm_assisted` | ✅ | usability 调试体验类用例已标注 |
| 输入退化标注 | ✅ | workflow-samples/ 与 business-context/ 退化已在产物中标注 |

---

## 验收结论

| 检查项 | 状态 |
|---|---|
| DoD 1 — 覆盖度评审 | ✅ 通过 |
| DoD 2 — 溯源链完整 | ✅ 通过 |
| DoD 3 — YAML 合规 | ✅ 通过 |
| DoD 4 — P0 覆盖 blocker | ✅ 通过 |
| DoD 5 — 安全负向断言 | ✅ 通过 |
| DoD 6 — 破坏性声明 | ✅ 通过 |
| DoD 7 — 基线交付 | ✅ 通过 |

**DoD 全绿 ✅**

---

## 交付物清单

| 产物 | 路径 | 说明 |
|---|---|---|
| 文本用例（新增） | `runs/2026-07-22-01/cases/text/*.md` | 62 个文件 |
| 可执行 YAML（新增） | `runs/2026-07-22-01/cases/yaml/*.yaml` | 62 个文件 |
| 用例全集清单 | `runs/2026-07-22-01/case-manifest.md` | 复用 95 + 新增 62 |
| 覆盖度报告 | `runs/2026-07-22-01/coverage.md` | 双轴覆盖 + 盲区 |
| DoD 验收清单 | `runs/2026-07-22-01/dod-checklist.md` | 本文件 |
| 意图库 | `runs/2026-07-22-01/intent-library.md` | 186 条准入 intent |
| 门禁日志 | `runs/2026-07-22-01/gate-log.md` | 去重/优先级/盲区 |
| 维度原始 intent | `runs/2026-07-22-01/intents/*.md` | 5 个文件 |
| 三份基线 | `baseline/*.md` | Parity Matrix + 风险登记册 + 质量门禁 |

> 本批次可交付第二部分（Phase 02）。
