用例 ID:   SEC-SHA-REF-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-021
母意图:    —
标题:      uses 支持 commit SHA 不可变引用，且 tag/分支重写风险应被识别

前置条件:
  - 目标 action 仓库存在已知 commit SHA 与 tag
  - 测试仓库有权引用该 action

操作步骤:
  1. 在 workflow 中使用 uses: owner/action@<commit-sha> 引用 action
  2. 观察运行是否成功拉取该 action
  3. 再测试 uses: owner/action@<tag> 在 tag 被强制推送后的行为

预期结果:
  - commit SHA 引用应始终解析到同一版本
  - tag 被重写后，原 workflow 不应静默执行不同代码

验证点:
  - [正向] SHA 引用运行成功
  - [负向] tag 重写后旧 run 不应静默失败或被劫持

清理:      重置 fixture 仓库
