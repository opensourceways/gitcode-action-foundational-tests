# GitCode Actions 测试验证 · 第一部分：用例设计 Agent Team 手册

> 本手册指导「场景分析 → 问题分析 → 测试用例产出」这一阶段的 team 搭建与运作。
> 组织形态：以 **agent team 为主**，人工做基线锚定与评审裁决。
> 归档主体：一批**文本测试用例**（人可读、稳定，作为 source of truth）；据此编译出可执行的声明式用例交付执行。另附 L0 基线产物。
> **边界声明**：本部分只负责「设计用例」，不负责执行。执行由第二部分承接，二者以《测试用例契约》为唯一交接面。

---

## 1. 目标与定位

对 GitCode 即将推出的类 GitHub Actions 功能，在上线前系统性地识别风险并产出可执行的测试用例，覆盖四个责任维度：**完备性、稳定性、安全性、易用性**。

本阶段回答两个问题：
1. 「我们该测什么」——基于规格、对标差异、历史经验和安全模型，把风险点挖全。
2. 「用例长什么样」——把风险点落成机器可执行、可评审的声明式用例。

关键背景约束（决定策略形态）：
- GitCode Actions **大部分兼容** GitHub Actions，存在**少量不一致**——兼容性差异是最大的隐性风险区，单列为一等测试类型。
- 本次验证可拿到**独立测试实例，可随意破坏/重置**——允许设计破坏性、混沌、安全渗透类用例。

---

## 2. 前置产物：L0 验收基线（team 启动的地基）

在 agent 大规模产出用例之前，必须先由人牵头、agent 协助，产出三份基线产物。它们是用例优先级和「能否上线」判断的客观标尺。**没有 L0，agent 会产出海量低价值用例。**

| 产物 | 作用 | 形态 |
|---|---|---|
| Feature Parity Matrix | 对标 GitHub Actions 的完备性标尺 | 能力清单 × 支持状态（完全/部分/不支持/未知）|
| 风险登记册 | 决定测试火力分配 | 风险项 × 影响 × 概率 × 维度 × 优先级 |
| 质量门禁 | 定义「凭什么敢上线」 | 分维度阈值 + blocker 判定规则 |

**建议顺序**：先拉 3~5 个真实开源项目的 workflow 跑通冒烟，同时手写 Parity Matrix 与风险登记册的首版。这一步会立刻暴露最扎眼的几个不一致点，让后续 agent 的火力分配有依据。

---

## 3. 组织轴：四个测试维度

team 按维度组织，而非按功能模块组织。每个维度对应一条责任，有独立的 owner agent。

- **完备性**：Feature parity + **兼容性 diff**（重点找「看起来一样、行为不一样」的点）。
- **稳定性**：并发、大规模、长时运行、资源配额、故障恢复、**混沌注入**。
- **安全性**：供应链、密钥、权限、注入、runner 隔离、资源滥用。开源社区任何人可提 PR 触发流水线，攻击面远大于企业内网，是唯一「漏一个可能上头条」的维度，建议单独立项并配懂 CI/CD 攻击面的人 review。
- **易用性**：错误信息质量、文档一致性、调试体验、**从 GitHub 迁移的摩擦**。

---

## 4. Agent Team 角色定义

务实分工，不求多。每个角色明确「职责 / 输入 / 输出」。

### 4.1 测试架构师（Orchestrator，建议人 + agent 协作）
- **职责**：持有 L0 基线；给各 agent 分配优先级；裁决意图库；防止重复与覆盖盲区。
- **输入**：L0 三份基线产物、各 agent 产出的 test intent。
- **输出**：意图库的优先级排序、任务分派、覆盖度缺口清单。

### 4.2 规格分析 agent
- **职责**：消化 GitCode Action 规格文档，产出结构化能力清单。
- **输入**：GitCode Action 规格文档、语法说明。
- **输出**：结构化能力清单（喂给 Parity Matrix）。

### 4.3 兼容性 diff agent（本次核心资产）
- **职责**：对比 GitHub Actions 官方语义与真实 workflow 行为，系统性产出「疑似不一致」意图。
- **输入**：GitHub Actions 语法文档、真实 workflow 样本、GitCode 能力清单。
- **输出**：兼容性差异 test intent（标注疑似不一致的具体点与预期对齐行为）。

### 4.4 安全 agent
- **职责**：基于安全加固手册与已知漏洞模式，产出攻击面测试意图（**只描述「要验证系统能防住什么」的防御性验收目标，不产出攻击 payload**）。
- **输入**：GitHub Actions 安全加固手册、公开漏洞/CVE 模式分析、权限与隔离规格。
- **输出**：安全 test intent（含负向断言目标：什么不应发生）。

