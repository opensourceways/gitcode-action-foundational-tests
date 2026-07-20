# runs/ — 按运行批次存档

每次 `/phase01-gen` 在此新建一个 `<run-id>/`（命名 `YYYY-MM-DD-NN`，NN 为当日序号）。run 目录**自包含**——含输入快照与全部过程数据，任何时候可回溯当时的判断依据。

## 单个 run 的结构

```
<run-id>/
├── run.md              # 元信息：参数、输入快照、时间线、关键决策、状态(open|gated|delivered)
├── intents/<dim>.md    # 阶段A 各维度原始 intent（spec/compat/security/reliability/usability）
├── intent-library.md   # 汇总意图库（ID / 维度 / 优先级 / 去重关系 / 准入标记）
├── gate-log.md         # 评审门禁过程数据：去重记录、优先级裁决、覆盖盲区、打回清单
├── cases/text/<ID>.md  # 文本用例（归档主体）
├── cases/yaml/<ID>.yaml# 派生可执行用例（过 schema 校验）
├── coverage.md         # 覆盖度报告（对照 Parity Matrix + 风险登记册）
└── dod-checklist.md    # DoD 勾选表
```

## 状态流转

`open`（生成中）→ `gated`（过评审门禁 STOP①）→ `delivered`（过 DoD STOP②，已交付第二部分）

- 增量更新（`/phase01-update`）在 run 内进行，`run.md` 时间线追加记录，旧结论标 `superseded` 不覆盖。
- 已 `delivered` 的 run 不原地改写；需变更时新开 run。
- 查看用 `/phase01-status <run-id>`。

> 本目录初始为空（仅此 README）。第一次 `/phase01-gen` 后会出现首个 run。
