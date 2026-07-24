## 校验失败 · USE-RUN-01-002 · 使用单标签 ubuntu-latest 时报错应给出三段式格式指引

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[bad-runner].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hosted',{os},{arch},{flavor}]，如['codearts-hosted','ubuntu-latest','x64','large']，其中'codearts-hosted'可省略；若为自定义资源池则定义为['self-hosted',{name},{label_1},{label_2},...,{label_n}]，如['self-hosted','my-private-pool','x64','region=cn-north-4']

- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-006 | trigger: workflow_dispatch
