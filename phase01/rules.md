# 全局规则（rules）

所有 agent 与命令都必须遵守。冲突时以本文件为准。

---

## 1. 命名与 ID（跨 run 唯一性）

### 1.1 维度标签（每条用例必标）

每条 intent 和用例必须**显式标注所属维度**，用于完整性审视与按维度过滤。维度标签取值：

| 维度 | 标签值 | 覆盖域 |
|---|---|---|
| 功能完备性 | `completeness` | Parity Matrix 能力项覆盖 |
| 兼容性 | `compatibility` | GitCode↔GitHub 行为差异 |
| 稳定性 | `reliability` | 并发/大规模/故障注入/恢复 |
| 安全性 | `security` | 攻击面/secret/权限/注入/供应链 |
| 易用性 | `usability` | 错误信息/文档/迁移摩擦/调试体验 |

> 意图和用例可以跨维度（如某 intent 同时涉及安全与兼容性），此时维度标签可多值（如 `[security, compatibility]`），但至少一个。intent 模板和用例模板都有 `dimensions` 字段。

### 1.2 缩写（仅用于 ID 编码）

- **维度缩写**：`COMP`(完备性) / `COMPAT`(兼容性) / `REL`(稳定性) / `SEC`(安全性) / `USE`(易用性)。

### 1.3 ID 格式（跨 run 唯一）

用例 ID 必须全局唯一（不同 run 不碰撞），格式为：

```
<维度>-<主题>-<run序列>-<序号>
```

- **意图 ID**：`INTENT-<维度>-<序号>`，如 `INTENT-SEC-014`（意图库内部序号，同 run 内唯一）。
- **用例 ID**：`<维度>-<主题>-<run序列>-<序号>`，如 `SEC-FORK-01-001`。其中 `run序列` 为 run-id 中的短标识（如 `2026-07-20-01` 取 `01`），`序号` 为三维内自增序号（如 `001`）。
  - 文本用例与其派生 YAML **共用同一 ID**。
  - 执行结果回绑 ID 即可直接定位文本用例，无需额外映射。
- **变体用例**：`<母ID>-Vn`，如 `SEC-FORK-01-001-V2`。

## 2. 优先级（取自风险登记册，不自造）

| 级别 | 含义 | 纪律 |
|---|---|---|
| P0 | blocker——不修不能上线 | 必须逐条对应风险登记册中的 blocker 项，不滥用 |
| P1 | 重要——影响大但有 workaround | |
| P2 | 一般——体验/边角 | |

优先级只能来自 `baseline/risk-register.md`。intent 若无法对齐任何风险项，门禁应质疑其价值。

## 3. 断言纪律（YAML 层必守）

- 每条用例断言必须**可确定性判定**；「跑绿了 / 没报错」不是合格断言。
- 三类断言必须按需覆盖（见 `templates/executable-case.yaml`）：
  - `positive` 应发生；`negative` 不应发生（安全命脉）；`nonfunctional` 非功能（时序/并发/可理解性）。
- **安全用例大多是 `negative`**；文本层必写「不应发生」的验证点。
- 易用性的「可理解性」判据若无法确定性判定，显式标注 `eval: llm_assisted`，交第二部分 LLM 辅助评判。

## 4. Oracle（期望从哪来）——关键

判定「预期结果」时，期望值的来源优先级：

1. **GitCode 官方规格**（`inputs/gitcode-spec/`）——GitCode 明确承诺的行为。
2. **GitHub Actions 官方语义**（`inputs/github-reference/`）——对「大部分兼容」的能力，GitHub 真实行为是默认 oracle；GitCode 未声明差异处，应与 GitHub 对齐。
3. **兼容性差异声明**——那「少量不一致」一旦澄清，写入 Parity Matrix，成为该点的权威 oracle，覆盖第 2 条。

**兼容性 diff 用例的期望必须写清「对齐谁」**：是应与 GitHub 行为一致（一致性用例），还是 GitCode 有意不同（差异确认用例）。含糊的「行为不一样」不是合格 intent。

## 5. Fixture 与破坏性纪律

- 本次验证有**独立、可随意破坏/重置的测试实例**——允许破坏性、混沌、渗透类用例。
- 每条破坏性用例必须正确声明 `teardown.reset`：`fixture`（重置夹具仓库）/ `full_instance`（重置整个实例）/ `none`。
- Fixture 仓库用模板名引用（如 `with-secrets`），模板定义与实例布置属第二部分 harness 职责；本部分只声明所需前置状态。

## 6. 安全红线（脱敏）

- 安全 agent **只产防御性验收目标**（「系统应防住什么 / 什么不应发生」），**不产可直接利用的攻击 payload、真实 exploit 代码或绕过步骤**。
- 描述攻击面用意图层语言（如「以外部 fork 贡献者身份提交试图输出 secret 的 workflow」），不写具体利用链。
- 用例、日志、intent 中不得出现真实密钥、真实 token、真实内网地址；一律用占位符（`DEPLOY_TOKEN` 等）。

## 7. 溯源链（不可断）

`风险项/能力项 → INTENT-xxx → 文本用例 ID → 派生 YAML(intent_ref)`。

- 每条文本用例必含 `溯源意图: INTENT-xxx`；每条 YAML 必含 `intent_ref`。
- 覆盖度评审即验证这条链的完整闭合：风险登记册每个 blocker、Parity Matrix 每个「部分/不支持/未知」项，都应能反查到覆盖它的用例。

## 8. 确定性与去 flaky

- intent/用例应尽量消除非确定性来源：显式固定并发度、超时、重试次数、随机种子。
- 涉及时序的断言给出明确阈值与容差，不用「应该很快」这类模糊表述。
- 破坏性/混沌用例必须声明「恢复预期」（`recovery_expectation`），否则无法判定通过与否。

## 9. 产出体量控制

- **意图先行**：agent 先产 intent、过门禁再展开。禁止跳过门禁直接产用例。
- 同一 intent 不重复展开；相似场景用变体（`-Vn`）显式关联，不各自新建独立用例。
- 门禁未准入的 intent 不进入 `cases/`，但保留在 `intent-library.md` 并标注「未准入 + 原因」，供回溯。

## 10. 不修改历史

- 已交付（`delivered`）的 run 目录不得原地改写结论；需要变更时新开 run 或在 `run.md` 时间线追加、旧结论标 `superseded`。
- 增量更新务必留痕（谁、何时、改了什么、为什么）。

## 11. 维度标注纪律

- 每条 intent 和每条文本用例**必须显式声明 `dimensions` 字段**，取值见 §1.1 维度标签表。
- 维度标签用于**完整性审视**：覆盖度报告需同时输出「按维度 × 按 Parity 能力项」的双轴覆盖。
- 门禁审计时检查：每个维度是否都有 P0 用例覆盖（尤其安全维度不可为空）。
- 跨维度意图/用例允许多标签（如 `[security, compatibility]`）。

## 12. 输入感知纪律

- 各 agent 在发散阶段必须**先读取对应 input 目录**（见 `inputs/INPUTS.md` 的消费方映射），在产出中标注「依哪份输入得出」。
- 当输入刷新（如 `platform-config/` 或 `business-context/` 更新），agent 必须在 intent/用例中显式标注**输入版本**（时间戳或内容摘要），便于 `/phase01-update` 时识别需重新审视的项。