### 4.5 稳定性 agent
- **职责**：设计并发、边界、资源耗尽、故障注入类意图。
- **输入**：容量/配额规格、runner 架构说明。
- **输出**：稳定性 test intent（含故障注入点与恢复预期）。

### 4.6 易用性 agent
- **职责**：设计错误信息、文档一致性、迁移摩擦类意图。
- **输入**：产品文档、错误码表、GitHub 迁移场景。
- **输出**：易用性 test intent（含「新手可理解性」判据）。

### 4.7 用例 writer / reviewer agent
- **职责**：先把评审通过的 intent 展开为**文本用例**（归档主体）；再依据当前 GitCode 规范把文本用例**编译为可执行 YAML**；去重、校验完整性。
- **输入**：评审通过的 test intent、GitCode 规范。
- **输出**：文本用例（归档、评审主体）+ 派生的可执行 YAML（第二部分的输入）。

---

## 5. 核心工作流：意图先行，用例后展开

**关键机制**：agent 不直接产用例，先产 **test intent（测试意图/风险点）**。这是控制用例质量与数量的闸门。

```
输入依赖 ──▶ 各维度 agent 产出 test intent ──▶ 意图库
                                                  │
                            ┌──── 评审门禁 ◀───────┘
                            │  去重 · 定优先级 · 覆盖度检查
                            ▼
              writer 展开为文本用例（归档主体，评审完整性）
                            │  依据 GitCode 规范编译
                            ▼
                 派生可执行 YAML（可再生）
                            │
                            ▼
                  交付验收（DoD，见 §7.6）──▶ 第二部分
```

- **阶段 A（发散）**：各维度 agent 依据输入，尽量把风险点挖全，产出 intent（此时只描述「测什么、为什么有风险、预期系统行为」，不写执行细节）。
- **评审门禁（收敛）**：由架构师裁决——去重、按风险登记册定优先级、对照 Parity Matrix 查覆盖盲区。**只有通过门禁的 intent 才允许展开**，避免在低价值路径上消耗展开成本。
- **阶段 B（收敛）**：writer agent 先把 intent 展开为**文本用例**（归档与完整性评审的主体），再据 GitCode 规范编译为可执行 YAML。

---

## 6. 输入依赖清单

| 类别 | 具体输入 | 主要消费方 |
|---|---|---|
| 产品规格 | GitCode Action 规格、语法、权限/配额说明 | 规格分析、稳定性、安全 agent |
| 对标基准 | GitHub Actions 官方语法/语义文档 | 兼容性 diff agent |
| 真实负载 | 一批真实开源项目 `.github/workflows` 样本 | 兼容性 diff、完备性 |
| 安全知识 | 安全加固手册、公开漏洞/CVE 模式分析 | 安全 agent |
| 历史经验 | 既有缺陷库、以往验证踩坑记录 | 全体 |

---

## 7. 交付规范 ★（归档主体与交接边界）

本节定义用例的**两层表示**，以及与第二部分的交接边界。核心原则：**文本用例是源与归档主体，可执行 YAML 是由它编译的派生物。评审看文本用例，执行用 YAML。**

### 7.1 两层用例表示（关键设计）

- **文本用例（Text Case）＝ 归档主体 / source of truth**：人可读的自然语言用例。它稳定、与 GitCode 具体语法解耦，是团队**评审完整性、沉淀经验、长期归档**的对象。我们审视覆盖度与完整性，优先且主要基于文本用例。
- **可执行用例（Executable Case，YAML）＝ 派生交接物**：由 writer agent 依据文本用例 **＋ 当前 GitCode 规范**编译生成，供第二部分 harness 执行。它**可再生**——GitCode 规范调整、或那「少量不一致」被澄清时，重新生成 YAML 即可，文本用例基本不动。

### 7.2 文本用例格式（归档主体模板）

```
用例 ID:   SEC-FORK-001          # 前缀=维度缩写
维度:      安全性
优先级:    P0                     # 取自风险登记册
溯源意图:  INTENT-SEC-014
标题:      fork PR 不应读取到仓库 secrets

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 以外部 fork 贡献者身份，提交一个试图输出 DEPLOY_TOKEN 的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - 系统阻止 fork PR 访问 DEPLOY_TOKEN，或 workflow 拿不到该值
  - 运行日志中不出现 DEPLOY_TOKEN 明文

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [正向] fork 身份无 secret 访问权限

清理:      重置 fixture 仓库
```

