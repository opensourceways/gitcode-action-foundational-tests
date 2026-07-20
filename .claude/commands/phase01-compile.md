---
description: 由文本用例重新编译可执行 YAML（GitCode 规范变更 / 差异澄清时用）
---

仅**重新编译**某 run 的可执行 YAML——文本用例（source of truth）基本不动。用于 GitCode 规范调整、或那「少量不一致」被澄清后，刷新交接给第二部分的 YAML。

## 参数
`$ARGUMENTS`：`<run-id> [ID或维度]`，可选限定重编译范围；空=该 run 全部文本用例。

## 执行
1. 定位 `phase01/runs/<run-id>/cases/text/`。
2. 用 Task 拉起 **case-writer**（读 `phase01/agents/case-writer/CLAUDE.md`），指令：**只做编译，不改文本用例**——依据当前 `phase01/inputs/gitcode-spec/` 规范，把文本用例重新编译为 `cases/yaml/<ID>.yaml`。
3. 每条 YAML 过 `phase01/schema/executable-case.schema.yaml` 校验。
4. 在 `run.md` 时间线追加：本次重编译的触发原因（规范变更点）、影响的用例 ID、schema 校验结果。
5. 若某文本用例因规范变更已不适用，**不擅自改文本用例**——列出来提示用户，建议走 `/phase01-update` 修订意图/文本。

## 纪律
- 只动 `cases/yaml/`，不动 `cases/text/`（保持文本层稳定）。
- 校验失败的 YAML 必须列出并说明原因，不静默交付。
