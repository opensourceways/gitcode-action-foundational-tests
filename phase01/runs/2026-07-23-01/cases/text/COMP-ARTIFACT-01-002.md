用例 ID:   COMP-ARTIFACT-01-002
维度标签:   [completeness, reliability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-015
参照来源:  inputs/gitcode-spec/core-concepts/artifacts-and-cache.md
母意图:    —
标题:      下载全部制品功能正常

前置条件:
  - workflow 上传多个 artifacts

操作步骤:
  1. job 1 上传多个 artifacts
  2. job 2 不指定 name 下载全部 artifacts

预期结果:
  - 所有 artifacts 被下载到指定目录

验证点:
  - [正向] 所有 artifact 文件均存在

清理:      none
