# GitCode Actions 测试验证工程

> 对 GitCode 即将推出的类 GitHub Actions 功能，在上线前系统性识别风险、产出可执行用例、自动化执行并交付可信的分维度测试报告。

---

## 两阶段设计

本工程采用**两阶段解耦**架构：第一阶段负责「该测什么、用例怎么写」，第二阶段负责「怎么跑、怎么判、怎么报」。两阶段之间以《测试用例契约》（声明式 YAML schema）为唯一交接面。

```
┌─────────────────────────────────────────────────┐
│  Phase 01 · 用例设计 Agent Team                  │
│  形态：agent team 为主，人工基线锚定              │
│  产出：文本用例（source of truth）                │
│       + 派生可执行 YAML                           │
│       + L0 基线（Parity Matrix / 风险登记册 / 质量门禁）│
│  回答：「该测什么」「用例长什么样」                │
└──────────────────┬──────────────────────────────┘
                   │  交接契约：可执行 YAML
                   │  phase01/schema/executable-case.schema.yaml
                   ▼
┌─────────────────────────────────────────────────┐
│  Phase 02 · 执行与报告 Harness                   │
│  形态：确定性脚本为主，LLM 辅助                   │
│  产出：分维度测试报告 + 回归 diff + flaky 标记    │
│  回答：「跑得对不对」「能不能上线」                │
└─────────────────────────────────────────────────┘
```

| | Phase 01 | Phase 02 |
|---|---|---|
| **重点** | Agent Team 协作 | 确定性自动化脚本 |
| **核心问题** | 测什么、用例怎么写 | 怎么跑、怎么判、怎么报 |
| **关键产出** | 文本用例 + 可执行 YAML | 测试报告 + 门禁结论 |
| **LLM 角色** | 主引擎（发散/收敛/展开） | 辅助（编译/失败分析） |
| **手册** | [`phase01.md`](phase01.md) | [`phase02.md`](phase02.md) |
| **工作区** | [`phase01/`](phase01/) | [`phase02/`](phase02/) |

---

## Phase 01：用例设计 Agent Team

### 核心原则

1. **文本用例是 source of truth，YAML 是派生物。** 评审看文本、执行用 YAML；规范变更时重新编译 YAML，文本用例基本不动。
2. **意图先行。** Agent 不直接产用例，先产 test intent（测试意图/风险点），过评审门禁才展开——这是控制用例质量与数量的闸门。
3. **没有 L0 基线，不产用例。** Feature Parity Matrix + 风险登记册 + 质量门禁是优先级与覆盖度的客观标尺。
4. **四个责任维度**：完备性 · 兼容性 · 稳定性 · 安全性 · 易用性。Team 按维度组织，不按功能模块。
5. **可复现、可回溯。** 每批次自成一个 run 目录，过程数据全部落盘。

### 入口

```bash
/phase01-baseline    # ① 打地基：产出 L0 三份基线（Parity Matrix / 风险登记册 / 质量门禁）
/phase01-gen         # ② 生成用例：intent 发散 → 门禁评审 → 展开文本用例 → 编译 YAML
/phase01-status      # ③ 查看过程数据：intent 数 / 覆盖度 / 门禁结论 / DoD
/phase01-update      # ④ 增量更新：补维度 / 重跑 intent / 局部再展开
/phase01-compile     # ⑤ 重编译：仅由文本用例重新生成 YAML（规范变更时）
```

### 设计手册 → [`phase01.md`](phase01.md) | 工作区 → [`phase01/`](phase01/)

---

## Phase 02：执行与报告 Harness

### 核心原则

1. **脚本为主，LLM 为辅。** 执行与判定主链路全部由确定性脚本完成；pass/fail 最终裁决**绝不交给 LLM**。
2. **Schema 校验是第一道闸门。** 不合规用例直接拒收并回报 Phase 01，绝不「尽力执行」残缺用例。
3. **YAML 编译是核心差异化能力。** 把 Phase 01 产出的文本意图编译为可在 GitCode 上真实运行的 workflow YAML 文件。
4. **断言三类全覆盖。** positive（应发生）/ negative（不应发生，安全命脉）/ nonfunctional（非功能：时序/并发/可理解性），全部确定性判定。
5. **可重复、可回归。** 同一用例任意时刻跑结果一致；每次 GitCode 发版自动重跑标回归。

