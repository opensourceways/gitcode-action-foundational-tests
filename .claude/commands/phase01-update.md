---
description: 对既有 run 批次做增量更新（重跑某维度 / 补 intent / 局部再展开）
---

对既有 run 做**增量更新**，不新建批次。严格遵守 `phase01/rules.md` §10（不修改历史、留痕）。

## 参数
`$ARGUMENTS`：`<run-id> <范围>`，范围可为：
- `dim:<维度>` — 重跑某维度 agent，补/更新其 intent（如 `dim:security`）
- `intent:<INTENT-ID>` — 针对某条 intent 补充或修正
- `expand:<INTENT-ID|dim>` — 对已准入 intent 局部再展开为用例
- `gate` — 重跑评审门禁（去重/优先级/盲区）
- `coverage` — 只重算覆盖度报告

## 执行
1. 定位 `phase01/runs/<run-id>/`；若状态=`delivered`，提醒用户：已交付批次不原地改写，确认是否改为新开 run。
2. 按范围用 Task 拉起相应 agent（读 `phase01/agents/<name>/CLAUDE.md`），只更新受影响的文件。
3. **留痕**：在 `run.md` 时间线追加一条（时间 / 范围 / 改了什么 / 为什么）；被取代的旧结论标 `superseded`，不删除。
4. 若更新涉及 intent 准入变化，重跑门禁相关部分并更新 `gate-log.md`、`coverage.md`。
5. 更新受影响的 `dod-checklist.md` 项。

## 纪律
- 增量、可回溯：不覆盖历史结论，只追加+标记 superseded。
- 更新后提示是否需要 `/phase01-compile`（若文本用例变了）或 `/phase01-status`（复核）。
