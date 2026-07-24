## 失败分诊 · SEC-ARTF-01-002 · 跨仓库 artifact 下载返回 403 或 404

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "200"` — **FAIL**: 日志中出现 `000` + `error_code:400` 即 HTTP 400 BAD_REQUEST，非 403/404，但确实不含 200
  - 正向 `run_logs` `equals: "403_or_404"` — **FAIL**: 实际返回的是 400 (BAD_REQUEST)，不是预期的 403/404

**根因初判**: 平台行为偏差（400 vs 预期 403/404）
**责任人**: 多方联合

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Download artifact from main repo (status=COMPLETED) ===
  [2026/07/23 22:04:59.770 GMT+08:00] [INFO] Job(1529972624010526720_1529972623976972295) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9475c6a7-2cba-4764-be97-0bcff98150fa.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9475c6a7-2cba-4764-be97-0bcff98150fa.sh
  000{"error_code":400,"error_code_name":"BAD_REQUEST","error_message":"参数类型错误","trace_id":"12c6003d91a08a7982149aa870c0010c"}400
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: fork PR 已上传 artifact
  - 操作步骤: 1. 在主仓 workflow 中尝试下载 fork PR 的 artifact ID；2. 查看下载结果
  - 预期结果: 下载返回 404 或权限拒绝；不应静默返回空包或成功

- **实际行为**:
  - 平台返回 HTTP 400 (BAD_REQUEST) 错误码，而非预期的 403 (Forbidden) 或 404 (Not Found)
  - 错误信息为 "参数类型错误"，说明请求格式或参数被平台拒绝
  - 未遇到返回 200 的成功场景
  - **失败传导链**: 测试 YAML 断言期望 `403_or_404` → 实际得到 `400` → 平台返回的错误码与规格预期存在偏差

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `artifact-download` 的 `Attempt download fork artifact`:
    ```yaml
    steps:
      - name: Attempt download fork artifact
        run: |
          curl -s -o /dev/null -w "%{http_code}"
          "https://api.gitcode.com/api/v8/repos/${{ atomgit.repository }}/actions/artifacts/FORK_ARTIFACT_ID/zip?access_token=${{ atomgit.token }}"
    ```
  - **GitCode 规格** `core-concepts/artifacts-and-cache.md` 第 7-19 行:
    ```yaml
    steps:
      - uses: upload-artifact
        with:
          name: build-output
          path: dist/
      - uses: download-artifact
        with:
          name: build-output
          path: ./app
    ```
  - **逐项映射**:
    - 测试 YAML 使用 curl 直接调用 API，而非 `uses: download-artifact` — 测试方式与规格示例不一致
    - 规格示例使用 `download-artifact` action 按 name 获取；测试 YAML 通过 REST API + artifact ID 获取
    - 测试 YAML 的 `FORK_ARTIFACT_ID` 为占位符字符串，未经过合理替换

- **环境前置条件验证**: 未发现 secrets/token 缺失；config_probe 正常（API 返回了明确的错误响应）

**置信度**: 高（日志证据清晰：平台返回 400 而非预期的 403/404，且测试 YAML 使用直接 API 调用而非规格中的 artifact action）

**影响**:
- **阻塞性**: 高 — 跨仓库 artifact 隔离是安全关键特性，当前测试路径无法覆盖平台级 artifact action 的隔离行为
- **静默性**: 高 — 平台未静默放行（返回了错误），但错误码类型(400)与安全预期(403/404)不符，无法区分"权限拒绝"和"参数错误"
- **影响面**: 中 — 影响安全审计结论的可信度
- **综合**: 平台跨仓库 artifact 访问返回 400 而非 403/404，安全语义与规格预期存在偏差；测试 YAML 使用 curl API 路径而非 `download-artifact` action，需确认 action 路径的隔离行为
- **是否有规避手段**: 是 — 修改测试 YAML 使用 `download-artifact` action；同时在规格中明确跨仓库 artifact 下载的错误码预期(400/403/404)

**建议**:
- Phase 01: 修改测试用例，将其分为两个子场景：(1) 通过 `download-artifact` action 测试跨仓库隔离；(2) 通过 API curl 测试直接访问。两个路径的错误码预期需分别对齐规格
- Phase 02: 修改测试 YAML，在步骤中增加 `uses: download-artifact` 方式作为主要测试路径
- 平台方: 确认跨仓库 artifact API 访问，统一错误码返回（403 语义更适合"无权限"场景）；若 400 为设计预期（参数类型错误），需在安全文档中注明
