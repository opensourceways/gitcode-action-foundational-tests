## 校验失败 · COMPAT-CONCUR-01-002 · concurrency 配置越界或不支持时应给出清晰报错

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — Cannot deserialize value of type `java.lang.String` from Array value (token `JsonToken.START_ARRAY`)
 at [Source: UNKNOWN; byte offset: #UNKNOWN] (through reference chain: com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.GitcodePipelineDefinition["concurrency"]->com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.strategy.GitcodeConcurrency["group"])

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-034 | trigger: workflow_dispatch
