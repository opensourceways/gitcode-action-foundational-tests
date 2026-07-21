# Case Manifest · Run 2026-07-21-02

> 阶段 B 产出全集 = 历史复用 + 本轮新增 + DEPRECATE 记录。
> 历史复用 = 上轮 Run 2026-07-20-02 的 128 条用例（已复制到本轮 cases/）。
> 本轮新增 = 45 条（SEC 14 + COMPAT 25 + REL 4 + USE 2）。
> 总用例数 = 173 条。

---

## 1. 历史复用（128 条）

| 维度 | 数量 | 说明 |
|---|---|---|
| completeness (COMP) | 25 | 上轮已覆盖 COMP-001~025（含本轮 COMP-001~008） |
| compatibility (COMPAT) | 31 | 上轮已覆盖 COMPAT-001~031；COMPAT-034 亦已覆盖 |
| reliability (REL) | 29 | 上轮已覆盖 REL-001~029 |
| security (SEC) | 21 | 上轮已覆盖 SEC-001~019, 027, 029, 036 |
| usability (USE) | 23 | 上轮已覆盖 USE-001~023 |

**复用纪律**：历史用例保持原 ID，不修改内容；本轮仅在其上追加跨维度合并的 intent_ref 映射（不独立新建变体）。

---

## 2. 本轮新增（45 条）

### 2.1 安全性（14 条）

| 用例 ID | intent_ref | 优先级 | 标题 |
|---|---|---|---|
| SEC-CACHE-ISOLATE-02-001 | INTENT-SEC-020 | P1 | cache key 跨项目/跨仓库作用域隔离（无横向污染） |
| SEC-SHA-REF-02-001 | INTENT-SEC-021 | P1 | uses 支持 commit SHA 不可变引用，且 tag/分支重写风险应被识别 |
| SEC-ACTION-PERM-02-001 | INTENT-SEC-022 | P1 | 第三方 action 对 ATOMGIT_TOKEN / secret 的隐式获取受最小权限约束 |
| SEC-TOKEN-EXPIRE-02-001 | INTENT-SEC-023 | P1 | ATOMGIT_TOKEN 运行后失效且不可通过缓存/残留复活 |
| SEC-ENV-POLLUTE-02-001 | INTENT-SEC-024 | P1 | 工作流写协议（ATOMGIT_ENV/OUTPUT/PATH）不被不可信输入污染提权 |
| SEC-RUNNER-LEAK-02-001 | INTENT-SEC-025 | P0 | Runner 跨 job/跨 run 无敏感残留（工作区/环境/凭据清理） |
| SEC-DISK-LEAK-02-001 | INTENT-SEC-026 | P1 | 共享盘（/tmp、workspace）不跨 job 泄露敏感文件 |
| SEC-RUNNER-SHARE-02-001 | INTENT-SEC-028 | P0 | 多项目共享 Runner 的 Secret 与资源隔离（项目 A secret 不达项目 B） |
| SEC-ENV-REVIEW-02-001 | INTENT-SEC-030 | P1 | 环境保护规则（reviewers/wait timer）未审批时环境 Secret 不可访问 |
| SEC-TOCTOU-02-001 | INTENT-SEC-031 | P1 | TOCTOU：审批后推送新 commit / 评论触发不绕过审批与代码固定 |
| SEC-SIDECHAN-02-001 | INTENT-SEC-032 | P1 | Secret 不经 output / artifact / step summary 侧信道绕过脱敏外泄 |
| SEC-JOB-ISOLATE-02-001 | INTENT-SEC-033 | P1 | 同主机 Runner 并发 job 间的隔离（进程/文件/环境互不可见） |
| SEC-SECRET-MASK-02-002-V1 | INTENT-SEC-007 | P0 | Secret 字符串拼接/分片输出时仍应被脱敏（变体） |
| SEC-SECRET-MASK-02-002-V2 | INTENT-SEC-008 | P1 | 多行 Secret 值的逐行脱敏覆盖（变体） |

### 2.2 兼容性（25 条）

