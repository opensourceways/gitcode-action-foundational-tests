# 兼容性 Diff 补充产出 · BLIND-08 RUNNER_* 系统变量注入回归验证

> 产出 Agent：compat-diff（差异猎手）
> Run：2026-07-21-02（增量更新，不修改历史结论）
> 目标盲区：BLIND-08 `C-VAR-05 RUNNER_* 系统变量注入`
> 背景：历史 TC-441/442 FAIL、TC-533 env 不注入 Shell、TC-206 owner 未注入（NEEDS-UPDATE）；COMPAT-033 触及命名但未验证「变量是否真注入 Shell」。
> 来源输入：
>   - `inputs/github-reference/reference/variables.md`（GitHub 默认环境变量注入语义，fetched 2026-07-20）
>   - `inputs/gitcode-spec/action-development/runtime-environment-variables.md`（GitCode 运行时环境变量表 + RUNNER_* 列表）
>   - `inputs/gitcode-spec/syntax-reference/variables.md`（ATOMGIT_* 系统变量完整列表）
>   - `baseline/case-base-detail.md`（TC-441/442/206/533 FAIL 历史记录）
>   - `coverage.md` BLIND-08 详情 / `gate-log.md` 门禁风格

---

```
意图 ID:    INTENT-COMPAT-062
维度标签:   [compatibility, reliability]
标题:       RUNNER_* / ATOMGIT_* 系统变量 Shell 真实注入回归验证——历史 TC-441/442/206 FAIL 重验

具体差异点:   系统变量是否在 step 的 shell 进程中真实可用（非空/未定义）。
GitHub 侧预期行为: GitHub 默认注入 `RUNNER_OS`/`RUNNER_ARCH`/`RUNNER_NAME`/`RUNNER_TEMP`/`RUNNER_TOOL_CACHE`/`RUNNER_ENVIRONMENT` 到每个 step 的 shell 环境；`$RUNNER_OS` 在 Linux 下可读得 `Linux`；不可覆盖 `GITHUB_*`/`RUNNER_*` 默认值。
GitCode 侧疑似行为: spec/runtime-environment-variables.md 列出 `RUNNER_ARCH`/`RUNNER_ENVIRONMENT`/`RUNNER_NAME`/`RUNNER_OS`/`RUNNER_TEMP`/`RUNNER_TOOL_CACHE`，方向与 GitHub 一致。但历史 TC-441（ATOMGIT_RUNNER_OS FAIL）、TC-442（ATOMGIT_RUNNER_ARCH FAIL）、TC-206（ATOMGIT_REPOSITORY_OWNER 为空）证明**实际注入存在空值/失败**；COMPAT-033 已发现 `RUNNER_OS` vs `ATOMGIT_RUNNER_OS` 双命名并存（G-23 文档矛盾），但**未验证任一命名在 shell 中能否读到真实值**。
风险点:     若系统变量未真正注入 shell（或注入的是空串），迁移脚本中依赖 `$RUNNER_OS` 做平台分支、`$RUNNER_TEMP` 写临时文件、`$RUNNER_ARCH` 选二进制包 的逻辑会全部失效。这是「文档说有、实际没有」的典型静默错误，比命名差异更隐蔽——命名错至少能发现空值，注入失败则根本无变量。
预期系统行为: 文档列出的所有 RUNNER_* 与 ATOMGIT_* 系统变量，在 step shell 中通过 `$VAR` 读取时非空且值正确；双命名矛盾消解后至少有一套命名稳定可用。
Oracle 来源: GitHub行为（variables.md:54-60）+ GitCode 声明（runtime-environment-variables.md:47-52）+ 差异声明（G-23 双命名矛盾）
对齐方向:   一致性（系统变量应默认注入 shell 且可读，与 GitHub 一致；实测空值/未定义即缺陷）

验证要点:
  - [正向] step shell 中 `echo "$RUNNER_OS"` 输出非空正确值（如 `Linux`）；`echo "$RUNNER_ARCH"` 输出非空（如 `X64`）。
  - [负向] 不应出现「变量存在但值为空串」或「变量未定义」（history: TC-441/442/206）。
  - [非功能] 若 `ATOMGIT_RUNNER_OS` 与 `RUNNER_OS` 并存，应明确哪套为权威命名并文档统一。

触发条件:   一个 workflow 的 step 中依次 echo `$RUNNER_OS`/`$RUNNER_ARCH`/`$RUNNER_NAME`/`$RUNNER_TEMP`/`$RUNNER_TOOL_CACHE`/`$RUNNER_ENVIRONMENT`/`$ATOMGIT_RUNNER_OS`/`$ATOMGIT_RUNNER_ARCH`/`$ATOMGIT_REPOSITORY_OWNER`，比对输出是否非空且值符合预期 runner 实际规格。
优先级线索: 关联 BLIND-08 高严重度历史 bug + testing-focus §10 上下文差异；历史已 FAIL，建议 P1（回归验证），若实测仍空值/未定义则升 P0。
来源输入:   github-reference/reference/variables.md:54-60；gitcode-spec/action-development/runtime-environment-variables.md:47-52；gitcode-spec/syntax-reference/variables.md:75-107；baseline/case-base-detail.md（TC-441/442/206 FAIL）；coverage.md BLIND-08
```

