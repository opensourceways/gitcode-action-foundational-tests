用例 ID:   USE-LBL-01-002
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-025
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      runs-on 标签因容量不足排队时应提示排队状态而非无可用 runner

前置条件:
  - 仓库有匹配的 runner 但当前无空闲资源

操作步骤:
  1. 触发一个使用正确标签但需要等待的 workflow

预期结果:
  系统提示当前无空闲 Runner，正在排队，而非报无可用 runner

验证点:
  - [非功能] 状态或日志中是否出现排队/等待字样
  - [非功能] 错误信息是否区分无匹配与容量不足

清理:      无

