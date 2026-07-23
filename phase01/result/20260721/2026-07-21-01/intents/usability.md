# Usability Test Intents

> Agent: usability | Run: 2026-07-21-01 | Date: 2026-07-21
>
> 输入快照:
> - `phase01/inputs/gitcode-spec/` (50 页, 2026-07-20)
> - `phase01/inputs/github-reference/` (12 页, 2026-07-20)
> - `phase01/inputs/existing-cases/cases.md` (631 条, 2026-07-20)
> - `phase01/inputs/history/issues-encountered.md` (95 条历史问题, 2026-07-20) **★ 本 run 新增**
> - `phase01/inputs/history/gitcode-actions-list.md` (25 个官方 Action 清单, 2026-07-20)
> - `phase01/baseline/risk-register.md` (RISK-USE-01)
> - `phase01/baseline/parity-matrix.md`
> - `phase01/baseline/quality-gate.md`
>
> 退化声明:
> - `inputs/workflow-samples/` 缺失: 迁移摩擦 intent 基于 spec diff 分析而非真实 workflow 搬运, 准确性打折。
> - `inputs/business-context/` 仅含 README 模板无实际数据: 无真实迁移规模/改造点/历史踩坑记录, 场景选择偏通用。
>
> 与上一 run (2026-07-20-01) 的关系:
> - 上一 run 产出 INTENT-USE-001 ~ INTENT-USE-023（23 条），聚焦 YAML 静态校验报错、文档一致性、迁移摩擦梳理、重新运行体验。
> - **本 run 的核心增量来自 `history/issues-encountered.md` (95 条真实用户问题)**, 重点关注：
>   - **日志查看体验**（历史 #6/#14/#28/#80/#81 — 用户最大痛点）
>   - **运行时错误信息质量**（历史 #23/#52/#83/#89 — 非 YAML 解析阶段的报错空洞）
>   - **变量/参数调试摩擦**（历史 #75/#76/#82/#85 — 类型转换、变量传递、uses 表达式）
>   - **Plugin/Action 发现与文档**（历史 #18/#47/#50 — 信息不可达）
>   - **界面展示与状态反馈**（历史 #24/#34/#56/#72/#73/#95）
>   - **迁移摩擦的补充场景**（从 COMPAT-NOTES 差异点 + 历史实证交叉验证）
> - 本 run intents ID 从 INTENT-USE-024 开始。
>
> 现有用例去重说明:
> - `cases.md` 631 条聚焦**功能行为验证**。日志相关的现有用例仅验证「日志能刷出来」(TC-022, TC-258)，不验证「日志加载速度、下载可用性、乱序」等体验维度。
> - 本批 intent 与上一 run 的分工:
>   - USE-001~006: YAML 解析阶段的报错可诊断性
>   - USE-024~031: **运行时**阶段的错误/日志/调试体验（历史实证）
>   - USE-032~036: 迁移摩擦的补充（变量系统、仓库名上下文、Plugin 发现等历史高频点）

---

## A. 日志查看体验（历史实证: 用户最大痛点）

> 历史问题 #6（日志无法下载）、#14（日志加载约 7min）、#28（无关日志多）、#80（乱序）、#81（不显示）构成日志维度的集中痛点。现有用例未覆盖日志的**体验维度**（加载性能、下载可用性、日志相关性、顺序一致性）。

---

意图 ID:    INTENT-USE-024
维度标签:   [usability]
标题:       Job 日志下载功能的可用性

风险点:     历史问题 #6 报告「job 的日志无法下载，日志很长翻起来体验不佳，没有对应的下载按钮」。文档 `view-job-logs.md` 声称「点击右上角"下载日志"按钮，获取该 job 的完整日志文件」。若下载按钮不存在或下载的文件为空/截断，用户面对数千行日志只能手动滚动翻找（尤其长构建日志场景）。
预期系统行为: 每个 job 的日志面板右上角存在可用的「下载日志」按钮；点击后下载的文件为 UTF-8 文本、包含该 job 的**完整**日志（不截断）、文件名含 job 名称或可辨识标识。

Oracle 来源: `gitcode-spec/running-pipelines/view-job-logs.md` §日志搜索与折叠; 历史问题 #6

验证要点:
  - [正向] 运行一个多 step job（>= 5 个 step，每个 step 输出 >= 20 行日志），点击「下载日志」按钮，验证下载成功且文件含全部 step 日志。
  - [正向] 运行一个 job 日志量 >= 500 行的构建，下载后验证行数匹配（与面板展示日志行数对比，允许少量行号偏移因面板折叠/截断）。
  - [负向] 下载按钮不应在日志加载中/加载失败时消失；若日志未就绪应有明确状态提示。

可理解性判据:
  - 确定性: 下载功能是否可用 (点击后有文件输出)、下载文件是否包含完整日志 (行数对比可判定)。
  - 无需 llm_assisted。

优先级线索: P1 (关联 RISK-USE-01: 日志是迁移后调试的首要工具；历史实证高频痛点)
破坏级别:   none
来源输入:   `gitcode-spec/running-pipelines/view-job-logs.md`; 历史问题 #6; `testing-focus.md` §9

---

意图 ID:    INTENT-USE-025
维度标签:   [usability]
标题:       日志加载性能的可接受性

风险点:     历史问题 #14 报告「任务失败查看日志时，日志加载时间过长，大约 7min 才能完全加载好」。用户在排查失败构建时，等待 7 分钟是严重的调试速度摩擦——尤其在多轮「改→跑→看日志」迭代中。
预期系统行为: 日志应在触发查看后 30 秒内完成初始加载（首屏可见），完整加载时间不应超过 60 秒（对日志量 <= 2000 行的典型 job）。若日志量超过 2000 行，应有进度指示器。

Oracle 来源: 历史问题 #14; 业界标准：日志系统首字节时间 < 5s, 完整加载 < 30s

验证要点:
  - [正向] 运行一个约 500 行日志的 job（如 `echo` 循环 500 次），从点击 step 到日志面板展示首屏/完整内容，记录耗时。
  - [正向] 运行一个约 2000 行日志的 job，同上。
  - [非功能] 若加载超过 30 秒，界面应有加载进度指示器（spinner / 进度条 / "正在加载..." 提示），不应白屏。
  - [非功能] 日志加载失败应有明确错误提示和重试入口。

可理解性判据:
  - 确定性: 加载时间是否在阈值内 (秒表计时可判定)。
  - `eval: llm_assisted`: 若超时，评估加载进度指示器的用户感知友好度。

