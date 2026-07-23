import os, json

BASE = r"D:/业务/action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases"

def write_text(cid, body):
    with open(os.path.join(BASE, "text", cid + ".md"), "w", encoding="utf-8") as f:
        f.write(body)

def write_yaml(cid, body):
    with open(os.path.join(BASE, "yaml", cid + ".yaml"), "w", encoding="utf-8") as f:
        f.write(body)

def build_yaml(cid, dims, dim, pri, title, intent, setup, trigger, wf, assertions, teardown, fault=None):
    lines = []
    lines.append("id: " + cid)
    lines.append("dimensions: " + json.dumps(dims))
    lines.append("dimension: " + dim)
    lines.append("priority: " + pri)
    lines.append('title: "' + title + '"')
    lines.append("intent_ref: " + intent)
    lines.append("setup:")
    lines.append("  repo_fixture: " + setup.get("repo_fixture", "default"))
    if setup.get("secrets"):
        lines.append("  secrets: " + json.dumps(setup["secrets"]))
    if setup.get("variables"):
        lines.append("  variables: " + json.dumps(setup["variables"]))
    if setup.get("branch_protection"):
        lines.append("  branch_protection: " + setup["branch_protection"])
    lines.append("workflow: |")
    for wl in wf.split("\n"):
        lines.append("  " + wl)
    lines.append("trigger:")
    lines.append("  event: " + trigger["event"])
    lines.append("  as: " + trigger["as"])
    lines.append("  params: " + json.dumps(trigger.get("params", {})))
    if fault:
        lines.append("fault_injection:")
        for k, v in fault.items():
            lines.append("  " + k + ": " + json.dumps(v))
    else:
        lines.append("fault_injection: null")
    lines.append("assertions:")
    for a in assertions:
        lines.append("  - type: " + a["type"])
        lines.append("    target: " + a["target"])
        for k, v in a.items():
            if k in ("type", "target"):
                continue
            lines.append("    " + k + ": " + json.dumps(v))
    lines.append("teardown:")
    lines.append("  reset: " + teardown)
    return "\n".join(lines) + "\n"

# ============================================================
# Group A: Fork PR Secret & Token Isolation
# ============================================================

# A1
write_text("SEC-FORK-01-001",
"""用例 ID:   SEC-FORK-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-001
母意图:    —
标题:      fork PR 触发 pull_request 时不可读取项目 secrets

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 以 fork 贡献者身份提交一个引用 secrets.DEPLOY_TOKEN 的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - 系统阻止 fork PR 访问 DEPLOY_TOKEN，引用时返回空值或安全报错
  - 运行日志中不出现 DEPLOY_TOKEN 明文

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [正向] fork PR 的 job 中 secrets 引用为空或不可访问

清理:      重置 fixture 仓库
""")

write_yaml("SEC-FORK-01-001", build_yaml(
    "SEC-FORK-01-001", ["security"], "security", "P0",
    "fork PR 触发 pull_request 时不可读取项目 secrets", "INTENT-SEC-001",
    {"repo_fixture": "with-secrets", "secrets": ["DEPLOY_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request", "as": "untrusted_contributor", "params": {}},
    "on:\n  pull_request:\n    branches: [main]\njobs:\n  check-secret:\n    name: Check secret isolation\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Try access secret\n        run: |\n          echo \"secret value is ${{ secrets.DEPLOY_TOKEN }}\"\n      - name: Print env\n        run: |\n          env | grep DEPLOY_TOKEN || echo \"not found\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "DEPLOY_TOKEN"},
        {"type": "positive", "target": "run_status", "equals": "completed_or_blocked"}
    ],
    "fixture"
))

# A2
write_text("SEC-FORK-01-002",
"""用例 ID:   SEC-FORK-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-001
母意图:    SEC-FORK-01-001
标题:      fork PR 中 secrets 引用返回空值且 job 不崩溃

前置条件:
  - 仓库配置了 secret API_KEY
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 以 fork 贡献者身份提交一个将 secrets.API_KEY 注入环境变量的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - secrets.API_KEY 返回空字符串，环境变量未设置
  - job 正常完成，不因 secret 不可访问而失败

验证点:
  - [负向] 环境变量 API_KEY 为空或未定义
  - [正向] job 状态为成功完成

清理:      重置 fixture 仓库
""")

write_yaml("SEC-FORK-01-002", build_yaml(
    "SEC-FORK-01-002", ["security"], "security", "P0",
    "fork PR 中 secrets 引用返回空值且 job 不崩溃", "INTENT-SEC-001",
    {"repo_fixture": "with-secrets", "secrets": ["API_KEY"], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request", "as": "untrusted_contributor", "params": {}},
    "on:\n  pull_request:\n    branches: [main]\njobs:\n  test-empty:\n    name: Test empty secret\n    runs-on: [dedicate-hosted, x64, large]\n    env:\n      API_KEY: ${{ secrets.API_KEY }}\n    steps:\n      - name: Check env empty\n        run: |\n          if [ -z \"$API_KEY\" ]; then\n            echo \"API_KEY is empty as expected\"\n          else\n            echo \"API_KEY is not empty\"\n            exit 1\n          fi",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "API_KEY"},
        {"type": "positive", "target": "run_status", "equals": "success"}
    ],
    "fixture"
))

# A3
write_text("SEC-PRTGT-01-001",
"""用例 ID:   SEC-PRTGT-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-002
母意图:    —
标题:      pull_request_target 下显式 checkout 不可信 PR 时 secrets 仍应受控

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 在 base 分支 workflow 中使用 pull_request_target 触发
  2. 显式 checkout fork PR 的 head sha 并执行脚本
  3. 观察 secrets 是否可被该脚本访问

预期结果:
  - 系统应阻止或限制在 pull_request_target 中直接执行未经审核的 fork PR 代码
  - secrets 不应被不可信代码直接读取

验证点:
  - [负向] 运行日志中不应出现 DEPLOY_TOKEN 明文
  - [正向] 若存在审批机制，未审批状态下 job 应处于挂起或拒绝态

清理:      重置 fixture 仓库
""")

write_yaml("SEC-PRTGT-01-001", build_yaml(
    "SEC-PRTGT-01-001", ["security"], "security", "P0",
    "pull_request_target 下显式 checkout 不可信 PR 时 secrets 仍应受控", "INTENT-SEC-002",
    {"repo_fixture": "with-secrets", "secrets": ["DEPLOY_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request_target", "as": "maintainer", "params": {}},
    "on:\n  pull_request_target:\n    branches: [main]\njobs:\n  risky-checkout:\n    name: Risky checkout test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Checkout PR head\n        uses: checkout\n        with:\n          ref: ${{ atomgit.event.pull_request.head.sha }}\n      - name: Attempt secret access\n        run: |\n          echo \"secret is ${{ secrets.DEPLOY_TOKEN }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "DEPLOY_TOKEN"},
        {"type": "positive", "target": "run_status", "equals": "blocked_or_pending"}
    ],
    "fixture"
))

print("Group A done")

# Group B continued
print("hello")
