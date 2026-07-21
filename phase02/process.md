# 流程定义（process）

本文件定义 Phase 02 的执行流程、门禁、run 生命周期与交付验收（DoD）。命令（`.claude/commands/phase02-*.md`）是这套流程的自动化入口。

---

## 0. 角色与编排机制

- 编排者：Claude Code（主会话）读取本文件与各命令，**调用确定性脚本**执行主链路，**用 Task 工具拉起 agent** 做 LLM 辅助工作。
- 脚本**串行**执行（同一用例的检查→触发→采集→断言→清理不可并行）；不同用例之间**可并行**（互不依赖）。
- 关键处设 **STOP**：校验不通过 / 安全事件 / 全量失败率超阈值时暂停，等人工决策。
- ★ 边界：**编写 workflow 归 Phase 01**；Phase 02 只**检查 + 执行**，不编译/不改写 workflow。

```
Phase 01 YAML 用例（含 Phase 01 编写的可运行 workflow）
        │
        ▼
[闸门] /phase02-schema-check ── 拒收清单 → Phase 01
        │
        ▼
[执行] /phase02-exec
        │  逐条用例（run_case.py，读契约的 workflow 原样执行）：
        │  ① workflow 合规检查 (preflight_validate + 可选 yaml-compiler 检查器)
        │       └─ 不合规 → COMPILE_ERROR，不 push，回报 Phase 01
        │  ② 部署 + 触发 (workflow_runner)
        │  ③ 等待 + 采集（v8 download_log zip） (workflow_runner)
        │  ④ 断言判定 (assertion_engine, §11)
        │  ⑤ 落库 (run_case)
        │  ⑥ 清理 teardown：删本次 push 的 workflow 文件 (workflow_runner)
        │  ⑦ 如需 → 失败根因初判 (failure-analyst 子 agent)
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

> ★ 由 `run_case.py` 编排；workflow 直接取自 Phase 01 契约的 `workflow:` 字段（Phase 02 不编译/不改写）。

```
① workflow 合规检查 (preflight_validate；可选 yaml-compiler 检查器)
   ├─ 取契约的 workflow: 字段（Phase 01 编写的可运行 workflow）
   ├─ 本地确定性检查：on: 映射形式、run: 冒号、runs-on 数组、step name、steps≤16、vars.* 等
   ├─ 不合规 → 判 COMPILE_ERROR，不 push，回报 Phase 01（不代改）
   └─ (可选) 加载断言绑定 sidecar compiled/<id>.asserts.json（rubric→kind+夹具明文）

② 部署 + 触发 (workflow_runner)
   ├─ 将契约 workflow 原样写入 .gitcode/workflows/<case-id>.yml（git push）
   ├─ 按 trigger.event 触发（当前主支持 push；pr/fork_pr/manual/schedule 待扩展）
   └─ 产出：本次 push 的 head_sha + 文件名（用于精确匹配 run）

③ 等待 + 采集 (workflow_runner)
   ├─ 轮询 /actions/runs，按 (head_sha AND file_path) **精确匹配**本次 run（共享仓防抓错）
   ├─ 超时控制（默认 300s，用例级可覆盖）
   ├─ 终态后：list_jobs（stages.jobs[].id）取 job/step 状态 + v8 download_log(zip) 取日志正文
   └─ 产出：RunResult { status, conclusion, jobs[], logs, ... }

④ 断言判定 (assertion_engine, §11)
   ├─ 逐条判定：mask/leak/value/status/run_status/config_probe（确定性，LLM 不参与）
   ├─ 假绿守卫：无 job/step 或空日志不得判 PASS
   └─ 产出：verdict ∈ §11 枚举 + assertion_results[]

⑤ 落库 (run_case)
   └─ 写 results/<case-id>.json + .md；合并 summary.json；更新 state.json（供 status 中途查看）

⑥ 清理 teardown (workflow_runner)
   ├─ fixture / full_instance → 删除本次 push 的 workflow 文件并 push（防仓库污染）
   └─ none → 保留

⑦ 失败归因（条件触发，LLM 辅助，不改判定）
   └─ 若 FAIL → 派 failure-analyst 子 agent 根因初判
      分类：产品缺陷 / 用例问题 / 环境问题 / 文档缺口（以 GitCode 文档为准绳）
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
