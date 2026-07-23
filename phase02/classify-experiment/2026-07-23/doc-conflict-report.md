# 9 INVALID Cases — Doc vs Platform Conflict Analysis

**数据源**: `phase02/classify-experiment/2026-07-23/INVALID/` (9 cases)
**校验时间**: 2026-07-23
**对照文档**: `phase01/inputs/gitcode-spec/` (GitCode 官方参考文档)

## Summary

| 冲突类型 | Cases | 说明 |
|----------|-------|------|
| **文档暗示支持但平台拒绝** | 3 | stages array、post.steps、post.run_always — doc 有示例但平台报 unknown property |
| **文档完全未提及限制** | 3 | steps ≤16、paths ≤32、preemption events 仅 `mr_id` — 无文档覆盖 |
| **case 用错语法** | 2 | failure() 应为 failed、schedule object 应为 array |
| **非 doc 问题** | 1 | uses 格式正确但引用文件不存在 |

---

## 逐 Case 分析

### 1. COMP-STAGES-01-001 — stages array→map

- **错误**: `Cannot deserialize Map from Array — stages`
- **官方文档** (`configure-dependencies-order.md`):
  - 同时展示了两种格式：
    - **array**: `stages:\n  - name: build-stage\n    jobs:\n ...`
    - **map**: `stages:\n  build_stage:\n    name: 构建\n    jobs:\n ...`
  - **未声明** array 不可用
- **平台实际**: 只接受 map 格式，拒绝 array
- **结论**: 📛 **文档误导** — 两种格式都给了示例，但只支持一种

### 2. COMP-STAGES-01-003 — post.steps / post.run_always unknown

- **错误**: `post.steps: unknown property` / `post.run_always: unknown property`
- **官方文档** (`core-concepts/workflow-job-step-action.md`):
  - "Post 后处理阶段是 AtomGit Action 的特殊 Stage 类型"
  - "在流水线达到终态后执行，默认 `run_always: true`"
  - "适合用于通知、清理、报告等收尾操作"
  - 甚至 `workflow-file-location-structure.md` 列出了 `post` 字段
- **平台实际**: 拒绝 `post.steps` 和 `post.run_always`，报 unknown property
- **结论**: 📛 **文档误导** — 文档描述了完整功能，但平台校验器不支持

### 3. COMPAT-PATHS-01-001 — paths 超限

- **错误**: `on.push.paths: 列表长度超出限制 — 总和不能小于1或超过32`
- **官方文档** (`configure-triggers.md`):
  - "paths 匹配前 **300** 个变更文件，超出部分不参与匹配判断"
  - **未提及** paths 数量限制为 32
- **平台实际**: paths 条目数 ≤32
- **结论**: ⚠️ **文档缺失** — 300 文件匹配上限 vs 32 条目限制是两个不同概念，但 doc 只写了 300

### 4. COMPAT-SCHEDULE-01-001 — schedule 格式

- **错误**: `Cannot deserialize ArrayList from Object — on.schedule`
- **官方文档** (`configure-triggers.md` / `trigger-events.md`):
  - **一致使用 array 格式**: `schedule:\n    - cron: "0 2 * * *"`
- **平台实际**: 要求 array 格式
- **结论**: ✅ **case 写错** — doc 正确，case 用了 GitHub Actions 的单对象格式 `schedule: {cron: ...}`

### 5. REL-PREEMPT-01-005 — preemption events 非法值

- **错误**: `concurrency.preemption.events: [push] 不在允许值中，允许值: [mr_id]`
- **官方文档** (`workflow-file-location-structure.md`):
  - 示例只有 `events: [mr_id]`
  - 说 "限制只能配置**不超过10个**"
  - **未枚举** 允许的事件值
- **平台实际**: 仅 `mr_id` 合法
- **结论**: ⚠️ **文档缺失** — 说"不超过10个"暗示有多种值可选，实际只有一个

### 6. REL-RACE-01-048 — failure() 不支持

- **错误**: `if表达式无法解析 — failure()第1位出现不支持的函数`
- **官方文档** (`configure-conditional-execution.md`):
  - GitCode 用 **`failed`** (无括号): `if: ${{ failed }}`
  - GitHub 用 **`failure()`** (带括号)
  - `COMPAT-NOTES.md` 明确注明差异: "GitCode 的失败函数名为 `failed`，GitHub 为 `failure()`"
- **平台实际**: 不支持 `failure()`
- **结论**: ✅ **case 用错语法** — 应使用 `${{ failed }}` 而非 `${{ failure() }}`

### 7. REL-STAGES-01-029 — stages array→map

- **错误**: 同 #1
- **结论**: 同 #1 — 📛 **文档误导**

### 8. REL-STEPS-01-042 — steps 超限

- **错误**: `jobs[test].steps: 列表长度必须在0到16之间`
- **官方文档** (`configure-steps.md`):
  - **未提及** 任何 step 数量限制
  - 搜索全部 spec 文件：无 `step.*limit` / `max.*steps` / `steps.*16` 匹配
- **平台实际**: 单 job 最多 16 个 step
- **结论**: ⚠️ **文档完全未覆盖** — 一个重要的硬限制没有任何文档记录

### 9. USE-NEST-02-001 — workflow call 文件不存在

- **错误**: `uses: 格式错误` / `插件 ./.gitcode/workflows/reusable-level1.yml 不存在`
- **官方文档** (`trigger-events.md`):
  - 支持 `uses: ./.gitcode/workflows/xxx.yml` 格式
- **平台实际**: 校验器通过 uses 格式，但引用的 workflow 文件在仓库中不存在
- **结论**: ➖ **非 doc 问题** — uses 格式合规，运行时缺少目标文件

---

## 待修正的 Doc Gaps

| # | Gap | 影响 | 建议 |
|---|-----|------|------|
| 1 | `stages` 文档同时展示 array/map，实际只支持 map | case-writer 可能选错格式 | 删除 array 示例，标注 "stages 只支持 map 格式" |
| 2 | `post` 文档描述了 post.steps/run_always，平台不支持 | case-writer 会使用不存在的字段 | 标注 "平台暂不支持 post.steps"，或从文档移除 |
| 3 | steps 数量限制 ≤16 完全未文档化 | case-writer 会创建超量 step | `configure-steps.md` 添加限制说明 |
| 4 | preemption.events 只写 "不超过10个"，未列出允许值 `[mr_id]` | case-writer 可能尝试其他事件 | 添加允许值枚举 |
