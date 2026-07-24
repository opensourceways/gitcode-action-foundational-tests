用例 ID:   COMPAT-RUNSON-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-027
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    COMPAT-RUNSON-01-001
标题:      runs-on 标签体系——单标签字符串应报错

前置条件:
  - 平台 Runner 池正常

操作步骤:
  1. 在工作流中声明 `runs-on: ubuntu-latest`（单标签字符串，非数组）
  2. 触发工作流，观察平台校验行为
  3. 再尝试 `runs-on: default` 等不规范写法

预期结果:
  - 单标签字符串格式不被平台接受
  - 解析阶段应报错，提示必须使用数组格式
  - 明确拒绝后不应静默调度到任意 Runner

验证点:
  - [负向] 单标签字符串格式在解析/校验阶段报错
  - [正向] 错误信息应明确说明需使用数组格式
  - [负向] 不应静默调度到不匹配标签的 Runner

清理:      fixture
