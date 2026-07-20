用例 ID:   REL-ENV-HYPHEN-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-049
标题:      env 变量带中划线 '-' 时渲染正确——历史 #38 回归

前置条件:
  - env 定义变量 MY-VAR: hello（含中划线）

操作步骤:
  1. 定义 env: MY-VAR: hello
  2. 在 step 中用 ${{ env.MY-VAR }} 表达式层读取
  3. 验证不触发 bash 替换歧义（不会把 MY-VAR 解析为 MY 减去 VAR）

预期结果:
  - ${{ env.MY-VAR }} 在表达式层正常渲染为 hello
  - 不触发 shell 默认值替换（${MY-VAR} → ${MY}减去${VAR}）

验证点:
  - [正向] 日志输出 hello
  - [负向] 不触发 bash bad substitution

清理:      none
