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

write_text("SEC-PRTGT-01-002",
"""用例 ID:   SEC-PRTGT-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-002
母意图:    SEC-PRTGT-01-001
标题:      pull_request_target 无审批不执行 fork PR 代码

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 在 base 分支 workflow 中使用 pull_request_target 触发
  2. 显式 checkout fork PR 的 head sha
  3. 在无审批状态下触发 workflow

预期结果:
  - 未审批状态下 job 应处于挂起或拒绝态
  - 不应直接执行 fork PR 的代码

验证点:
  - [负向] 绝不应在无审批情况下，让 pull_request_target 的 job 直接执行 fork PR 的构建脚本
  - [正向] 若存在审批机制，未审批状态下 job 应处于挂起或拒绝态

清理:      重置 fixture 仓库
""")

write_yaml("SEC-PRTGT-01-002", build_yaml(
    "SEC-PRTGT-01-002", ["security"], "security", "P0",
    "pull_request_target 无审批不执行 fork PR 代码", "INTENT-SEC-002",
    {"repo_fixture": "with-secrets", "secrets": ["DEPLOY_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request_target", "as": "maintainer", "params": {}},
    "on:\n  pull_request_target:\n    branches: [main]\njobs:\n  unapproved-checkout:\n    name: Unapproved checkout test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Checkout PR head\n        uses: checkout\n        with:\n          ref: ${{ atomgit.event.pull_request.head.sha }}\n      - name: Run build\n        run: |\n          echo \"Building PR code\"",
    [
        {"type": "negative", "target": "run_status", "must_not_equal": "success_without_approval"},
        {"type": "positive", "target": "run_status", "equals": "pending_or_blocked"}
    ],
    "fixture"
))

write_text("SEC-DOS-01-001",
"""用例 ID:   SEC-DOS-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-033
母意图:    —
标题:      大 artifact / 大 cache 必须受配额与边界限制

前置条件:
  - 仓库支持 artifact 和 cache 上传

操作步骤:
  1. 提交一个 workflow，尝试上传超大 artifact 或写入超大 cache
  2. 触发 workflow 并查看上传结果

预期结果:
  - 超过大小上限的 artifact/cache 上传绝不应成功写入
  - 超限时应给出明确报错（大小限制值），不应静默截断或卡死

验证点:
  - [负向] 超过大小上限的 artifact/cache 上传绝不应成功写入
  - [非功能] 超限时应给出明确报错（大小限制值），不应静默截断或卡死

清理:      重置 fixture 仓库
""")

write_yaml("SEC-DOS-01-001", build_yaml(
    "SEC-DOS-01-001", ["security"], "security", "P0",
    "大 artifact / 大 cache 必须受配额与边界限制", "INTENT-SEC-033",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  quota-test:\n    name: Test size quota\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Create large file\n        run: |\n          dd if=/dev/zero of=large.bin bs=1M count=1100\n      - name: Upload large artifact\n        uses: upload-artifact\n        with:\n          name: large-artifact\n          path: large.bin",
    [
        {"type": "negative", "target": "run_status", "must_not_equal": "success"},
        {"type": "positive", "target": "run_logs", "equals": "size_limit_exceeded_error"}
    ],
    "fixture"
))

write_text("SEC-OIDC-01-001",
"""用例 ID:   SEC-OIDC-01-001
维度标签:   [security, compatibility]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-034
母意图:    —
标题:      OIDC / 短时凭据支持若缺失，必须明确标注为平台限制并提供替代安全方案

前置条件:
  - 仓库需要云部署凭据

操作步骤:
  1. 查阅 GitCode 文档，确认 OIDC 支持状态
  2. 若不支持，验证文档是否明确标注并提供替代方案

预期结果:
  - 不支持 OIDC 时，系统绝不应提供可长期复用的高权限云部署凭证作为默认方案
  - 文档中明确标注 OIDC 不支持，或 OIDC token 确实具备短时效与一次性

验证点:
  - [负向] 不支持 OIDC 时，系统绝不应提供可长期复用的高权限云部署凭证作为默认方案
  - [非功能] 若支持，应提供审计日志追踪 OIDC token 的签发与使用

清理:      无
""")

write_yaml("SEC-OIDC-01-001", build_yaml(
    "SEC-OIDC-01-001", ["security", "compatibility"], "security", "P1",
    "OIDC / 短时凭据支持若缺失，必须明确标注为平台限制并提供替代安全方案", "INTENT-SEC-034",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  oidc-check:\n    name: Check OIDC documentation\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Document check placeholder\n        run: |\n          echo \"Checking OIDC support documentation\"",
    [
        {"type": "negative", "target": "platform_docs", "must_not_contain": "long_term_cloud_token_default"},
        {"type": "positive", "target": "platform_docs", "equals": "oidc_limitation_documented"}
    ],
    "none"
))

print("b13 done")
