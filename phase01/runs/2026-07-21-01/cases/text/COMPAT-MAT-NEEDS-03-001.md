用例 ID:   COMPAT-MAT-NEEDS-03-001
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-091
标题:      matrix job 的 needs 依赖导致「任务初始化错误」——历史 #101 回归验证

前置条件:
  - 定义 matrix job build（3 个实例）
  - 定义 job test 依赖 build（needs: build）

操作步骤:
  1. 定义 matrix job build：strategy.matrix.node=[18,20,22]
  2. 定义 job test：needs: build
  3. 触发 workflow，观察 test 是否在 build 全完成后正常启动

预期结果:
  - build 所有 3 个实例成功完成后，test 应正常启动
  - test 不应报「任务初始化错误」（已知 #101 bug）
  - 这是 matrix + needs 在 CI 中最常见模式的核心验证

验证点:
  - [正向] build 完成后 test 正常启动并执行成功
  - [负向] test 不出现「任务初始化错误」
  - [非功能] needs.test.result 应返回 success

清理:      fixture
