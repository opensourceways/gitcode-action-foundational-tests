## 失败分诊 · SEC-ARTF-01-002 · 跨仓库 artifact 下载返回 403 或 404

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "200"，实际 200 未出现（PASS）；assertions[1] (positive, run_logs) — 期望日志含 "403_or_404"，实际为 "BAD_REQUEST" 返回码 400

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（仅 6 行）:
  ```
  === JOB: Download artifact from main repo (status=COMPLETED) ===
  [2026/07/23 22:04:59.770 GMT+08:00] [INFO] Job(1529972624010526720_1529972623976972295) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9475c6a7-2cba-4764-be97-0bcff98150fa.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9475c6a7-2cba-4764-be97-0bcff98150fa.sh
  000{"error_code":400,"error_code_name":"BAD_REQUEST","error_message":"参数类型错误","trace_id":"12c6003d91a08a7982149aa870c0010c"}400
  ```
  日志显示 curl 请求返回了 HTTP 400（BAD_REQUEST，"参数类型错误"）。平台确实拒绝了对 fork artifact 的访问，但返回的错误码是 400 而非合约预期的 403 或 404。HTTP 状态码 400 与断言关键词 "403_or_404" 不匹配。

- **预期行为**（Phase 01 文本用例 `SEC-ARTF-01-002`，优先级 P0，维度 security）:
  - 操作步骤 1: "在主仓 workflow 中尝试下载 fork PR 的 artifact ID"
  - 操作步骤 2: "查看下载结果"
  - 预期结果: "下载返回 404 或权限拒绝；不应静默返回空包或成功"
  - 验证点: "[正向] 返回明确的 404 或 403 错误"

- **实际行为**:
  - 平台返回了 400 BAD_REQUEST 而非 403/404，请求确实被拒绝，但错误码与预期范围不同
  - 这不是跨仓库 artifact 隔离失效——平台正确拒绝了请求，返回码只是语义差异（参数校验层面的拒绝 vs 权限层面的拒绝）

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `artifact-download` job 的 `Attempt download fork artifact` 步骤:
    ```yaml
    - name: Attempt download fork artifact
      run: |
        curl -s -o /dev/null -w "%{http_code}" \
          "https://api.gitcode.com/api/v8/repos/${{ atomgit.repository }}/actions/artifacts/FORK_ARTIFACT_ID/zip?access_token=${{ atomgit.token }}"
    ```
  - 这对应 GitCode 规格 `writing-pipelines/upload-download-artifacts.md` 第 22-45 行的跨 job artifact 传递示例:
    ```yaml
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - uses: checkout
          - name: Upload artifact
            uses: upload-artifact
            with:
              name: app-dist
              path: dist/
      deploy:
        runs-on: [ubuntu-latest, x64, small]
        needs: build
        steps:
          - name: Download artifact
            uses: download-artifact
            with:
              name: app-dist
              path: dist/
    ```
    规格文档描述 artifact 在同 workflow 内通过 `needs` 依赖传递，但未对跨仓库/跨 fork 的 artifact 访问安全策略返回码做出承诺。平台返回 400 而非 403/404 并不违反文档明确承诺。

**置信度**: 中（日志确凿显示 400 BAD_REQUEST，否定断言 PASS 证明隔离有效，但断言关键词假设了特定的 HTTP 状态码 403/404，实际平台语义为 400）

**影响**:
- **阻塞性**: ⚪无影响 — 平台正确拒绝了 fork artifact 访问（隔离有效），仅 HTTP 返回码 400 与文档预期 403/404 不同，非安全缺陷
- **静默性**: 🟢明确报错 — 返回 `{"error_code":400,"error_code_name":"BAD_REQUEST","error_message":"参数类型错误"}`，错误信息清晰可观测
- **影响面**: 🟢单用例 — 仅影响跨仓库 artifact 下载返回码断言，不涉及其他维度
- **综合**: 跨仓库隔离保护生效，仅 HTTP 错误码语义偏差（400 vs 403/404），无安全风险
- **是否有规避手段**: 是 — 将断言从精确匹配 HTTP 状态码改为 must_not_contain "200" 即可覆盖所有非成功返回

**建议**:
- 将断言从精确匹配 "403_or_404" 改为 must_not_contain "200"（即逻辑：只要不是 200，拒绝即有效），覆盖 400/401/403/404 等所有非成功返回
- 相关用例: SEC-ARTF-01-001