### 入口

```bash
/phase02-schema-check # ① 第一道闸门：逐条校验 YAML，拒收不合规用例
/phase02-exec         # ② 执行：环境准备 → 编译 → 部署触发 → 采集 → 断言 → 清理
/phase02-status       # ③ 查看进度：通过率 / 失败摘要 / 预估剩余时间
/phase02-report       # ④ 生成报告：分维度报告 + 门禁判定 + 回归 diff + flaky 标记
```

### 设计手册 → [`phase02.md`](phase02.md) | 工作区 → [`phase02/`](phase02/)

---

## 两阶段契约

> 完整定义见 [`phase02/contract.md`](phase02/contract.md)

### Phase 01 → Phase 02 交接物

| 产物 | 必需 | 说明 |
|---|---|---|
| 可执行 YAML 用例 | **是** | `phase01/runs/<run-id>/cases/yaml/*.yaml`，通过 schema 校验 |
| Feature Parity Matrix | **是** | 报告分维度聚合参照 |
| 风险登记册 | **是** | P0/P1/P2 优先级来源 |
| 质量门禁 | **是** | 报告「能否上线」阈值依据 |
| 文本用例 | 参考 | 失败分析时回溯意图层描述 |

### Phase 02 → Phase 01 回流传导

| 产物 | 说明 |
|---|---|
| 拒收清单 | Schema 校验不通过，回报 Phase 01 修复 |
| 失败分诊 | LLM 根因初判（产品 bug / 用例问题 / 环境问题） |
| 衍生用例建议 | 失败举一反三，回流 Phase 01 评审 |
| Flaky 标记 | 时绿时红的用例，供 Phase 01 审视用例质量 |

### 溯源链（不可断）

```
风险项/能力项 → INTENT-xxx → 文本用例 ID → 派生 YAML → Phase 02 执行结果 → 报告
```

---

## 目录总览

```
gitcode-action/
├── README.md                          # 本文件 — 工程总览
├── phase01.md                         # Phase 01 设计手册（Agent Team）
├── phase02.md                         # Phase 02 设计手册（Harness）
│
├── phase01/                           # Phase 01 工作区
│   ├── README.md                      # 用例设计工作区入口
│   ├── process.md                     # 流程定义（intent → gate → 展开 → 编译）
│   ├── rules.md                       # 全局规则（命名/优先级/断言/溯源/安全红线）
│   ├── testing-focus.md               # Workflow 型系统测试关注点
│   ├── agents/                        # 8 个 agent 定义
│   │   ├── orchestrator/              #   测试架构师
│   │   ├── spec-analyst/              #   规格分析
│   │   ├── compat-diff/               #   兼容性 diff（核心资产）
│   │   ├── security/                  #   安全
│   │   ├── reliability/               #   稳定性
│   │   ├── usability/                 #   易用性
│   │   ├── review-gate/               #   评审门禁
│   │   └── case-writer/               #   用例 writer/reviewer
│   ├── inputs/                        # 5+ 类输入（规格/对标/样本/安全知识/业务场景）
│   ├── baseline/                      # L0 三份基线产物
│   ├── templates/                     # intent / 文本用例 / 可执行 YAML 模板
│   ├── schema/                        # 可执行 YAML 校验 schema
│   └── runs/                          # 按批次存档
│
├── phase02/                           # Phase 02 工作区
│   ├── README.md                      # 执行工作区入口
│   ├── process.md                     # 流程定义（8 步执行链路）
│   ├── rules.md                       # 全局规则（判定铁律/LLM 边界/断言纪律）
│   ├── contract.md                    # ★ Phase 01 ↔ Phase 02 接口契约
│   ├── agents/                        # 3 个 agent 定义（LLM 辅助角色）
│   │   ├── harness-orchestrator/      #   执行编排器
│   │   ├── yaml-compiler/             #   ★ YAML 编译（核心差异化能力）
│   │   └── failure-analyst/           #   失败根因分析
│   ├── scripts/                       # 6 个确定性脚本规格
│   │   ├── schema-validator.md        #   Schema 校验闸门
│   │   ├── api-client.md              #   GitCode API 客户端（20 个 v8 端点）
│   │   ├── workflow-runner.md         #   部署→触发→采集
│   │   ├── assertion-engine.md        #   ★ 三类断言确定性判定
│   │   ├── report-builder.md          #   分维度报告 + 门禁 + 回归
│   │   └── env-manager.md             #   环境隔离/重置
│   ├── inputs/                        # 输入清单（引用 Phase 01 产物 + 平台配置）
│   ├── templates/                     # 执行结果 / 测试报告模板
│   ├── runs/                          # 按执行批次存档
│   └── reports/                       # 归档报告
│
└── .claude/commands/                  # Claude Code 命令（共 9 个）
    ├── phase01-baseline.md            # Phase 01: 打地基
    ├── phase01-gen.md                 # Phase 01: 生成用例
    ├── phase01-status.md              # Phase 01: 查看状态
    ├── phase01-update.md              # Phase 01: 增量更新
    ├── phase01-compile.md             # Phase 01: 重编译 YAML
    ├── phase02-schema-check.md        # Phase 02: 校验输入
    ├── phase02-exec.md                # Phase 02: 执行用例
    ├── phase02-report.md              # Phase 02: 生成报告
    └── phase02-status.md              # Phase 02: 查看进度
```

