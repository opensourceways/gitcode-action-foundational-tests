# 输入清单总表（INPUTS）

> 需求 3：各 agent 基于这些输入做设计。**跑流程前请你把对应资料放进各子目录**；本清单说明每类要放什么、格式、谁消费、是否必需。
> 缺输入不会让流程崩，但相关维度会退化：agent 会在产物里显式标注「缺哪份输入 → 哪些 intent 无法产出」。

## 快速自检（跑 `/phase01-gen` 前）

| 子目录 | 必需度 | 放了吗 |
|---|---|---|
| `gitcode-spec/` | **必需**（无则规格分析/编译 YAML 无依据） | ✅ 已补充（官方文档 50 页离线镜像，2026-07-20） |
| `github-reference/` | **必需**（无则兼容性 diff 失去 oracle） | ✅ 已补充（GitHub Actions 核心规格 12 页，2026-07-20） |
| `workflow-samples/` | 强烈建议（真实负载最能暴露差异） | ☐ |
| `security-knowledge/` | 建议（安全维度深度依赖它） | ☐ |
| `platform-config/` | 建议（配额/容量/规格 → 稳定性边界用例） | ☐ |
| `business-context/` | 建议（部署方式/迁移场景/历史问题 → 贴合实际） | ☐ |
| `existing-cases/` | 建议（已有用例列表 → 去重/查漏/继承覆盖） | ✅ 已补充（631 条用例，已预转为 cases.md） |
| `history/` | 可选（有则火力分配更准） | ☐ |

---

## 各类输入明细

### 1. `gitcode-spec/` — GitCode Action 产品规格
- **放什么**：GitCode Action 官方规格文档、YAML 语法说明、支持的触发器/表达式/内置 action 清单、权限模型、配额与容量说明、runner 架构说明、错误码表、产品文档。
- **格式**：Markdown / PDF / HTML 均可；能贴链接的也放一份 `links.md`。
- **消费方**：spec-analyst（能力清单）、case-writer（编译 YAML 的语法依据）、security（权限/隔离）、reliability（配额/runner）、usability（错误码/文档）。
- **缺失影响**：能力清单无法建立、YAML 无法编译——**这是最关键的一份**。

### 2. `github-reference/` — GitHub Actions 对标基准
- **放什么**：GitHub Actions 官方语法/语义文档（workflow syntax、contexts、expressions、events that trigger workflows）、安全加固指南（Security hardening for GitHub Actions）、内置 action（checkout/cache 等）行为说明。
- **格式**：Markdown / PDF / 链接清单。可整站抓取关键页存为 md。
- **消费方**：compat-diff（差分测试的 oracle 基准）、security（加固实践对标）。
- **缺失影响**：兼容性 diff 失去权威 oracle，只能靠常识，质量大降。

### 3. `workflow-samples/` — 真实开源 workflow 样本
- **放什么**：3~5+ 个真实开源项目的 `.github/workflows/*.yml`（覆盖多样场景：构建、测试、发布、matrix、复用、缓存、部署）。建议按项目分子目录，附一份 `SOURCES.md` 记录来源与选取理由。
- **格式**：原始 `.yml` 文件。
- **消费方**：compat-diff（真实负载找差异）、usability（迁移摩擦素材）、L0 冒烟。
- **缺失影响**：差异发现偏理论、迁移摩擦无从实测。

### 4. `platform-config/` — 平台规格与容量参数
- **放什么**：最大并发数、job 超时、matrix 上限、artifact/cache 上限、日志上限、secret 数量限制、Runner 规格与架构。
- **格式**：Markdown / YAML。数字平铺，不要套 PDF/截图——agent 需要读具体数值。
- **消费方**：reliability（边界值源头）· spec-analyst（验证规格真实性）· compat-diff（对照 GitHub limits）。
- **刷新影响**：配额变了 → `/phase01-update dim:reliability` 重审边界用例。

### 5. `security-knowledge/` — 安全知识库
- **放什么**：CI/CD 安全加固手册、公开漏洞/CVE 模式分析、OWASP CI/CD Top 10 摘要、Actions 已知攻击模式（脚本注入、`pull_request_target` 滥用、cache 投毒、供应链）汇总。
- **格式**：Markdown / PDF / 链接。**只放防御知识与模式分析，不放真实 exploit。**
- **消费方**：security agent。
- **缺失影响**：安全维度退化为通用清单，缺针对性。

### 6. `business-context/` — 业务场景与历史问题
- **放什么**：Runner 部署方式、典型业务 workflow 模板、迁移重点与已知改造点、历史踩坑记录/已知问题列表。
- **格式**：Markdown（见子目录 README 的字段模板）。
- **消费方**：usability（迁移摩擦）· compat-diff（改造点补差异盲区）· security（部署模型影响攻击面）· orchestrator（历史问题→风险登记册优先级）。
- **刷新影响**：业务场景变了 → `/phase01-update dim:usability` 或 `dim:compat` 重审。

### 7. `history/` — 历史经验（原始缺陷数据）
- **放什么**：既有缺陷库、以往验证/迁移踩坑记录、已知问题列表、用户反馈/工单中的高频问题。
- **格式**：Markdown / CSV / 导出表。可脱敏。
- **消费方**：全体 agent（尤其 orchestrator 定火力）、风险登记册。
- **缺失影响**：风险优先级少了实证依据，靠推断。

### 8. `existing-cases/` — 第一版用例参考
- **放什么**：已有的第一版测试用例列表（Excel `.xlsx`），含用例 ID / 标题 / 维度 / 优先级 / 前置条件 / 操作步骤 / 预期结果 / 状态 / 备注等列。
- **格式**：Excel。列名不强求精确匹配——agent 会自适应解析。
- **消费方**：case-writer（先扫已有用例，避免重复展开）· orchestrator（比对已有覆盖 vs 新 intent）· review-gate（去重时纳入已有用例）。
- **处理逻辑**：已有用例覆盖了新 intent → 标注关联不重复展开；已有用例有覆盖但风险登记册无 intent → 提示盲区。
- **缺失影响**：新产用例可能与已有用例重复，但不会阻塞流程。

---

## 放置约定

- 每个子目录先有 `README.md`（已预置）说明期望内容；你放好资料后可删可留。
- 大文件（PDF）直接放；网页优先抓成 Markdown 便于 agent 检索。
- 敏感信息（真实 token/内网地址/客户名）**入库前脱敏**——见 `phase01/rules.md` §6。
- 放好后建议在对应子目录留一行「已补充 / 版本 / 日期」，便于 run 记录输入快照。
