用例 ID:   COMPAT-CONTAINER-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-001
母意图:    —
标题:      container 字段不被支持时应明确报错而非静默忽略

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个包含 `jobs.<id>.container` 字段的 workflow 文件
  2. 该字段指定 `image: ubuntu:latest`
  3. 提交该 workflow 到仓库

预期结果:
  - 系统拒绝该 workflow（GitCode 不支持 container 字段）
  - 报错信息应明确指出 `container` 字段不被支持
  - 报错不应仅给出模糊的 "unknown property" 或静默忽略该字段导致用户误以为容器环境生效

验证点:
  - [负向] 不通过无指引的原始报错（如仅报 generic YAML error）
  - [负向] 不通过静默忽略（workflow 被接受但容器未生效）
  - [正向] 报错信息包含 `container` 关键字及可操作建议
  - [正向] 报错指向正确行号或字段名

清理:      重置 fixture 仓库
