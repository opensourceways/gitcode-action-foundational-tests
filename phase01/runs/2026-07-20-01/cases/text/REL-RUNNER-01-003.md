用例 ID:   REL-RUNNER-01-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-014
标题:      前 job 文件残留不污染后续 job

前置条件: 串行 job A→B，A 写 marker 文件，B 检查
操作步骤: A 创建 /tmp/cross-job-marker → B 检查不存在
预期结果: B workspace 中无 A 残留；B env 中无 A 自定义变量
验证点: [负向] B 看不到 A 的 marker；[负向] B env 无 A 变量
清理: fixture
