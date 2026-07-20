# 历史问题记录 · 遇到的问题

> 来源：`gitcode issues.xlsx` 工作表「遇到的问题」，101 行，2026-07-20 导出
> 预处理说明：图片引用（`DISPIMG(...)`）已忽略，仅保留文字描述与处理结论
> 用途：作为全体 agent（尤其 security / reliability / usability / compat-diff）生成 intent 的实证输入

---

## 问题清单

| # | 试点产品 | 问题描述 | 处理进展 | 结论 |
|---|---|---|---|---|
| 1 | mindcluster | 配置好yml, 开启白名单，触发之后Actions下面没有记录 | 5/20：非问题关闭。5/13: 定位中，只支持单源，临时去掉sources字段保存下就有了 | — |
| 2 | mindcluster | yml中with部分参数无法渲染，导致任务失败卡住 | 5/13：已优化。5/14: 新包测试无问题，问题解决 | — |
| 3 | mindcluster | gitcode action测试，类似pipeline_id/pipeline_run_id/build_num参数没有协调好，当前提供的系统参数对应不上，无法通过这些信息区分具体的workflow | 6.12：已上线。atomgit.workflow_run_id、atomgit.run_number已下发，atomgit.job_run_id待适配 | 以atomgit上下文参数为准，如有遗漏参数提诉求 |
| 5 | MindCluster | job中经常出现异常提示 | 6/2：GitCode反馈已解决 | 开发内部对逻辑进行排查 |
| 6 | MindCluster | job的日志无法下载，日志很长翻起来体验不佳，没有对应的下载按钮 | 6/2：问题合并至32号。近两天会上线job级别日志下载功能；查看日志时支持从后往前加载 | — |
| 7 | MindIE-SD | 配置3个并行任务，2个runner空闲，自定义runner+image任务触发后一直显示运行中/排队中，1h后失败，日志只有1行 | label问题，已处理 | — |
| 8 | MindIE-SD | 默认runner+自定义image模式还不支持 | 6.10：方案需要改动，11号上线 | 调度存在问题，定位中 |
| 9 | MindIE-SD | pr触发上午可以，下午就不行了 | 语法格式问题，close | — |
| 10 | MindIE-SD | 同时触发多个records，停止指定record时不管用，总是以出栈方式停止最上面的 | 体验问题，向上反映 | — |
| 11 | MindIE-SD | 同一私密参数，在一个job的两个相邻step引用，第二次报bad substitution | 6/5：已解决 | 单点问题例行跟踪 |
| 12 | pytorch | workflow运行中有两个job持续处于等待状态，重试也一样等待，但资源池已释放 | 5/30：已修复 | — |
| 13 | pytorch | 新增校验yaml的能力，但影响第一行代码的阅读 | — | wget |
| 14 | pytorch | 任务失败查看日志时，日志加载时间过长，大约7min才能完全加载好 | 近两天会上线job级别日志下载功能 | — |
| 15 | pytorch | 自定义镜像+自定义资源池环境执行完编译后执行obs上传命令失败 | 6/1：验证发现是网络问题，先用obs插件代替 | 待单点验证 |
| 16 | pytorch | obs上传插件不支持按照目录上传，目录为变量则无法解析 | 6/1: 上传目录需使用atomgit上下文如`${{atomgit.workspace}}`。最新版已支持按目录上传 | — |
| 17 | MindIE-SD | 新建代码仓同步代码后，Actions不识别流水线配置；需要手动修改一次库上yml文件后才能识别到 | — | 存在文件处理上限，后续优化 |
| 18 | pytorch | yml编辑workflow时插件详情页默认展示最初版本信息，容易误导 | 6.16：当前只展示最新插件版本 | 长期：支持多版本展示但默认展示最新 |
| 19 | pytorch | job执行之后概率性展示异常信息，刷新后又恢复正常 | — | 开发内部对逻辑进行排查 |
| 20 | pytorch | atomgit上下文中不支持workflow启动时间字段，存在4.4.5系统变量和atomgit上下文两套系统变量 | 6/4：验证没问题 | 以atomgit上下文参数为准 |
| 21 | pytorch | 问题同20（atomgit上下文字段缺失） | 6/5：已修复 | — |
| 22 | openlibing | fork模式下提PR触发不了流水线 | 已适配，待验证 | 已实现，后端更新，待验证 |
| 23 | openlibing | 手动传参时输入参数后无法触发流水线 | — | 输入参数未指定type类型导致流水线无法启动，建议添加报错信息 |
| 24 | openlibing | PR检查未展示代码化流水线的执行记录 | 6.15：已上线广州 | 需要gitcode调流水线接口展示 |
| 25 | openlibing | checkout插件不支持PR预合并 | — | 不支持PR预合并 |
| 26 | openlibing | setup-python插件指定版本时异常 | 需要指定执行机`runs-on: ['codearts-hosted', 'ubuntu-latest', x64, 'large']` | 当前支持9个python版本 |
| 27 | openlibing | 插件触发uses暂不支持使用gitcode代码仓地址执行 | — | 6.30实现 |
| 28 | openlibing | 无关日志较多 | 低优先级，630后评估 | — |
| 29 | openlibing | 任务间依赖关系缺失 | yml链接已提供 | 功能未实现 |
| 30 | openlibing | workflow_call无法拉起子任务，但显示已完成 | — | bug待修复 |
| 31 | openlibing | official_checkout,official_shell等官方插件命名建议不要带official | 6.8 全量完成 | — |
| 33 | MindIE-SD | fork仓提PR，PR在主仓，actions在个人仓，获取不到变量及环境配置 | 6/4：已解决。pr提交后actions在主仓触发 | — |
| 34 | MindIE-SD | pr创建的actions，其他人手动重新执行后，原pr提交人账号会变更为执行人 | 显示最新执行人是合理的（审计角度）。后续会做重试执行历史记录功能 | — |
| 35 | openlibing | 自定义插件本地无法触发 | 6.4：已适配 | 已实现 |
| 36 | openlibing | setup-node插件使用报错 | 6.3：已修复 | — |
| 37 | pytorch | 组织下定义了runner分组，给代码仓加了权限但代码仓无法使用runner，调度会失败 | 6/3：已解决 | — |
| 38 | MindIE-SD | 使用自定义`${MindIE-SD_REPOSITORY_NAME}`发生异常，参数名中"-"中划线导致参数异常 | shell中`${aaa-bbb}`的"-"后边是默认值 | — |
| 39 | MindIE-SD | 流水线状态异常：显示取消成功，任务运行状态仍是队列中 | 6/4：已解决 | — |
| 40 | openlibing | 无法查看报错信息，不清楚违规信息的评判标准是什么 | 6.9：已优化上线 | — |
| 41 | pytorch | 引用仓库内自定义action，任务执行失败且无报错信息 | 当前不支持复合操作（composite action）特性 | 流水线复合操作 |
| 42 | MindIE-SD | 使用wget下载包出现概率性失败 | 自定义资源池偶现网络问题 | — |
| 43 | MindCluster | pr/push触发，仓库名和仓库链接中的仓库不一致，没有能直接获取链接中仓库名的系统变量 | 建议从仓库地址中解析 | — |
| 44 | MindIE-SD | 自有资源池拉取自定义镜像报错 | 6/10：已解决 | — |
| 45 | MindCluster | 手动执行流水线，上下文没有下发仓库别名 | — | — |
| 46 | MindIE-SD | env中定义参数，run中通过`${{env.参数名}}`调用，打印输出为空 | 6.22: 已验证可用。6/5：暂不支持，630前支持 | — |
| 47 | openlibing | Actions市场中搜索upload-artifact插件无法找到详细描述；文件上传后存储桶地址也无从得知 | gitcode页面不支持通过display name查找 | — |
| 48 | openubmc | kubernetes-Runner会被调度到arm节点上 | 6.25：需改镜像方式，现在不支持选架构 | — |
| 49 | openlibing | 自定义资源池无法直接获取智算资源，只能通过插件获取 | — | — |
| 50 | openlibing | setup-* 插件未说明支持安装的版本，自己指定版本经常下载失败 | 6.15：已准备好版本说明。需使用正确的插件 | — |
| 51 | openlibing | fork仓提PR能够获取到主仓的密钥 | — | **★ 安全严重问题** |
| 52 | MindIE-SD | 默认runner和自定义image模式，pending约10min报失败，失败没有详细日志 | 7.02：待验证。镜像与资源池异地，公网带宽已是上限 | 预计7月上线预拉取功能 |
| 53 | openlibing | code-metrics-scan插件线上解压报错 | — | — |
| 54 | MindIE-SD | 自有资源池+自定义容器镜像，资源空闲但一直拉取不到资源，无日志无报错 | 6/23: 验证已可用 | — |
| 55 | openlibing | 全量代码检查任务已经跑成功，状态一直显示运行中 | — | — |
| 56 | openlibing | Summary里的链接会被套一层无关的域名 | 非问题。中间页符合平台规范 | — |
| 57 | MindIE-SD | `if: contains(atomgit.event.comment.body, '/deploy')`报错job-if表达式有误 | — | — |
| 58 | openlibing | 关闭pr后重新提交pr，checkout插件会拉取失败 | 7.06：广州已上线 | — |
| 59 | openlibing | setup-jdk插件不支持java21 | — | — |
| 60 | openlibing | atomgit.repository上下文变量返回值有误 | — | — |
| 61 | openubmc | 新建pr时好像没触发action | 7.01: yaml有问题 | — |
| 62 | openlibing | ATOMGIT.REPOSITORY系统变量返回占位符 | 7.13：已上线 | — |
| 63 | openlibing | 自定义runner如何指定分配资源 | — | — |
| 64 | pytorch | workflow_call任务失败，job if未生效 | 7.06：715解决 | — |
| 65 | MindSpore | 无法连外网下载三方件 | 自定义资源池，确认资源池是否可访问外网 | 基于GitCode官方资源池验证 |
| 66 | openlibing | pull_request_target访问secrets的fork PR场景目前还未实现 | 开发中，715 | **★ P0 安全关注** |
| 67 | openlibing | 流水线频繁触发，每次改动标签都会触发流水线 | 7.16：已解决 | — |
| 68 | op-plugin | workflow_call的runs-on使用变量报错Self-hosted执行机未注册 | — | — |
| 69 | op-plugin | setup-node插件在自定义资源池执行成功后，还是无法使用npm（默认资源池可以） | 7.14：确认只有自定义资源池+自定义镜像场景出现 | — |
| 70 | op-plugin | 拉镜像时间过长超过默认环境准备时间 | 通过预拉取镜像插件解决 | 基于GitCode官方资源池验证 |
| 71 | mindie | checkout pr预合并不可用 | — | — |
| 72 | op-plugin | codecheck插件检查结果为不通过时，插件仍然执行成功 | 7.17：无法验证（ak/sk登录问题） | — |
| 73 | op-plugin | codecheck插件检查结果summary未显示 | 7.17：无法验证 | — |
| 74 | op-plugin | codecheck插件更换codearts账号后，前几次PR检查变成了版本级检查 | 7.17：无法验证 | — |
| 75 | op-plugin | inputs中定义string "3.10"，使用时变成了3.10（类型转换bug） | 先使用'3.10' | **★ 类型安全关注** |
| 76 | op-plugin | 主workflow定义的env作为入参调用另一个yml，传进去的参数取不到 | 715：还是用不了 | **★ 变量传递bug** |
| 77 | openlibing | 评论有评论但流水线打印的评论是空的 | 已验证 | — |
| 78 | op-plugin | 没有任务在执行时runner也显示运行中，再触发流水线会一直转圈 | 已修复 | — |
| 79 | openlibing | 自定义资源池checkout插件运行失败 | 检查自定义资源池网络 | — |
| 80 | openlibing | 日志打印乱序 | — | — |
| 81 | op-plugin | 日志大概率不显示 | — | — |
| 82 | op-plugin | checkout插件写法一样但有的执行成功有的执行失败 | uses中不支持`${{atomgit.repository}}` | **★ uses 不支持表达式** |
| 83 | mindcluster | pre-commit插件使用报错：Port number was not a decimal number | precommit插件依赖checkout，必须先执行checkout | — |
| 84 | mindcluster | 任务改为workflow_call方式后bad substitution | 问题同94 | — |
| 85 | mindcluster | 子workflow更新后从日志看用的还是旧代码（yml缓存问题） | 7.9已上广州 | **★ yml缓存未更新** |
| 86 | openlibing | 官方Runner有docker但没有可连接的daemon | 默认资源池不支持启docker镜像 | — |
| 87 | MindCluster | 旧编译构建任务BUILDNUMBER在job层面没有类似排序性质的参数 | pipeline不会将插件任务产出的数据作为环境变量下发给后续任务，只能通过output | 待澄清 |
| 89 | akg | 自定义资源池拉取自定义镜像拉取失败，也没有报错 | — | — |
| 90 | akg | 使用gitcode官方插件cache，文件报错插件找不到 | 生产环境已提供，待验证 | — |
| 91 | mindcluster | codearts资源池调试，突然断断续续出现任务申请资源错误 | — | — |
| 92 | openlibing | 在自定义执行机上下载python报错，不支持当前执行机的EulerOS2.0系统 | 执行机minGlibc>=2.35 | — |
| 93 | mindcluster | 编译过程中安装依赖时报错 could not read username for https://gitee.com | 初步判断执行机访问域名证书问题 | 待定位 |
| 94 | mindcluster | 希望支持获取指定step执行结果或至少提供等效替代办法 | 7.17：开发中，待上线 | — |
| 95 | mindcluster | 优化流水线展示界面任务布局，11个任务不缩放页面展示不全 | 鼠标可以拖动 | — |
| 96 | op-plugin | runs_on规格改成2xlarge，arm任务申请资源错误 | — | — |
| 97 | openlibing | 流水线评论触发时未能获取prid | — | — |
| 98 | — | action setup-go,setup-python,setup-java 不生效（若干重复报告） | — | — |
| 101 | — | 如果jobA need一个matrix jobB，jobB成功了jobA依然会初始化失败 | — | **★ matrix needs 依赖bug** |

