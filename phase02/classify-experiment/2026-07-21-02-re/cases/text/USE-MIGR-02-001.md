用例 ID:   USE-MIGR-02-001
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-014
标题:      直接搬运 .github/workflows/ci.yml 到 .gitcode/workflows/ 后的开箱报错路径

前置条件:
  - 将标准 GitHub workflow 原样放入 .gitcode/workflows/

操作步骤:
  1. 复制含 github.* / ubuntu-latest / actions/checkout@v4 / failure() / permissions: contents 的 GitHub workflow
  2. 触发 push 事件
  3. 观察一次性报错数量

预期结果:
  - 应一次性报告所有发现的问题
  - 每个报错可定位到对应迁移改造点

验证点:
  - [正向] 多错误一次性暴露
  - [非功能] 每个报错可定位迁移点: eval=llm_assisted

清理:      fixture