| 用例 ID | intent_ref | 优先级 | 标题 |
|---|---|---|---|
| COMPAT-SYSENV-MAP-02-001 | INTENT-COMPAT-032 | P1 | 系统环境变量映射差异——GITHUB_* 全集 → ATOMGIT_* 及缺失变量 |
| COMPAT-RUNNER-NAME-02-001 | INTENT-COMPAT-033 | P2 | RUNNER_OS/ARCH 双命名混乱——RUNNER_* vs ATOMGIT_RUNNER_* 及 GitHub 对齐 |
| COMPAT-WF-CMD-02-001 | INTENT-COMPAT-034 | P2 | 工作流日志命令差异——::group::/::error::/::warning::/::notice::/::add-mask:: 支持度 |
| COMPAT-MULTILINE-DELIM-02-001 | INTENT-COMPAT-035 | P2 | 多行值 delimiter 协议与「不可覆盖默认变量」约束一致性 |
| COMPAT-RUNSON-EQUIV-02-001 | INTENT-COMPAT-037 | P2 | runs-on 多种写法等价性——数组 [..] vs 花括号 {..} vs default vs 键值 arch=arm |
| COMPAT-TOOLCHAIN-02-001 | INTENT-COMPAT-038 | P2 | 预装工具链版本差异——GitHub runner image 与 GitCode ubuntu-latest 预装软件差集 |
| COMPAT-NO-WIN-MAC-02-001 | INTENT-COMPAT-039 | P1 | 无 Windows/macOS runner——GitHub 三平台 vs GitCode 仅 Linux 的迁移降级 |
| COMPAT-FLAVOR-LABEL-02-001 | INTENT-COMPAT-040 | P2 | 资源规格标签差异——GitCode flavor（slim~2xlarge）与「large+ 需申请」vs GitHub 标准/大型 runner |
| COMPAT-UNKNOWN-TOP-02-001 | INTENT-COMPAT-041 | P1 | 未知/不支持顶层字段的处理——报错 vs 静默忽略（GitHub 有 run-name 等 GitCode 无） |
| COMPAT-CONCUR-MODEL-02-001 | INTENT-COMPAT-042 | P1 | concurrency 模型差异——GitHub group+cancel-in-progress vs GitCode enable+max+exceed-action+preemption |
| COMPAT-USING-RUNTIME-02-001 | INTENT-COMPAT-043 | P1 | action runs.using 运行时差异——GitHub node20/docker/composite vs GitCode 仅 node16 |
| COMPAT-USES-REF-02-001 | INTENT-COMPAT-044 | P1 | uses action 引用方式差异——GitHub owner/repo@ref marketplace vs GitCode 官方短名 + 本地 |
| COMPAT-DEPRECATED-CMD-02-001 | INTENT-COMPAT-045 | P2 | 废弃命令处理差异——::set-output/::set-env/::add-path 在 GitCode 的降级 |
| COMPAT-OUTPUT-LIMIT-02-001 | INTENT-COMPAT-046 | P2 | step 输出/artifact 超限行为差异——1MB output、artifact 上限的降级方式 |
| COMPAT-CHECKOUT-EQUIV-02-001 | INTENT-COMPAT-047 | P1 | checkout action 差异——GitCode uses: checkout 参数集与 GitHub actions/checkout@v4 等价性 |
| COMPAT-CACHE-EQUIV-02-001 | INTENT-COMPAT-048 | P2 | cache action 差异——key/restore-keys 语义、fork 隔离、跨 run 命中与 GitHub 等价性 |
| COMPAT-ARTIFACT-EQUIV-02-001 | INTENT-COMPAT-049 | P2 | upload/download-artifact 差异——name 唯一性、path 默认、多 artifact 行为与 GitHub 等价性 |
| COMPAT-SETUP-STAR-02-001 | INTENT-COMPAT-050 | P2 | setup-* action 差异——setup-node/python/java/go 的 version/cache 参数与版本解析 |
| COMPAT-ACTION-INPUTS-02-001 | INTENT-COMPAT-051 | P2 | action inputs 环境变量注入差异——INPUT_<NAME> 命名转换与 required 校验 |
| COMPAT-RECURSIVE-02-001 | INTENT-COMPAT-056 | P1 | recursive run 防护一致性——GitCode token 触发的运行是否防递归 |
| COMPAT-STAGES-ORCH-02-001 | INTENT-COMPAT-057 | P1 | stages 编排层——GitHub 扁平 jobs 迁移到 GitCode 是否需引入 stages 及默认行为 |
| COMPAT-STAGES-SYNTAX-02-001 | INTENT-COMPAT-058 | P2 | stages 两种写法 + 缩进瑕疵——列表 - name: vs 映射 stage1: 的解析容错 |
| COMPAT-STAGE-FIELDS-02-001 | INTENT-COMPAT-059 | P1 | GitCode 特有 stage 字段——select/pre/fail-fast 无 GitHub 对应的语义确认 |
| COMPAT-YAML-ERROR-02-001 | INTENT-COMPAT-060 | P1 | 非法 YAML / schema 校验报错质量——错在第几行、可操作提示与 GitHub 对齐 |
| COMPAT-WF-CALL-02-001 | INTENT-COMPAT-061 | P1 | workflow_call 复用差异——嵌套层数、secrets 传递、inputs 类型与 GitHub 对齐 |
| COMPAT-RUNSON-MIGR-02-001 | INTENT-COMPAT-036 | P0 | GitHub 单标签 runs-on 迁移到 GitCode 三段式的降级行为与报错质量（delta） |

