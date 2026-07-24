## 失败分诊 · SEC-ARTF-01-002 · 跨仓库 artifact 下载返回 403 或 404

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "200" — 实际日志含 "000" + "400"，符合负向断言但未命中正向
- positive, run_logs, equals "403_or_404" — 实际返回 400 BAD_REQUEST，不匹配

**根因初判**: 平台缺陷
**责任人**: 平台方

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Download artifact from main repo (status=COMPLETED) ===
  [2026/07/23 22:04:59.770 GMT+08:00] [INFO] Job(1529972624010526720_1529972623976972295) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9475c6a7-2cba-4764-be97-0bcff98150fa.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9475c6a7-2cba-4764-be97-0bcff98150fa.sh
  000{"error_code":400,"error_code_name":"BAD_REQUEST","error_message":"参数类型错误","trace_id":"12c6003d91a08a7982149aa870c0010c"}400
  ```

- **预期行为** (Phase 01 文本用例 SEC-ARTF-01-002, 优先级 P0, 维度 security):
  - 前置条件: fork PR 已上传 artifact
  - 操作步骤 1: 在主仓 workflow 中尝试下载 fork PR 的 artifact ID
  - 操作步骤 2: 查看下载结果
  - 预期结果: 下载返回 404 或权限拒绝；不应静默返回空包或成功

- **实际行为**:
  - curl 请求返回 HTTP 400 + JSON 错误体 `{"error_code":400,"error_code_name":"BAD_REQUEST","error_message":"参数类型错误"}`
  - 平台未返回预期的 403 (权限拒绝) 或 404 (未找到)
  - `atomgit.token` 展开后可能为空导致 Authorization header 格式异常，平台应拒绝请求为 403 而非 400

- **对照 GitCode 规格** `security-permissions/pr-mr-pipeline-security.md`:
  - 第 12-15 行: "ATOMGIT_TOKEN 权限 | 仅 read 权限（安全限制）| fork 来源不可访问项目 Secret"
  - 第 44 行: "恶意 PR 提交者可以修改 workflow 文件内容，但由于无 Secret 和写权限，攻击范围有限"
  - 跨仓库 artifact 访问应在 API 层面返回 403/404，而非 400 参数错误

- **环境前置条件验证**: YAML `setup.repo_fixture: with-artifacts`，无 `secrets` 字段，无 config_probe。`atomgit.token` 为平台注入变量，其为空值导致 API 参数错误。

**置信度**: 高 (平台 API 返回 400 而非安全标准码 403/404，行为可复现)

**影响**:
- **阻塞性**: 🔴阻塞 — 跨仓库 artifact 隔离是安全关键功能，平台应返回明确的安全拒绝码
- **静默性**: 🟡可察觉 — 有错误码返回但非预期的安全语义，可能误导安全自动化
- **影响面**: 🟡同维度 — artifact 安全隔离矩阵中同维度多处受影响
- **综合**: 平台 artifact 下载 API 对非法/跨仓请求返回 400 而非 403/404，安全语义不明确
- **是否有规避手段**: 否

**建议**:
- 平台修复 API 层权限校验逻辑，对跨仓库 artifact 访问明确返回 403（Forbidden）而非 400
- 测试 YAML 添加 config_probe 步骤确认 `atomgit.token` 被正确注入