```
意图 ID:    INTENT-COMPAT-063
维度标签:   [compatibility, reliability]
标题:       env > vars 优先级链在 Shell 中的真实覆盖回归验证——历史 TC-533「env 不注入 Shell」重验

具体差异点:   同名 env 在 workflow/job/step 三级定义时，shell 中实际读到的是哪一级值；以及 vars 是否意外介入 env 覆盖。
GitHub 侧预期行为: GitHub 中 env 三级覆盖为 step env > job env > workflow env，vars 是独立上下文（`${{ vars.X }}`）**不参与 env 覆盖**——shell 中 `$VAR` 读不到 vars 值，除非显式通过 `env: VAR: ${{ vars.X }}` 映射。引用不存在的属性求值为空字符串。
GitCode 侧疑似行为: spec C-VAR-02/C-VAR-03 声明同一顺序 step>job>workflow env；但历史 TC-533 FAIL「env 不注入 Shell」说明**优先级链可能在 shell 层未真实落地**；TC-534 FAIL「vars 与系统变量同名覆盖」暗示 vars 可能参与了不应有的覆盖；COMPAT-006 已指出 GitCode 疑似将 vars 与 env 合并进同一优先级链。
风险点:     (a) 若 env 不注入 shell，迁移 workflow 中所有通过 env 传递的配置（如 API endpoint、feature flag）在脚本层全部失效——这是比命名差异更严重的「功能静默消失」；(b) 若 vars 静默覆盖 env（与 GitHub 独立机制不同），则 GitHub 中「env.X 与 vars.X 互不干扰」的假设被打破，同名时脚本读到 vars 值而非 env 值，导致环境隔离失效。
预期系统行为: step env 在 shell 中生效且覆盖上层 env；vars 不直接介入 shell 环境变量覆盖（除非显式映射）。
Oracle 来源: GitHub行为（workflow-syntax.md:94；variables.md:63-66）+ GitCode 声明（C-VAR-02/C-VAR-03）+ 差异声明（COMPAT-006 已标 vars/env 合并疑似）
对齐方向:   一致性（env 三级覆盖应与 GitHub 一致；vars 不直接覆盖 env）+ 差异确认（若 GitCode 有意让 vars 参与覆盖，需文档明确）

验证要点:
  - [正向] workflow/job/step 各定义 `ENV_LEVEL: <级名>`，step shell 中 `echo "$ENV_LEVEL"` 输出 `step`（最内层生效）。
  - [负向] 不应出现「step env 定义但 shell 中读不到」（history: TC-533）；不应出现「vars 与 env 同名时 vars 静默覆盖 env 使 shell 读到 vars 值」。
  - [非功能] 优先级链文档表述与实测一致；vars 如何进入 shell 环境（显式映射 vs 自动合并）清晰。

触发条件:   （a）workflow/job/step 三级同名 env，step 读取 $ENV_LEVEL 验证覆盖；（b）平台设置 vars.ENV_LEVEL，不通过 env 映射，观察 step shell 中 $ENV_LEVEL 是否为空（GitHub 行为）还是读到 vars 值（GitCode 特有）；（c）env 与 vars 同名且值不同，观察 shell 中读到哪个。
优先级线索: 关联 BLIND-08 高严重度历史 bug + testing-focus §10 上下文差异；TC-533 已 FAIL，建议 P1（回归验证），若 env 仍不注入 Shell 则升 P0（功能静默消失）。
来源输入:   github-reference/reference/workflow-syntax.md:94；variables.md:63-66；gitcode-spec/core-concepts/variables-secrets-context-expressions.md；baseline/case-base-detail.md（TC-533/534 FAIL）；compat.md INTENT-COMPAT-006
```

