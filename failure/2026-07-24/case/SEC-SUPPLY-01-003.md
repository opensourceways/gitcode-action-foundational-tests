## 校验失败 · SEC-SUPPLY-01-003 · 第三方 Action 来源应具备信任边界（typosquatting 限制）

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (2 条):
  - [Error] L0:C0 — jobs[typo-test].steps[0].uses: 格式错误：pluginname@version，其中 pluginname 为 1~50 位字母、数字、"-"、"_"，version（官方插件不填）为 00-99.00-99.00-99 三段两位数字
  - [Error] L0:C0 — stages[default].jobs[typo-test]: 插件checkout-action@v1不存在

- 维度: security | 优先级: P0
- intent_ref: INTENT-SEC-015 | trigger: workflow_dispatch
