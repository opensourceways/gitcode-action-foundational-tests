## 校验失败 · COMPAT-SECRET-01-005 · 环境级 secrets 不支持时应明确报错而非降级为项目级

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[test-env-secret].environment: unknown property

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-NEW-002 | trigger: workflow_dispatch