```
意图 ID:    INTENT-COMPAT-064
维度标签:   [compatibility, reliability]
标题:       缺失系统变量引用行为与注入时机验证——「未定义报错 vs 空串」及「启动前注入 vs 延迟注入」

具体差异点:   （1）shell 中引用不存在的 `RUNNER_XXX`/`ATOMGIT_XXX` 变量时，返回空串还是报错/未定义；（2）系统变量是在 step 启动前注入（与 GitHub 一致）还是延迟注入，影响脚本首行即可读取的假设。
GitHub 侧预期行为: （1）引用不存在的 context 属性求值为**空字符串**（不报错）；在 shell 中 `$UNDEFINED_VAR` 若未设置则展开为空串（bash 默认行为，配合 `set -u` 才会报错，但 GitHub 默认 shell `bash -e` 不含 `-u`）。（2）默认环境变量在 step 进程启动前即设置好，用户脚本第一行即可读取 `$GITHUB_SHA`/`$RUNNER_OS`。
GitCode 侧疑似行为: （1）spec C-EXPR-06 声明「引用不存在属性求值为空字符串」——但此声明针对的是 `${{ context.property }}` 表达式求值，**未覆盖 shell 层 `$UNDEFINED` 的行为**；历史 TC-206（ATOMGIT_REPOSITORY_OWNER 为空）说明某些变量「存在但值为空」而非「未定义」，暗示变量列表可能预注册了键但值为空。（2）注入时机未在任何文档中声明；若延迟注入（如 step 开始后才异步设置），则脚本开头读取变量会得到空值。（3）runtime-environment-variables.md 7.4 声明「不要覆盖平台默认变量（ATOMGIT_* / RUNNER_*）」——但「覆盖是否被拒绝」未验证。
风险点:     （1）若 GitCode 默认 shell 带了 `-u`（或类似严格模式），迁移脚本中防御性引用 `$RUNNER_FOO` 会直接导致 step 失败——而 GitHub 下只是空串；（2）若延迟注入，依赖「脚本第一行读 `$ATOMGIT_SHA` 做初始化」的 workflow 会拿到空值，导致后续逻辑全部基于错误初始状态；（3）若允许覆盖系统变量，恶意/误写可污染 `$RUNNER_OS` 等影响下游行为。
预期系统行为: 缺失变量引用不报错（返回空串）；系统变量在 step 启动前已注入完成；尝试覆盖 RUNNER_* / ATOMGIT_* 系统变量被拒绝或至少不生效。
Oracle 来源: GitHub行为（variables.md:11「不可覆盖默认值」；contexts.md:35-59 缺失属性=空串）+ GitCode 声明（C-EXPR-06 + runtime-environment-variables.md 7.4）
对齐方向:   一致性（缺失变量行为、注入时机、不可覆盖约束应与 GitHub 一致；不一致即缺陷+缺口）

验证要点:
  - [正向] step 第一行立即 `echo "$RUNNER_OS"`/`"$ATOMGIT_SHA"` 可读得非空正确值（验证启动前注入）。
  - [负向] `echo "$RUNNER_NONEXISTENT"` 不应报错导致 step 失败（应输出空行）；尝试 `RUNNER_OS=Faked` 后再 echo，应仍读到真实值（验证不可覆盖）。
  - [非功能] 注入时机与不可覆盖约束文档化；默认 shell 的严格模式标志（是否有 `-u`）文档明确。

触发条件:   （a）step run 第一行立即读取系统变量；（b）同一 step 中 `echo "$RUNNER_FAKE_VAR"` 观察是否报错；（c）step 中尝试 `export RUNNER_OS=Fake` 后再读取，观察是否被允许覆盖；（d）与 GitHub 同脚本对照执行。
优先级线索: 关联 BLIND-08 高严重度历史 bug + testing-focus §10 默认值/隐式行为差异；注入时机影响所有迁移脚本，建议 P1（回归验证），若延迟注入或缺失变量报错则升 P0。
来源输入:   github-reference/reference/variables.md:11；contexts.md:35-59；gitcode-spec/syntax-reference/context.md:74；gitcode-spec/action-development/runtime-environment-variables.md:7.4；baseline/case-base-detail.md（TC-206 FAIL）
```

---

## 补充说明

- **接续规则**：本文件 intent ID 从 INTENT-COMPAT-062 起，接续 compat.md 已有的 COMPAT-061（workflow_call 复用差异）。
- **历史复用**：TC-441/442/206/533 等历史用例已在 NEEDS-UPDATE 列表中，case-writer 展开时应读取 `baseline/case-base-detail.md` 对应 TC 的原始断言，仅对「新增验证点」生成 delta，不重复生成已有语法层用例。
- **与 COMPAT-033 的关系**：COMPAT-033 已覆盖 RUNNER_OS/ARCH 双命名混乱（差异确认），本补充 intent **不重复命名验证**，聚焦「变量是否真注入 Shell」这一执行层盲区。
- **跨维标签**：三条均标 `[compatibility, reliability]`——因涉及历史已确证 bug 的回归验证，稳定性维度同样关注「修复后是否再次失效」。
- **优先级建议**：三条均建议 P1（回归验证）。若实测仍复现 TC-441/442/533/206 的 FAIL 表现，应按 gate-log §2 标准升 P0（blocker 级功能静默失效）。

*产出时间: 2026-07-21*
*基于 compat.md COMPAT-033/061 + coverage.md BLIND-08 + gate-log.md §6 + baseline/case-base-detail.md 历史 FAIL 记录生成*
