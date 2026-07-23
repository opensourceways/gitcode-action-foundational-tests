# DoD Checklist · Run 2026-07-23-01

> 按 `phase01/process.md` §4 验收标准逐项自检。

---

| # | 验收项 | 状态 | 证据 |
|---|---|---|---|
| 1 | 所有准入 intent 均生成 ≥1 条用例 | ✅ | 186/186 intent 覆盖，284 条用例 |
| 2 | 每条用例均有对应文本用例 + YAML | ✅ | cases/text/ 284 份 + cases/yaml/ 284 份 |
| 3 | 所有 YAML 通过 schema 解析校验 | ✅ | 284/284 条 Python yaml.safe_load 通过 |
| 4 | 安全用例含 negative 断言 | ✅ | 全部 51 条 security 用例均含 ≥1 negative |
| 5 | 无真实密钥/token/内网地址 | ✅ | 全用占位符（API_KEY / DEPLOY_TOKEN / TEST_SECRET 等） |
| 6 | 用例 ID 含 run 序列且不冲突 | ✅ | 全部 ID 含 `-01-`，与 2026-07-22-01 不冲突 |
| 7 | 文本用例可溯源到 intent_ref | ✅ | 每条 YAML 和文本用例均含 `intent_ref` |

---

**结论：全部 7 项 DoD 达标，本次 run 具备交付条件。**

*DoD Checklist 最后更新: 2026-07-23*
