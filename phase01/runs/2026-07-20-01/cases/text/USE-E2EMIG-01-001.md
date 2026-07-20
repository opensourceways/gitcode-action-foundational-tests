用例 ID:   USE-E2EMIG-01-001
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-014
标题:      直接搬运 .github/workflows/ci.yml 到 .gitcode/workflows/ 后的开箱报错路径
前置条件:  准备标准 GitHub workflow 文件（含 ubuntu-latest / actions/checkout@v4 / success() / permissions:contents 等）
操作步骤:
  1. 将未修改的 GitHub workflow 放入 .gitcode/workflows/
  2. 触发 push 事件
  3. 观察平台报错列表
  4. 统计一台提交后暴露的错误数量
  5. 修正 github→atomgit + runs-on + permissions 命名后再次提交
预期结果: 应一次性报告所有语法/语义问题，非逐错修复
验证点:
  - [正向] 平台尽量一次暴露所有语法/语义错误
  - [非功能] 每个报错消息能让开发者定位到对应的迁移改造点
清理:      fixture
