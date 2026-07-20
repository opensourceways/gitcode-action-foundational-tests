# 流程定义（process）

本文件定义 Phase 02 的执行流程、门禁、run 生命周期与交付验收（DoD）。命令（`.claude/commands/phase02-*.md`）是这套流程的自动化入口。

---

## 0. 角色与编排机制

- 编排者：Claude Code（主会话）读取本文件与各命令，**调用确定性脚本**执行主链路，**用 Task 工具拉起 agent** 做 LLM 辅助工作。
- 脚本**串行**执行（同一用例的环境准备→编译→触发→采集→断言→清理不可并行）；不同用例之间**可并行**（互不依赖）。
- 关键处设 **STOP**：校验不通过 / 安全事件 / 全量失败率超阈值时暂停，等人工决策。

```
Phase 01 YAML 用例
        │
        ▼
[闸门] /phase02-schema-check ── 拒收清单 → Phase 01
        │
        ▼
[执行] /phase02-exec
        │  逐条用例：
        │  ① 环境准备 (env-manager)
        │  ② YAML 编译 (yaml-compiler agent)
        │  ③ 部署 + 触发 (workflow-runner)
        │  ④ 等待 + 采集 (workflow-runner)
        │  ⑤ 断言判定 (assertion-engine)
        │  ⑥ 落库 (report-builder)
        │  ⑦ 清理 (env-manager)
        │  ⑧ 如需 → 失败分析 (failure-analyst agent)
        ▼
   runs/<run-id>/results/
        │
        ▼
[报告] /phase02-report
        │  分维度聚合 + 回归 diff + flaky 标记 + 门禁判定
        ▼
   reports/<run-id>/report.md
```

---

## 1. 前置：输入校验（命令 `/phase02-schema-check`）

**在任何执行之前**，必须先校验所有输入 YAML：

1. 扫描 `phase01/runs/<run-id>/cases/yaml/` 下所有 `.yaml`/`.yml` 文件
2. 逐条过 `phase01/schema/executable-case.schema.yaml` 校验
3. 通过的用例进入执行队列；不通过的生成拒收清单（格式见 `contract.md` §4.2）

**门禁**：所有进入执行的用例必须通过 schema 校验。不通过的不执行，待 Phase 01 修复后重新运行本命令。

---

## 2. 一次完整执行（命令 `/phase02-exec`）

### 2.1 新建 run

在 `runs/` 下按 `YYYY-MM-DD-NN`（NN 为当日序号）新建 run 目录：

```
runs/<run-id>/
├── run.md                    # 元信息：参数、输入快照、时间线、状态
├── queue.md                  # 执行队列（通过校验的用例清单，按优先级排序）
├── results/<case-id>.md      # 每条用例的完整执行结果
├── summary.json              # 结构化汇总（分维度统计）
└── timeline.md               # 执行时间线
```

`run.md` 记录：
- 触发参数（覆盖哪些维度、并发数、超时上限）
- 输入快照（Phase 01 run-id、YAML 文件 hash 清单）
- 平台配置快照（API base URL、runner 标签等）
- 状态：`running` | `completed` | `aborted`

### 2.2 执行循环（逐条用例）

每条用例按以下链路串行执行：

```
① 环境准备 (env-manager)
   ├─ 读取 setup.repo_fixture → 创建/重置临时仓库
   ├─ 配置 setup.secrets / setup.variables
   ├─ 设置 setup.branch_protection
   ├─ 获得 owner/repo 标识
   └─ 产出：测试仓库上下文 { owner, repo, branch }

② YAML 编译 (yaml-compiler agent)
   ├─ 读用例 YAML 的 workflow: 字段
   ├─ 读 trigger 字段确定文件路径/触发方式
   ├─ 编译为符合 GitCode 规范的 .gitcode/workflows/<name>.yml
   ├─ 处理：事件映射、runner 标签、secrets 引用、表达式适配
   └─ 产出：完整的 GitCode workflow YAML 文件内容

③ 部署 + 触发 (workflow-runner)
   ├─ 将 workflow YAML 写入仓库（git push）
   ├─ 按 trigger.event 选择触发方式：
   │   push → git push 自然触发
   │   pr / fork_pr → 创建 PR（按 trigger.as 切换身份）
   │   manual → 调 API 手动触发
   │   schedule → 配置 cron 等待
   │   tag → 创建 tag 触发
   ├─ 记录 run_id（从 API 响应或 git push 返回获取）
   └─ 产出：GitCode run_id

④ 等待 + 采集 (workflow-runner)
   ├─ 轮询 GET /api/v8/repos/:owner/:repo/actions/runs/:run_id
   ├─ 超时控制（默认 30 min，用例级可覆盖）
   ├─ 状态变为 COMPLETED/FAILED/CANCELED 后：
   │   ├─ 获取 run 详情（状态/结论/耗时）
   │   ├─ 获取 job 列表 + 每个 job 详情
   │   ├─ 下载全量日志
   │   └─ 列出 artifacts
   ├─ 如有 fault_injection：在 at 时机执行注入动作
   └─ 产出：RunResult { status, conclusion, duration, jobs, logs, artifacts }

⑤ 断言判定 (assertion-engine)
   ├─ 逐条 assertions 判定：
   │   positive → 比对 status/产物/退出码
   │   negative → 全文扫描日志（secret 泄露/越权）
   │   nonfunctional → 阈值比对/并发隔离/错误信息
   ├─ 安全用例 extra check：日志中 secret 占位符是否被遮蔽
   ├─ 判定结论：PASS / FAIL / FLAKY / TIMEOUT / ENV_ERROR
   └─ 产出：AssertionResult[] + 总体判定

⑥ 落库 (report-builder 局部)
   └─ 将 RunResult + AssertionResult[] 写入 results/<case-id>.md

⑦ 清理 (env-manager)
   ├─ fixture → 删除临时仓库
   ├─ full_instance → 触发实例全量重置（IaC）
   └─ none → 跳过

⑧ 失败分析（条件触发）
   └─ 若判定为 FAIL → 调 failure-analyst agent 做根因初判
      分类：产品 bug / 用例问题 / 环境问题 / 需人工判断
```