> 注：问题4/32（图片型问题，无文字描述）已省略。编号保留原始行号以便追溯。

---

## 关键发现总结（用于指导用例生成）

### 🔴 P0 级安全问题

| 问题 | 编号 | 说明 | 关联 Intent |
|---|---|---|---|
| fork PR 可获取主仓密钥 | #51 | 安全隔离失败——fork PR 应完全隔离 secrets | INTENT-SEC-001, 002 |
| pull_request_target 的 fork PR secret 隔离未实现 | #66 | 核心安全机制缺失 | INTENT-SEC-003, 004 |

### 🟡 P1 级典型缺陷

| 类别 | 问题编号 | 模式 | 关联维度 |
|---|---|---|---|
| **变量/参数处理** | #2, #11, #38, #46, #60, #62, #75, #76, #82, #84, #85, #101 | 参数渲染失败、bad substitution、类型转换、中划线异常、uses 不支持表达式、yml缓存未更新 | completeness / compatibility |
| **触发/调度** | #1, #7, #9, #22, #23, #55, #61, #67, #78 | 触发不生效、手动触发参数问题、频繁触发、runner 状态异常 | completeness / reliability |
| **日志/调试** | #6, #14, #28, #80, #81 | 日志无法下载、加载慢(7min)、无关日志多、乱序、不显示 | usability |
| **Plugin/Action** | #25, #26, #27, #35, #36, #41, #50, #53, #59, #69, #72, #73, #74, #82, #83, #90, #98 | checkout 不支持 PR 预合并、setup-* 版本问题、插件报错、composite action 不支持 | completeness / usability |
| **Runner/资源** | #7, #44, #48, #52, #54, #63, #65, #70, #78, #86, #89, #91, #92, #96 | 资源调度失败、镜像拉取慢/失败、arm/x86 架构不区分、网络隔离 | reliability |
| **Workflow 模型** | #17, #29, #30, #64, #68, #76, #84, #87, #94, #101 | workflow_call 失败、job 依赖缺失、outputs 传递、step 结果获取 | completeness / reliability |
| **上下文/变量** | #3, #20, #43, #45, #56, #60, #62 | 系统变量不完整/不一致、atomgit 上下文字段缺失 | completeness / compatibility |

