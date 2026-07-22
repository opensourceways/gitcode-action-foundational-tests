# inputs/workflow-samples/

真实开源项目的 GitCode Actions workflow 样本，作为兼容性测试与易用性分析的真实负载。

消费方：compat-diff · usability · L0 冒烟

---

## 当前样本

### cann/（7 个文件，共 817 行）

来源：CANN（昇腾 AI 异构计算架构）项目，华为开源，GitCode 内部试点项目。

| 文件 | 触发方式 | 核心 Action | 说明 |
|------|---------|------------|------|
| `arm_compile_action.yml` | `workflow_dispatch`（手动，含 task_name / image_version 入参） | checkout · obs-download · build-accelerate · obs-upload · 自定义 verify-package | ARM 编译流水线，`runs-on: [dedicate-hosted, arm64, xlarge]` |
| `x86_compile_action.yml` | `workflow_dispatch`（手动，含 task_name / image_version 入参） | checkout · obs-download · build-accelerate · obs-upload · 自定义 verify-package | x86 编译流水线，`runs-on: [dedicate-hosted, x64, large]` |
| `llt_action.yml` | `workflow_dispatch`（手动，含 image_version 入参） | checkout · obs-download · 自定义 ut-cov-report · obs-upload | 单元测试 + 覆盖率，`runs-on: [dedicate-hosted, x64, xlarge]` |
| `codecheck_action.yml` | `workflow_dispatch`（手动，含 precommit_image_version / codecheck_image_version 入参） | checkout · obs-download · 自定义 precommit / codecheck · obs-upload | 代码检查（precommit + codecheck 两个 job），`runs-on: [dedicate-hosted, x64, small]` |
| `staticcheck_action.yml` | `workflow_dispatch`（手动，含 image_version 入参） | checkout · obs-download · 自定义 staticcheck · obs-upload | 静态检查，`runs-on: [dedicate-hosted, x64, small]` |
| `ops-nn_action.yml` | `pull_request_comment` / `pr_comment`（评论触发，keyword 正则匹配） | checkout · obs-upload · obs-download · 自定义 revise-img / get-pr · build-accelerate | 多 stage 多 job 流水线，含 `stages:` 结构、`vars` 上下文（已知不支持 #11）、自定义 composite action 引用 |
| `sub_pipline_support.yaml` | `pr_comment`（评论触发，keyword 正则匹配） | — | 子流水线触发配置示例（仅含 `on:` 定义，无 jobs） |

**覆盖场景**：手动触发含入参、评论触发、OBS 上传/下载、构建加速、自定义 composite action 引用、多 stage 多 job、ARM / x86 双架构、`dedicate-hosted` 资源池。

---

### op-plugin/（1 个文件，424 行）

来源：op-plugin（昇腾算子插件）项目，华为开源，GitCode 内部试点项目。

| 文件 | 触发方式 | 核心 Action | 说明 |
|------|---------|------------|------|
| `PR-pipeline_op-plugin.yml` | `pull_request_comment`（评论触发）| checkout · sca-pr-scan · setup-python · antipoison · openlibing-pre-commit-action · reusable workflow（`.gitcode/workflows/build_job.yml`） | 完整 PR 流水线，含 3 个 stage：stage_1（SCA / Antipoison / CodeCheck / doc-only 判断）、stage_2（x86 + ARM 双架构 × 6 个 pytorch 版本共 12 个并行构建 job，全部调用可复用 workflow）、stage_3（UT）；含 `concurrency`（最大并发 5、抢占式）、workflow-level `inputs` 定义、多镜像版本矩阵（env 变量管理）、`runs-on: [dedicate-hosted, x64/arm64, 2xlarge/large]` |

**覆盖场景**：大规模并行构建（12 个构建 job）、可复用 workflow 调用（`workflow_call`）、并发控制与抢占、workflow-level inputs、多版本镜像矩阵、SCA 安全扫描、PR 评论触发、混合 x86/ARM 架构。

---

### testorg/（3 个文件）

来源：MindIE-SD（昇腾推理引擎）项目，华为开源，GitCode 内部试点项目。一个主流水线 + 两个可复用 workflow 的组合。

