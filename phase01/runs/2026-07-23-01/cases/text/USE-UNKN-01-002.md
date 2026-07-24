用例 ID:   USE-UNKN-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-023
参照来源:  inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md
母意图:    —
标题:      未知字段报错若识别为 GitHub 特有应追加迁移提示

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 workflow 中使用 GitHub 特有的 jobs.<id>.container 字段

预期结果:
  报错除指出字段不支持外，还提示该字段为 GitHub Actions 特有

验证点:
  - [非功能] 报错中是否出现 GitHub Actions 特有等迁移提示

清理:      无

