# 用例归档

用例 ID:   COMPAT-CONCUR-01-002
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-034
母意图:    —
标题:      concurrency 配置越界或不支持时应给出清晰报错

前置条件:
  - 仓库已启用 workflow
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow 文件，配置不支持的 concurrency 语法（如 group 值为数组、或包含非法字符）
  2. 尝试通过 API 或 UI 提交/校验该 workflow
  3. 观察报错信息

预期结果:
  - 系统拒绝该 workflow
  - 报错信息应明确指出 concurrency 配置错误的位置和原因
  - 报错应给出可操作的修改建议（如正确的 group 格式应为字符串）

验证点:
  - [负向] 不通过无指引的原始报错（如仅报 generic YAML error）
  - [正向] 报错信息包含 `concurrency` 关键字
  - [正向] 报错指向具体字段（group 或 cancel-in-progress）

清理:      重置 fixture 仓库
