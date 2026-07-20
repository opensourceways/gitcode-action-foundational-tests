# Phase 02 · 执行与报告 Harness（可运行骨架）

> 本目录是「执行用例 → 采集 → 判定 → 产出报告」阶段的 **可运行、可复现、可增量更新** 的工作区。
> 完整设计手册见根目录 [`../phase02.md`](../phase02.md)；本目录把它落成可跑的组件、流程、命令与模板。

## 与 Phase 01 的关系

```
Phase 01（用例设计 Agent Team）
  │  产出：文本用例（source of truth）+ 派生可执行 YAML + 三份基线
  │  交接契约：phase01/schema/executable-case.schema.yaml
  ▼
Phase 02（执行与报告 Harness）★ 本目录
  │  读入 YAML → 编译 GitCode workflow → 触发 → 采集 → 断言 → 报告
  │  形态：确定性脚本为主，LLM 辅助
```

## 这套东西怎么用（3 分钟版）

```
① 校验输入        → /phase02-schema-check  逐条过 schema，拒收不合规用例
② 执行用例        → /phase02-exec          新建 run，按维度执行
③ 查看进度        → /phase02-status        看通过率 / 失败摘要 / 进度
④ 生成报告        → /phase02-report        分维度报告 + 回归 diff + flaky 标记
```

## 目录导航

| 路径 | 是什么 |
|---|---|
| [`process.md`](process.md) | 流程定义：执行链、门禁、run 生命周期、DoD |
| [`rules.md`](rules.md) | 全局规则：断言纪律、判定铁律、LLM 边界、脱敏 |
| [`contract.md`](contract.md) | ★ 与 Phase 01 的接口契约（对齐文档） |
| [`agents/`](agents/) | 3 个 agent 定义（LLM 辅助角色） |
| [`scripts/`](scripts/) | 6 个确定性脚本规格 |
| [`inputs/`](inputs/) | 输入清单：接收 Phase 01 的 YAML 用例 + 平台配置 |
| [`runs/`](runs/) | 按执行批次存档，每次 `/phase02-exec` 生成一个 `<run-id>/` |
| [`templates/`](templates/) | 执行结果模板 / 测试报告模板 |
| [`reports/`](reports/) | 归档报告 |

## 核心原则（务必先读）

1. **脚本为主，LLM 为辅。** 执行与判定主链路全部由确定性脚本完成；LLM 只做 YAML 编译、失败分析、易用性评判等辅助工作。pass/fail 的最终裁决**绝不交给 LLM**。
2. **Schema 校验是第一道闸门。** 不合规用例直接拒收并回报 Phase 01，绝不「尽力执行」残缺用例。
3. **YAML 编译是 Phase 02 核心差异化能力。** 把 Phase 01 产出的文本意图（`workflow:` 字段）编译为可在 GitCode 上真实运行的 workflow YAML 文件。
4. **断言三类全覆盖。** positive（应发生）/ negative（不应发生，安全命脉）/ nonfunctional（非功能：时序/并发/可理解性）。
5. **可复现、可回归。** 每次执行自成一个 run 目录，结果结构化落库，支持与上次 run 对比回归。

## 与第一部分（设计）的边界

Phase 02 只**执行用例、采集结果、产出报告**，不判断「该测什么」。唯一合法输入是 Phase 01 通过 DoD 验收的可执行 YAML（经 schema 校验）。详见 [`contract.md`](contract.md)。
