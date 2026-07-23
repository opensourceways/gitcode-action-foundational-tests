用例 ID:   COMP-ACT-03-011
维度标签:   [completeness]
维度:      功能完备性
优先级:    P2
溯源意图:  INTENT-ACT-011
母意图:    —
标题:      setup_terraform IaC 工具安装——指定版本/默认版本/不存在版本/terraform init 连通性

前置条件:
  - 仓库配置了 Terraform 安装 workflow
  - Terraform 二进制下载依赖 HashiCorp 官方源

操作步骤:
  1. 配置 workflow 使用 `uses: setup_terraform`，指定 `terraform-version: 1.5.0`
  2. 触发 workflow，在后续 step 中执行 `terraform version` 验证
  3. 不指定 terraform-version，观察默认版本行为
  4. 指定不存在版本（如 `terraform-version: 99.99`），观察报错
  5. 安装后执行 `terraform init`，验证在 GitCode runner 上网络连通性

预期结果:
  - 指定版本 1.5.0 时，`terraform version` 输出确认为 1.5.0
  - 不指定版本时安装合理的默认版本
  - 不存在版本时给出清晰报错
  - `terraform init` 可正常执行（或给出明确的网络错误提示）

验证点:
  - [正向] `terraform version` 输出版本号与指定一致
  - [正向] 默认版本安装成功
  - [正向] 不存在的版本给出可理解的错误信息
  - [状态] 若 HashiCorp 官方源大陆不可达——标记为 blocked-by-network

清理: fixture
