用例 ID:   COMP-ACT-03-002
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-ACT-002
母意图:    —
标题:      setup-yarn 安装与版本选择——指定版本/默认版本/不存在版本/Node.js 兼容性

前置条件:
  - 仓库配置了使用 `setup-yarn` Action 的 workflow
  - 已知 setup-* 系列版本说明缺失、下载失败频繁 (#50, #98)

操作步骤:
  1. 配置 workflow 先 `uses: setup-node`（Node.js 18），再 `uses: setup-yarn`，指定 `yarn-version: 1.22.19`
  2. 触发 workflow，在后续 step 中执行 `yarn --version` 验证
  3. 变更 yarn-version 为 `3.x`，验证 Yarn 3+ 在 Node.js 18 上是否正常
  4. 不指定 yarn-version，观察默认版本（Yarn 1.x 经典版 vs 3.x）
  5. 指定不存在版本（如 `yarn-version: 99.99`），观察报错信息

预期结果:
  - 指定版本 1.22.19 时，`yarn --version` 输出确认为 1.22.19
  - Yarn 3.x 在 Node.js 18 上可正常安装和使用
  - 不指定版本时，安装合理的默认版本
  - 指定不存在版本时，报错信息清晰

验证点:
  - [正向] `yarn --version` 输出版本号与指定一致
  - [正向] Yarn 3+ 与 Node.js 16+ 兼容
  - [正向] 不存在的版本给出可理解的错误信息
  - [状态] 若下载失败（已知 #50/#98）——标记为 blocked-by-platform

清理: fixture