优先级线索: P1 (历史 #14 实证; 直接影响调试效率)
破坏级别:   none
来源输入:   历史问题 #14; `gitcode-spec/running-pipelines/view-job-logs.md`; `testing-focus.md` §9

---

意图 ID:    INTENT-USE-026
维度标签:   [usability]
标题:       日志内容的相关性与无关噪音过滤

风险点:     历史问题 #28 报告「无关日志较多」。Runner 日志中可能混入平台内部运维日志（如镜像拉取进度、网络诊断、系统初始化脚本输出），用户真正关心的「我的脚本输出」被淹没。尤其在排查失败时，用户需要快速定位自己代码的错误行，而非翻阅平台内部信息。
预期系统行为:
             - 日志面板应**默认折叠**平台内部运维日志（如镜像拉取、系统初始化），仅展开用户 step 的输出。
             - 每条日志行应有来源标注（用户 script vs 平台系统 vs Action 内部），便于过滤。
             - 日志搜索/高亮功能应可用（文档 `view-job-logs.md` 声称支持关键词高亮）。

Oracle 来源: 历史问题 #28; `gitcode-spec/running-pipelines/view-job-logs.md` §日志搜索与折叠

验证要点:
  - [正向] 运行一个 job（含 `checkout` + 用户 `run: echo "USER_LOG_MARKER"`），验证用户日志行可见且不被平台日志淹没。
  - [正向] 在日志搜索框输入 `USER_LOG_MARKER`，验证能定位并高亮。
  - [非功能] 平台内部日志行应有可辨识的输出前缀或缩进/颜色区分。

可理解性判据:
  - 确定性: 搜索/高亮功能是否可用 (界面可操作判定)；用户日志是否可见。
  - `eval: llm_assisted`: 平台日志 vs 用户日志的视觉区分度 (0=完全无法区分, 1=需仔细看, 2=一眼可辨)。

优先级线索: P2 (体验改善；有 workaround: 用户在自己的脚本里打唯一标记然后搜索)
破坏级别:   none
来源输入:   历史问题 #28; `gitcode-spec/running-pipelines/view-job-logs.md`

---

意图 ID:    INTENT-USE-027
维度标签:   [usability, reliability]
标题:       日志输出的顺序一致性与完整性

风险点:     历史问题 #80 报告「日志打印乱序」、#81 报告「日志大概率不显示」。这是两类不同但同样严重的问题: 乱序导致用户误判执行流程（以为 step A 在 step B 之后执行）；不显示导致用户完全无法调试。这两种情况尤其在长时运行或多并发 step 场景下高发。
预期系统行为:
             - 同一 step 内日志行应按时间顺序严格线性排列（先输出的先展示）。
             - 每个 step 的日志应完整展示（不丢失行），除非 step 本身被 kill 导致日志截断（此时应有明确标注）。
             - 多 job 并发执行时，各 job 日志独立且顺序一致。

Oracle 来源: 历史问题 #80, #81; `gitcode-spec/running-pipelines/view-job-logs.md`

验证要点:
  - [正向] 在 step 中执行 `for i in $(seq 1 100); do echo "COUNT:$i"; done`，验证日志中 COUNT:1 到 COUNT:100 严格升序。
  - [正向] 运行 3 个并发 job，每个 job 各自输出 50 行带 job-id 标记的日志，验证各 job 日志内部顺序正确且无交叉污染。
  - [负向] 日志不应出现「运行成功的 step 无日志输出」(#81)。
  - [非功能] 若 step 因超时/被 kill 导致日志截断，应有 "Log truncated: step killed/timeout" 类标注。

可理解性判据:
  - 确定性: 日志顺序是否正确 (逐行比对预期序列可判定); 日志是否完整 (全部预期行存在可判定)。
  - 无需 llm_assisted。

优先级线索: P1 (历史 #80/#81 实证; 日志乱序/缺失直接致调试无效)
破坏级别:   none
来源输入:   历史问题 #80, #81; `gitcode-spec/running-pipelines/view-job-logs.md`; `testing-focus.md` §9

---

## B. 运行时错误信息质量（非 YAML 解析阶段）

> 上一 run USE-001~006 覆盖了 YAML 解析阶段（提交前/静态校验）的报错可诊断性。但历史实证显示，大量用户困惑来自**运行时**的报错空洞（#23 手动触发无报错、#52 镜像拉取失败无日志、#83 报错误导、#89 拉镜像失败也无报错）。

---

意图 ID:    INTENT-USE-028
维度标签:   [usability]
标题:       手动触发 (workflow_dispatch) 参数无效时的错误反馈

风险点:     历史问题 #23 报告「手动传参时输入参数后无法触发流水线」，用户建议「输入参数未指定 type 类型导致流水线无法启动，建议添加报错信息」。若 workflow_dispatch 界面接受用户输入后静默失败（按钮无反应 / 无任何提示），用户无法判断是「我填错了」还是「平台坏了」。
预期系统行为: 当 workflow_dispatch 的输入参数不合法（如 required 参数未填、值格式不符合预期）时，平台应在提交前给出**即时校验反馈**（表单级 inline error），不应接受提交后到运行时才发现未触发。

Oracle 来源: 历史问题 #23; `gitcode-spec/writing-pipelines/configure-triggers.md` §workflow_dispatch

验证要点:
  - [正向] 定义 `workflow_dispatch.inputs.name.required: true`，不填 name 直接点触发，验证界面给出 red inline error "此字段为必填"。
  - [正向] 定义 `workflow_dispatch.inputs.count.default: "1"`, 提交后验证 run 被创建且 `inputs.count` 值为 "1"。
  - [负向] 即使参数有问题，也不应静默不触发；任何导致 workflow 无法启动的输入错误都应有可见提示。

可理解性判据:
  - 确定性: 前端是否显示 inline validation error (可截图判定); run 是否被创建 (可 API 查)。
  - `eval: llm_assisted`: 若报错, 评估是否足以让用户知道「哪个参数、错在哪、怎么改」(三级评判)。

优先级线索: P1 (关联 RISK-USE-01; 历史 #23 实证)
破坏级别:   none
来源输入:   历史问题 #23; `gitcode-spec/writing-pipelines/configure-triggers.md`; `testing-focus.md` §1

---

意图 ID:    INTENT-USE-029
维度标签:   [usability]
标题:       Runner 环境准备阶段失败时的错误信息质量

风险点:     历史问题 #52 报告「默认 runner 和自定义 image 模式，pending 约 10min 报失败，失败没有详细日志」。镜像拉取失败、Runner 启动失败等环境准备阶段的问题，可能长达 10 分钟无反馈然后直接失败且无日志——用户完全无法定位根因。
预期系统行为: Runner 环境准备（镜像拉取、资源分配、初始化）阶段应有**阶段性进度反馈**（如 "Pulling image... (50%)"）；若某阶段失败，应给出具体失败原因（如 "Image pull failed: connection timeout to registry" 而非 "Setup failed"）。

Oracle 来源: 历史问题 #52, #89; `testing-focus.md` §9（可观测性）

验证要点:
  - [正向] 使用一个较大的自定义镜像（如 > 1GB），观察镜像拉取阶段是否有进度反馈。
  - [正向] 使用一个不存在的自定义镜像（如 `nonexistent:latest`），验证失败消息包含镜像名和失败原因（而非 "Setup failed"）。
  - [非功能] 环境准备阶段不应长时间无日志输出（理想情况每 30 秒有阶段性日志）。

可理解性判据:
  - 确定性: 失败消息是否包含镜像名和失败原因 (可字符串匹配判定)。
  - `eval: llm_assisted`: 若消息存在但不具体 (如 "Setup failed"), 评估用户能否定位根因。

优先级线索: P1 (历史 #52/#89 实证; 长达 10min 无反馈后失败对用户极度挫败)
破坏级别:   none
来源输入:   历史问题 #52, #89; `testing-focus.md` §9; `gitcode-spec/runner-management/configuring-images-toolchains.md`

---

意图 ID:    INTENT-USE-030
维度标签:   [usability]
标题:       Plugin/Action 前置依赖缺失时的错误信息指导性

风险点:     历史问题 #83 报告「pre-commit 插件使用报错 `Port number was not a decimal number`」，实际根因是「precommit 插件依赖 checkout，必须先执行 checkout」。报错误导——用户会去查端口号问题而非补 checkout step。这是典型的「错误信息指向了症状而非根因」问题。
预期系统行为: 当 Action 因缺少前置 step（如未 checkout）而失败时，错误信息应明确指示缺失前置条件（如 "This action requires a checkout step before it"），而非输出 Action 内部的低级错误。

Oracle 来源: 历史问题 #83; `testing-focus.md` §1（报错质量: "错在第几行、给不给可操作提示"）

验证要点:
  - [正向] 配置一个仅含 `uses: pre-commit` 不带 `uses: checkout` 的 job，验证失败消息是否提示需要 checkout。
  - [正向] 对其他有前置依赖的 Action（如需要 checkout 的 `cache`），同样验证。

可理解性判据:
  - 确定性: 报错是否指向「缺少 checkout」而非 Action 内部错误 (可字符串匹配判定)。
  - `eval: llm_assisted`: 同 INTENT-USE-001 三级评判。

优先级线索: P2 (影响特定 Action 组合场景；历史 #83 实证但频率相对低)
破坏级别:   none
来源输入:   历史问题 #83; `testing-focus.md` §1

---

意图 ID:    INTENT-USE-031
维度标签:   [usability, compatibility]
标题:       `uses` 中不支持表达式时的错误信息可诊断性

风险点:     历史问题 #82 报告「checkout 插件写法一样但有的执行成功有的执行失败」，根因是 `uses` 中不支持 `${{ atomgit.repository }}` 表达式，但报错没有明确点出这一点。用户看到「有时能用有时不能用」会认为是平台不稳定的 bug 而非语法限制。
预期系统行为: 当 `uses` 字段中使用了表达式语法（如 `uses: ${{ atomgit.repository }}/actions/my-action@main`），平台应在解析阶段明确报错：「`uses` 字段不支持 `${{ }}` 表达式」，并给出正确写法示例（相对路径 `./path/to/action` 或完整 `owner/repo/path@ref`）。

Oracle 来源: 历史问题 #82; `gitcode-spec/writing-pipelines/using-actions.md` §配置说明

验证要点:
  - [正向] 配置 `uses: ${{ env.MY_ACTION_PATH }}`, 验证解析阶段报错且指出 `uses` 不支持表达式。
  - [正向] 配置 `uses: ${{ atomgit.repository }}/actions/my-action@main`, 同上。

可理解性判据:
  - 确定性: 报错是否发生; 消息是否包含 'uses' + 'expression'/'expressions'/'${{ }}' 等关键词 (可判定)。
  - `eval: llm_assisted`: 同 INTENT-USE-001 三级评判。

优先级线索: P1 (关联 RISK-USE-01; 历史 #82 实证; 报错不明确导致用户误判为平台不稳定)
破坏级别:   none
来源输入:   历史问题 #82; `gitcode-spec/writing-pipelines/using-actions.md`

---

## C. 变量、参数与上下文调试摩擦

> 历史问题中变量/参数处理是最集中的问题域 (15+ 条，见 issues-encountered.md §高频问题特征)。以下选取最具「易用性」属性的子集 —— 那些导致用户困惑但本质上不是「功能没实现」而是「行为意外/报错不清」的场景。

---

意图 ID:    INTENT-USE-032
维度标签:   [usability]
标题:       `inputs` 字符串类型被隐式转换（如 "3.10" → 3.1）的可诊断性与文档提示

风险点:     历史问题 #75 报告 `inputs 中定义 string "3.10"，使用时变成了 3.10`——字符串被隐式转为浮点数，导致 "3.10" 变成 3.1。用户定义了 `type: string` 却发生了类型转换，这不仅是一个 bug，更是一个**文档未预警的隐式行为**——用户无法通过读文档预判此风险。
预期系统行为:
             - `inputs` 值必须严格保持字符串类型，不应发生隐式类型转换（"3.10" 始终为 "3.10"）。
             - 文档 (`configure-triggers.md` §workflow_dispatch) 应明确说明 inputs 为纯字符串传递，避免用户期望 `type: string` 有自动类型保护。

Oracle 来源: 历史问题 #75; `gitcode-spec/writing-pipelines/configure-triggers.md`

验证要点:
  - [正向] 定义 `workflow_dispatch.inputs.version.type: string, default: "3.10"`, 在 step 中用 `${{ inputs.version }}` 输出，验证输出为 "3.10"（严格字符串）。
  - [正向] 测试其他易被误转的字符串: "1e5", "true", "false", "null", "0xff"，验证全部保持字符串原样。
  - [负向] `${{ inputs.version == '3.10' }}` 不应因类型转换而失效。
  - [非功能] 文档中的 inputs 说明应警告用户所有值均为 string，如需数字比较需手动转换。

可理解性判据:
  - 确定性: 输出值是否与定义值完全一致 (字符串比对可判定); 文档是否有类型警告 (grep 可判定)。
  - 无需 llm_assisted。

优先级线索: P0 (数据完整性: 隐式类型转换可能导致 CI 逻辑错误而用户无法察觉; 历史 #75 实证)
破坏级别:   none
来源输入:   历史问题 #75; `gitcode-spec/writing-pipelines/configure-triggers.md`

---

意图 ID:    INTENT-USE-033
维度标签:   [usability, compatibility]
标题:       `env` 变量在 `workflow_call` 间的传递行为与报错

风险点:     历史问题 #76 报告「主 workflow 定义的 env 作为入参调用另一个 yml，传进去的参数取不到」。`workflow_call` 是 GitCode 的可重用工作流机制，但与 GitHub 的 `workflow_call` 在 env 传递语义上可能有差异。用户期望调用方 env 能透传到被调用 workflow——若不行，这是迁移摩擦；若行为没有明确文档化，这是文档缺失。
预期系统行为:
             - 文档应明确声明 `workflow_call` 场景下 env 的传递/隔离语义: 调用方 env 是否对 callee 可见？若不透传，需要通过 `inputs` 显式传递哪些 env 值？
             - 若 callee 需要调用方 env 值但未通过 inputs 传递，应有明确的诊断信息（而非 "parameter not found" 或空值静默）。

Oracle 来源: 历史问题 #76; `gitcode-spec/writing-pipelines/configure-triggers.md` §workflow_call; `github-reference/reference/workflow-syntax.md` (GitHub `workflow_call` 语义作对照)

验证要点:
  - [正向] 定义主 workflow 有 `env: MY_VAR: hello`，子 workflow 在 step 中 `echo $MY_VAR`。若不透传: 子 workflow 应收到空值且文档应明确此行为；若透传: 子 workflow 应收到 "hello"。
  - [正向] 通过 `workflow_call.inputs` 显式传递 `MY_VAR`，验证子 workflow 可用 `${{ inputs.MY_VAR }}` 正确获取。
  - [非功能] 文档应有明确的「env 传递模型」图表或说明。

可理解性判据:
  - 确定性: 实际行为 (透传 vs 不透传) 可观测; 文档是否覆盖 (可判定)。
  - `eval: llm_assisted`: 若文档缺失此说明，评估用户从现有文档是否能推断出正确传递方式。

优先级线索: P1 (关联 RISK-USE-01; 历史 #76 实证; workflow_call 是高频复用机制)
破坏级别:   none
来源输入:   历史问题 #76; `gitcode-spec/writing-pipelines/configure-triggers.md`; `github-reference/reference/workflow-syntax.md`

---

意图 ID:    INTENT-USE-034
维度标签:   [usability, compatibility]
标题:       系统上下文变量命名体系的一致性（避免两套系统共存）

风险点:     历史问题 #3 和 #20 揭示了同一类困惑: 存在 pipeline_* 系变量和 atomgit.* 系变量两套系统、且字段不完整。用户不知道「到底该用哪一套」——文档说 atomgit.*，但历史上下文里又有 pipeline_run_id 等字段。
             COMPAT-NOTES.md §2 的差异也说明存在 `ATOMGIT_*` vs `GITHUB_*` 的命名差异，但历史 #3/#20 暴露的是 GitCode 内部的变量体系不统一。
预期系统行为: 文档应始终引用 `atomgit.*` 上下文变量，不应在示例中混用 pipeline_* 变量。所有有效上下文字段应在 `context.md` 中有完整枚举。不应存在「文档上说用 A，但实际只有 B 好用」的情况。

Oracle 来源: 历史问题 #3, #20; COMPAT-NOTES.md §2; `gitcode-spec/syntax-reference/context.md`

验证要点:
  - [正向] 全文搜索 `gitcode-spec/` 下所有 `.md` 文件，列出仍含 `pipeline_*` 变量引用（非对比/非弃用标注上下文）的实例。
  - [正向] 对比 `context.md` 声明的 atomgit 上下文字段列表与 `runtime-environment-variables.md` 的 `ATOMGIT_*` 列表，验证一致性和完整覆盖率。
  - [非功能] 每个声明的 atomgit 上下文字段应有明确的含义说明、示例值、可用性范围 (workflow/job/step level)。

可理解性判据:
  - 确定性: 文档中 pipeline_* 残留引用数量; 字段列表一致性 (grep+diff 可判定)。
  - 无需 llm_assisted。

优先级线索: P2 (文档缺陷; 长期改善迁移体验和开发者心智模型)
破坏级别:   none
来源输入:   历史问题 #3, #20; COMPAT-NOTES.md §2; `gitcode-spec/syntax-reference/context.md`; `gitcode-spec/action-development/runtime-environment-variables.md`

---

意图 ID:    INTENT-USE-035
维度标签:   [usability]
标题:       可重用工作流 (workflow_call) 的 YAML 缓存陈旧问题——用户可见的诊断

风险点:     历史问题 #85 报告「子 workflow 更新后从日志看用的还是旧代码（yml 缓存问题）」。这表明 workflow_call 调用的子 workflow 存在缓存，更新后不立即生效。用户改完子 workflow 后在主 workflow 看到的是过期行为，会以为是「我的改动没写对」然后反复无效调试。
预期系统行为:
             - 若存在 workflow_call 缓存机制: 文档应明确声明缓存 TTL 和强制刷新的方法（如通过某参数或重新保存子 workflow）。
             - 当子 workflow 被调用时所用版本与最新版本不一致，日志中应有明确的版本标注（如 "Using callee workflow @ commit a1b2c3d"）。
             - 理想情况: 缓存应在子 workflow 源文件保存后立即失效。

Oracle 来源: 历史问题 #85; `gitcode-spec/writing-pipelines/configure-triggers.md` §workflow_call

验证要点:
  - [正向] 创建 A → B 的 workflow_call 链。先运行一次，之后修改 B 的 step 输出内容，再次触发 A，验证 B 的新输出是否生效（即缓存是否刷新）。
  - [正向] 若存在缓存延迟，日志/详情页应明确标注 B 的调用版本 (SHA / 时间戳)。
  - [非功能] 若缓存不刷新，应有可见的告警或 mechanism 提示用户手动刷新。

可理解性判据:
  - 确定性: 修改后 B 的输出是否更新 (可观测); 日志是否标注调用版本 (可字符串匹配判定)。
  - `eval: llm_assisted`: 若存在缓存且无版本标注，评估用户能否从日志中推断出「用的是旧版本」。

优先级线索: P1 (关联 RISK-USE-01; 历史 #85 实证; 静默缓存陈旧直接导致无效调试循环)
破坏级别:   none
来源输入:   历史问题 #85; `gitcode-spec/writing-pipelines/configure-triggers.md`

---

## D. Action/Plugin 发现与文档

> 历史问题 #18（插件信息陈旧）、#47（搜索不到插件）、#50（setup-* 插件不说明支持版本）表明 Action 生态的**可发现性**和**文档完整性**有显著缺口——用户知道想要什么但找不到、或找到了但信息不足。

---

意图 ID:    INTENT-USE-036
维度标签:   [usability]
标题:       setup-* 系列 Action 的版本支持文档完整性

风险点:     历史问题 #50 报告「setup-* 插件未说明支持安装的版本，自己指定版本经常下载失败」。setup-node、setup-python、setup-java、setup-go 是最常用的开发环境 Action，若文档不列支持版本，用户只能试错——指定一个版本 → 提交 → 失败 → 换版本 → 提交 → ...，极度低效。
预期系统行为: 每个 setup-* Action 的文档应明确列出支持的版本列表，且该列表应与 Action 实际支持范围一致。用户指定未支持的版本时，应有明确的错误提示指出「不支持的版本 X，支持: Y, Z...」。

Oracle 来源: 历史问题 #50; `gitcode-spec/writing-pipelines/using-actions.md`; `gitcode-spec/reference/runner-images-tools.md`

验证要点:
  - [正向] 检查 setup-node 文档是否列出支持的 Node.js 版本；对比实际支持的版本（通过 `node-version: "999"` 触发报错看合法值列表）。
  - [正向] 同理检查 setup-python、setup-java、setup-go。
  - [正向] 对每个 setup-* Action，指定一个文档声称支持但实际不支持的版本（或反之），记录差异。
  - [非功能] 指定不支持的版本时，错误消息应含合法版本列表。

可理解性判据:
  - 确定性: 文档是否列出版本列表 (grep 可判定); 实际支持版本与文档是否一致 (行为比对可判定)。
  - `eval: llm_assisted`: 若不支持的版本报错缺少合法版本列表，评估用户能否从报错信息自行找到正确版本 (0=不能, 1=需搜索, 2=消息直接给)。

优先级线索: P1 (历史 #50 实证; setup-* 系列是最常用的 Action，版本支持是使用第一步)
破坏级别:   none
来源输入:   历史问题 #50; `gitcode-spec/writing-pipelines/using-actions.md`; `gitcode-spec/syntax-reference/runner-images-tools.md`

---

意图 ID:    INTENT-USE-037
维度标签:   [usability]
标题:       Action 市场的搜索可发现性

风险点:     历史问题 #47 报告「Actions 市场中搜索 upload-artifact 插件无法找到详细描述；文件上传后存储桶地址也无从得知」。搜索按 display name 找不到意味着用户只能通过精确插件名搜索，但新用户不知道精确名称。此外，插件的「详细描述」「输入参数」「输出」等信息在搜索结果中是否可见决定用户能否快速评估是否适用。
预期系统行为:
             - Action 市场搜索应支持按 display name（如 "上传制品" / "upload artifact"）和功能描述进行模糊匹配。
             - 搜索结果应展示每个 Action 的基本信息: 名称、简要描述、作者、最近更新时间。
             - 每个 Action 的详情页应有完整的 inputs/outputs 说明和使用示例。

Oracle 来源: 历史问题 #47; `gitcode-spec/writing-pipelines/using-actions.md`; GitHub Actions Marketplace 搜索体验作参照。

验证要点:
  - [正向] 在 Action 市场/选择界面搜索 "upload"，验证 upload-artifact 出现在结果中且含描述。
  - [正向] 搜索中文关键词 "上传"，验证是否有合理结果。
  - [正向] 点击 upload-artifact 进入详情，验证有 inputs（name, path 等）和 outputs 的完整说明。

可理解性判据:
  - 确定性: 搜索结果是否包含预期 Action (可判定); 详情页是否含 inputs/outputs 说明 (可逐项判定)。
  - `eval: llm_assisted`: 搜索结果的相关性和排序是否合理 (需整体评估)。

优先级线索: P2 (历史 #47 实证; 体验改善但不阻塞核心功能)
破坏级别:   none
来源输入:   历史问题 #47; `gitcode-spec/writing-pipelines/using-actions.md`

---

意图 ID:    INTENT-USE-038
维度标签:   [usability]
标题:       Workflow 编辑器中 Action 版本信息的时效性

风险点:     历史问题 #18 报告「yml 编辑 workflow 时插件详情页默认展示最初版本信息，容易误导」。用户在编辑 workflow 时看到的 Action 版本信息可能是过时的，导致用户以为最新版本仍是旧版——进而使用旧版本引用，错过重要更新。
预期系统行为: workflow 编辑器（YAML 编辑页面或 Action 选择器）应始终展示每个 Action 的**最新可用版本**（含版本号和发布日期）。若支持历史版本查看，默认展示最新。

Oracle 来源: 历史问题 #18

验证要点:
  - [正向] 在有多个版本的 Action 上（如果有），进入 workflow 编辑器，验证默认展示的 Action 版本信息是最新的。
  - [正向] 若 Action 最近更新过，验证编辑器中的版本信息在 24 小时内同步更新。

可理解性判据:
  - 确定性: 编辑器展示的版本号是否与最新版本一致 (可对比 API 返回值判定)。
  - 无需 llm_assisted。

优先级线索: P2 (历史 #18 实证; 影响版本选择决策但可通过查看 Action 仓库确认)
破坏级别:   none
来源输入:   历史问题 #18

---

## E. 界面展示与状态反馈

> 历史问题 #24（PR 检查未展示）、#34（重跑变更执行人）、#56（Summary 链接被套无关域名）、#72（插件 exit code 正确但状态错误）、#73（Summary 不显示）、#95（多任务布局问题）构成界面维度的用户困扰。

---

意图 ID:    INTENT-USE-039
维度标签:   [usability]
标题:       PR 页面的 Checks 状态与流水线执行记录的完整性

风险点:     历史问题 #24 报告「PR 检查未展示代码化流水线的执行记录」。文档 `view-run-results.md` 声称「PR 页面的 Checks 标签页汇总该 PR 触发的所有流水线运行结果」。若 PR 页面不展示流水线结果，评审人需要手动切到 Actions 标签页查找对应 run，割裂代码评审流程。
预期系统行为: 每个 PR 的 Checks 标签页应展示该 PR 触发的所有 workflow 运行，每条包含 workflow 名称、运行状态、触发 commit、完成时间，并可直接点击进入运行详情。

Oracle 来源: 历史问题 #24; `gitcode-spec/running-pipelines/view-run-results.md` §入口三

验证要点:
  - [正向] 在 PR 分支 push 代码触发 workflow，进入 PR 页面 → Checks 标签，验证有对应 run 记录且状态正确。
  - [正向] 点击 run 记录，验证跳转到正确的运行详情页。

可理解性判据:
  - 确定性: Checks 标签是否存在; run 记录是否展示; 点击是否跳转正确 (可逐个判定)。
  - 无需 llm_assisted。

优先级线索: P1 (关联 RISK-USE-01; 历史 #24 实证; PR check 是代码评审核心流程)
破坏级别:   none
来源输入:   历史问题 #24; `gitcode-spec/running-pipelines/view-run-results.md`

---

意图 ID:    INTENT-USE-040
维度标签:   [usability]
标题:       Step 级别执行结果状态回写的准确性（exit code vs 展示状态一致性）

风险点:     历史问题 #72 报告「codecheck 插件检查结果为不通过时，插件仍然执行成功」——即 Action 内部有 exit code > 0（或不通过标记），但 step 状态仍标注为 success。用户看 Actions 列表全绿，但实际上关键检查已失败——这是最危险的「假绿」场景。
预期系统行为: step 的成功/失败状态必须与其内部执行的**实际结果**一致。若 Action 返回非零 exit code，step 必须标记为 failure。若 Action 有自定义的「不通过」标记（非 exit code），Action 应能通过 `ATOMGIT_OUTPUT` 设置输出供后续判断，但 step 状态仍需反映 exit code。

Oracle 来源: 历史问题 #72; `testing-focus.md` §9（运行状态机）

验证要点:
  - [正向] 使用 `run: exit 1` 的 step，验证 step 状态为 failure（非 success）。
  - [正向] 使用一个已知「检查不通过但返回 exit 0」的 Action（如某些 linter 的 warning 模式），验证 step 状态与其文档声明行为一致。
  - [负向] step 不应在 exit code != 0 时仍显示 success 状态。

可理解性判据:
  - 确定性: exit code 与 step 状态是否一致 (可 shell 脚本断言)。
  - `eval: llm_assisted`: 若存在 exit code=0 但语义上应视为失败的情况 (如 Action 使用 output 传递失败状态)，评估 status 回写是否合理。

优先级线索: P1 (历史 #72 实证; "假绿" 直接导致 CI 信噪比失效——用户将不再信任绿色徽章)
破坏级别:   none
来源输入:   历史问题 #72; `testing-focus.md` §9; `gitcode-spec/running-pipelines/view-run-results.md`

---

意图 ID:    INTENT-USE-041
维度标签:   [usability]
标题:       Step Summary 的展示完整性与链接有效性

风险点:     历史问题 #73 报告「codecheck 插件检查结果 summary 未显示」、#56 报告「Summary 里的链接会被套一层无关的域名」。Summary 是 workflow 运行结果的核心可读性输出（类似 GitHub 的 Job Summary），若: (1) summary 内容不显示 → 用户不知道检查结果细节; (2) 链接被 rewrite → 用户点击后跳到非预期页面。
预期系统行为:
             - 通过 `>> $ATOMGIT_STEP_SUMMARY` 写入的 Markdown 内容应在运行详情页的 Summary 区域完整渲染。
             - Summary 中的链接不应被平台注入无关域名或跳转中间页; 应保持原始链接或明确标注「外部链接」。
             - 支持 Markdown 表格、列表、代码块等基本格式。

Oracle 来源: 历史问题 #56, #73; `gitcode-spec/syntax-reference/workflow-commands.md` §5.4

验证要点:
  - [正向] 在 step 中写入 `echo "## Test Results" >> $ATOMGIT_STEP_SUMMARY` + `echo "|Status|Count|" >> $ATOMGIT_STEP_SUMMARY` + `echo "|---|---|" >> $ATOMGIT_STEP_SUMMARY` + `echo "|PASS|10|" >> $ATOMGIT_STEP_SUMMARY`, 验证运行详情页 Summary 区域渲染为 Markdown 表格。
  - [正向] 在 Summary 中写入 `[external link](https://example.com)`, 验证链接可直接访问且不被注入中间页。
  - [非功能] 写入含中文、emoji、代码块的 Markdown, 验证渲染正确。

可理解性判据:
  - 确定性: Summary 内容是否展示 (可截图判定); 格式渲染是否正确 (可目视判定); 链接 href 是否被改写 (可 HTML 检查判定)。
  - 无需 llm_assisted。

优先级线索: P1 (历史 #56/#73 实证; Summary 是 workflow 结果的可读化核心; 链接改写涉及安全合规)
破坏级别:   none
来源输入:   历史问题 #56, #73; `gitcode-spec/syntax-reference/workflow-commands.md`; `testing-focus.md` §9

---

意图 ID:    INTENT-USE-042
维度标签:   [usability]
标题:       重新运行 (Re-run) 后执行人身份的展示一致性

风险点:     历史问题 #34 报告「pr 创建的 actions，其他人手动重新执行后，原 pr 提交人账号会变更为执行人」。从审计角度这可能合理（显示最新执行人），但从用户体验角度: 原 PR 提交人看到「自己的 run 被不知道谁重跑了而且名字也变了」会困惑。界面应区分「原始触发人」与「最新执行人」。
预期系统行为:
             - 运行列表和详情页应同时展示「触发人」(actor) 和「最新执行人」(若被他人 re-run)。
             - 若 run 被重新执行，应有明确的 re-run 标记（如 "Re-run by @userB from #42"）而非仅替换 actor。
             - 历史执行记录（若有功能）应在后续上线时关联展示。

Oracle 来源: 历史问题 #34; `gitcode-spec/running-pipelines/rerun-failed-jobs.md`

验证要点:
  - [正向] 用户 A 提交 PR 触发 workflow，用户 B 手动 re-run，验证运行列表/详情页仍显示用户 A 为「触发人」，同时显示用户 B 为「重新执行人」。
  - [正向] 验证详情页有 re-run 标记和来源 run 编号。

可理解性判据:
  - 确定性: 原始触发人和最新执行人是否区分展示 (可界面截图判定)。
  - `eval: llm_assisted`: 若二合一，评估普通用户是否会产生混淆。

优先级线索: P2 (历史 #34 实证; 体验改善; 审计维度上当前行为可能有其合理性)
破坏级别:   none
来源输入:   历史问题 #34; `gitcode-spec/running-pipelines/rerun-failed-jobs.md`

---

意图 ID:    INTENT-USE-043
维度标签:   [usability]
标题:       多 Job Workflow 的运行详情页布局可用性

风险点:     历史问题 #95 报告「优化流水线展示界面任务布局，11 个任务不缩放页面展示不全」，答复为「鼠标可以拖动」。11 个 job 是 matrix 展开场景的常见规模（如 3 OS x 4 语言版本 = 12 jobs）。若需拖动/缩放才能看到全部 job、且无概览模式，用户无法快速评估整体运行状态。
预期系统行为:
             - 默认视口（1920x1080）应能一览至少 12 个 job 的状态（通过合理卡片大小/排列）。
             - 若 job 数量超过一屏，应有「折叠已完成/all green」的批量收起功能或概览摘要（如 "10/12 passed, 1 failed, 1 running"）。
             - 水平滚动应保留 job 名称列固定 (sticky)。

Oracle 来源: 历史问题 #95; `testing-focus.md` §9

验证要点:
  - [正向] 构造 12-job workflow（如 3x4 matrix），在 1920x1080 视口下查看运行详情页，验证所有 job 状态是否一览可见（或可通过概览 bar 了解整体状态）。
  - [非功能] 若有大量 job (>= 20)，页面不应出现布局破坏（如重叠、溢出隐藏 job）。

可理解性判据:
  - 确定性: 在标准视口下是否所有 job 卡片可见 (可截图判定); 概览摘要是否存在 (可界面检查判定)。
  - `eval: llm_assisted`: 整体布局的视觉可用性评估 (需截图评判: 0=混乱, 1=可用但挤, 2=清晰)。

优先级线索: P2 (历史 #95 实证; 体验改善; 有 workaround: zoom out 或拖动)
破坏级别:   none
来源输入:   历史问题 #95; `testing-focus.md` §9

---

## F. 迁移摩擦补充场景

> 上一 run 的 USE-014~019 已覆盖端到端迁移主路径和关键差异点（runs-on/permissions/builtin actions/inputs 类型/迁移指南）。以下补充从历史实证 + COMPAT-NOTES 交叉验证发现的两个额外摩擦面。

---

意图 ID:    INTENT-USE-044
维度标签:   [usability, compatibility]
标题:       仓库名上下文字段缺失——从 URL 解析 vs 系统变量不一致

风险点:     历史问题 #43 报告「pr/push 触发，仓库名和仓库链接中的仓库不一致，没有能直接获取链接中仓库名的系统变量」。用户需要仓库 URL 中的名称做 artifact 命名、通知消息等，但 `atomgit.repository` 的值与仓库 URL 中的名称可能不一致，且没有独立的 `atomgit.repository_url_name` 或类似字段。用户被迫手动解析 URL。
预期系统行为:
             - `atomgit.repository` 的值应与仓库 URL 中的路径一致（如 URL `owner/repo` → `atomgit.repository` 返回 `owner/repo`）。
             - 若存在 URL name 与 repo name 不同的场景（如重命名后 URL 保留旧 path），应提供 `atomgit.repository_url` 或 `atomgit.repository_full_name` 等字段。

Oracle 来源: 历史问题 #43; `gitcode-spec/syntax-reference/context.md`; `github-reference/reference/contexts.md` (GitHub `github.repository` 对照)

验证要点:
  - [正向] 查看 `atomgit.repository` 返回值，与仓库浏览器地址栏中的 `owner/repo` 路径对比，验证一致性。
  - [正向] 若仓库被重命名，验证 `atomgit.repository` 是否更新为新名。
  - [非功能] 若存在不一致: 是否提供额外字段供用户获取 URL 路径中的仓库名。

可理解性判据:
  - 确定性: 两个来源的仓库名是否一致 (字符串比对可判定); 额外字段是否存在 (grep context 文档可判定)。
  - `eval: llm_assisted`: 若不一致且无额外字段，评估用户从现有上下文字段能否推导出正确的仓库 URL name。

优先级线索: P2 (历史 #43 实证; 影响自动化脚本但可 workaround 手动解析)
破坏级别:   none
来源输入:   历史问题 #43; `gitcode-spec/syntax-reference/context.md`; `github-reference/reference/contexts.md`

---

意图 ID:    INTENT-USE-045
维度标签:   [usability, compatibility]
标题:       首次开启 Actions 后的 Workflow 自动识别——新仓库初始体验

风险点:     历史问题 #17 报告「新建代码仓同步代码后，Actions 不识别流水线配置；需要手动修改一次库上 yml 文件后才能识别到」。这意味着用户新建仓库、推送含 `.gitcode/workflows/ci.yml` 的代码后，Actions 标签页可能一片空白。新用户第一印象是「我的配置有问题」或「功能坏了」。
预期系统行为:
             - 仓库首次推送含 `.gitcode/workflows/*.yml` 的提交后，Actions 标签页应在**合理时间内**（如 1 分钟内）识别并列出所有 workflow。
             - 若存在识别延迟，界面应有明确的状态提示（如 "Scanning for workflows..."）。
             - 不应需要用户手动修改 YAML 文件才能触发识别。

Oracle 来源: 历史问题 #17

验证要点:
  - [正向] 新建仓库 → push 含 3 个 workflow 文件的提交 → 立即进入 Actions 标签页，观察 workflow 列表出现时间。
  - [正向] 若首次出现延迟，验证是否有扫描中的状态提示。
  - [负向] 不应需要用户进入编辑再保存才触发识别。

可理解性判据:
  - 确定性: workflow 是否被识别 (Actions 列表是否非空可判定); 识别耗时 (秒表计时可判定)。
  - 无需 llm_assisted。

优先级线索: P1 (关联 RISK-USE-01; 历史 #17 实证; 新用户第一印象——迁移成功与否的第一个检查点)
破坏级别:   none
来源输入:   历史问题 #17; `gitcode-spec/writing-pipelines/workflow-file-location-structure.md`

---

意图 ID:    INTENT-USE-046
维度标签:   [usability, compatibility]
标题:       Action 运行时 `runs.using` 声明的实际支持范围与文档一致性

风险点:     COMPAT-NOTES.md §10 指出 Action 运行时 `runs.using` 文档仅列 `node16`，而 GitHub 支持 `node20`/`docker`/`composite`。如果用户开发 Action 时按 GitHub 的 `node20` 或 `composite` 写法，且文档没有明确说不支持——用户会在本地测试通过、上传后运行时失败，且报错可能不直观。
预期系统行为:
             - 文档 (`action-development/top-level-fields.md`, `plugin-development-guide.md`) 应明确枚举 GitCode 支持的 `runs.using` 值列表。
             - 若 `node20` 不支持，使用它的 Action 应有明确的报错消息（如 "runs.using 'node20' is not supported. Supported: node16"）。
             - 历史问题 #41 指出 composite action 当前不支持——文档须标注「暂不支持」。

Oracle 来源: COMPAT-NOTES.md §10; 历史问题 #41; `gitcode-spec/action-development/top-level-fields.md`; `gitcode-spec/action-development/plugin-development-guide.md`

验证要点:
  - [正向] 创建一个 `runs.using: 'node20'` 的 Action 并引用，观察运行时报错质量。
  - [正向] 创建一个 `runs.using: 'composite'` 的 Action 并引用，同上。
  - [正向] 检查文档中 `runs.using` 的枚举列表与实际支持是否一致。

可理解性判据:
  - 确定性: 报错是否发生; 消息是否含不支持的值 + 支持的值列表 (可判定)。
  - `eval: llm_assisted`: 同 INTENT-USE-001。

优先级线索: P1 (关联 RISK-USE-01; 历史 #41 实证; 影响 Action 开发者)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §10; 历史问题 #41; `gitcode-spec/action-development/top-level-fields.md`; `github-reference/reference/workflow-syntax.md`

---

## 覆盖度自检

| 维度子类 | 覆盖 intent | 说明 |
|---|---|---|
| **日志查看体验** | INTENT-USE-024/025/026/027 | 下载可用性、加载性能、噪音过滤、顺序一致性 |
| **运行时错误信息** | INTENT-USE-028/029/030/031 | 手动触发参数、Runner 准备、Action 前置依赖、uses 表达式 |
| **变量/参数调试** | INTENT-USE-032/033/034/035 | 类型转换、env 传递、变量体系一致性、yml 缓存陈旧 |
| **Action/Plugin 发现** | INTENT-USE-036/037/038 | setup-* 版本文档、市场搜索、编辑器版本信息 |
| **界面展示** | INTENT-USE-039/040/041/042/043 | PR Checks、状态回写、Summary、Re-run 身份、多 Job 布局 |
| **迁移摩擦补充** | INTENT-USE-044/045/046 | 仓库名上下文、首次识别、runs.using 支持范围 |

## 风险覆盖核对

| 风险 ID | 覆盖 intent | 说明 |
|---|---|---|
| RISK-USE-01 (迁移报错不指明 GitCode 差异) | USE-028/029/030/031/032/033/035/044/045/046 | 10 条 intent 从运行时维度补充迁移报错质量 |

## 历史问题覆盖核对（issues-encountered.md 高频模式）

| 模式 | 历史问题编号 | 覆盖 intent |
|---|---|---|
| 日志可下载性 | #6 | INTENT-USE-024 |
| 日志加载慢 (7min) | #14 | INTENT-USE-025 |
| 无关日志多 | #28 | INTENT-USE-026 |
| 日志乱序 | #80 | INTENT-USE-027 |
| 日志不显示 | #81 | INTENT-USE-027 |
| 手动触发无报错 | #23 | INTENT-USE-028 |
| 镜像拉取失败无日志 | #52, #89 | INTENT-USE-029 |
| 报错误导（pre-commit 缺 checkout） | #83 | INTENT-USE-030 |
| uses 不支持表达式 | #82 | INTENT-USE-031 |
| 字符串类型隐式转换 ("3.10"→3.1) | #75 | INTENT-USE-032 |
| workflow_call env 传递失败 | #76 | INTENT-USE-033 |
| 系统变量两套体系 | #3, #20 | INTENT-USE-034 |
| yml 缓存陈旧 | #85 | INTENT-USE-035 |
| setup-* 版本未文档化 | #50 | INTENT-USE-036 |
| 市场搜索不到插件 | #47 | INTENT-USE-037 |
| 插件版本信息陈旧 | #18 | INTENT-USE-038 |
| PR Checks 未展示 | #24 | INTENT-USE-039 |
| 假绿 (exit code 0 但检查未过) | #72 | INTENT-USE-040 |
| Summary 不显示 / 链接被套域名 | #56, #73 | INTENT-USE-041 |
| Re-run 后执行人变更 | #34 | INTENT-USE-042 |
| 多 Job 页面布局 | #95 | INTENT-USE-043 |
| 仓库名上下文不一致 | #43 | INTENT-USE-044 |
| 首次 Actions 不识别 | #17 | INTENT-USE-045 |
| runs.using 支持范围 / composite | #41 | INTENT-USE-046 |

## 与上一 run 的差异说明

| | 上一 run (USE-001~023) | 本 run (USE-024~046) |
|---|---|---|
| 核心输入 | COMPAT-NOTES + gitcode-spec | **+ issues-encountered.md (95 条)** |
| 聚焦阶段 | YAML 解析/静态校验阶段 | **运行时** + **调试循环** + **界面交互** |
| 日志维度 | 未覆盖 | 4 条 (下载/性能/噪音/顺序) — 用户最大痛点 |
| 运行时报错 | 未覆盖 | 4 条 (手动触发/Runner准备/Action前置依赖/uses表达式) |
| 变量调试 | 未覆盖 (上一 run 认为属 completeness) | 4 条 (类型转换/env传递/体系一致/cache陈旧) — 从易用性视角切入 |
| Action 生态 | 仅覆盖 uses 引用格式差异 | 3 条 (版本文档/市场搜索/编辑器时效) |
| 界面反馈 | 仅覆盖状态机和排队 | 5 条 (PR Checks/假绿/Summary/身份/布局) |
