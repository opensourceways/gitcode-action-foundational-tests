# Completeness Supplement · Run 2026-07-21-02

> 产出 Agent：spec-analyst（完备性 agent）
> 任务：Phase 01 增量更新——针对 BLIND-02/03/10 发散 test intent
> 前提：已有 INTENT-COMP-001~008，本补充从 COMP-009 起编
> 纪律：不修改已有 intent 文件；停在意图层，不写 GitCode 具体语法

---

```
意图 ID:    INTENT-COMP-009
维度标签:   [completeness, security]
标题:       验证 job 级 container 自定义镜像执行能力（含私有镜像认证）

风险点:     BLIND-02 — 文档声明支持 container 字段（image/credentials/env/volumes/options），但历史 TC-273 FAIL（容器能力不可用），且本轮无 intent 覆盖容器实际执行与私有镜像认证。若平台已修复但未被验证，或仅部分字段生效（如 image 可用但 credentials/volumes/options 被忽略），将导致用户在迁移后遭遇静默行为差异或私有镜像拉取失败。
预期系统行为: 配置 container.image 后，job 应在指定容器内执行步骤；container.credentials 引用的 secret 应被用于私有镜像仓库认证；container.env 应注入容器环境；container.volumes 应正确挂载；container.options 应传递至容器运行时。任一字段不生效或认证失败时，应给出明确报错而非静默回退到宿主机 Runner。
Oracle 来源: GitCode规格（configuring-images-toolchains.md:9-52；C-RUN-09/10）

验证要点:
  - [正向] 配置公共镜像后，job 内步骤执行的文件系统/工具链与镜像声明一致（可通过镜像特有路径或预装命令验证）。
  - [正向] 配置私有镜像 + credentials 引用 secret 后，平台能成功认证并拉取镜像，job 正常执行。
  - [负向] 私有镜像配错 credentials 时不应静默回退到默认 Runner 环境，应给出镜像拉取失败的明确报错。
  - [负向] 不存在的镜像地址不应无限挂起，应在合理超时后报错。
  - [非功能] 容器启动/镜像拉取日志应可被观测，错误信息需指明是镜像问题还是认证问题。

负向断言目标: 容器不可用时绝不静默回退到宿主机执行；判定证据=步骤输出中应出现镜像环境特有标识（如特定文件路径或预装软件版本），若与宿主机 Runner 一致则视为未生效。
优先级线索: BLIND-02 高严重度；关联 C-RUN-09/10。
来源输入: inputs/gitcode-spec/runner-management/configuring-images-toolchains.md（fetched 2026-07-20）；baseline/case-base-detail.md TC-273（FAIL：容器能力不可用）
```

```
意图 ID:    INTENT-COMP-010
维度标签:   [completeness, compatibility]
标题:       验证 matrix include 向已有组合追加额外变量及新增组合的正确展开

风险点:     BLIND-03 — 文档声明 include 可「向现有矩阵追加特定组合或为特定组合添加额外变量」，但本轮仅 REL-010 覆盖组合数上限探测，include 的追加语义（基础矩阵已存在组合 vs 全新组合、追加变量注入正确性）无 intent。GitHub Actions 的 include 语义有明确规则（如未在基础矩阵定义的变量会被追加），GitCode 若实现不一致将导致迁移后矩阵 job 缺少变量或生成错误实例数。
预期系统行为: include 中匹配基础矩阵维度的项应为对应组合追加额外变量；include 中定义全新维度值的项应生成新的 job 实例；追加后的变量应在 job 步骤内可访问且值正确；总实例数 = 基础矩阵笛卡尔积实例数 + 新增组合数 - 被排除数。
Oracle 来源: GitCode规格（configure-matrix-builds.md:78-92；C-EXEC-16）

验证要点:
  - [正向] 基础矩阵 os×version 生成 4 个实例，include 为其中 1 个现有组合追加 experimental=true，该实例应能读取 experimental 且其他实例无此变量。
  - [正向] include 引入全新组合（如基础矩阵没有的 os 值），应生成额外 job 实例且该实例变量完整。
  - [负向] include 追加的变量不应泄漏到不匹配的基础矩阵实例中。
  - [非功能] 矩阵展开后的各实例 job 名/日志应能区分，便于用户识别 include 追加的实例。

对齐方向:   一致性（GitCode 声明与 GitHub 语义一致处应保持对齐；若有意不同需差异确认）
优先级线索: BLIND-03 中严重度；关联 C-EXEC-16。历史基底 TC-327 覆盖基础 include，本 intent 补「追加变量」与「全新组合」语义。
来源输入: inputs/gitcode-spec/writing-pipelines/configure-matrix-builds.md（fetched 2026-07-20）；baseline/case-base-detail.md TC-327
```

