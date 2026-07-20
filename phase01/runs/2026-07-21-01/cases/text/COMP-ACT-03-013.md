用例 ID:   COMP-ACT-03-013
维度标签:   [completeness]
维度:      功能完备性
优先级:    P2
溯源意图:  INTENT-ACT-013
母意图:    —
标题:      paths_filter 路径过滤——glob pattern/多 pattern 组合/if 条件联动/否定 pattern

前置条件:
  - 仓库配置了路径过滤 workflow
  - 仓库中有不同目录结构的源文件

操作步骤:
  1. 配置 workflow 使用 `uses: official_paths_filter`，指定 filter pattern `src/**`
  2. 提交仅变更 `src/main.js` 的 commit，触发 workflow，验证过滤结果命中
  3. 提交仅变更 `docs/README.md` 的 commit，验证过滤结果未命中
  4. 指定多个 pattern（如 `src/**, tests/**`），验证 OR 语义
  5. 在后续 step 中使用 `if` 条件判断过滤结果控制执行
  6. 测试否定 pattern（如 `!docs/**`），观察是否支持
  7. 测试 glob 边界（`**/*.js`、`*.md`、单文件路径）

预期结果:
  - 变更文件命中 pattern 时正确输出过滤结果
  - 变更文件未命中 pattern 时正确标记为未变更
  - 多 pattern OR 语义正确
  - `if` 条件可正确使用过滤结果控制 step 执行
  - 否定 pattern 行为明确（支持或报错）

验证点:
  - [正向] 命中 pattern 时过滤结果正确
  - [正向] 未命中 pattern 时过滤结果正确
  - [正向] 多 pattern OR 语义符合预期
  - [正向] `if` 条件联动 step 执行正确
  - [状态] 若否定 pattern 不支持——标记为 known-limitation

清理: fixture
