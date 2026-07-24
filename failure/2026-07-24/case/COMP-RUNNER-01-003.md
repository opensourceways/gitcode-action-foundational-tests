## 校验失败 · COMP-RUNNER-01-003 · 不存在的标签组合导致 job 排队或失败

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[verify].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hosted',{os},{arch},{flavor}]，如['codearts-hosted','ubuntu-latest','x64','large']，其中'codearts-hosted'可省略；若为自定义资源池则定义为['self-hosted',{name},{label_1},{label_2},...,{label_n}]，如['self-hosted','my-private-pool','x64','region=cn-north-4']

- 维度: completeness | 优先级: P1
- intent_ref: INTENT-COMP-010 | trigger: workflow_dispatch
