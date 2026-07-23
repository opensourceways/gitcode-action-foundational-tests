用例 ID:   COMPAT-SETUP-STAR-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-050
母意图:    —
标题:      setup-* action 差异——setup-node/python/java/go 的 version/cache 参数与版本解析

前置条件:
  - runner 预装对应 setup action

操作步骤:
  1. 使用 setup-node 与 setup-python 安装指定版本
  2. 测试 cache 参数是否生效

预期结果:
  - 指定版本应正确安装
  - cache 参数应加速后续运行

验证点:
  - [正向] node/python 版本与声明一致
  - [nonfunctional] cache 参数生效

清理:      重置 fixture 仓库
