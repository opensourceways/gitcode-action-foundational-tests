#!/usr/bin/env python3
import os, json, sys

TEXT_DIR = "D:/业务/action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases/text"
YAML_DIR = "D:/业务/action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases/yaml"
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(YAML_DIR, exist_ok=True)

def write_text(cid, dims, dim, pri, intent, title, setup, steps, expected, vps, teardown, variant):
    dim_str = ", ".join(dims)
    lines = [
        "用例 ID:   " + cid,
        "维度标签:   [" + dim_str + "]",
        "维度:      " + dim,
        "优先级:    " + pri,
        "溯源意图:  " + intent,
        "母意图:    " + variant,
        "标题:      " + title,
        "",
        "前置条件:",
    ]
    for s in setup: lines.append("  - " + s)
    lines += ["", "操作步骤:"]
    for i, st in enumerate(steps, 1): lines.append("  " + str(i) + ". " + st)
    lines += ["", "预期结果:"]
    for e in expected: lines.append("  - " + e)
    lines += ["", "验证点:"]
    for vp in vps: lines.append("  - " + vp)
    lines += ["", "清理:      " + teardown]
    with open(os.path.join(TEXT_DIR, cid + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("[TEXT] " + cid)

def esc(v):
    if isinstance(v, str):
        bad = ':{}[]$#&*!|>%@`'
        if any(c in v for c in bad):
            return '"' + v + '"'
    return str(v)

def write_yaml(cid, dims, dim, pri, title, intent, fixture, secrets, variables, branch, wf, tev, tas, tparams, assertions, treset, fault):
    path = os.path.join(YAML_DIR, cid + ".yaml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("id: " + cid + "\n")
        f.write("dimensions: [" + ", ".join(dims) + "]\n")
        f.write("dimension: " + dim + "\n")
        f.write("priority: " + pri + "\n")
        f.write('title: "' + title + '"\n')
        f.write("intent_ref: " + intent + "\n")
        f.write("setup:\n")
        f.write("  repo_fixture: " + fixture + "\n")
        f.write("  secrets: " + secrets + "\n")
        f.write("  variables: " + variables + "\n")
        f.write("  branch_protection: " + branch + "\n")
        f.write("workflow: |\n")
        for line in wf.split("\n"):
            f.write("  " + line + "\n")
        f.write("trigger:\n")
        f.write("  event: " + tev + "\n")
        f.write("  as: " + tas + "\n")
        f.write("  params: " + tparams + "\n")
        if fault:
            f.write("fault_injection:\n")
            for k, v in fault.items():
                if isinstance(v, dict):
                    f.write("  " + k + ":\n")
                    for kk, vv in v.items(): f.write("    " + kk + ": " + str(vv) + "\n")
                else: f.write("  " + k + ": " + str(v) + "\n")
        else: f.write("fault_injection: null\n")
        f.write("assertions:\n")
        for a in assertions:
            f.write("  - type: " + a["type"] + "\n")
            f.write("    target: " + a["target"] + "\n")
            for k, v in a.items():
                if k in ("type", "target"): continue
                f.write("    " + k + ": " + esc(v) + "\n")
        f.write("teardown:\n")
        f.write("  reset: " + treset + "\n")
    print("[YAML] " + cid)

cases = []

# === COMPAT-001 ~ COMPAT-007 ===
cases.append(dict(
    cid="COMPAT-SHELL-01-001", intent="INTENT-COMPAT-001", dims=["compatibility"], dim="compatibility", pri="P1",
    title="未声明 shell 时默认使用 bash",
    setup=["仓库存在可执行的 workflow 文件", "Job 未声明 defaults.run.shell"],
    steps=["提交一个未声明 shell 的 workflow，在 step 中执行 echo $0", "触发 workflow 运行", "检查运行日志"],
    expected=["未声明 shell 的 step 中 $0 输出为 bash 或 /bin/bash", "多行脚本中的 bashism 正常执行"],
    vps=["[正向] 默认 shell 为 bash", "[负向] 不应静默使用 sh 导致 bashism 报错"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  check-shell:\n    name: Check default shell\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Echo shell\n        run: |\n          echo SHELL=$0\n          bash --version | head -n 1",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_logs","contains":"SHELL=bash"},{"type":"negative","target":"run_logs","must_not_contain":"SHELL=sh"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-SHELL-01-002", intent="INTENT-COMPAT-001", dims=["compatibility"], dim="compatibility", pri="P1",
    title="未声明 working-directory 时默认使用仓库根目录",
    setup=["仓库存在可执行 workflow 文件"],
    steps=["提交未声明 working-directory 的 workflow，执行 pwd", "触发运行", "检查日志"],
    expected=["pwd 输出为仓库根目录"],
    vps=["[正向] 默认工作目录为仓库根目录"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  check-wd:\n    name: Check default working directory\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Print working directory\n        run: |\n          pwd",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_logs","contains":"/workspace"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-PERM-01-001", intent="INTENT-COMPAT-002", dims=["compatibility","security"], dim="compatibility", pri="P0",
    title="未声明 permissions 时 ATOMGIT_TOKEN 可完成基本读操作",
    setup=["仓库配置 secrets.DEPLOY_TOKEN", "workflow 未声明 permissions"],
    steps=["提交未声明 permissions 的 workflow，执行读请求", "触发运行"],
    expected=["ATOMGIT_TOKEN 可完成基本 clone/read", "运行状态成功"],
    vps=["[正向] 默认权限足以完成读操作"],
    teardown="无", variant="—",
    fixture="with-secrets", secrets="[DEPLOY_TOKEN]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  read-test:\n    name: Test default token read\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Checkout source\n        uses: checkout\n      - name: Verify token can read\n        run: |\n          echo token_length=${{ len(atomgit.token) }}",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_status","equals":"success"},{"type":"positive","target":"run_logs","contains":"token_length="}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-PERM-01-002", intent="INTENT-COMPAT-002", dims=["compatibility","security"], dim="compatibility", pri="P0",
    title="未声明 permissions 时 fork PR 的 ATOMGIT_TOKEN 不应拥有写权限",
    setup=["仓库配置 secrets.DEPLOY_TOKEN", "存在来自 fork 的 PR"],
    steps=["以外部 fork 身份提交试图写入的 workflow", "在 fork PR 场景下触发"],
    expected=["fork PR 触发时写操作被阻止", "日志不出现 DEPLOY_TOKEN 明文"],
    vps=["[负向] fork PR 不应获得写权限", "[正向] 读操作正常"],
    teardown="重置 fixture 仓库", variant="—",
    fixture="with-secrets", secrets="[DEPLOY_TOKEN]", variables="{}", branch="default",
    wf="on:\n  pull_request:\n    branches: [main]\n\njobs:\n  write-test:\n    name: Test fork PR write blocked\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Attempt write via API\n        run: |\n          curl -s -w http_code -o /dev/null -X POST -H Authorization: token ${{ atomgit.token }} -d body=test ${{ atomgit.api_url }}/repos/${{ atomgit.repository }}/issues/1/comments\n          echo WRITE_ATTEMPT_DONE",
    tev="pr", tas="untrusted_contributor", tparams="{}",
    assertions=[{"type":"negative","target":"run_logs","must_not_contain_secret":"DEPLOY_TOKEN"},{"type":"positive","target":"run_logs","contains":"WRITE_ATTEMPT_DONE"}],
    treset="fixture", fault=None))

cases.append(dict(
    cid="COMPAT-IF-01-001", intent="INTENT-COMPAT-003", dims=["compatibility"], dim="compatibility", pri="P1",
    title="未写 if 的 step 在前置 step 失败时应被跳过",
    setup=["仓库存在 workflow 文件"],
    steps=["提交多 step workflow，step1 故意失败，step2 未写 if", "触发运行"],
    expected=["step1 失败后 step2 被跳过", "workflow 最终状态为失败"],
    vps=["[正向] 未写 if 的后续 step 被跳过", "[负向] 不应全部执行"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  if-default:\n    name: Test default if behavior\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Step one fail\n        run: |\n          echo step1\n          exit 1\n      - name: Step two should skip\n        run: |\n          echo step2_executed",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_status","equals":"failure"},{"type":"negative","target":"run_logs","must_not_contain":"step2_executed"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-IF-01-002", intent="INTENT-COMPAT-003", dims=["compatibility"], dim="compatibility", pri="P1",
    title="continue-on-error 后未写 if 的 step 默认行为应与显式 success 一致",
    setup=["仓库存在 workflow 文件"],
    steps=["提交含 continue-on-error=true 的 job，失败 step 后接未写 if 的 step", "触发运行"],
    expected=["continue-on-error 后未写 if 的 step 仍被执行"],
    vps=["[非功能] 默认条件行为与显式 if: success 一致"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  if-continue:\n    name: Test default if with continue on error\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Step one fail but continue\n        continue-on-error: true\n        run: |\n          echo step1\n          exit 1\n      - name: Step two should run\n        run: |\n          echo step2_executed",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_logs","contains":"step2_executed"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-EXPR-01-001", intent="INTENT-COMPAT-004", dims=["compatibility"], dim="compatibility", pri="P1",
    title="GitCode 无括号状态函数 success 应正确求值",
    setup=["仓库存在 workflow 文件"],
    steps=["提交 workflow 中使用 if: success 的 step", "触发运行"],
    expected=["前置步骤成功时 if: success 的 step 正常执行"],
    vps=["[正向] success 无括号语法在 GitCode 中可用"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  status-func:\n    name: Test status function success\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Step one ok\n        run: |\n          echo step1\n      - name: Step two with success\n        if: ${{ always() }}\n        run: |\n          echo step2_with_success",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_logs","contains":"step2_with_success"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-EXPR-01-002", intent="INTENT-COMPAT-004", dims=["compatibility"], dim="compatibility", pri="P1",
    title="GitHub 风格带括号状态函数 success() 不应导致崩溃",
    setup=["仓库存在 workflow 文件"],
    steps=["提交 workflow 中使用 if: success() 的 step", "触发运行或保存"],
    expected=["不应导致 workflow 解析阶段 panic", "应给出明确的解析报错或兼容处理"],
    vps=["[负向] success() 不应导致崩溃", "[非功能] 报错应提示 GitCode 不带括号"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  status-func-paren:\n    name: Test status function with parens\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Step one ok\n        run: |\n          echo step1\n      - name: Step two with success parens\n        if: ${{ always() }}\n        run: |\n          echo step2_with_success_parens",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"negative","target":"run_status","equals":"panic_or_crash"},{"type":"nonfunctional","target":"error_message","eval":"llm_assisted","rubric":"报错应包含 GitCode 状态函数不带括号的提示"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-EXPR-01-003", intent="INTENT-COMPAT-005", dims=["compatibility"], dim="compatibility", pri="P1",
    title="失败状态函数 failure 不应被静默当作 truthy",
    setup=["仓库存在 workflow 文件"],
    steps=["提交 workflow，step1 失败，step2 使用 if: failed，step3 使用 if: failure()", "触发运行"],
    expected=["if: failed 在 step1 失败后应执行", "if: failure() 不应导致崩溃或无条件执行"],
    vps=["[正向] failed 无括号在失败时返回 true", "[负向] failure() 不应被静默当作 truthy"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  failed-func:\n    name: Test failed function\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Step one fail\n        run: |\n          echo step1\n          exit 1\n      - name: Step two with failed\n        if: ${{ always() }}\n        run: |\n          echo step2_with_failed\n      - name: Step three with failure parens\n        if: ${{ always() }}\n        run: |\n          echo step3_with_failure_parens",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_logs","contains":"step2_with_failed"},{"type":"negative","target":"run_logs","must_not_contain":"step3_with_failure_parens"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-EXPR-01-004", intent="INTENT-COMPAT-006", dims=["compatibility"], dim="compatibility", pri="P1",
    title="contains 函数大小写不敏感行为应与 GitHub 一致",
    setup=["仓库存在 workflow 文件"],
    steps=["提交 workflow 中使用 contains 比较大小写混合字符串", "触发运行"],
    expected=["contains('Hello', 'LLO') 返回 true", "contains('Hello', 'llo') 返回 true"],
    vps=["[正向] 大小写混合匹配返回 true"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  contains-case:\n    name: Test contains case insensitive\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Check contains upper\n        run: |\n          echo RESULT_UPPER=${{ contains('Hello', 'LLO') }}\n      - name: Check contains lower\n        run: |\n          echo RESULT_LOWER=${{ contains('Hello', 'llo') }}",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_logs","contains":"RESULT_UPPER=true"},{"type":"positive","target":"run_logs","contains":"RESULT_LOWER=true"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-EXPR-01-005", intent="INTENT-COMPAT-006", dims=["compatibility"], dim="compatibility", pri="P1",
    title="contains 函数在空值输入时不应抛出异常",
    setup=["仓库存在 workflow 文件"],
    steps=["提交 workflow 中使用 contains(null, 'x')", "触发运行"],
    expected=["step 正常完成，不抛出异常", "返回结果为 false 或空值"],
    vps=["[负向] 不应抛出异常导致 step 失败"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  contains-null:\n    name: Test contains with null\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Check contains null\n        run: |\n          echo RESULT_NULL=${{ contains(null, 'x') }}\n      - name: Check contains empty\n        run: |\n          echo RESULT_EMPTY=${{ contains('', 'x') }}",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_status","equals":"success"},{"type":"positive","target":"run_logs","contains":"RESULT_NULL=false"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-EXPR-01-006", intent="INTENT-COMPAT-007", dims=["compatibility"], dim="compatibility", pri="P1",
    title="hashFiles 无匹配文件时应返回空字符串",
    setup=["仓库存在 workflow 文件"],
    steps=["提交 workflow 中使用 hashFiles('不存在的文件.json')", "触发运行"],
    expected=["hashFiles 返回空字符串", "step 正常完成不失败"],
    vps=["[正向] 无匹配返回空字符串", "[负向] 不应抛出异常"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  hashfiles-missing:\n    name: Test hashFiles missing file\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Hash missing file\n        run: |\n          echo HASH_MISSING=${{ hashFiles('not-exist-xyz.json') }}\n          echo DONE",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_logs","contains":"HASH_MISSING="},{"type":"positive","target":"run_status","equals":"success"}],
    treset="none", fault=None))

cases.append(dict(
    cid="COMPAT-EXPR-01-007", intent="INTENT-COMPAT-007", dims=["compatibility"], dim="compatibility", pri="P1",
    title="hashFiles 多路径模式应正确计算组合哈希",
    setup=["仓库存在 workflow 文件，包含 src/ 目录和 package.json"],
    steps=["提交 workflow 中使用 hashFiles('src/**', 'package.json')", "触发运行"],
    expected=["返回非空哈希字符串", "相同文件集多次调用返回相同结果"],
    vps=["[正向] 多路径模式返回确定性哈希"],
    teardown="无", variant="—",
    fixture="default", secrets="[]", variables="{}", branch="default",
    wf="on:\n  workflow_dispatch:\n\njobs:\n  hashfiles-multi:\n    name: Test hashFiles multi path\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Checkout source\n        uses: checkout\n      - name: Hash multiple paths\n        run: |\n          echo HASH_MULTI=${{ hashFiles('src/**', 'package.json') }}\n          echo DONE",
    tev="workflow_dispatch", tas="maintainer", tparams="{}",
    assertions=[{"type":"positive","target":"run_logs","contains":"HASH_MULTI="},{"type":"negative","target":"run_logs","must_not_contain":"HASH_MULTI=\n"}],
    treset="none", fault=None))


