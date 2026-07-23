用例 ID:   SEC-MASK-01-005
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-027
标题:      ::add-mask:: workflow 命令的正确性与安全性

前置条件:
  - 仓库有正常 workflow 配置
  - 准备动态敏感值用于 mask 注册

操作步骤:
  1. 在 step 中使用 echo '::add-mask::MY_DYNAMIC_SECRET' 注册 mask
  2. 后续 step 中 echo 该动态敏感值 → 验证日志中显示 ***
  3. 注册多个不同 mask 值 → 验证不互相覆盖
  4. 注册 mask 后在跨 step 中 echo → 验证 mask 持续有效

预期结果:
  - ::add-mask:: 注册后，该值在后续所有 step 日志中被遮蔽
  - mask 注册不可逆（不应因 stop-commands 恢复明文）
  - 多个 mask 值独立生效，不互相覆盖或泄露
  - mask 在注册后的所有 step 中持续有效

验证点:
  - [正向] add-mask 后 echo 敏感值 → 显示 ***
  - [负向] 多个 mask 独立生效，不互相覆盖
  - [负向] mask 注册后跨 step 持续遮蔽

清理:      fixture
