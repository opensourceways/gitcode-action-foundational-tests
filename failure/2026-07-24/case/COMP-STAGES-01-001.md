## 校验失败 · COMP-STAGES-01-001 · stages 阶段间串行、阶段内 job 并行执行

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — Cannot deserialize value of type `java.util.LinkedHashMap<java.lang.String,com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.structs.GitcodeStage>` from Array value (token `JsonToken.START_ARRAY`)
 at [Source: UNKNOWN; byte offset: #UNKNOWN] (through reference chain: com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.GitcodePipelineDefinition["stages"])

- 维度: completeness | 优先级: P1
- intent_ref: INTENT-COMP-007 | trigger: workflow_dispatch
