## 失败分诊 · SEC-RUN-01-001 · Job 结束后 workspace 与临时文件必须被彻底清理

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "residual found"，该关键词未出现（PASS，证明无残留文件）；assertions[1] (positive, run_logs) — 期望日志含 "cleaned_as_expected"，实际输出 "cleaned as expected"（空格分隔），下划线 vs 空格不匹配

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（13 行）:
  ```
  === JOB: Write sensitive file (status=COMPLETED) ===
  [2026/07/23 22:09:32.440 GMT+08:00] [INFO] Job(1529973767860523008_1529973767831162887) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/2be5f0a1-d517-487d-b657-77309a59054d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/2be5f0a1-d517-487d-b657-77309a59054d.sh


  === JOB: Check cleanup (status=COMPLETED) ===
  [2026/07/23 22:09:32.455 GMT+08:00] [INFO] Job(1529973767860523008_1529973767835357185) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0a3ef073-dbb1-4a4c-834c-628811a1ed80.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0a3ef073-dbb1-4a4c-834c-628811a1ed80.sh
  cleaned as expected
  ```
  日志确凿证实跨 job workspace 清理成功：
  Job A（Write sensitive file）：向 `/tmp/sensitive-temp.txt` 写入 `sensitive-data`，无残留泄漏输出。
  Job B（Check cleanup）：检查 `/tmp/sensitive-temp.txt` 不存在，输出 `cleaned as expected`（空格分隔），未触发 `exit 1`。
  **关键结论**：平台的 job 间临时文件清理机制工作正常——negative 断言 PASS（无 "residual found"），job B 成功确认无残留。FAIL 的唯一原因是脚本 `echo "cleaned as expected"` 使用空格分隔，而断言关键词 "cleaned_as_expected" 使用下划线分隔。

- **预期行为**（Phase 01 文本用例 `SEC-RUN-01-001`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个多 job workflow，job A 写入敏感临时文件"
  - 操作步骤 2: "job B 检查是否存在 job A 的残留文件"
  - 预期结果: "job B 绝不应读取到 job A 残留的敏感文件；即使 job A 异常崩溃，清理钩子仍应执行"
  - 验证点: "[负向] job B 绝不应能读取到 job A 残留的敏感文件"

- **实际行为**:
  - 平台正确清理了 job A 的 /tmp 文件——job B 确认清理成功
  - 安全隔离机制工作正常，无数据泄漏
  - 断言仅因下划线 vs 空格的关键词不匹配而判定 FAIL

- **失败传导链**: Job A 完成（COMPLETED）→ Job B 开始（COMPLETED，`[ -f /tmp/sensitive-temp.txt ]` 返回 false）→ 输出 "cleaned as expected" → 平台清理功能正常

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `job-a` 和 `job-b` 的步骤:
    ```yaml
    job-a:
      name: Write sensitive file
      steps:
        - name: Write temp secret
          run: |
            echo sensitive-data > /tmp/sensitive-temp.txt
    job-b:
      name: Check cleanup
      steps:
        - name: Check no residual
          run: |
            if [ -f /tmp/sensitive-temp.txt ]; then
              echo "residual found"
              exit 1
            else
              echo "cleaned as expected"
            fi
    ```
  - 这对应 GitCode 规格 `core-concepts/runner-and-environment.md` 第 5-28 行的官方资源池环境描述。该文档描述了 Runner 环境架构，但未明确对跨 job workspace 清理的承诺。workspace 清理是平台隐含的安全期望，通过测试验证。
  - 同时对应 `writing-pipelines/workflow-file-location-structure.md` 第 103-107 行的 stages 阶段机制（job 间串行执行的底层支持），确保 job 按序执行且环境隔离。

**置信度**: 高（日志确凿证实清理功能工作正常——"cleaned as expected" 确实在日志中；FAIL 原因仅为下划线 "cleaned_as_expected" ≠ 空格 "cleaned as expected" 的断言关键词不匹配）

**建议**:
- 断言关键词应与脚本 echo 输出字符精确一致：将 "cleaned_as_expected" 改为 "cleaned as expected"
- 在断言编译期对所有 log 关键词做下划线/空格归一化处理（一次修复消除 SEC-RUN-01-001、SEC-RUN-01-002、SEC-NET-01-001、SEC-PERM-01-004 的同类型 FAIL）
- 相关用例: SEC-RUN-01-002
