# harness-selftest — Phase 02 harness 可复用性自测语料

> 目的：在**新机器**上验证 Phase 02 harness 端到端可跑通，不依赖 Phase 01 现阶段（尚不能稳定
> 产出可运行 workflow）。这 5 条是**已在真实 bingo 实例验证过 PASS** 的状态型用例，写成 Phase 01
> 契约格式，可被 harness 直接消费。

## 语料特征（为什么选这 5 条）

- **push 触发**（harness 当前唯一实现的触发方式）。
- **映射形式 `on:`**、合规 GitCode 语法 → 过 preflight。
- **状态型自断言**：断言写在 workflow 内的 shell `test`，失败即 step 非零退出 → 平台 FAILED →
  harness 判非绿 → FAIL；成功即 PASS。**不需要 `.asserts.json` sidecar**，自包含。
- 依赖被测仓 `ComputingActionTest/bingo` 的既有配置（见 `phase02/inputs/fixture-map.md`）。

| 用例 | 维度 | 验证点 |
|---|---|---|
| COMP-ST-CTXTOKEN-01-001 | completeness | `atomgit.token` 上下文非空 |
| COMP-ST-CHECKOUT-01-001 | completeness | `uses: checkout` 检出仓库内容 |
| COMP-ST-TRIGPUSH-01-001 | completeness | push 触发 + `atomgit.event_name` 可读 |
| SEC-ST-SETENV-01-001 | security | 废弃 `::set-env::` 默认不传播 |
| SEC-ST-SECRETUNDEF-01-001 | security | 未定义 secret 展开为空 |

## 新机器上怎么跑（可复用性验证步骤）

```bash
# 0. 前置：git pull（yyl-support 分支）；配置 OAuth token
export GITCODE_ACCESS_TOKEN=<你的token>        # 或放 ~/.gitcode-token
#    该 token 需能 push 到 ComputingActionTest/bingo（与自测语料同实例）

# 1. 闸门：schema 校验 + 建队列（p1-run-id=harness-selftest，p2-run-id 自取）
python phase02/scripts/schema_check.py harness-selftest 2026-XX-XX-01

# 2. 执行：逐条真跑（push→采集日志→§11判定→teardown 清理）
python phase02/scripts/run_batch.py 2026-XX-XX-01

# 3. 中途/完成查看进度
python phase02/scripts/status.py 2026-XX-XX-01

# 4. 报告：分维度 + 门禁
python phase02/scripts/report_builder.py 2026-XX-XX-01
```

（或用 slash 命令 `/phase02-schema-check`、`/phase02-exec`、`/phase02-status`、`/phase02-report`。）

**预期**：5 条全部 PASS（completeness 3/3、security 2/2，门禁 GO）。若某条 FAIL/INCONCLUSIVE，
即暴露 harness 在新环境的问题（token 权限 / 网络 / 平台变更），正是本自测要检出的。

> 运行产物落 `phase02/runs/<p2-run-id>/`（已 gitignore，不入库）。
