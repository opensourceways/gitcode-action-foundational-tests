用例 ID:   USE-INPT-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-008
母意图:    —
标题:      使用 boolean 类型 input 时报错应提示仅支持 string

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 声明 workflow_dispatch inputs 的 type: boolean

预期结果:
  YAML 校验报错，明确说明 GitCode 仅支持 string 类型，并给出转换指引

验证点:
  - [负向] 不应静默降级为 string
  - [非功能] 报错中应包含 string 与类型转换相关提示

清理:      无

