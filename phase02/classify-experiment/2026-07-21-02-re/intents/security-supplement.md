# 安全维度补充产出 · BLIND-05 / BLIND-11(wait timer) / BLIND-02(安全面)

> 产出 Agent：security（攻击面测绘师 / 防御性安全评审）
> Run：2026-07-21-02（增量更新，不修改历史结论）
> 目标盲区：
>   - BLIND-05 `C-SEC-13 ATOMGIT_REF_PROTECTED`（分支保护 ref 标志）
>   - BLIND-11 `C-SEC-14 环境保护 wait timer`
>   - BLIND-02 `C-RUN-09/10 container 自定义镜像`（container credentials / 运行时 secret 隔离）
> 已有 intent 最后序号：SEC-036
> 本补充序号：SEC-037 ~ SEC-040
> 纪律遵守：
>   - 不修改 `security.md` 已有内容
>   - 只产防御性验收目标，不写 exploit 代码，无真实密钥
> 来源输入：
>   - `inputs/gitcode-spec/action-development/runtime-environment-variables.md`（ATOMGIT_REF_PROTECTED，fetched 2026-07-20）
>   - `inputs/gitcode-spec/security-permissions/using-secrets.md`（环境审批机制，fetched 2026-07-20）
>   - `inputs/gitcode-spec/runner-management/configuring-images-toolchains.md`（container 完整字段，fetched 2026-07-20）
>   - `coverage.md` BLIND-02/05/11 详情

---

```
意图 ID:    INTENT-SEC-037
维度标签:   [security, completeness]
标题:       验证保护分支上下文标志 `atomgit.ref_protected` / `ATOMGIT_REF_PROTECTED` 的可用性与正确性

风险点:     基于保护分支的安全策略（如「仅保护分支可部署生产环境」）依赖 `ATOMGIT_REF_PROTECTED` 的真值。若该标志缺失、求值错误或时序不对（如未在 job 启动前确定），则条件门控可被绕过，导致非保护分支获得生产环境 secret 或触发部署——CICD-03。
预期系统行为: 当触发 ref 为配置了分支保护或规则集的分支/标签时，`atomgit.ref_protected` / `ATOMGIT_REF_PROTECTED` 求值为 `true`；否则为 `false`。该值在 job 条件判断（`if:`）和步骤运行时均稳定可用。
Oracle 来源: GitCode规格（runtime-environment-variables.md:28 「若为触发 ref 配置了分支保护或规则集，则为真」；C-SEC-13）

验证要点:
  - [正向] 在保护分支上触发的工作流中，`${{ atomgit.ref_protected }}` 与 `$ATOMGIT_REF_PROTECTED` 均求值为 `true`。
  - [负向] 在未配置保护的分支、PR merge 分支或标签上触发时，该标志不得为 `true`；保护分支上的值不得因缓存或并发而错误为 `false`。
  - [非功能] 标志值在 job 级 `if:` 条件求值时即已确定，不因运行过程中保护策略变更而改变。

负向断言目标: 未受保护的分支绝不应使 `ref_protected` 求值为 `true`，从而绕过基于保护分支的安全门控。判定证据 =（a）非保护分支运行日志中标志值为 `false`；（b）基于 `if: atomgit.ref_protected == true` 的部署 job 在非保护分支上被跳过。
威胁类别: STRIDE-Elevation / Info Disclosure；OWASP CICD-03。
优先级线索: 建议 P1 候选（BLIND-05 中严重度；C-SEC-13 缺口）。
破坏级别:   fixture
来源输入:   runtime-environment-variables.md:28；spec.md C-SEC-13
```

```
意图 ID:    INTENT-SEC-038
维度标签:   [security, reliability]
标题:       验证环境保护 wait timer 倒计时期间环境 Secret 不可访问

风险点:     环境级 Secret 可配置审批人（using-secrets.md:69），但 wait timer（强制等待期）是审批 gate 的时间维度补充。若 wait timer 期间 job 已能访问环境 secret，则「强制冷却」机制失效，攻击者可在审批后、等待期结束前即获得部署凭据并执行操作——CICD-03。
预期系统行为: 配置了 wait timer 的环境，对应 job 在 wait timer 倒计时期间处于等待/挂起状态，环境 secret 未被注入 job 运行时；倒计时结束后（且审批人要求已满足）job 才继续执行并可访问环境 secret。
Oracle 来源: GitCode规格（using-secrets.md:69 环境审批机制）+ 差异声明（C-SEC-14 wait timer 语义未详，需实测确立）；coverage.md BLIND-11。

验证要点:
  - [正向] wait timer 结束后且审批通过，环境 secret 可被授权 job 正常读取和使用。
  - [负向] wait timer 倒计时期间，job 不应开始执行含环境 secret 的步骤；环境 secret 不应以环境变量或 `${{ secrets.* }}` 形式注入等待中的 job。
  - [非功能] wait timer 的剩余时间可被观测；倒计时状态与 secret 可访问性强绑定，不可被重触发/跳过事件绕过。

负向断言目标: wait timer 倒计时期间绝不应访问受保护环境的 secret。判定证据 =（a）等待期间 job 步骤未执行，secret 环境变量未注入；（b）日志中无该环境 secret 的引用或值；（c）无绕过 wait timer 直达 secret 访问阶段的路径。
威胁类别: STRIDE-Elevation / Repudiation；OWASP CICD-03 / CICD-08。
优先级线索: 建议 P1 候选（BLIND-11 中严重度；C-SEC-14 缺口）。
破坏级别:   fixture
来源输入:   using-secrets.md:69；spec.md C-SEC-14；coverage.md BLIND-11
```

