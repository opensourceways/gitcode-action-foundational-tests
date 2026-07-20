用例 ID:   SEC-INJECT-03-005
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-014
母意图:    —
标题:      不可信输入注入到 ATOMGIT_ENV/ATOMGIT_OUTPUT 文件不导致环境变量污染

前置条件:
  - workflow 从 PR 标题获取不可信输入
  - 将不可信输入写入 ATOMGIT_ENV（通过 set-env 或直接 echo）
  - 将不可信输入写入 ATOMGIT_OUTPUT

操作步骤:
  1. 构造含换行符+环境变量定义（如 `FOO=bar\nMALICIOUS=evil`）的 PR 标题
  2. 将 PR 标题写入 ATOMGIT_ENV 文件
  3. 后续 step 读取环境变量，检查是否有多余变量被注入
  4. 同样针对 ATOMGIT_OUTPUT 验证

预期结果:
  - ATOMGIT_ENV 写入协议应对值做安全处理
  - 多行值不导致额外环境变量被注入
  - ATOMGIT_OUTPUT 含特殊字符的值在后续 step 不被二次解释

验证点:
  - [负向] 后续 step 不应出现 MALICIOUS=evil 环境变量
  - [负向] ATOMGIT_OUTPUT 中的特殊字符不触发命令替换
  - [正向] 写入的原始值可通过标准方式读取（单行）

清理: fixture
