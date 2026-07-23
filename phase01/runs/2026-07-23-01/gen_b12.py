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
    lines.append("workflow: |")
    for wl in wf.split("\n"):
        lines.append("  " + wl)
    lines.append("trigger:")
    lines.append("  event: " + trigger["event"])
    lines.append("  as: " + trigger["as"])
    lines.append("  params: " + json.dumps(trigger.get("params", {})))
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

write_text("SEC-TOCTOU-01-002",
"""用例 ID:   SEC-TOCTOU-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-031
母意图:    SEC-TOCTOU-01-001
标题:      评论触发不应绕过代码固定与 PR 审批

前置条件:
  - 仓库配置了 issue_comment 触发 workflow

操作步骤:
  1. 提交一个由 issue_comment 触发的高权限 workflow
  2. 在评论触发后、执行前推送新 commit
  3. 观察运行是否执行了最新 commit 而非触发时的 commit

预期结果:
  - 评论触发不应绕过代码固定
  - 运行应执行评论触发时刻锁定的 commit SHA

验证点:
  - [负向] 评论触发后推送的新 commit 绝不应被该次特权运行自动执行
  - [正向] 运行日志中的 commit SHA 与触发时刻一致

清理:      重置 fixture 仓库
""")

write_yaml("SEC-TOCTOU-01-002", build_yaml(
    "SEC-TOCTOU-01-002", ["security"], "security", "P0",
    "评论触发不应绕过代码固定与 PR 审批", "INTENT-SEC-031",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "issue_comment", "as": "untrusted_contributor", "params": {}},
    "on:\n  issue_comment:\n    types: [created]\njobs:\n  comment-toctou:\n    name: Test comment TOCTOU\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Check fixed commit\n        run: |\n          echo \"Executing commit: ${{ atomgit.sha }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "new_commit_after_trigger"},
        {"type": "positive", "target": "run_logs", "equals": "trigger_sha_matched"}
    ],
    "fixture"
))

write_text("SEC-SIDE-01-001",
"""用例 ID:   SEC-SIDE-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-032
母意图:    —
标题:      Secret 不经 output 侧信道绕过脱敏外泄

前置条件:
  - 仓库配置了 secret API_KEY

操作步骤:
  1. 提交一个 workflow，将 secret 写入 ATOMGIT_OUTPUT
  2. 触发 workflow 并检查 output 内容

预期结果:
  - Secret 明文不应以未遮蔽形式出现在 job output 中
  - output 中 secret 值应为 *** 或被拦截

验证点:
  - [负向] Secret 明文不应以未遮蔽形式出现在 job output 中
  - [非功能] 覆盖 output 侧信道

清理:      重置 fixture 仓库
""")

write_yaml("SEC-SIDE-01-001", build_yaml(
    "SEC-SIDE-01-001", ["security"], "security", "P0",
    "Secret 不经 output 侧信道绕过脱敏外泄", "INTENT-SEC-032",
    {"repo_fixture": "with-secrets", "secrets": ["API_KEY"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  side-output:\n    name: Test secret in output\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Write secret to output\n        id: step1\n        run: |\n          echo \"result=${{ secrets.API_KEY }}\" >> $ATOMGIT_OUTPUT\n      - name: Check output masked\n        run: |\n          echo \"output is ${{ steps.step1.outputs.result }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "API_KEY"},
        {"type": "negative", "target": "step_output", "must_not_contain_secret": "API_KEY"}
    ],
    "fixture"
))

write_text("SEC-SIDE-01-002",
"""用例 ID:   SEC-SIDE-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-032
母意图:    SEC-SIDE-01-001
标题:      Secret 不经 artifact 侧信道绕过脱敏外泄

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN

操作步骤:
  1. 提交一个 workflow，将 secret 写入文件并上传为 artifact
  2. 触发 workflow 并下载 artifact 检查内容

预期结果:
  - Artifact 中不应包含 secret 明文
  - 若 artifact 包含 secret，应被拦截或遮蔽

验证点:
  - [负向] Secret 明文不应以未遮蔽形式出现在上传的 artifact 中
  - [非功能] 覆盖 artifact 侧信道

清理:      重置 fixture 仓库
""")

write_yaml("SEC-SIDE-01-002", build_yaml(
    "SEC-SIDE-01-002", ["security"], "security", "P0",
    "Secret 不经 artifact 侧信道绕过脱敏外泄", "INTENT-SEC-032",
    {"repo_fixture": "with-secrets", "secrets": ["DEPLOY_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  side-artifact:\n    name: Test secret in artifact\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Write secret to file\n        run: |\n          echo \"token=${{ secrets.DEPLOY_TOKEN }}\" > secret.txt\n      - name: Upload artifact\n        uses: upload-artifact\n        with:\n          name: secret-artifact\n          path: secret.txt",
    [
        {"type": "negative", "target": "artifact_content", "must_not_contain_secret": "DEPLOY_TOKEN"},
        {"type": "positive", "target": "run_status", "equals": "blocked_or_masked"}
    ],
    "fixture"
))

print("b12 done")
