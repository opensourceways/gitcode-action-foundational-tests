# Reports 归档目录

每次 `/phase02-report` 生成的报告写入 `reports/<run-id>/report.md`。

## 目录结构

```
reports/
├── README.md                  # 本文件
├── latest/ → <latest-run-id>/ # 软链到最新报告
└── <run-id>/
    ├── report.md              # 完整测试报告
    └── summary.json           # 结构化汇总（供回归 diff）
```

## 报告生命周期

- **生成**：`/phase02-report` 命令
- **归档**：不删除，作为历史基线保留
- **对比**：每次新报告生成时，自动与 `reports/latest/summary.json` 对比产生回归 diff
- **latest 软链**：每次生成后更新指向最新 run

## 报告命名

`<run-id>` 与 `runs/<run-id>/` 对应。如 `2026-07-20-01`。
