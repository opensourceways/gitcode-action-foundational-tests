用例 ID:   USE-CONC-01-002
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-027
母意图:    —
标题:      concurrency.max 配置 -1 时报错应提示有效范围

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 workflow 中配置 concurrency: max: -1

预期结果:
  YAML 校验报错，明确说明 max 取值范围应为 1-5

验证点:
  - [负向] 不应静默截断
  - [非功能] 报错中是否包含有效范围说明

清理:      无

