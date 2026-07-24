## 校验失败 · SEC-WCMD-01-004 · ATOMGIT_OUTPUT 不被不可信输入污染提权

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — while scanning a simple key
 in 'string', line 12, column 1:
    hijacked=bad" >> $ATOMGIT_OUTPUT
    ^
could not find expected ':'
 in 'string', line 13, column 13:
          - name: Check no hijack
                ^


- 维度: security | 优先级: P0
- intent_ref: INTENT-SEC-030 | trigger: workflow_dispatch
