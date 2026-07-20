# 文本用例模板（归档主体 / source of truth）

> 阶段 B 由 case-writer 产出，存 `runs/<id>/cases/text/<ID>.md`。
> 人可读、与 GitCode 具体语法解耦——这是团队评审完整性、沉淀经验、长期归档的对象。
> **只描述「验证什么」（意图层），不写 GitCode 具体 `.yml` 语法**（语法落在 YAML 层）。

```
用例 ID:   SEC-FORK-01-001       # <维度>-<主题>-<run序列>-<序号>；与派生 YAML 共用
维度标签:   [security]               # 见 rules.md §1.1: completeness|compatibility|reliability|security|usability
维度:      安全性
优先级:    P0                        # 取自风险登记册，不自造
溯源意图:  INTENT-SEC-014
母意图:    —                         # 变体用例填母用例/母意图 ID
标题:      fork PR 不应读取到仓库 secrets

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自 fork 的 PR

操作步骤:                          # 意图层描述，不写具体 .yml
  1. 以外部 fork 贡献者身份，提交一个试图输出 DEPLOY_TOKEN 的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - 系统阻止 fork PR 访问 DEPLOY_TOKEN，或 workflow 拿不到该值
  - 运行日志中不出现 DEPLOY_TOKEN 明文

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [正向] fork 身份无 secret 访问权限

清理:      重置 fixture 仓库        # 对应 YAML 的 teardown.reset
```

## 写作纪律
- 溯源意图必填；变体用例填「母意图」。
- 安全用例必含「不应发生」的负向验证点。
- 破坏性用例写清「清理」级别。
- 不出现真实密钥/token/内网地址，用占位符。
- 不写 GitCode 语法细节——保持文本层稳定、可长期归档。
