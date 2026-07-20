用例 ID:   COMP-ACT-03-003
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-ACT-003
母意图:    —
标题:      setup-pnpm 安装与版本选择——指定版本/默认版本/不存在版本/Node.js 兼容性

前置条件:
  - 仓库配置了使用 `setup-pnpm` Action 的 workflow
  - 已知 setup-* 系列版本说明缺失、下载失败频繁 (#50, #98)

操作步骤:
  1. 配置 workflow 使用 `uses: setup-pnpm`，指定 `pnpm-version: 8.x`
  2. 触发 workflow，在后续 step 中执行 `pnpm --version` 验证
  3. 变更 pnpm-version 为 `9.0.0`，验证精确版本安装
  4. 不指定 pnpm-version，观察默认版本行为
  5. 指定不存在版本（如 `pnpm-version: 99.99`），观察报错信息

预期结果:
  - 指定版本 8.x 时，安装 pnpm 8 系最新版本
  - 指定版本 9.0.0 时，`pnpm --version` 输出确认为 9.0.0
  - 不指定版本时，安装合理的默认版本
  - 指定不存在版本时，报错信息清晰

验证点:
  - [正向] `pnpm --version` 输出版本号与指定一致
  - [正向] pnpm 在后续 step 中可正常执行
  - [正向] 不存在的版本给出可理解的错误信息
  - [状态] 若下载失败（已知 #50/#98）——标记为 blocked-by-platform

清理: fixture
