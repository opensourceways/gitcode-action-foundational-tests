# /phase02-schema-check — 输入校验闸门

## 用途
Phase 02 第一道闸门。校验 Phase 01 交付的可执行 YAML 用例是否合规，产出**执行队列**（通过）与**拒收清单**（不合规，回报 Phase 01）。**绝不「尽力执行」残缺用例**。

## 确定性内核
本命令的校验由 `phase02/scripts/schema_check.py` 完成（确定性、可 CI）。命令层只负责选定 run-id 与展示结果。

## 参数
- `<phase01-run-id>`：Phase 01 用例来源（必需，如 `2026-07-21-01`）
- `[<phase02-run-id>]`：本次执行批次 id（可选；不给则用今天日期 + 当日下一序号 `YYYY-MM-DD-NN`）
- `--dims <a,b>` / `--priority <P0|P1|P2>`：只纳入指定维度/优先级（可选）

## 执行步骤
1. **定 run-id**：若用户未给 `<phase02-run-id>`，列 `phase02/runs/` 下今天的目录，取下一个序号，形如 `2026-07-21-NN`。
2. **跑校验**：
   ```
   python phase02/scripts/schema_check.py <phase01-run-id> <phase02-run-id> [--dims ..] [--priority ..]
   ```
   产出 `runs/<phase02-run-id>/`：`queue.json`（待执行）、`rejected.json`（拒收）、`state.json`（status=ready）、`run.md`。
3. **展示**：报通过/拒收条数。若有拒收，摘要列出前几条错误字段，提示回报 Phase 01 修复后重编译。

## 门禁
- 有拒收不阻断后续（拒收项本就不进队列），但需**如实回报**给 Phase 01（`rejected.json`）。
- 校验通过的用例进入 `queue.json`，供 `/phase02-exec` 消费。

## 输出
- `runs/<phase02-run-id>/queue.json` · `rejected.json` · `state.json` · `run.md`

## 示例
```
/phase02-schema-check 2026-07-21-01                      # 全量校验
/phase02-schema-check 2026-07-21-01 --dims security      # 只纳入 security
```
