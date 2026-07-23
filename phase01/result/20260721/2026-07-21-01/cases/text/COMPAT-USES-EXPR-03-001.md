用例 ID:   COMPAT-USES-EXPR-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-090
标题:      uses 字段不支持 ${{ }} 表达式——历史 #82 回归验证

前置条件:
  - workflow 中 uses 字段使用 ${{ }} 表达式引用动态 action 路径

操作步骤:
  1. 配置 uses: ${{ atomgit.repository }}/.gitcode/workflows/ci.yml@main
  2. 配置 uses: ${{ env.ACTION_PATH }}（env 变量动态引用）
  3. 触发 workflow 观察报错

预期结果:
  - uses 中的表达式应明确报错：「uses 字段不支持 ${{ }} 表达式」
  - 报错应给出正确写法示例（相对路径或完整 owner/repo/path@ref）
  - 不应出现「action not found」这类误导性报错

验证点:
  - [正向] uses 含表达式时解析阶段明确报错
  - [正向] 报错含「uses」和「expression」关键词
  - [负向] 不应报「Self-hosted 执行机未注册」等误导信息（历史 #68/82）

清理:      fixture
