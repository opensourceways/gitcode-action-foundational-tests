## 校验失败 · COMPAT-VARS-01-005 · vars 在条件表达式 if 中的可用性差异

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[test-vars-if].steps[1].if: if表达式无法解析 表达式：vars.ENABLE_FEATURE == 'true'第1位出现不支持的关键字

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-022 | trigger: workflow_dispatch
