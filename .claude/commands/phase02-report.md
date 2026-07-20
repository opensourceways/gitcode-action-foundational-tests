# /phase02-report — 生成测试报告

## 用途
在所有用例执行完成（或部分完成）后，聚合结果、生成分维度测试报告、对照 Phase 01 quality-gate 做门禁判定、生成回归 diff、标记 flaky。

## 何时使用
- `/phase02-exec` 完成后
- 需要查看某次 run 的报告时
- 需要与上次 run 对比回归时
- 中途想生成阶段性报告时（即使执行未完全完成）

## 前置条件
- `phase02/runs/<run-id>/results/` 下至少有一条执行结果
- Phase 01 三份基线（quality-gate / risk-register / parity-matrix）可用

## 执行步骤

1. **加载数据**（参照 `phase02/scripts/report-builder.md`）：
   - 扫描 `runs/<run-id>/results/*.json`，收集所有执行结果
   - 读取 Phase 01 三份基线
   - 读取上次 run 的 `summary.json`（如存在）

2. **汇总统计**：
   - 总通过/失败/超时/flaky/环境错误/跳过
   - 按 dimension 分组统计通过率
   - 列出 P0 失败

3. **门禁判定**：
   - 对照 `phase01/baseline/quality-gate.md` 的分维度阈值
   - 判断每个维度是否达标
   - P0 失败 → 整体 BLOCKED

4. **回归 diff**：
   - 与上次 run 的 `summary.json` 对比
   - 标出「上次绿、本次红」的回归项
   - 标出「上次红、本次绿」的已修复项

5. **Flaky 标记**：
   - 同一用例多次执行结果不一致 → 标记 FLAKY
   - 给出可能原因提示

6. **失败详情**：
   - 每条 FAIL 用例展示：断言失败详情、日志指纹
   - 如有 LLM 根因初判，附带展示

7. **生成报告**（参照 `phase02/templates/test-report.md`）：
   - 写入 `reports/<run-id>/report.md`
   - 更新 `reports/latest/` 软链
   - 复制 `summary.json` 到 `reports/<run-id>/`

8. **展示摘要**：在终端输出报告关键数据（执行摘要 + 门禁结论 + P0 失败清单）

## 参数
- `<run-id>`：Phase 02 run-id（必需，如 `2026-07-20-01`）
- `--compare <prev-run-id>`：与指定历史 run 对比（可选，默认自动选上次 run）
- `--no-gate`：跳过门禁判定（可选，仅做统计汇总）

## 输出
- `phase02/reports/<run-id>/report.md` — 完整测试报告
- `phase02/reports/<run-id>/summary.json` — 结构化汇总
- `phase02/reports/latest/ → <run-id>/` — 软链
- 终端输出：报告关键数据摘要

## 示例
```
/phase02-report 2026-07-20-01                          # 生成报告（自动对比上次）
/phase02-report 2026-07-20-01 --compare 2026-07-19-01  # 与指定历史 run 对比
/phase02-report 2026-07-20-01 --no-gate                # 仅统计，不做门禁
```
