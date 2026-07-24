## 校验失败 · COMPAT-PATHS-01-001 · paths 过滤器 300 条边界测试

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L3:C5 — on.push: 列表长度超出限制，paths paths-ignore之和不能小于1或超过32

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-012 | trigger: push
