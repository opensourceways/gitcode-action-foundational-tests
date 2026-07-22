用例 ID:   USE-ERR-MSG-02-003
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-006
标题:      上下文对象命名差异 github.* vs atomgit.* 的错误信息可诊断性

前置条件:
  - 在 workflow 中使用 ${{ github.ref }} / ${{ github.event_name }}

操作步骤:
  1. ${{ github.ref }} → 验证报错提示用 atomgit.ref
  2. ${{ github.event_name }} → 同上
  3. ${{ github.workspace }} → 同上

预期结果:
  - 报错指出 github 上下文不被识别
  - 消息暗示替换为 atomgit

验证点:
  - [正向] 报错发生
  - [正向] 消息含 github 不识别
  - [非功能] 暗示原子 atomgit 替换: eval=llm_assisted

清理:      fixture
