## 校验失败 · COMPAT-ACTIONDEV-01-001 · action.yml 元数据校验与 GitHub 差异

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (2 条):
  - [Error] L0:C0 — jobs[test-action-meta].steps[1].uses: 格式错误：pluginname@version，其中 pluginname 为 1~50 位字母、数字、"-"、"_"，version（官方插件不填）为 00-99.00-99.00-99 三段两位数字
  - [Error] L0:C0 — stages[default].jobs[test-action-meta]: 插件./.github/actions/my-action不存在

- 维度: compatibility | 优先级: P2
- intent_ref: INTENT-COMPAT-NEW-010 | trigger: workflow_dispatch
