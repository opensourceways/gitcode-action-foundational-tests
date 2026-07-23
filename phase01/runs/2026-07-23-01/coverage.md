# Coverage Report · Run 2026-07-23-01

> 生成时间: 2026-07-23
> 基准: Parity Matrix + Risk Register + Quality Gate

---

## 1. Intent 覆盖率

| 指标 | 数值 |
|---|---|
| 准入 intent 总数 | 186 |
| 有对应用例的 intent 数 | 184 |
| Intent 覆盖率 | 184/186 (98.9%) |

### 各维度 Intent 覆盖

| 维度 | 准入 intent | 已覆盖 intent | 覆盖率 |
|---|---|---|---|
| completeness | 16 | 18 | 112.5% |
| compatibility | 35 | 35 | 100.0% |
| security | 36 | 36 | 100.0% |
| reliability | 66 | 66 | 100.0% |
| usability | 29 | 29 | 100.0% |

---

## 2. Parity Matrix 覆盖度

对照 `baseline/parity-matrix.md` 44 项能力项：

| 覆盖状态 | 数量 | 说明 |
|---|---|---|
| 有 ≥1 条用例覆盖 | 40 | 含全部 P0 安全项、核心兼容性差异、稳定性边界 |
| 未直接覆盖（文档/可发现性类） | 4 | annotation 机制完整端到端、action `runs.using` 支持范围、runner.debug 触发方式、自托管 Runner 多 Job 并发 |

**未直接覆盖项详情**（来自 gate-log.md 盲区清单）：
1. **注解(annotation)机制** — parity-matrix 标记为 ❓，仅 usability 覆盖报错质量，无完整端到端验证
2. **action `runs.using` 支持范围** — GAP-017，文档仅列 `node16`，node20/docker/composite 未知
3. **runner.debug 触发方式** — GAP-018，文档未说明如何开启 debug 模式
4. **自托管 Runner 同时运行多个 Job** — GAP-019，文档未明确是否支持

---

## 3. 风险登记册覆盖度

对照 `baseline/risk-register.md` 5 项风险：

| 风险 ID | 描述 | 覆盖状态 | 覆盖用例数 |
|---|---|---|---|
| RISK-SEC-01 | fork PR secret 隔离失效 | ✅ 全覆盖 | 30+ 条 P0（security + completeness + compatibility） |
| RISK-SEC-02 | pull_request_target Pwn Request | ✅ 全覆盖 | 8+ 条 P0 |
| RISK-COMPAT-01 | 默认值差异致行为静默不同 | ✅ 全覆盖 | 25+ 条 P1（compatibility + usability） |
| RISK-REL-01 | 并发洪泛下排队/公平性失效 | ✅ 全覆盖 | 15+ 条 P1（reliability） |
| RISK-USE-01 | 迁移报错不指明 GitCode 差异 | ✅ 全覆盖 | 15+ 条 P1（usability + compatibility） |

**全部 5 项风险均有 P0/P1 用例覆盖。**

---

## 4. 优先级分布

| 优先级 | 数量 | 占比 |
|---|---|---|
| P0 | 83 | 29.2% |
| P1 | 198 | 69.7% |
| P2 | 3 | 1.1% |

---

## 5. 断言类型分布（抽样统计）

基于 security / reliability 维度重点抽样：

| 断言类型 | 数量 | 占比 |
|---|---|---|
| negative | 80+ | ~25% |
| positive | 180+ | ~55% |
| nonfunctional | 60+ | ~20% |

---

*Coverage Report 最后更新: 2026-07-23*
