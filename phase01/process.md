# 流程定义（process）

本文件定义 team 的运作流程、门禁、run 生命周期与交付验收（DoD）。命令（`.claude/commands/phase01-*.md`）是这套流程的自动化入口。

---

## 0. 角色与编排机制

- 编排者：Claude Code（主会话）读取本文件与各命令，**用 Task 工具逐个拉起 `agents/<name>/CLAUDE.md`**。
- 阶段 A（发散）四个维度 agent **可并行**拉起；门禁、展开、编译**串行**。
- 关键处设 **STOP**：把中间产物摊给用户裁决后再继续，避免在错误方向上消耗展开成本。

```
输入(inputs/) + L0(baseline/)
        │
        ▼
[阶段A 发散] spec-analyst / compat-diff / security / reliability / usability
        │  产出 test intent（只描述「测什么·为什么有风险·预期系统行为」）
        ▼
   intent-library.md（汇总）
        │
        ▼
[评审门禁 收敛] review-gate + orchestrator
        │  去重 · 按风险登记册定优先级 · 对照 Parity Matrix 查覆盖盲区
        │  ——只有通过门禁的 intent 才允许展开——           ← STOP①
        ▼
[阶段B 收敛] case-writer
        │  ① intent → 文本用例（归档主体，评审完整性）
        │  ② 文本用例 + GitCode 规范 → 编译可执行 YAML（可再生）
        ▼
   coverage.md + dod-checklist.md                        ← STOP②
        │
        ▼
   交付第二部分（文本用例 + YAML + 三份基线）
```

---

## 1. 前置：L0 验收基线（命令 `/phase01-baseline`）

在大规模产用例前，先由人牵头、agent 协助产出三份基线，落在 `baseline/`：

| 产物 | 文件 | 作用 |
|---|---|---|
| Feature Parity Matrix | `baseline/parity-matrix.md` | 对标 GitHub Actions 的完备性标尺 |
| 风险登记册 | `baseline/risk-register.md` | 决定测试火力分配、给 intent 定优先级 |
| 质量门禁 | `baseline/quality-gate.md` | 定义分维度阈值与 blocker 判定 |

**建议起手式**：先拉 3~5 个真实开源项目的 workflow 跑通冒烟（样本放 `inputs/workflow-samples/`），同时手写 Parity Matrix 与风险登记册首版——这一步会立刻暴露最扎眼的不一致点。

**门禁**：`baseline/` 三份非空且经人评审后，才允许 `/phase01-gen`。

---

## 2. 一次完整生成（命令 `/phase01-gen`）

### 2.1 新建 run

在 `runs/` 下按 `YYYY-MM-DD-NN`（NN 为当日序号）新建 run 目录，初始化 `run.md`：记录触发参数（覆盖哪些维度）、输入快照（inputs/ 与 baseline/ 的版本/哈希或时间戳）、时间线。

### 2.2 阶段 A — 发散产 intent

并行拉起 5 个 agent（若命令限定维度则只拉相应的），各自把 intent 写入 `runs/<id>/intents/<dim>.md`，然后汇总进 `intent-library.md`。intent 遵循 [`templates/intent.md`](templates/intent.md)。

**产出纪律**：intent 只描述意图层（测什么 / 为什么有风险 / 预期系统行为），**不写执行细节、不写 GitCode 具体语法**。

### 2.3 评审门禁 — 收敛（STOP①）

`review-gate` + `orchestrator` 对意图库执行：
1. **去重**：合并同义 intent，变体显式关联母 intent。
2. **定优先级**：逐条对齐 `risk-register.md`，P0 必须覆盖所有 blocker 风险项。
3. **查覆盖盲区**：对照 `parity-matrix.md` 与风险登记册，列出未被任何 intent 覆盖的能力/风险项。

过程全部写入 `gate-log.md`。**输出「准入意图清单」后 STOP**，请用户确认（可增补专家意图、否决低价值项）再继续。

### 2.4 阶段 B — 基底 diff + 增量生成（加速模式 ★ 2026-07-21）

`case-writer` 采用**基底加速**模式（`rules.md` §9b）：