| 文件 | 触发方式 | 核心 Action | 说明 |
|------|---------|------------|------|
| `full_pr.yaml` | `pull_request`（branches dev/master/master_for_actions，types open/reopen/update/merge，含 `code-update` / `branches-ignore` / `paths-ignore`）+ `pull_request_comment`（正则 `^(?:\/)?compile*`） | checkout（pre-merge）· sca-pr-scan · openlibing-pre-commit-action · reusable workflow（`./.gitcode/workflows/build_job.yaml` / `ut_job.yaml`） | 主 PR 流水线，含 `stages:` 结构：stage1 静态检查（SCA / Antipoison 反投毒 shell / pre-commit）、stage2 编译构建（x86 abi1 / arm abi1 / arm abi0 三个构建 job + DTArmID 单测，全部调用可复用 workflow 并传 secrets）；含 workflow-level `inputs`（12 个，混用 `${gitcode_*}` / `${PIPELINE_*}` / `${{atomgit.*}}` 三种变量风格 + `manual_override` 字段）、`select: selected_by_default`、`if: ${{ default() }}`；混合资源池 `codearts-hosted`/`ubuntu-latest` 与 `dedicate-hosted`；`concurrency` 段被注释 |
| `build_job.yaml` | `workflow_call`（inputs: abi_type / CP_DOCKER_IMG / pr_id / runs_on_arch / arch；secrets: OBS_AK / OBS_SK required） | checkout（pre-merge）· obs-upload · 内联 shell（python 3.11 校验、abi/devtoolset 切换、ascend set_env、`setup.py bdist_wheel`） | 被调用的可复用构建 workflow，`runs-on: [dedicate-hosted, ${{ inputs.runs_on_arch }}, xlarge]` |
| `ut_job.yaml` | `workflow_call`（inputs: CP_DOCKER_IMG / pr_id / runs_on_arch；无 secrets） | checkout（pre-merge）· 内联 shell（`build.sh`、aarch64 上跑 UT + coverage、grep OK 判定成败） | 被调用的可复用单测 workflow；注意 `name: Build Job` 系复制粘贴残留 |

**覆盖场景**：`pull_request` 触发（含 branches/types/ignore 过滤）、`workflow_call` 入口、本地路径可复用 workflow 调用（`uses: ./.gitcode/workflows/*.yaml` + `secrets:` 传递）、pre-merge checkout（`refs/merge-requests/N/merge`）、`select` / `if: default()` 选择性执行、abi0/abi1 构建矩阵、多变量插值风格混用、反投毒 shell、混合资源池。

**已知边缘/风险点**（供 compat-diff / usability 关注）：`types: [open, reopen, update, merge]` 非标准事件类型名、`code-update` 为非标准 `on` 字段、`comments` 正则 `compile*`（`*` 作用于 `e`）疑似笔误、`ut_job.yaml` 的 `name` 与文件用途不符。

---

## 样本覆盖度分析

| 场景维度 | 覆盖情况 |
|---------|---------|
| 触发方式 | `workflow_dispatch`（手动）、`pull_request_comment`/`pr_comment`（评论触发）、`pull_request`（含 branches/types/ignore 过滤，testorg）、`workflow_call` 入口（testorg build_job/ut_job）；**缺**：`push`、`schedule` |
| 资源池 | `dedicate-hosted`（自定义资源池）、`codearts-hosted`/`ubuntu-latest`（官方资源池，testorg）均有覆盖 |
| 架构 | ARM（arm64）、x86（x64）均有覆盖 |
| 核心 Action | checkout · obs-upload/download · build-accelerate · setup-python · sca-pr-scan · pre-commit · antipoison；**缺**：setup-node/go/jdk、cache、upload-artifact/download-artifact、docker 系列 |
| Workflow 模型 | 单 job、多 job、多 stage、可复用 workflow 调用（`uses: .gitcode/workflows/` 远程与 `./.gitcode/workflows/*.yaml` 本地路径 + `secrets:` 传递）均有覆盖 |
| 并发控制 | `concurrency` + 抢占式配置已覆盖（op-plugin 生效、testorg 注释态） |
| 安全场景 | SCA 扫描、antipoison 反投毒检查、secrets 传递可复用 workflow 已覆盖；**缺**：fork PR 触发、secrets 隔离验证场景 |

---

已补充 / 3 个项目 / 11 个样本文件 / 2026-07-22
