## 校验失败 · USE-YAML-01-002 · YAML 缩进错误时报错应指出具体行号与列号

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — while parsing a block mapping
 in 'string', line 5, column 5:
        name: indent error
        ^
expected <block end>, but found '<block sequence start>'
 in 'string', line 11, column 6:
         - name: step two
         ^


- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-022 | trigger: workflow_dispatch