```
意图 ID:    INTENT-COMP-011
维度标签:   [completeness, compatibility]
标题:       验证 matrix exclude 排除特定组合后剩余组合的正确性

风险点:     BLIND-03 — 文档声明 exclude 可从矩阵中排除特定组合，历史 TC-328 覆盖基础 exclude，但本轮无 intent 深入验证「排除后剩余组合是否完整、无遗漏、无多生成」。若平台 exclude 实现有 bug（如仅排除第一个匹配项、或条件匹配过于宽松导致误排），将直接影响 CI 覆盖率——用户以为某些环境已测试，实际被静默跳过。
预期系统行为: exclude 中指定的维度值组合应被精确移除，不生成对应 job 实例；其余未匹配组合应全部保留并正常展开；多个 exclude 项应各自独立生效；极端情况下 exclude 全部组合时应产生 0 实例或有明确报错（而非不可预期行为）。
Oracle 来源: GitCode规格（configure-matrix-builds.md:94-108；C-EXEC-17）

验证要点:
  - [正向] 二维矩阵 2×3=6 个实例，exclude 其中 1 个特定组合，剩余 5 个实例全部生成且变量正确。
  - [正向] 多个 exclude 项（排除 2 个不同组合）同时生效，剩余 4 个实例正确。
  - [负向] 被排除的组合绝不应出现在运行记录中；判定证据=运行详情中该组合的 job 实例数为 0。
  - [负向] exclude 条件与基础矩阵不完全匹配时（如 exclude 中仅写 os 未写 version），不应误排所有该 os 的实例——需确认平台是精确匹配还是部分匹配。
  - [非功能] 矩阵展开结果应在运行详情中可枚举，便于人工核对实例数。

对齐方向:   一致性（GitHub exclude 为精确全匹配；GitCode 若部分匹配则需差异确认）
优先级线索: BLIND-03 中严重度；关联 C-EXEC-17。历史基底 TC-328 覆盖基础 exclude，本 intent 补「精确性」与「多 exclude 叠加」语义。
来源输入: inputs/gitcode-spec/writing-pipelines/configure-matrix-builds.md（fetched 2026-07-20）；baseline/case-base-detail.md TC-328
```

```
意图 ID:    INTENT-COMP-012
维度标签:   [completeness, compatibility]
标题:       验证 matrix 动态 runs-on——不同组合是否调度到对应 Runner 标签

风险点:     BLIND-03 — 文档声明 runs-on 可引用 matrix 变量动态选择 Runner（C-EXEC-20），但此能力与 include/exclude 结合时的调度行为未验证。若矩阵某组合的动态 runs-on 指向不存在的 Runner 标签，平台应明确失败；若平台静默跳过或挂起，将导致 CI 假阴性（用户以为测试通过，实际未执行）。此外，不同组合被调度到不同 OS/架构 Runner 上时，环境差异可能导致步骤命令不兼容，需确认平台是否允许并正确处理。
预期系统行为: 矩阵各实例的 runs-on 经 matrix 变量求值后，应调度到与求值结果匹配的 Runner；无匹配 Runner 时应给出明确、可理解的调度失败报错，而非无限排队或静默跳过；调度结果应与矩阵实例一一对应，无串扰。
Oracle 来源: GitCode规格（configure-matrix-builds.md:131-143；C-EXEC-20）

验证要点:
  - [正向] 矩阵含 ubuntu-latest/windows-latest 两值，runs-on 引用 matrix.os，两实例分别调度到对应 OS 的 Runner 并成功执行。
  - [正向] include 追加的全新组合含有效 os 值，该实例也能正确调度。
  - [负向] 矩阵某组合 runs-on 求值后指向不存在的 Runner 标签，不应无限排队，应在合理时限内给出调度失败报错。
  - [负向] 不同实例不应被调度到同一 Runner 后互相覆盖环境（验证隔离性）。
  - [非功能] 调度失败时错误信息应指明「无匹配 Runner」而非泛化失败，便于用户修正标签。

对齐方向:   一致性（GitHub Actions 动态 runs-on 行为一致）
优先级线索: BLIND-03 中严重度；关联 C-EXEC-20。与 REL-010（组合数上限）互补：REL-010 测规模，本 intent 测调度正确性。
来源输入: inputs/gitcode-spec/writing-pipelines/configure-matrix-builds.md（fetched 2026-07-20）
```

