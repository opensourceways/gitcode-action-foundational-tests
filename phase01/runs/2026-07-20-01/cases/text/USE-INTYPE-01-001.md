用例 ID:   USE-INTYPE-01-001
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-018
标题:      `workflow_dispatch.inputs` 使用 GitHub 支持的非 string 类型时的行为与报错

前置条件:
  - GitCode inputs 仅支持 `string` 类型，GitHub 支持 boolean/choice/number/environment

操作步骤:
  1. 配置 `workflow_dispatch.inputs.dry_run.type: boolean`，手动触发
  2. 配置 `type: number`，手动触发
  3. 配置 `type: choice`，手动触发
  4. 观察每种情况：是报错还是当 string 静默处理？
  5. 若静默处理：验证 `default: true` 是否变成字符串 "true"，表达式 `inputs.dry_run == true` 是否因类型不匹配静默失败

预期结果:
  - 平台应明确报错，指出不支持的类型
  - 应提示 GitCode 仅支持 `string` 类型

验证点:
  - [正-非功能] type: boolean 时报错且提示仅支持 string
  - [正-非功能] type: number 时报错同上
  - [正-非功能] type: choice 时报错同上
  - [负向] 不应静默将非 string 类型当 string 处理（若静默，需验证表达式行为）

清理:      fixture
