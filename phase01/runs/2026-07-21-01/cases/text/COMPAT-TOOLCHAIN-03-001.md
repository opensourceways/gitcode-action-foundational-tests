用例 ID:   COMPAT-TOOLCHAIN-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-061
标题:      预装工具链版本差异：验证托管 Runner 上的 node/python/go/java 版本矩阵

前置条件:
  - 使用默认托管 Runner（ubuntu-latest, x64, small）

操作步骤:
  1. 执行 node --version 记录预装 Node.js 版本
  2. 执行 python3 --version 记录 Python 版本
  3. 执行 java -version 记录 Java 版本
  4. 执行 go version 记录 Go 版本
  5. 与 GitHub Runner 镜像工具链清单对比

预期结果:
  - 每项工具链版本可观测
  - 与文档声明的预装版本一致
  - 版本差异应在文档中公开（如 setup-jdk 不支持 Java 21）

验证点:
  - [正向] 每种语言工具链版本可观测
  - [正向] 预装版本与文档声明一致
  - [正向] 文档应公开 Runner 镜像预装工具版本矩阵

清理:      fixture
