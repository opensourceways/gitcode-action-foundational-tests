## 失败分诊 · SEC-RUN-01-002 · Runner 环境变量与共享目录必须跨 job 隔离

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "isolation broken" — 未出现泄露（通过）
- positive, run_logs, equals "isolated_as_expected" — 实际文本为 `isolated as expected`（空格），不匹配下划线格式

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量** (13 行):
  ```
  === JOB: Set env and tmp (status=COMPLETED) ===
  [2026/07/23 22:09:43.134 GMT+08:00] [INFO] Job(1529973812697632768_1529973812668272647) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/ae32645c-6c03-4c98-8e96-718cf793d193.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/ae32645c-6c03-4c98-8e96-718cf793d193.sh
  
  
  === JOB: Check env isolation (status=COMPLETED) ===
  [2026/07/23 22:09:43.135 GMT+08:00] [INFO] Job(1529973812697632768_1529973812668272649) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/f649cccc-4a31-4695-af37-c62095ab268d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/f649cccc-4a31-4695-af37-c62095ab268d.sh
  isolated as expected
  ```

- **预期行为** (Phase 01 文本用例 SEC-RUN-01-002, 优先级 P0, 维度 security):
  - 前置条件: 仓库支持多 job workflow
  - 操作步骤 1: 提交一个多 job workflow，job A 设置环境变量和 /tmp 文件
  - 操作步骤 2: job B 检查环境变量和 /tmp 是否被污染
  - 预期结果: job B 的环境变量和共享目录在启动时为干净状态；job B 不应继承 job A 的设置

- **实际行为**:
  - Job A: 成功写入 `MY_SECRET_ENV=leaked` 到 `ATOMGIT_ENV` 和 `leaked-data` 到 `/tmp/env-test.txt`
  - Job B: 输出 `isolated as expected` — 确认 `MY_SECRET_ENV` 为空且 `/tmp/env-test.txt` 不存在
  - **平台功能正确**: 跨 job 环境变量和 /tmp 隔离机制正常工作
  - **断言格式差异**: 日志实际输出 `isolated as expected`（空格），断言期望 `isolated_as_expected`（下划线）

- **对照 GitCode 规格** `writing-pipelines/using-variables-secrets.md`:
  - 第 81 行: "Step级 > Job级 > Workflow级。同名的 step 级变量会覆盖 job 级和 workflow 级变量"
  - 第 128 行: "ATOMGIT_ENV | 环境变量写入文件路径" — 环境变量作用域为 job 级

- **环境前置条件验证**: YAML `setup.repo_fixture: default`, 无 secrets, 无 config_probe。跨 job 环境/文件隔离正常。

**置信度**: 高 (平台隔离功能正确，仅断言字符串格式不匹配)

**影响**:
- **阻塞性**: ⚪无影响 — 平台环境隔离功能正确，job B 确认无污染
- **静默性**: 🟢明确报错 — "isolated as expected" 明确传达隔离成功
- **影响面**: 🟢单用例 — 仅断言格式需调整
- **综合**: 平台正确隔离了跨 job 环境变量和 /tmp 目录；断言应使用空格格式
- **是否有规避手段**: 是

**建议**:
- 修正 Phase 01 断言: `isolated_as_expected` → `isolated as expected`
- 考虑增加跨 workflow 运行的持久化环境污染测试（如自托管 runner 场景）