### 2.3 并发控制

- 同维度内用例串行（避免相互干扰）
- 不同维度用例可并行（最多 N 个并发，N 由配置文件指定）
- `full_instance` 级重置的用例独占执行（重置期间无其他用例在跑）

---

## 3. 报告生成（命令 `/phase02-report`）

### 3.1 聚合

从 `runs/<run-id>/results/` 和 `summary.json` 聚合：

1. **执行摘要**：总用例数 / PASS / FAIL / FLAKY / TIMEOUT / ENV_ERROR
2. **分维度通过率**：按 `dimension` 分组统计，对照 Phase 01 quality-gate 逐维度判断
3. **P0 失败高亮**：所有 `priority=P0` 且结果为 FAIL 的用例单独列出
4. **回归 diff**：与上次 run 的 `summary.json` 对比，标出「上版本绿、本版本红」的回归项
5. **Flaky 标记**：重复执行 N 次时绿时红的用例
6. **失败详情**：每条失败用例的日志指纹 + LLM 根因初判
7. **LLM 辅助产出**：易用性评分（`eval: llm_assisted` 断言）、衍生用例建议

### 3.2 门禁判定

对照 Phase 01 `baseline/quality-gate.md` 的分维度阈值：
- 某维度通过率低于阈值 → 该维度 **BLOCKED**
- 任何 P0 失败 → 整体 **BLOCKED**
- 全维度通过 → **GO**

### 3.3 落盘

报告写入 `reports/<run-id>/report.md`，同时更新 `reports/latest/` 软链。

---

## 4. run 目录生命周期与状态

| 状态 | 含义 |
|---|---|
| `queued` | 已创建，等待执行 |
| `running` | 正在执行 |
| `completed` | 执行完成（含部分失败） |
| `aborted` | 人工中止（安全事件/环境故障） |

- **复现**：run 目录自包含（含输入快照、日志、断言详情），任何时候可回看当时的判断依据。
- **增量执行**：可指定维度/优先级过滤，只跑一部分用例。
- **不修改历史**：已完成的 run 不得原地改写；需要变更新开 run。

---

## 5. 查看进度（命令 `/phase02-status`）

聚合当前 run 的 `run.md` + `summary.json` + `timeline.md`，输出快照：
- 当前状态 / 进度（已执行 n/m 条）
- 暂态通过率
- 最近失败的用例及原因
- 预估剩余时间

---

## 6. 交付验收清单（Definition of Done）

- [ ] 所有进入执行的用例通过 schema 校验（拒收清单已回报 Phase 01）
- [ ] 支持 maintainer / untrusted_contributor 两种触发身份
- [ ] 三类断言均可确定性判定；pass/fail 不经 LLM
- [ ] 破坏性用例执行后按声明级别自动重置，无跨用例污染
- [ ] 报告含分维度通过率、门禁判定、回归 diff、flaky 标记
- [ ] LLM 辅助产出均为建议/信号，不参与判定裁决
- [ ] 整套可在 GitCode 发版流水线中自动触发

---

## 7. 门禁一览

| 门禁 | 位置 | 通过条件 |
|---|---|---|
| Schema 校验 | `/phase02-schema-check` 之后 | 所有用例通过校验，无 schema violation |
| 环境就绪 | `/phase02-exec` 启动时 | API token 有效、测试实例可达 |
| 安全事件 | 执行过程中 | 无真实 secret 泄露事件 |
| 失败率阈值 | 全量执行后 | 失败率不超过配置阈值（否则暂停人工判断） |
