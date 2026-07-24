# Failure Analyst 归因报告 · run 2026-07-24-valid297-final

## 汇总

| 根因 | 数量 | 占比 |
|---|---|---|
| 产品缺陷 | 22 | 27% |
| 用例问题 | 25 | 31% |
| 环境问题 | 18 | 22% |
| 编译缺口/标记不匹配 | 10 | 12% |
| 需人工判断 | 6 | 7% |

## 产品缺陷（22）

### SECURITY
| 案例 | 描述 | 规格依据 |
|---|---|---|
| SEC-MASK-01-001 | secret 脱敏输出空串而非 `***` | using-secrets.md:66 |
| SEC-MASK-01-005 | multiline secret 同上 | using-secrets.md:66 |
| SEC-PERM-01-003 | 无 permissions 声明时 token 未自动生成 | token-permissions.md:99-103 |
| SEC-SUPPLY-01-001 | SHA 引用 action 静默失败零诊断 | using-actions.md:95-100 |
| SEC-SUPPLY-01-002 | 无效 hash 静默失败零诊断 | using-actions.md:95-100 |

### COMPLETENESS
| 案例 | 描述 |
|---|---|
| COMP-ARTIFACT-01-001 | artifact 插件导致 job 静默失败，步骤零输出 |
| COMP-ARTIFACT-01-002 | 同上，download-artifact 无 name=all 模式 |
| COMP-ARTIFACT-01-003 | 同上，retention-days 参数未文档化 |
| COMP-CACHE-01-001 | cache 插件导致 job 静默失败 |
| COMP-CACHE-01-002 | 同上 |

### RELIABILITY
| 案例 | 描述 |confirm|evidence|
|---|---|---|--|
| REL-NEEDS-01-025 | needs 失败传播不生效，下游未 skip | fake |https://gitcode.com/ComputingActionTest/foundational-tests/actions/runs/33c72b47d51b493490bd665d1a659324|
| REL-YAMLCACHE-01-060 | 推送新 YAML 后平台仍执行旧版本（缓存不失效） |fake|https://gitcode.com/ComputingActionTest/foundational-tests/actions/runs/beb155d45c804a479fd3ba73ee23b5cf/job/77e450d25ce04d64a7fab68d4d234b3d,https://gitcode.com/ComputingActionTest/foundational-tests/actions/runs/fca4c7f3203b40e389ffb757b7173f1f/job/6da949a9f74d4bb8837acf9832ff994b|

### COMPATIBILITY
| 案例 | 描述 |
|---|---|
| COMPAT-CACHE-01-001 | dispatch 事件禁用 cache |
| COMPAT-DIR-01-002 | 平台识别 .github/workflows/ 目录下的 workflow |
| COMPAT-INPUTS-01-001 | boolean input 静默接受 |
| COMPAT-RUNSON-01-002 | 接受单字符串 runs-on 格式 |
| COMPAT-VARS-01-006 | `vars.ACTION_VAR` 在 Action `with:` 中求值为空 |

### USABILITY
| 案例 | 描述 |
|---|---|
| USE-CONC-01-001 | concurrency.max=10 静默接受 |
| USE-CTX-01-001 | atomgit.ref 返回短格式 main 而非 refs/heads/main |
| USE-CTX-01-002 | github 上下文静默转为 placeholder |
| USE-DISP-01-002 | dispatch 默认值不生效 |
| USE-ENV-01-002 | GITHUB_SHA 崩溃无映射提示 |
| USE-EXPR-01-001 | 不存在属性静默求值为空串 |
| USE-INPT-01-002 | boolean input 静默接受 |
| USE-OS-01-001 | runner.os 返回小写 linux（文档承诺 Linux） |
| USE-SECNAME-01-001 | ATOMGIT_ 前缀 secret 未被拒绝 |

## 用例问题（25）

主要模式：
- 标记不匹配：COMPLETED vs success/SKIPPED/FAILED、关键字 vs 实际输出
- 四括号语法错误：`${{{{ }}}}` 模板变量未展开（REL-ARTCONC-01-063, REL-MATRIX-01-038/039, REL-OUTPUT-01-016）
- pre-condition 缺失：缺 checkout/pull --rebase、缺 git config
- 单字符 leak 假阳性：`must_not_contain:"2"` 匹配时间戳数字
- curl 缺 `--fail` 导致回声 fallback 不触发

## 环境问题（18）

- artifact 名称冲突 + namespace quota 超限（4 条）
- harness 307s 超时截断长时 timeout/long-run 测试（6 条）
- 故障注入（SIGKILL/网络/磁盘满）在 runner 容器环境不可行（3 条）
- K8s 自托管 runner 不可用（1 条）
- cache 插件 eventValidation 拒绝 dispatch 事件（1 条）
- PR 已关闭/合并导致 merge ref 不存在（1 条）
- 其他（2 条）

## 编译缺口/标记不匹配（10）

- step_status/job_status target 退化编译为 run_status（COMPAT-OUTCOME-01-002/003）
- step_summary target 退化编译为 run_logs（COMP-SUMMARY-01-001, USE-MD-01-001）
- step 名称 vs shell 输出标记不匹配（USE-LOG-01-001）
- run_status label 未归一化：SUCCESS_OR_BLOCKED/SUCCESS_OR_FAILURE/SUCCESS_OR_YAML_ERROR/SUCCESS_WITH_BASE_WORKFLOW/BLOCKED_OR_MASKED（5 条）

## 需人工判断（6）

- COMP-CALL-01-001: 零输出原因不明
- COMP-SECRET-01-001: secret 为空 vs 脱敏为空
- COMP-TIMEOUT-01-002: CANCELLED vs FAILED 超时语义
- COMPAT-PERM-01-001: token read 权限 vs fixture README 缺失
- SEC-NAME-01-002: 日志采集缺口 vs 命令输出为空
- SEC-SIDE-01-002: artifact 中 secret 未被拦截（spec 未明确承诺此能力）
- REL-RUNNER-01-049-V2: 2xlarge runner 原因不明
