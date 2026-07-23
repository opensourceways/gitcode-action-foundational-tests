用例 ID:   COMPAT-YML-CACHE-03-001
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-092
标题:      YML 缓存未更新：子 workflow 修改后仍执行旧代码——历史 #85 回归验证

前置条件:
  - 创建主 workflow 通过 workflow_call 调用子 workflow
  - 子 workflow 输出 "v1"

操作步骤:
  1. 创建主 workflow A 调用子 workflow B（B 输出 echo "v1"）
  2. 首次触发 A，确认 B 输出 "v1"
  3. 修改子 workflow B 输出 echo "v2"
  4. 再次触发 A，观察 B 的输出是 "v1" 还是 "v2"

预期结果:
  - B 应输出 "v2"（最新版本）
  - 不应缓存旧 YML 导致输出 "v1"（历史 #85 已知 bug）
  - 若存在缓存：日志应标注被调用 workflow 的版本/SHA

验证点:
  - [正向] 修改子 workflow 后再次调用体现新行为
  - [负向] 不应输出旧版本内容
  - [正向] 若缓存存在应有版本标注

清理:      fixture
