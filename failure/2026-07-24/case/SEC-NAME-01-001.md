## 失败分诊 · SEC-NAME-01-001 · Secret/变量名含特殊字符时不可导致意外求值或权限绕过

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain_secret "MY-VAR"，实际该值未在日志中明文出现（PASS）；assertions[1] (positive, run_status) — 期望 equals "success_or_yaml_error"，实际 run_status=COMPLETED，不匹配此复合关键词

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（仅 6 行）:
  ```
  === JOB: Test special secret name (status=COMPLETED) ===
  [2026/07/23 22:07:51.101 GMT+08:00] [INFO] Job(1529973342604107776_1529973342566359047) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/69d87b28-0d35-4dbf-b109-f07c69b27f7b.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/69d87b28-0d35-4dbf-b109-f07c69b27f7b.sh
  value is 
  ```
  日志显示 secret 含连字符名称 `MY-VAR` 被平台静默接受（workflow dispatch 成功，job COMPLETED），但 `${{ secrets.MY-VAR }}` 展开后值为空。这符合"不支持的命名被静默忽略而非报错"。run_status 为 COMPLETED，断言期望的 "success_or_yaml_error" 是复合语义词汇，非平台原生状态值。

- **预期行为**（Phase 01 文本用例 `SEC-NAME-01-001`，优先级 P0，维度 security/compatibility）:
  - 操作步骤 1: "提交一个 workflow，引用 secrets.MY-VAR 并在 shell 中使用"
  - 操作步骤 2: "触发 workflow 并查看运行日志"
  - 预期结果: "含中划线的 secret 不应因解析错误而被泄露到日志；若不支持中划线，应在 YAML 校验阶段报错"
  - 验证点: "[负向] 含中划线的 secret 绝不应因解析错误而被泄露到日志或环境变量"

- **实际行为**:
  - 含连字符的 secret 名被静默接受，但值为空——平台未在 YAML 校验阶段报错（期望的行为之一）
  - Secret 原值未泄漏（negative 断言 PASS），但平台也未在提交阶段拒绝非法名称
  - run_status "COMPLETED" 不等于断言期望的复合词汇 "success_or_yaml_error"——这是断言设计层面的 标记不匹配

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `special-name` job 的 `Use hyphen secret` 步骤:
    ```yaml
    - name: Use hyphen secret
      run: |
        echo "value is ${{ secrets.MY-VAR }}"
    ```
  - 这对应 GitCode 规格 `security-permissions/using-secrets.md` 第 43-47 行的 Secret 名称规则:
    ```
    引用语法为 ${{ secrets.SECRET_NAME }}，Secret 名称规则：

    - 仅允许大写字母、数字和下划线
    - 不得以 ATOMGIT_ 开头（与系统变量冲突）
    - 不得以数字开头
    ```
    规格第 45 行明确声明 Secret 名称"仅允许大写字母、数字和下划线"。`MY-VAR` 包含连字符 `-`，违反命名规则。按规范第 22 行的期望，平台"应在 YAML 校验阶段报错"。实际平台静默接受该名称但将值解析为空——这属于"运行期静默失败"的非预期行为。
  - 同时对应第 47 行"不得以数字开头"规则，证明文档对命名规范有确凿承诺。

**置信度**: 中（日志确凿显示含连字符 secret 被静默接受但值为空，run_status 断言关键词 "success_or_yaml_error" ≠ COMPLETED 是标记不匹配；但平台未在 YAML 校验阶段报错属于平台行为偏差）

**影响**:
- **阻塞性**: ⚪无影响 — 含连字符的 secret 名 `MY-VAR` 被平台静默接受但值为空，secret 原值未泄漏；平台未在 YAML 校验阶段报错属于行为偏差但非安全漏洞
- **静默性**: 🟡可察觉 — 日志输出 `value is `（空值），用户可观察但无法获知原因是命名非法还是 secret 未定义
- **影响面**: 🟢单用例 — 仅影响 SEC-NAME-01-001 的特殊字符 secret 名称测试
- **综合**: run_status "COMPLETED" ≠ 断言期望的复合词汇 "success_or_yaml_error" 是标记不匹配；平台静默接受非法 secret 名但值为空，无安全泄漏
- **是否有规避手段**: 是 — 平台应在 YAML 校验阶段拒绝非法 secret 名称并给出明确错误；断言应使用平台原生状态值

**建议**:
- 平台应在 YAML 校验阶段拒绝含非法字符的 secret 名称（连字符、数字开头等），给出明确错误
- run_status 断言应使用平台原生值（"COMPLETED" 映射到 "success"）而非自定义复合词汇
- 相关用例: SEC-NAME-01-002