文本用例只描述「验证什么」（意图层），不写 GitCode 具体语法——「提交一个试图输出 token 的 workflow」是意图层描述，落成什么样的 `.yml` 由 writer 按 GitCode 规范生成。这正是它稳定、可长期归档的原因。

### 7.3 可执行用例契约（派生 YAML schema）

由文本用例编译生成，供 harness 消费。**这是交给第二部分的交接物，可随 GitCode 规范重新生成。** 每条是一份声明式 YAML：

```yaml
id: SEC-FORK-001                 # 全局唯一，前缀=维度缩写
dimension: security              # completeness | reliability | security | usability
priority: P0                     # P0 blocker / P1 / P2，取自风险登记册
title: fork PR 不应读取到仓库 secrets
intent_ref: INTENT-SEC-014       # 溯源到意图库

setup:                           # 前置状态，由 harness 布置
  repo_fixture: with-secrets     # fixture 仓库模板名
  secrets: [DEPLOY_TOKEN]
  variables: {}
  branch_protection: default

workflow: |                      # 被测的 workflow 定义（内联）
  on: [pull_request_target]
  jobs:
    echo:
      runs-on: default
      steps:
        - run: echo "$DEPLOY_TOKEN"

trigger:
  event: fork_pr                 # push | pr | fork_pr | manual | schedule
  as: untrusted_contributor      # maintainer | untrusted_contributor
  params: {}

fault_injection: null            # 稳定性用例在此声明注入点，见 §7.2

assertions:                      # 三类断言，见 §7.3
  - type: negative
    target: run_logs
    must_not_contain_secret: DEPLOY_TOKEN
  - type: positive
    target: run_status
    equals: blocked_or_no_secret_access

teardown:
  reset: fixture                 # fixture | full_instance | none
```

### 7.4 故障注入声明（稳定性用例，YAML 层）

```yaml
fault_injection:
  at: mid_job                    # 注入时机
  action: kill_runner            # kill_runner | network_partition | disk_full | cpu_saturate | concurrent_flood
  params: { concurrency: 50 }
  recovery_expectation: retry_and_succeed
```

### 7.5 断言类型（YAML 层，必须覆盖三类）

| type | 说明 | 典型 target |
|---|---|---|
| `positive` | 应发生：状态/产物/退出码符合预期 | run_status, artifact, exit_code |
| `negative` | **不应发生**（安全命脉）：密钥不泄露、权限不越界、副作用不产生 | run_logs, secret_access, side_effect |
| `nonfunctional` | 非功能：时序、并发无干扰、错误信息可理解 | latency, concurrency_isolation, error_message |

**要点**：安全用例大多是 `negative` 断言；稳定性/易用性大量是 `nonfunctional`。writer agent 必须保证每条用例的断言可被确定性判定（易用性的「可理解性」判据除外，交由第二部分 LLM 辅助评判，需在断言里显式标注 `eval: llm_assisted`）。

### 7.6 交付验收清单（Definition of Done）

完整性以**文本用例**为准评审；YAML 为其派生物。一批用例交付给第二部分前，必须满足：
- [ ] 完整性/覆盖度评审基于文本用例：对照 Parity Matrix 与风险登记册无盲区。
- [ ] 每条文本用例可溯源到某个 `intent_ref`，含明确的预期结果与验证点。
- [ ] 每条文本用例有对应的、通过 schema 校验的可执行 YAML；YAML 由文本用例＋GitCode 规范编译，规范变更时可重新生成。
- [ ] 优先级取自风险登记册，P0 覆盖所有 blocker 风险项。
- [ ] 安全用例文本层必含「不应发生」的验证点，YAML 层落为 `negative` 断言。
- [ ] 破坏性用例正确声明 `teardown.reset` 级别。

### 7.7 附带交付：基线产物
Feature Parity Matrix、风险登记册、质量门禁随用例一并交付并持续维护——它们是第二部分报告分维度聚合与门禁判断的依据。

---

## 8. 质量标准（评审关注点）

- **覆盖度 / 完整性**：以**文本用例**为准，相对 Parity Matrix 和风险登记册可度量，而非主观「差不多了」。
- **可执行性**：每条用例的 setup/trigger/assertions 足够具体，harness 无需猜测即可执行。
- **断言明确性**：断言可确定性判定；「跑绿了」不是合格断言。
- **无重复**：同一 intent 不重复展开；变体用例应显式关联母 intent。
- **优先级真实**：P0 就是不修不能上线的，不滥用。
