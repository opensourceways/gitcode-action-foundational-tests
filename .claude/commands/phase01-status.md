---
description: 查看某个 run 批次的进度与过程数据（intent/覆盖度/门禁/DoD）
---

汇总展示 GitCode Action 用例设计某批次的过程数据。

## 参数
`$ARGUMENTS`：run-id（如 `2026-07-20-01`）；空=列出所有 run 并展示最新一个。

## 执行
1. 若无参数：列出 `phase01/runs/` 下所有 run 目录及其状态（open/gated/delivered），选最新的展开。
2. 读取该 run 的：`run.md`、`intent-library.md`、`gate-log.md`、`coverage.md`、`dod-checklist.md`。
3. 输出一份**只读快照**（不修改任何文件）：

```
Run: <run-id>   状态: <open|gated|delivered>
参数/输入快照: <维度范围 / inputs·baseline 版本>
时间线: <关键节点>

意图: 总 N 条 | 各维度分布 | 准入 M 条 / 打回 K 条
覆盖度: Parity 覆盖 x/y | 风险 blocker 覆盖 a/b | 盲区 <清单>
用例: 文本 P 条 / YAML Q 条 | schema 校验 <通过/失败清单>
DoD: <逐项 ✅/❌>
下一步建议: <补 intent / 修 schema / 可交付 ...>
```

4. 若发现缺口（盲区、DoD 未过、schema 失败），明确指出并建议用哪个命令修（`/phase01-update` 或 `/phase01-compile`）。

## 纪律
纯只读，不改任何 run 文件。
