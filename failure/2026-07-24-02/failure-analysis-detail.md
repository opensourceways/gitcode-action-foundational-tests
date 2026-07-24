# Failure Analyst 详细归因报告 · run 2026-07-24-valid297-final

## SECURITY（19 条）
见子报告 SEC 输出。

## COMPLETENESS（14 条）

### 核心发现
8/14 为"零步骤输出"模式——平台调度成功但步骤日志全部缺失。5 条 artifact/cache 内建 Action 导致 job 静默失败。3 条标记不匹配（COMPLETED 无法映射到非标准 run_status 枚举）。1 条编译缺口（step_summary target 退化）。

## RELIABILITY（24 条）

### 核心发现
- 5 条用例问题：3 条四括号语法（${{{{ }}}}）、1 条验证步骤路径错误、1 条 matrix 未设计失败实例
- 16 条环境问题：6 条 harness 超时截断、3 条故障注入未触发、3 条 artifact 冲突、4 条其他
- 2 条产品缺陷：REL-NEEDS-01-025（needs 失败传播不生效）、REL-YAMLCACHE-01-060（YAML 缓存不失效）
- 1 条需人工判断：REL-CONTINUE-01-030、REL-RUNNER-01-049-V2

## COMPATIBILITY + USABILITY（20 条）

### 核心发现
- 9 条产品缺陷：静默接受非法配置（5 条）+ 文档实现不一致（3 条）+ dispatch 默认值不生效
- 4 条用例问题：断言设计缺陷
- 2 条环境问题：cache 事件限制 + PR ref 不存在
- 3 条编译缺口/标记不匹配
- 1 条 Engine Bug：runner.os 大小写

---

## 全量汇总

### FAIL 归因（81 条）

| 根因 | 数量 | 占比 |
|---|---|---|
| 产品缺陷 | 22 | 27% |
| 用例问题 | 25 | 31% |
| 环境问题 | 18 | 22% |
| 编译缺口/标记不匹配 | 10 | 12% |
| 需人工判断 | 6 | 7% |

### 非 FAIL 统计

| 判定 | 数量 | 主因 |
|---|---|---|
| COMPILE_ERROR | 63 | 54 条 intent_ref 格式不合规 |
| TIMEOUT | 15 | 9 条 harness 300s 截断 + 6 条平台排队 |
| ENV_ERROR | 4 | dispatch_workflow HTTP 400 |
| INCONCLUSIVE | 1 | fork_pr 需第二账号 |

详见 `non-fail-summary.md`

| 根因 | 数量 | 占比 |
|---|---|---|
| 产品缺陷 | 22 | 27% |
| 用例问题 | 25 | 31% |
| 环境问题 | 18 | 22% |
| 编译缺口/标记不匹配 | 10 | 12% |
| 需人工判断 | 6 | 7% |

### 最严重平台缺陷（P0）
1. SEC-MASK-01-001/005: secret 脱敏输出空串而非 `***`
2. SEC-PERM-01-003: 无 permissions 时 token 未自动生成
3. SEC-SUPPLY-01-001/002: SHA 引用 action 静默失败
4. COMPAT-INPUTS-01-001/USE-INPT-01-002: boolean input 静默接受
5. USE-CTX-01-001: atomgit.ref 返回短格式
6. USE-EXPR-01-001: 不存在属性静默求值
7. REL-NEEDS-01-025: needs 失败传播不生效
8. REL-YAMLCACHE-01-060: YAML 缓存不失效
