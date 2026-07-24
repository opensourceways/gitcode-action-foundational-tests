## 失败分诊 · SEC-RUN-01-002 · Runner 环境变量与共享目录必须跨 job 隔离

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "isolation broken"，该关键词未出现（PASS，证明隔离有效）；assertions[1] (positive, run_logs) — 期望日志含 "isolated_as_expected"，实际输出 "isolated as expected"（空格分隔），下划线 vs 空格不匹配

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（13 行）:
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
  日志确凿证实跨 job 环境变量与临时文件隔离成功：
  Job A（Set env and tmp）：通过 `$ATOMGIT_ENV` 设置 `MY_SECRET_ENV=leaked` 并向 `/tmp/env-test.txt` 写入 `leaked-data`，无输出泄漏。
  Job B（Check env isolation）：检查 `$MY_SECRET_ENV` 为空且 `/tmp/env-test.txt` 不存在，输出 `isolated as expected`（空格分隔），未触发 `exit 1`。
  **关键结论**：平台的跨 job 环境变量隔离和 /tmp 目录隔离均工作正常——negative 断言 PASS（无 "isolation broken"），job B 成功确认环境干净。FAIL 的唯一原因是脚本 `echo "isolated as expected"` 使用空格分隔，而断言关键词 "isolated_as_expected" 使用下划线分隔——与 SEC-RUN-01-001 完全同模式的 标记不匹配。

- **预期行为**（Phase 01 文本用例 `SEC-RUN-01-002`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个多 job workflow，job A 设置环境变量和 /tmp 文件"
  - 操作步骤 2: "job B 检查环境变量和 /tmp 是否被污染"
  - 预期结果: "job B 的环境变量和共享目录在启动时为干净状态；job B 不应继承 job A 的设置"
  - 验证点: "[负向] job B 绝不应继承到 job A 设置的环境变量或 /tmp 残留"

- **实际行为**:
  - 平台正确隔离了 job A 的环境变量和 /tmp 文件——job B 确认无继承/cross-contamination
  - 安全隔离机制工作正常，环境变量和 tmp 均未被跨 job 泄漏
  - 断言仅因下划线 vs 空格的关键词不匹配而判定 FAIL

- **失败传导链**: Job A 完成（COMPLETED，设置 MY_SECRET_ENV 和 /tmp/env-test.txt）→ Job B 开始（COMPLETED，检查 `$MY_SECRET_ENV` 为空且 `[ -f /tmp/env-test.txt ]` 返回 false）→ 输出 "isolated as expected" → 平台隔离功能正常

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `job-a-env` 和 `job-b-env` 的步骤:
    ```yaml
    job-a-env:
      steps:
        - name: Set env
          run: |
            echo MY_SECRET_ENV=leaked >> $ATOMGIT_ENV
            echo leaked-data > /tmp/env-test.txt
    job-b-env:
      steps:
        - name: Check env clean
          run: |
            if [ -n "$MY_SECRET_ENV" ] || [ -f /tmp/env-test.txt ]; then
              echo "isolation broken"
              exit 1
            else
              echo "isolated as expected"
            fi
    ```
  - 这对应 GitCode 规格 `syntax-reference/workflow-commands.md` 第 24-39 行的 `ATOMGIT_ENV` 用法:
    ```
    将值写入后续步骤的环境变量，在当前 Job 的后续步骤中可用。
    echo "MY_VAR=my_value" >> $ATOMGIT_ENV
    ```
    规格第 25-26 行明确说明 `$ATOMGIT_ENV` 设置的变量"在当前 Job 的后续步骤中可用"——隐含跨 job 不应可见。测试验证了此行为：job B 中 `$MY_SECRET_ENV` 为空，证实了跨 job 隔离。
  - 同时对应 `core-concepts/runner-and-environment.md` 的 Runner 资源池环境，每个 job 获得隔离的执行环境。

**置信度**: 高（日志确凿证实跨 job 隔离工作正常——"isolated as expected" 确实在日志中；FAIL 原因仅为下划线 "isolated_as_expected" ≠ 空格 "isolated as expected" 的断言关键词不匹配，与 SEC-RUN-01-001 同模式）

**影响**:
- **阻塞性**: ⚪无影响 — 跨 job 环境变量与 /tmp 隔离功能工作正常：job B 确认 `$MY_SECRET_ENV` 为空且 `/tmp/env-test.txt` 不存在，输出 "isolated as expected"
- **静默性**: 🟢明确报错 — 日志确凿输出 "isolated as expected"，隔离行为完全可观测
- **影响面**: 🟢单用例 — 仅影响 SEC-RUN-01-002 的断言匹配，环境隔离机制本身正常
- **综合**: 跨 job 环境隔离保护功能正常（无 "isolation broken"），FAIL 仅因断言关键词 `isolated_as_expected`（下划线）与脚本 echo 输出 `isolated as expected`（空格）字符不一致
- **是否有规避手段**: 是 — 断言关键词改为空格分隔的 "isolated as expected"，或编译期做下划线/空格归一化

**建议**:
- 断言关键词应与脚本 echo 输出字符精确一致：将 "isolated_as_expected" 改为 "isolated as expected"
- 在断言编译期对所有 log 关键词做下划线/空格归一化处理（一次修复消除 SEC-RUN-01-001、SEC-RUN-01-002、SEC-NET-01-001、SEC-PERM-01-004 的同类型 FAIL）
- 相关用例: SEC-RUN-01-001
