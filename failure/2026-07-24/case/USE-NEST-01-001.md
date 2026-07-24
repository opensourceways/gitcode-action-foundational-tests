## 校验失败 · USE-NEST-01-001 · workflow_call 嵌套 3 层时报错应明确提示上限为 2 层

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (2 条):
  - [Error] L0:C0 — jobs[caller].steps[0].uses: 格式错误：pluginname@version，其中 pluginname 为 1~50 位字母、数字、"-"、"_"，version（官方插件不填）为 00-99.00-99.00-99 三段两位数字
  - [Error] L0:C0 — stages[default].jobs[caller]: 插件./.gitcode/workflows/reusable-level1.yml不存在

- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-026 | trigger: workflow_dispatch
