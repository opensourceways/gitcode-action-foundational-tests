## 校验失败 · COMPAT-RUNNER-01-004 · 自定义特征标签不被支持时应给出可用标签列表

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[test-custom-label].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hosted',{os},{arch},{flavor}]，如['codearts-hosted','ubuntu-latest','x64','large']，其中'codearts-hosted'可省略；若为自定义资源池则定义为['self-hosted',{name},{label_1},{label_2},...,{label_n}]，如['self-hosted','my-private-pool','x64','region=cn-north-4']

- 维度: compatibility | 优先级: P2
- intent_ref: INTENT-COMPAT-NEW-008 | trigger: workflow_dispatch
