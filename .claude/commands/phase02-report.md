# /phase02-report — 生成分维度报告 + 门禁判定

## 用途
执行完成（或部分完成）后，聚合结果 → **分维度通过率 + §11 对外三态映射 + 门禁判定（GO/BLOCKED）+ 回归 diff**，并汇入 failure-analyst 的失败归因。

## 确定性内核
`phase02/scripts/report_builder.py`（聚合 `results/*.json`，对照阈值判门禁，与上次 run 对比回归）。

## 参数
- `<phase02-run-id>`：批次 id（必需）
- `--compare <prev-run-id>`：与指定历史 run 对比回归（可选）

## 执行步骤
1. **生成报告**：
   ```
   python phase02/scripts/report_builder.py <run-id> [--compare <prev-run-id>]
   ```
   产出 `reports/<run-id>/report.md`：分维度表（通过/问题发现/未发现问题/不可测试 + 通过率 + 门禁）、门禁总判、问题发现清单、不可测试清单、回归 diff。
2. **汇入失败归因**：读 `runs/<run-id>/results/*.analysis.md`（`/phase02-exec` ③ 产出），把每条 FAIL 的根因初判（产品缺陷/用例问题/环境/文档缺口）摘要进报告的「问题发现」段——**区分「确认平台缺陷」与「我方用例问题」**（前者才是对 GitCode 的问题发现）。
3. **展示**：终端输出门禁结论 + 各维度通过率 + P0 失败 + 回归项。

## 判定口径（rules.md §11.3）
- 对外三态：`通过 / 未发现问题 / 不可测试`；确认缺陷走独立**问题发现**层。
- 通过率分母**剔除**「不可测试」「未发现问题」。
- 门禁：任何 P0 FAIL → 整体 BLOCKED；维度通过率低于阈值 → 该维度 BLOCKED。

## 输出
- `reports/<run-id>/report.md` · `reports/<run-id>/summary.json` · `reports/latest.txt`

## 示例
```
/phase02-report 2026-07-21-10                       # 出报告
/phase02-report 2026-07-21-10 --compare 2026-07-21-08   # 带回归对比
```
