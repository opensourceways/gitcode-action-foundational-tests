用例 ID:   USE-MIGR-02-002
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-015
标题:      runs-on 使用 GitHub 风格标签时的错误信息质量与迁移指引

前置条件:
  - 配置 runs-on: ubuntu-latest（GitHub 格式）

操作步骤:
  1. runs-on: ubuntu-latest → 验证报错指出三标签格式
  2. runs-on: [ubuntu-latest]（数组单标签）→ 同上

预期结果:
  - 报错含标签格式说明
  - 给出 GitCode 可用标签示例
  - 或有文档链接

验证点:
  - [正向] 报错指出格式不匹配
  - [正向] 消息含三段式示例
  - [非功能] 消息可诊断: eval=llm_assisted

清理:      fixture