### 📋 高频问题特征

1. **参数渲染/变量传递**是最集中的问题域（15+ 条）——`${{ }}` 表达式求值、env 传递、中划线处理、类型转换
2. **Plugin/Action 兼容性**次之（12+ 条）——setup-* 版本支持、checkout PR 预合并、自定义 action 引用
3. **日志/调试体验**是用户最大痛点——无法下载、加载极慢(7min)、乱序/不显示
4. **Runner/资源调度**在自定义资源池场景下不稳定——拉镜像超时、架构不匹配、网络问题
5. **workflow_call** 是功能缺陷高发区——子任务无法拉起、变量传递失败、if 不生效

### 🎯 对用例生成的指导

1. **安全测试**必须覆盖 #51（fork PR→主仓密钥）和 #66（pull_request_target 未隔离）——这两条是已知的真实漏洞，应作为 P0 用例的验证目标
2. **变量/参数**类用例应重点设计中划线、类型转换、uses 中表达式等边界场景
3. **日志/易用性**用例应覆盖下载、加载性能、乱序检测、Summary 正确性
4. **workflow_call** 和 **matrix needs** 应作为完备性 P0 的核心验证点
5. **Runner 调度**用例应覆盖自定义资源池+自定义镜像的组合场景（#7/44/52/54/69/89）