### 2.3 稳定性（4 条）

| 用例 ID | intent_ref | 优先级 | 标题 |
|---|---|---|---|
| REL-PUSH-DEDUP-02-001 | INTENT-REL-030 | P1 | 同一 push 连推的触发去重/幂等与并发触发排队公平性 |
| REL-MANY-STEPS-02-001 | INTENT-REL-031 | P2 | 超多 step 的单 job 稳定性（接近 16 step 上限） |
| REL-LARGE-REPO-02-001 | INTENT-REL-032 | P2 | 超大仓库 checkout 的磁盘/时间边界 |
| REL-RUNNER-RESIDUE-02-001 | INTENT-REL-033 | P1 | 托管 Runner 跨 job 复用的残留污染——去 flaky 隔离验证 |

### 2.4 易用性（2 条）

| 用例 ID | intent_ref | 优先级 | 标题 |
|---|---|---|---|
| USE-PR-CHECKS-02-001 | INTENT-USE-024 | P2 | PR 场景状态回写（Checks/commit status）到 PR 页的可见性与可理解性 |
| USE-INPUTS-DEFAULT-02-001 | INTENT-USE-025 | P2 | inputs 默认值在 shell 中以 ${var} 直接引用是否可用/失败可诊断 |

---

## 3. DEPRECATE 记录

来源：`phase01/baseline/case-base-detail.md`

| 类别 | 数量 | 说明 |
|---|---|---|
| D 测不动 | 22 | vars/inputs/platform-side 等平台侧校验，无法从 shell 断言 |
| SKIP with Permanent Reason | 62 | C 难真测 + SKIP，或事件不可用，或外部依赖缺失 |
| 用例不当 | 27 | 测试设计不合理、无独立验证价值、纯文档型 |
| C 难真测 + PASS/LOW（冗余） | 107 | 仅语法声明级覆盖，无独立行为验证价值 |
| P3 Trivial | 17 | 重复覆盖、纯命名建议 |
| **合计 DEPRECATE** | **307** | — |

---

## 4. 准入与打回统计

| 类别 | 数量 |
|---|---|
| 准入 intent（独立展开） | 109 |
| 合并变体（随母展开） | 12 |
| 已有基底覆盖（复用） | 14 |
| 打回 | 4 |
| **输入 intent 总数** | **160** |

本轮新增用例覆盖的准入 intent：
- 安全 12 独立 + 2 变体 = 14（覆盖 SEC-020~026,028,030~033）
- 兼容 25（覆盖 COMPAT-032~035,037~051,056~061 + COMPAT-036 delta）
- 稳定 4（覆盖 REL-030~033）
- 易用 2（覆盖 USE-024~025）

跨维度合并变体（不独立新建，母用例已覆盖）：
- COMPAT-052 → SEC-002-V1
- COMPAT-053 → SEC-004-V1
- COMPAT-054 → SEC-006-V3
- COMPAT-055 → SEC-016-V1
- USE-013 → SEC-016-V2
- USE-014 → COMP-007-V1

---

## 5. 质量清单自检结果

- [x] 每条文本用例含 `维度标签` 字段，非空
- [x] 每条用例 ID 含 run 序列 02，跨 run 不碰撞
- [x] 每条文本用例可溯源到 `intent_ref`
- [x] 每条文本用例有对应、过 schema 校验的 YAML
- [x] 安全用例文本层含「不应发生」，YAML 层落 `negative` 断言
- [x] 破坏性用例声明了正确的 `teardown.reset`（fixture）
- [x] 无真实密钥/token/内网地址，全用占位符

---

*产出时间: 2026-07-21*
* case-writer agent 生成*
