用例 ID:   COMP-DIR-01-002
维度标签:   [completeness]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-001
母意图:    —
标题:      .github/workflows/ 下的 YAML 不被识别为 workflow

前置条件:
  - 仓库 .github/workflows/ 目录下存在 ci.yml
  - 仓库 .gitcode/workflows/ 下无同名 workflow

操作步骤:
  1. 向默认分支推送代码变更
  2. 观察 Actions 标签页是否出现新运行

预期结果:
  - .github/workflows/ci.yml 不被识别为 workflow
  - push 事件不会触发该文件对应的运行

验证点:
  - [负向] 运行列表中不存在源自 .github/workflows/ci.yml 的运行

清理:      none
