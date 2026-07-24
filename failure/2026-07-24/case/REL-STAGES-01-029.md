## 校验失败 · REL-STAGES-01-029 · stages fail_fast 机制——阶段内任一 job 失败应立即终止同阶段其他 jobs

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — Cannot deserialize value of type `java.util.LinkedHashMap<java.lang.String,com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.structs.GitcodeStage>` from Array value (token `JsonToken.START_ARRAY`)
 at [Source: UNKNOWN; byte offset: #UNKNOWN] (through reference chain: com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.GitcodePipelineDefinition["stages"])

- 维度: reliability | 优先级: P1
- intent_ref: INTENT-REL-029 | trigger: workflow_dispatch