0. **复制上一轮用例**（2026-07-21 新增）：`cp` 最近一次 `delivered` 状态 run 的 `cases/text/` 和 `cases/yaml/` 到本轮 run 目录。**这确保本轮 run 自包含全部历史用例，Phase 02 只需访问一个目录。**
1. **加载基底**：读 `baseline/case-base-detail.md` + 上一轮 run 的已有用例，合并为完整基底。
2. **意图映射**：将准入 intent 与完整基底做 diff——已覆盖的不重复生成；未覆盖的标记缺口。
3. **增量生成**：仅对缺口 intent 展开文本用例 → `cases/text/<ID>.md` + 编译 YAML → `cases/yaml/<ID>.yaml`。
4. **统一 manifest**：`case-manifest.md` = 历史用例 + 新增用例，一份全集清单。

**加速效果**：首次 run 需评估 631 条生成 `case-base-detail.md`（一次性成本 ~5-10 min）。后续 run 仅做复制 + diff + 少量补充（~1-3 min，新增 10-50 条而非 100+ 条）。

**🚫 禁止事项**：
- 禁止用 `yaml.dump()` 序列化含 `workflow:` 的 YAML（`on:` → `true:` boolean 陷阱）
- 禁止跳过步骤 0（复制上一轮用例）直接从零生成

### 2.5 验收（STOP②）

生成 `coverage.md`（对照 Parity Matrix + 风险登记册的覆盖度）与 `dod-checklist.md`（见 §4）。摊给用户确认后，本批次可交付第二部分。

---

## 3. run 目录生命周期与状态

```
runs/<run-id>/
├── run.md              # 元信息：参数、输入快照、时间线、关键决策、状态(open/gated/delivered)
├── intents/<dim>.md    # 阶段A 各维度原始 intent
├── intent-library.md   # 汇总意图库（含 ID、维度、优先级、去重关系）
├── gate-log.md         # 门禁过程数据：去重记录、优先级裁决、覆盖盲区清单
├── cases/text/<ID>.md  # 文本用例（归档主体）
├── cases/yaml/<ID>.yaml# 派生可执行用例
├── coverage.md         # 覆盖度报告
└── dod-checklist.md    # DoD 勾选表
```

- **复现**：run 目录自包含（含输入快照），任何时候可回看当时的判断依据。
- **增量更新**（`/phase01-update`）：在既有 run 内重跑某维度、补 intent、或局部再展开；每次更新在 `run.md` 时间线追加一条，不覆盖历史结论（旧结论标注 superseded）。
- **重编译**（`/phase01-compile`）：GitCode 规范变更时，只由 `cases/text/` 重新生成 `cases/yaml/`，文本用例基本不动。
- **查看**（`/phase01-status`）：聚合 `run.md` + `intent-library.md` + `gate-log.md` + `coverage.md` + `dod-checklist.md` 输出快照。

---

## 4. 交付验收清单（Definition of Done）

完整性以**文本用例**为准评审；YAML 为派生物。一批用例交付前必须满足：

- [ ] 完整性/覆盖度评审基于文本用例：对照 Parity Matrix 与风险登记册无盲区（`coverage.md` 有据）。
- [ ] 每条文本用例可溯源到某 `intent_ref`，含明确预期结果与验证点。
- [ ] 每条文本用例有对应、且通过 `schema/` 校验的可执行 YAML。
- [ ] 优先级取自风险登记册，P0 覆盖所有 blocker 风险项。
- [ ] 安全用例文本层必含「不应发生」验证点，YAML 层落为 `negative` 断言。
- [ ] 破坏性用例正确声明 `teardown.reset` 级别。
- [ ] 附带交付：Parity Matrix / 风险登记册 / 质量门禁随用例一并交付。

---

## 5. 门禁一览（哪些步骤会 STOP）

| 门禁 | 位置 | 通过条件 |
|---|---|---|
| L0 门禁 | `/phase01-baseline` 之后 | 三份基线非空且人已评审 |
| STOP① 意图准入 | 阶段 A 之后 | 用户确认准入意图清单 |
| STOP② 交付验收 | 阶段 B 之后 | DoD 全绿、覆盖度无盲区 |
