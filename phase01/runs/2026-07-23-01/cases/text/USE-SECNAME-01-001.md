用例 ID:   USE-SECNAME-01-001
维度标签:   ['usability', 'security']
维度:      usability/security
优先级:    P1
溯源意图:  INTENT-USE-028
母意图:    —
标题:      Secret 名称以 ATOMGIT_ 开头时应给出命名规则错误

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 workflow 中引用 ${{ secrets.ATOMGIT_TOKEN }}

预期结果:
  系统在校验或运行时给出明确的命名规则提示，区分名称违规与未配置

验证点:
  - [负向] 不应仅报 Secret not found
  - [非功能] 报错中是否包含 Secret 名称规则、大写字母/数字/下划线、不得以 ATOMGIT_ 开头等提示

清理:      无

