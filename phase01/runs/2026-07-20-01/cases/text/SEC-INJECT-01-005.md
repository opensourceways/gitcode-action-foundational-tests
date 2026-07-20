用例 ID:   SEC-INJECT-01-005
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-014
母意图:    —
标题:      不可信输入注入到 GITHUB_ENV / GITHUB_OUTPUT 文件不导致环境变量污染

前置条件:
  - 仓库配置了 pull_request 触发器
  - 存在一个来自 fork 的 PR，PR 标题含换行符和特殊字符
  - workflow 将不可信输入（PR 标题）写入 ATOMGIT_ENV 文件

操作步骤:
  1. 创建 fork PR，标题设为：`fix\nINJECTED_VAR=malicious_value`
  2. 在 workflow 的 step 中将 `${{ atomgit.event.pull_request.title }}` 写入 `$ATOMGIT_ENV`
  3. 在后续 step 中读取环境变量，检查是否有额外变量被注入
  4. 同样测试写入 `$ATOMGIT_OUTPUT` 文件，检查多行值和特殊字符穿越

预期结果:
  - 写入 ATOMGIT_ENV 的多行值不应导致额外的环境变量被注入
  - 后续 step 读取到的环境变量值 = 写入的原始值（不含注入的额外 KEY=VALUE）
  - 环境变量列表总数应符合预期（无额外注入变量）
  - 写入 ATOMGIT_OUTPUT 的含特殊字符值不应在读取时被二次解释

验证点:
  - [负向] 写入含换行符的不可信值到 ATOMGIT_ENV，不应产生额外环境变量
  - [负向] 后续 step 中 echo $INJECTED_VAR 应为空（该变量不应存在）
  - [正向] 后续 step 读取的正常变量值与写入值一致
  - [负向] ATOMGIT_OUTPUT 写入的特殊字符不应导致二次解释

清理:      fixture
