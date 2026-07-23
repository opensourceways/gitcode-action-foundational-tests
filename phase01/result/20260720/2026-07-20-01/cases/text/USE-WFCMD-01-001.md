用例 ID:   USE-WFCMD-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-010
标题:      日志中 `::group::` / `::error::` / `::warning::` workflow 命令的实际支持情况

前置条件:
  - GitCode 文档 `workflow-commands.md` 未列出 `::group::`/`::endgroup::` 等命令
  - 但日志界面文档 `view-job-logs.md` 有"折叠"概念

操作步骤:
  1. 在 step 中使用 `echo "::group::My Group"` ... `echo "::endgroup::"`，观察日志折叠效果
  2. 在 step 中使用 `echo "::error file=app.js,line=10::Something wrong"`，观察是否生成 annotation
  3. 在 step 中使用 `echo "::warning::Some warning"`，观察同上
  4. 若平台不支持，验证 step 不应因不识别而失败

预期结果:
  - 若支持：日志应有可视化折叠效果；error/warning 应有 annotation 展示
  - 若不支持：文档需明确说明；不支持的命令不应导致 step 失败
  - 不支持的命令宜在日志中原样输出（不吞掉）

验证点:
  - [正-非功能] ::group:: 是否产生折叠效果（可截图判定）
  - [正-非功能] ::error:: 是否产生 annotation
  - [正-非功能] ::warning:: 是否产生 annotation
  - [负向] 不支持时 step 不应非零退出

清理:      fixture
