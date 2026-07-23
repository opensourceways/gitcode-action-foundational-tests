用例 ID:   COMPAT-PATH-300-03-001
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-033
标题:      paths 过滤 300 文件上限边界：变更 301 个文件时第 301 个不触发

前置条件:
  - workflow 配置 paths: src/** 过滤
  - 准备一次大 commit 变更 300+ 文件

操作步骤:
  1. 创建 workflow 配置 on.push.paths: [src/**]
  2. 提交变更：299 个占位文件（docs/*.txt）+ src/trigger.txt 在第 301 位置
  3. 观察 workflow 是否触发
  4. 对比：将 src/trigger.txt 放在前 300 内，验证触发

预期结果:
  - src/trigger.txt 在第 301 位置时不触发（超出 300 扫描范围）
  - src/trigger.txt 在前 300 内时正常触发
  - 文档应明确标注 300 文件上限（vs GitHub 3000）

验证点:
  - [正向] 匹配文件在前 300 内时触发
  - [正向] 匹配文件在第 301+ 时不触发（边界行为明确）
  - [负向] 不应因超限导致全部跳过或全部触发

清理:      fixture
