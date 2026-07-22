用例 ID:   SEC-REFPROT-02-001
维度标签:   [security, completeness]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-037
标题:      保护分支上下文标志 atomgit.ref_protected 的可用性与正确性

前置条件:
  - 目标仓库存在已配置分支保护或规则集的分支（如 main）
  - 同时存在未配置保护的分支（如 feature/test）
  - 工作流中配置了基于 atomgit.ref_protected 的条件门控

操作步骤:
  1. 在保护分支（main）上 push 触发工作流
  2. 在未保护分支（feature/test）上 push 触发工作流
  3. 分别观测两种触发场景下 atomgit.ref_protected / ATOMGIT_REF_PROTECTED 的求值结果
  4. 检查基于该标志的 job 条件门控是否按预期执行或跳过

预期结果:
  - 保护分支触发时，atomgit.ref_protected 与 ATOMGIT_REF_PROTECTED 均求值为 true
  - 未保护分支触发时，该标志求值为 false
  - 基于 if: atomgit.ref_protected == true 的部署 job 在非保护分支上被跳过

验证点:
  - [正向] 保护分支运行日志中标志值为 true，条件门控 job 被执行
  - [负向] 未保护分支上该标志不应求值为 true；保护分支上的值不应因缓存或并发而错误为 false
  - [负向] 基于保护分支的安全门控不应被非保护分支绕过
  - [非功能] 标志值在 job 级 if 条件求值时即已确定，不因运行过程中保护策略变更而改变

清理:      fixture
