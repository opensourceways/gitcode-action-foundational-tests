## 校验失败 · COMPAT-SCHEDULE-01-002 · schedule 不支持 timezone 字段差异

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — Cannot deserialize value of type `java.util.ArrayList<com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.on.GitcodeScheduleOn>` from Object value (token `JsonToken.START_OBJECT`)
 at [Source: UNKNOWN; byte offset: #UNKNOWN] (through reference chain: com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.GitcodePipelineDefinition["on"]->com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.on.GitcodeOn["schedule"])

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-013 | trigger: schedule
