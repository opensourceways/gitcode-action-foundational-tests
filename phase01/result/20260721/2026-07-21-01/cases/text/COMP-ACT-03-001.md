用例 ID:   COMP-ACT-03-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-ACT-001
母意图:    —
标题:      setup-gradle 安装与版本选择——指定版本/默认版本/不存在版本/后续可用性

前置条件:
  - 仓库配置了使用 `setup-gradle` Action 的 workflow
  - 已知 setup-* 系列版本说明缺失、下载失败频繁 (#50, #98)

操作步骤:
  1. 配置 workflow 使用 `uses: setup-gradle`，指定 `gradle-version: 8.5`
  2. 触发 workflow 运行
  3. 在后续 step 中执行 `gradle --version` 验证版本是否为 8.5
  4. 不指定 gradle-version，观察默认安装版本
  5. 指定不存在版本（如 `gradle-version: 999.0`），观察报错信息

预期结果:
  - 指定版本 8.5 时，`gradle --version` 输出确认为 8.5
  - 不指定版本时，安装合理的默认版本（如最新稳定版）
  - 指定不存在版本时，报错信息清晰指明「版本 999.0 不存在」而非泛化 failure
  - Gradle 在后续 step 中可正常执行

验证点:
  - [正向] `gradle --version` 输出版本号与指定一致
  - [正向] 默认版本安装成功且版本号合理
  - [正向] 不存在的版本给出可理解的错误信息（含版本号和原因）
  - [状态] 若下载失败（已知 #50/#98）——标记为 blocked-by-platform

清理: fixture