```
意图 ID:    INTENT-COMP-013
维度标签:   [completeness, usability]
标题:       验证 atomgit.actor 存在性与上下文种类数一致性（12 种声明 vs 实际表）

风险点:     BLIND-10 — G-28/G-29 记录两处文档矛盾：(1) `atomgit.actor`/`atomgit.actor_id` 被日志页示例引用，但 context.md 的 atomgit 属性表未列出；(2) 上下文总览正文声明「12 种上下文」，但可用性表仅列 11 行。历史 TC-570 验证了 atomgit.actor 非空，但「属性表缺失」与「种类数缺口」未坐实。若 actor 在部分事件/位置不可用，或实际仅有 11 种上下文导致某类上下文缺失，将直接影响表达式引用与迁移兼容性。
预期系统行为: `atomgit.actor` 应存在于 atomgit 上下文且可在 job logs/表达式中读取（值应为触发者用户名/ID）；上下文总种类数应与文档声明的 12 种一致；若实际为 11 种，缺失的种类应被识别并记录为规格缺口。
Oracle 来源: GitCode规格（syntax-reference/context.md:5,23-49,275-292；runtime-environment-variables.md；view-job-logs.md:42）

验证要点:
  - [正向] 在 job step 中通过表达式读取 atomgit.actor，值应为非空字符串，且与触发该次运行的用户一致。
  - [正向] 枚举上下文可用性表中实际列出的所有上下文种类，与文档声明的 12 种逐项比对。
  - [负向] 不应出现「日志示例可用但属性表未声明」导致用户无法确认该属性是否官方支持的情况。
  - [非功能] 若种类数确实为 11 而非 12，需明确识别缺失的是哪一种（疑为 env/job/jobs 计数差异或某上下文未在表中列出），供 usability 出文档勘误。

可理解性判据: 实测结果应能消解文档矛盾——若 actor 可用，则补全属性表；若种类数为 11，则修正正文声明。实测值作为权威 oracle 回写 Parity Matrix。
优先级线索: BLIND-10 中严重度；关联 G-28/G-29、C-EXPR-07。历史 TC-570 已覆盖 actor 非空，本 intent 补「存在性坐实」与「种类数缺口核对」。
来源输入: inputs/gitcode-spec/syntax-reference/context.md（fetched 2026-07-20）；baseline/case-base-detail.md TC-570
```

---

## 溯源与闭合

| 盲区 ID | 能力项/缺口 | 覆盖 Intent | 历史基底 | 备注 |
|---|---|---|---|---|
| BLIND-02 | C-RUN-09/10 container 自定义镜像 | INTENT-COMP-009 | TC-273(FAIL), TC-262/263/575(PASS但难真测) | 补容器执行+私有镜像认证 |
| BLIND-03 | C-EXEC-15~20 matrix include/exclude 正确性 | INTENT-COMP-010/011/012 | TC-325~328(PASS但兼容差异未挖) | 补 include 追加语义、exclude 精确性、动态 runs-on 调度 |
| BLIND-10 | G-28/G-29 atomgit.actor 缺失 + 上下文 12vs11 计数 | INTENT-COMP-013 | TC-570(PASS, actor 非空) | 补属性表缺失坐实与种类数核对 |

*产出时间: 2026-07-21*
*基于 coverage.md + spec.md + case-base-detail.md + gitcode-spec 输入生成*
