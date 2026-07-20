用例 ID:   COMPAT-FAIL-FN-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-011
标题:      failed vs failure() 命名差异：验证 GitCode 失败函数名与 GitHub 不同且无括号

前置条件:
  - workflow 中定义两个 job：故意失败的 job-A 和依赖 job-A 的 job-B
  - job-B 的 if 条件使用不同的失败检查写法

操作步骤:
  1. 配置 job-A 执行 exit 1，job-B 使用 if: ${{ failed }}（GitCode 风格）
  2. 再创建一个 workflow 使用 if: ${{ failure() }}（GitHub 风格）
  3. 分别触发两个 workflow，观察 job-B 的执行情况

预期结果:
  - if: ${{ failed }} → job-B 应在 job-A 失败后执行（GitCode 无括号语法正确生效）
  - if: ${{ failure() }} → 应明确报错（解析阶段或运行时），报错应指出「应使用 failed 而非 failure()」
  - 报错信息应包含可操作的替换指引

验证点:
  - [正向] ${{ failed }} 在 job-A 失败后使 job-B 执行
  - [负向] ${{ failure() }} 不应被静默接受为 falsy 导致 job-B 跳过
  - [正向] failure() 报错信息应指向「去掉括号 + 将 failure 改为 failed」

清理:      fixture