---

## 快速开始

### 前置条件

- Claude Code（Agent Team 与 Harness 的运行环境）
- GitCode 测试实例（可随意破坏/重置的独立实例）
- GitCode OAuth2.0 Access Token（Phase 02 需要，配置为 `GITCODE_ACCESS_TOKEN` 环境变量）

### 典型流程

```bash
# === Phase 01：设计用例 ===
# 1. 补齐输入资料 → phase01/inputs/ 各子目录
# 2. 打地基
/phase01-baseline
# 3. 生成用例（含 STOP① 确认意图准入 + STOP② 确认交付验收）
/phase01-gen

# === 两阶段交接 ===
# Phase 01 DoD 通过后，可执行 YAML 即可被 Phase 02 消费

# === Phase 02：执行与报告 ===
# 4. 校验输入（闸门）
/phase02-schema-check 2026-07-20-01
# 5. 执行用例
/phase02-exec 2026-07-20-01
# 6. 中途查看进度
/phase02-status
# 7. 生成报告
/phase02-report 2026-07-20-01

# === GitCode 发版时 ===
# 增量：Phase 01 重编译 YAML → Phase 02 重新校验 → 增量执行 → 回归报告
/phase01-compile 2026-07-20-01
/phase02-schema-check 2026-07-20-01
/phase02-exec 2026-07-20-01 --compare 2026-07-19-01
/phase02-report 2026-07-20-01
```

---

## 设计特性

| 特性 | 说明 |
|---|---|
| **两阶段解耦** | 设计与执行独立；Phase 02 可对同一批用例在不同版本上反复回归 |
| **文本用例是源** | Phase 01 的文本用例与 GitCode 具体语法解耦，长期稳定归档 |
| **YAML 可再生** | 规范变更时重新编译 YAML，文本用例不动，执行脚本不动 |
| **确定性判定** | Phase 02 pass/fail 由断言引擎（脚本）裁定，LLM 不参与裁决 |
| **分维度报告** | 对照 Phase 01 质量门禁逐维度判断，不混成一个总通过率 |
| **回归网** | 挂到 GitCode 发版流水线，每次发版自动重跑、标回归 |
| **安全红线** | 安全用例全是 negative 断言（验证「什么不应发生」）；secret 脱敏；真实凭证不出现在用例/日志中 |
| **可随意破坏** | 独立测试实例，破坏性用例跑完即 IaC 重置 |

---

## 相关文档

- [Phase 01 设计手册](phase01.md) — Agent Team 完整运作手册
- [Phase 02 设计手册](phase02.md) — Harness 完整运作手册
- [Phase 01 工作区](phase01/) — Agent 定义、输入、基线、模板、schema
- [Phase 02 工作区](phase02/) — 脚本规格、Agent 定义、接口契约、模板
- [接口契约](phase02/contract.md) — Phase 01 ↔ Phase 02 交接细节
