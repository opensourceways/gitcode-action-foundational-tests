用例 ID:   COMPAT-DEF-SHELL-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-014
标题:      默认值差异：验证 defaults.run.shell 与默认 permissions 行为是否与 GitHub 对齐

前置条件:
  - workflow 中未显式指定 defaults.run.shell
  - workflow 中未显式声明 permissions

操作步骤:
  1. 创建不含 defaults.run.shell 的 workflow，验证 run step 默认使用的 shell
  2. 验证 `run: exit 1` 是否因 bash -e 导致 step 标记失败
  3. 验证未声明 permissions 时 ATOMGIT_TOKEN 的实际权限范围
  4. 验证 defaults.run.working-directory 默认为 $ATOMGIT_WORKSPACE

预期结果:
  - 未指定 shell 时默认使用 bash 且行为与 bash -e {0} 一致
  - exit 1 导致 step 标记 failure
  - ATOMGIT_TOKEN 默认权限可观测并文档化
  - 工作目录默认为 workspace

验证点:
  - [正向] 未指定 shell 时 step 在 bash 中执行
  - [正向] run: exit 1 导致 step failure（bash -e 行为）
  - [正向] 未声明 permissions 时 ATOMGIT_TOKEN 权限范围可观测
  - [负向] 不应在 sh/dash 等非预期 shell 中执行

清理:      fixture
