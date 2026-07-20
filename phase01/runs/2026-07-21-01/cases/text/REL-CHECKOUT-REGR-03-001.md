用例 ID:   REL-CHECKOUT-REGR-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-054
标题:      official_checkout 在标准仓库上完整可用——回归基础可用性

前置条件:
  - 标准小型仓库 (< 100MB)
  - push 事件触发

操作步骤:
  1. 使用 uses: checkout（官方 action）
  2. 验证 checkout 完成后工作区有代码文件
  3. 验证 git rev-parse HEAD 输出与触发 commit SHA 一致

预期结果:
  - checkout 在 3min 内完成
  - 工作区文件与仓库一致
  - HEAD SHA 正确

验证点:
  - [正向] checkout 完成，工作区有文件
  - [正向] git rev-parse HEAD = 触发 SHA
  - [非功能] checkout 耗时 < 3min

清理:      fixture