```
意图 ID:    INTENT-SEC-039
维度标签:   [security]
标题:       验证私有 container 镜像拉取凭证的安全传递与日志不泄露

风险点:     `container.credentials` 引用 `${{ secrets.REGISTRY_USERNAME }}` / `${{ secrets.REGISTRY_PASSWORD }}` 拉取私有镜像。若凭证在镜像 pull 阶段被记录到 runner 系统日志、job 日志或错误回显中，或被以不安全方式（如明文环境变量）传递给 Docker daemon，则 registry 凭据泄露——CICD-05。
预期系统行为: runner 安全解析 secret 并用于 registry 认证；凭证串在任何日志、报错消息或运行输出中均不出现；非 secret 引用语法（如硬编码明文）虽功能可用，但平台应鼓励/强制使用 secret 引用。
Oracle 来源: GitCode规格（configuring-images-toolchains.md:32-34 / using-secrets.md:55-59 container.credentials 语法；C-SEC-03 日志遮掩）+ 差异声明（凭证传递机制覆盖待实测）。

验证要点:
  - [正向] 使用 `${{ secrets.REGISTRY_USERNAME }}` / `${{ secrets.REGISTRY_PASSWORD }}` 时，私有镜像可正常拉取。
  - [负向] 镜像拉取失败或成功的日志中，不得出现 registry 用户名/密码明文；runner 系统日志、daemon 输出中同样不得出现。
  - [非功能] 凭证脱敏覆盖 stdout、stderr 及异常堆栈回显。

负向断言目标: 私有镜像仓库凭证绝不应以明文出现在任何日志或输出中。判定证据 =（a）job 日志 grep 凭证占位原值命中数为 0；（b）拉取失败时的错误消息仅显示仓库地址，不显示认证头或密码。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05。
优先级线索: 建议 P1 候选（BLIND-02 安全面；container secret 泄露）。
破坏级别:   fixture
来源输入:   configuring-images-toolchains.md:24-43；using-secrets.md:49-59；spec.md C-SEC-03 / C-RUN-09
```

```
意图 ID:    INTENT-SEC-040
维度标签:   [security, completeness]
标题:       验证 container 运行时 step 对宿主机环境变量/Secret 的隔离有效性

风险点:     `container` 字段将 step 运行在自定义 Docker 容器内，但容器与宿主机 runner 共享内核。若隔离不当，容器内进程可通过 `/proc/<pid>/environ`、挂载宿主机目录（`volumes`）或默认 Docker 参数访问宿主机 secret 环境变量、`.git-credentials`、runner 临时文件——CICD-06。
预期系统行为: container 内的 step 只能看到显式声明的 job `env`、step `env`、container `env` 以及经 `${{ secrets.* }}` 显式传入的环境变量；无法读取宿主机 runner 进程环境、未挂载的宿主机敏感文件或相邻 job 的残留。
Oracle 来源: GitCode规格（configuring-images-toolchains.md:38-51 container.volumes/options 说明；C-RUN-09/10）+ 差异声明（容器与宿主机隔离度待实测）。

验证要点:
  - [正向] 显式传入 container `env` 或 step `env` 的变量在容器内正常可用。
  - [负向] 容器内 step 不应能读取宿主机 runner 的进程环境变量（如宿主机上注入的其他 secret、ATOMGIT_TOKEN 若未显式映射）；不应通过默认挂载访问宿主机 `/tmp`、`/home/runner` 或工作区外的敏感文件。
  - [非功能] 隔离对官方托管 Runner 与自托管 Runner 的差异可被判定。

负向断言目标: container 内 step 绝不应访问到未显式传入的宿主机环境变量或 secret。判定证据 =（a）容器内枚举 `/proc/*/environ` 或等价手段无法取得宿主机标记性 secret；（b）容器内访问宿主机默认敏感路径（如 runner 家目录、全局 tmp）失败或看不到标记文件。
威胁类别: STRIDE-Info Disclosure / Elevation；OWASP CICD-06。
优先级线索: 建议 P1 候选（BLIND-02 安全面；container secret 泄露）。
破坏级别:   fixture
来源输入:   configuring-images-toolchains.md:24-51；spec.md C-RUN-09/10
```

---

## 补充自检

| 必覆盖攻击面 | 对应 intent | 状态 |
|---|---|---|
| 分支保护 ref 标志可用性与正确性 | SEC-037 | 新增 |
| 环境保护 wait timer secret 隔离 | SEC-038 | 新增 |
| container 镜像拉取凭证安全 | SEC-039 | 新增 |
| container 运行时 secret 隔离 | SEC-040 | 新增 |

## 红线合规声明
- 全文仅描述意图层攻击面与防御性验收目标，未包含可直接利用的 payload、exploit 代码或绕过步骤。
- 无真实密钥、token、内网地址；敏感值一律使用占位符（`REGISTRY_USERNAME`、`REGISTRY_PASSWORD`、`DEPLOY_TOKEN` 等）。
- 每条 intent 均含明确「负向断言目标（什么不应发生）+ 确定性判定证据」。
