用例 ID:   COMPAT-DOCKER-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-044
标题:      Docker daemon 在托管 Runner 上的可用性——历史 #86

前置条件:
  - 使用托管 Runner（ubuntu-latest, x64, small）

操作步骤:
  1. 在 step 中执行 docker ps 检查 daemon 连接
  2. 执行 docker info 获取 daemon 信息
  3. 若 daemon 不可用，记录报错信息质量

预期结果:
  - 若有 Docker daemon：docker ps 返回容器列表
  - 若无 daemon：明确报错「Cannot connect to the Docker daemon」
  - 文档应明确声明托管 Runner 的 Docker 支持状态

验证点:
  - [正向] docker ps 执行结果可观测（有 daemon 或明确报错）
  - [正向] 文档声明 Docker daemon 可用性状态
  - [负向] 不应 Docker CLI 安装但 daemon 不可用且报错不明确

清理:      fixture
