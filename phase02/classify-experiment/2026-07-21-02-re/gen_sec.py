#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 01 Run 2026-07-21-02 增量用例生成脚本
生成 46 条新用例（44 独立缺口 + 2 变体）的文本用例 + 可执行 YAML
"""
import os

RUN_DIR = "phase01/runs/2026-07-21-02"
TEXT_DIR = os.path.join(RUN_DIR, "cases", "text")
YAML_DIR = os.path.join(RUN_DIR, "cases", "yaml")

def write_text_case(data):
    path = os.path.join(TEXT_DIR, f"{data['id']}.md")
    lines = [
        f"用例 ID:   {data['id']}",
        f"维度标签:   {data['dimensions']}",
        f"维度:      {data['dimension_label']}",
        f"优先级:    {data['priority']}",
        f"溯源意图:  {data['intent_ref']}",
    ]
    if data.get('mother'):
        lines.append(f"母意图:    {data['mother']}")
    else:
        lines.append("母意图:    —")
    lines.append(f"标题:      {data['title']}")
    lines.append("")
    lines.append("前置条件:")
    for pre in data['preconditions']:
        lines.append(f"  - {pre}")
    lines.append("")
    lines.append("操作步骤:")
    for i, step in enumerate(data['steps'], 1):
        lines.append(f"  {i}. {step}")
    lines.append("")
    lines.append("预期结果:")
    for exp in data['expected']:
        lines.append(f"  - {exp}")
    lines.append("")
    lines.append("验证点:")
    for vp in data['verification_points']:
        lines.append(f"  - {vp}")
    lines.append("")
    lines.append(f"清理:      {data['cleanup']}")
    lines.append("")
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"[text] {data['id']}")

def write_yaml_case(data):
    path = os.path.join(YAML_DIR, f"{data['id']}.yaml")
    workflow_lines = data['workflow'].strip().split('\n')
    # Indent workflow for block scalar if needed; here we assume workflow already formatted
    workflow_block = '\n'.join(workflow_lines)

    assertions_yaml = ""
    for a in data['assertions']:
        assertions_yaml += "  - type: " + a['type'] + "\n"
        assertions_yaml += "    target: " + a['target'] + "\n"
        for k, v in a.items():
            if k in ('type', 'target'):
                continue
            if isinstance(v, str):
                # Escape if needed
                assertions_yaml += f"    {k}: \"{v}\"\n"
            else:
                assertions_yaml += f"    {k}: {v}\n"

    trigger_params = data.get('trigger_params', {})
    trigger_params_yaml = ""
    if trigger_params:
        for k, v in trigger_params.items():
            if isinstance(v, str):
                trigger_params_yaml += f"    {k}: \"{v}\"\n"
            else:
                trigger_params_yaml += f"    {k}: {v}\n"

    fault_yaml = "null"
    if data.get('fault_injection'):
        fi = data['fault_injection']
        fault_yaml = f"""at: {fi['at']}
  action: {fi['action']}
  params:
"""
        for k, v in fi.get('params', {}).items():
            fault_yaml += f"    {k}: {v}\n"
        fault_yaml += f"  recovery_expectation: {fi['recovery_expectation']}"

    secrets_list = data.get('secrets', [])
    secrets_yaml = "[" + ", ".join(f'"{s}"' for s in secrets_list) + "]" if secrets_list else "[]"

    content = f"""id: {data['id']}
dimensions: {data['dimensions']}
dimension: {data['dimension']}
priority: {data['priority']}
title: "{data['title']}"
intent_ref: {data['intent_ref']}

setup:
  repo_fixture: {data['repo_fixture']}
  secrets: {secrets_yaml}
  variables: {{}}
  branch_protection: default

workflow: |
{workflow_block}

trigger:
  event: {data['trigger_event']}
  as: {data['trigger_as']}
  params:
{trigger_params_yaml}
fault_injection: {fault_yaml}

assertions:
{assertions_yaml}teardown:
  reset: {data['teardown_reset']}
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[yaml] {data['id']}")

def main():
    os.makedirs(TEXT_DIR, exist_ok=True)
    os.makedirs(YAML_DIR, exist_ok=True)

    cases = []

    # ========== SEC 缺口 (12 独立 + 2 变体) ==========

    # SEC-020
    cases.append({
        'id': 'SEC-CACHE-ISOLATE-02-001',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': 'cache key 跨项目/跨仓库作用域隔离（无横向污染）',
        'intent_ref': 'INTENT-SEC-020',
        'mother': '',
        'preconditions': [
            '存在两个独立仓库 repo-A 与 repo-B',
            '两仓库均配置了同名 cache key'
        ],
        'steps': [
            '在 repo-A 的 workflow 中写入 cache（key=shared-test-key）',
            '在 repo-B 的 workflow 中尝试 restore 相同 key',
            '观察 repo-B 的 cache 命中状态'
        ],
        'expected': [
            'repo-B 应产生 CACHE_MISS，不应读取到 repo-A 的缓存数据',
            '缓存作用域应至少隔离到仓库级别'
        ],
        'verification_points': [
            '[负向] 日志不含 repo-A 写入的缓存内容',
            '[正向] repo-B 出现 CACHE_MISS'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'basic-ci',
        'secrets': [],
        'workflow': """  on:
  - push
  jobs:
    cache-write:
      name: Cache Write
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Write cache
        uses: cache
        with:
          key: cross-repo-isolation-test
          path: ./cached-data.txt
      - name: Create cache data
        run: echo "REPO_A_SECRET_DATA" > cached-data.txt""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {'cross_repo_check': 'true'},
        'assertions': [
            {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '同仓库第二次运行出现 CACHE_HIT'},
            {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '跨仓库运行不出现 REPO_A_SECRET_DATA'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-021
    cases.append({
        'id': 'SEC-SHA-REF-02-001',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': 'uses 支持 commit SHA 不可变引用，且 tag/分支重写风险应被识别',
        'intent_ref': 'INTENT-SEC-021',
        'mother': '',
        'preconditions': [
            '目标 action 仓库存在已知 commit SHA 与 tag',
            '测试仓库有权引用该 action'
        ],
        'steps': [
            '在 workflow 中使用 uses: owner/action@<commit-sha> 引用 action',
            '观察运行是否成功拉取该 action',
            '再测试 uses: owner/action@<tag> 在 tag 被强制推送后的行为'
        ],
        'expected': [
            'commit SHA 引用应始终解析到同一版本',
            'tag 被重写后，原 workflow 不应静默执行不同代码'
        ],
        'verification_points': [
            '[正向] SHA 引用运行成功',
            '[负向] tag 重写后旧 run 不应静默失败或被劫持'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'basic-ci',
        'secrets': [],
        'workflow': """  on:
  - push
  jobs:
    sha-ref:
      name: SHA Ref Test
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Use action by SHA
        uses: checkout@a1b2c3d4e5f6""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'run 状态为成功'},
            {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '无 action 被篡改的异常日志'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-022
    cases.append({
        'id': 'SEC-ACTION-PERM-02-001',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': '第三方 action 对 ATOMGIT_TOKEN / secret 的隐式获取受最小权限约束',
        'intent_ref': 'INTENT-SEC-022',
        'mother': '',
        'preconditions': [
            '仓库配置了 TEST_SECRET',
            '使用一个非官方第三方 action'
        ],
        'steps': [
            '在 workflow 中调用第三方 action',
            '该 action 的代码尝试读取 secrets.TEST_SECRET 或 atomgit.token',
            '观察运行日志与权限行为'
        ],
        'expected': [
            '第三方 action 不应默认获得仓库 secrets 访问权',
            '系统应通过 permissions 或 token 范围限制其权限'
        ],
        'verification_points': [
            '[负向] 第三方 action 日志不含 TEST_SECRET 明文',
            '[正向] permissions 声明生效'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'with-secrets',
        'secrets': ['TEST_SECRET'],
        'workflow': """  on:
  - push
  permissions:
    repository: read
  jobs:
    third-party:
      name: Third Party Action
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Run third party action
        uses: some-third-party/action
        with:
          input-param: test""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'TEST_SECRET'},
            {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '若权限不足则 action 失败或被限制'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-023
    cases.append({
        'id': 'SEC-TOKEN-EXPIRE-02-001',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': 'ATOMGIT_TOKEN 运行后失效且不可通过缓存/残留复活',
        'intent_ref': 'INTENT-SEC-023',
        'mother': '',
        'preconditions': [
            '仓库配置了 TOKEN_TEST_SECRET',
            'workflow 在运行中将 token 写入临时文件'
        ],
        'steps': [
            '在 run step 中将 ${{ atomgit.token }} 写入 /tmp/token_dump.txt',
            '在后续 step 中尝试读取该文件并使用 token 调用 API',
            '在 run 结束后尝试从外部复用该 token'
        ],
        'expected': [
            '运行期间临时文件中的 token 不应在运行结束后仍然有效',
            'runner 工作区应在 job 结束后清理'
        ],
        'verification_points': [
            '[负向] 运行结束后 token 调用 API 被拒绝',
            '[正向] 同一 runner 后续 job 读取不到旧 token 文件'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'basic-ci',
        'secrets': ['TOKEN_TEST_SECRET'],
        'workflow': """  on:
  - push
  jobs:
    token-lifecycle:
      name: Token Lifecycle
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Dump token to file
        run: echo "${{ atomgit.token }}" > /tmp/token_dump.txt
      - name: Verify token file exists in same job
        run: cat /tmp/token_dump.txt""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '同 job 内可读取 token 文件'},
            {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'TOKEN_TEST_SECRET'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-024
    cases.append({
        'id': 'SEC-ENV-POLLUTE-02-001',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': '工作流写协议（ATOMGIT_ENV/OUTPUT/PATH）不被不可信输入污染提权',
        'intent_ref': 'INTENT-SEC-024',
        'mother': '',
        'preconditions': [
            'workflow 接收来自 PR 标题/评论等不可信输入',
            '存在后续高权限 step'
        ],
        'steps': [
            '在 PR 标题中注入恶意字符串（如包含换行符的伪造 workflow 命令）',
            '在 workflow 中将 PR 标题写入 $ATOMGIT_ENV',
            '观察后续 step 的环境变量与行为'
        ],
        'expected': [
            '不可信输入写入 ATOMGIT_ENV 时不应解析执行注入命令',
            '后续 step 不应因写协议污染而获得提权'
        ],
        'verification_points': [
            '[负向] 无注入命令被执行',
            '[负向] 环境变量不含恶意换行注入内容'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'basic-ci',
        'secrets': [],
        'workflow': """  on:
  - pull_request
  jobs:
    env-pollute:
      name: Env Pollute Test
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Write untrusted input to env
        run: |
          PR_TITLE="${{ atomgit.event.pull_request.title }}"
          echo "PR_TITLE=$PR_TITLE" >> $ATOMGIT_ENV
      - name: Read env in next step
        run: echo "$PR_TITLE"""",
        'trigger_event': 'pr',
        'trigger_as': 'untrusted_contributor',
        'trigger_params': {'pr_title_injection': 'true'},
        'assertions': [
            {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '无额外命令被执行'},
            {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'run 正常完成或按预期失败'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-025
    cases.append({
        'id': 'SEC-RUNNER-LEAK-02-001',
        'dimensions': '[security, reliability]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P0',
        'title': 'Runner 跨 job/跨 run 无敏感残留（工作区/环境/凭据清理）',
        'intent_ref': 'INTENT-SEC-025',
        'mother': '',
        'preconditions': [
            'runner 支持多 job 复用',
            '前一个 job 写入了敏感文件与环境变量'
        ],
        'steps': [
            'job-1 在 workspace 与 /tmp 写入标记文件与 secret',
            'job-2 在相同 runner 上检查 workspace 与 /tmp 是否存在 job-1 残留',
            'job-2 检查环境变量中是否残留 job-1 的 secrets'
        ],
        'expected': [
            'job-2 不应发现 job-1 的文件残留',
            '环境变量不应包含 job-1 的 secret 值'
        ],
        'verification_points': [
            '[负向] job-2 日志不含 job-1 的 secret 明文',
            '[负向] job-2 检查不到 job-1 的标记文件'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'with-secrets',
        'secrets': ['LEAK_TEST_SECRET'],
        'workflow': """  on:
  - push
  jobs:
    job-leak-a:
      name: Job Leak A
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Write sensitive data
        run: |
          echo "${{ secrets.LEAK_TEST_SECRET }}" > /tmp/sensitive.txt
          echo "SENSITIVE_FILE_CREATED"
    job-leak-b:
      name: Job Leak B
      needs: job-leak-a
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Check for残留
        run: |
          if [ -f /tmp/sensitive.txt ]; then
            echo "LEAK_FOUND_UNEXPECTED"
          else
            echo "NO_LEAK_AS_EXPECTED"
          fi""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 NO_LEAK_AS_EXPECTED'},
            {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志不出现 LEAK_FOUND_UNEXPECTED'},
            {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'LEAK_TEST_SECRET'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-026
    cases.append({
        'id': 'SEC-DISK-LEAK-02-001',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': '共享盘（/tmp、workspace）不跨 job 泄露敏感文件',
        'intent_ref': 'INTENT-SEC-026',
        'mother': '',
        'preconditions': [
            'job-A 在 /tmp 与 workspace 创建含敏感数据的文件'
        ],
        'steps': [
            'job-A 写入 /tmp/secret.txt 与 $GITHUB_WORKSPACE/secret.txt',
            'job-B 读取 /tmp/secret.txt 与 workspace/secret.txt'
        ],
        'expected': [
            'job-B 应读取不到 job-A 的敏感文件',
            '共享盘在 job 切换时应被清理或隔离'
        ],
        'verification_points': [
            '[负向] job-B 日志不含 job-A 的敏感数据',
            '[正向] job-B 报告文件不存在'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'with-secrets',
        'secrets': ['DISK_TEST_SECRET'],
        'workflow': """  on:
  - push
  jobs:
    disk-a:
      name: Disk A
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Write secret to tmp
        run: echo "${{ secrets.DISK_TEST_SECRET }}" > /tmp/disk_secret.txt
    disk-b:
      name: Disk B
      needs: disk-a
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Check tmp file
        run: |
          if [ -f /tmp/disk_secret.txt ]; then
            echo "DISK_LEAK_FOUND"
          else
            echo "DISK_NO_LEAK"
          fi""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 DISK_NO_LEAK'},
            {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志不出现 DISK_LEAK_FOUND'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-028
    cases.append({
        'id': 'SEC-RUNNER-SHARE-02-001',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P0',
        'title': '多项目共享 Runner 的 Secret 与资源隔离（项目 A secret 不达项目 B）',
        'intent_ref': 'INTENT-SEC-028',
        'mother': '',
        'preconditions': [
            '同一 runner 组被多个项目共享',
            '项目 A 配置了 SECRET_A，项目 B 未配置同名 secret'
        ],
        'steps': [
            '在项目 A 的 workflow 中输出 secrets.SECRET_A',
            '在项目 B 的 workflow 中尝试读取 secrets.SECRET_A',
            '观察两项目的运行结果'
        ],
        'expected': [
            '项目 B 的 workflow 不应读取到项目 A 的 SECRET_A',
            'runner 上的 secret 注入应严格按项目隔离'
        ],
        'verification_points': [
            '[负向] 项目 B 日志不含 SECRET_A 明文',
            '[正向] 项目 B 中 secrets.SECRET_A 为空或报错'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'with-secrets',
        'secrets': ['SECRET_A'],
        'workflow': """  on:
  - push
  jobs:
    cross-project:
      name: Cross Project Secret
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Access secret
        run: |
          VAL="${{ secrets.SECRET_A }}"
          if [ -z "$VAL" ]; then
            echo "SECRET_EMPTY_AS_EXPECTED"
          else
            echo "SECRET_NOT_EMPTY"
          fi""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {'cross_project': 'true'},
        'assertions': [
            {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 SECRET_EMPTY_AS_EXPECTED'},
            {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'SECRET_A'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-030
    cases.append({
        'id': 'SEC-ENV-REVIEW-02-001',
        'dimensions': '[security, usability]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': '环境保护规则（reviewers/wait timer）未审批时环境 Secret 不可访问',
        'intent_ref': 'INTENT-SEC-030',
        'mother': '',
        'preconditions': [
            '仓库配置了 environment "production" 与对应 reviewers',
            '环境配置了环境级 secret ENV_SECRET'
        ],
        'steps': [
            '触发一个指向 production 环境的 workflow',
            '在审批通过前观察 workflow 状态',
            '审批通过后再次观察'
        ],
        'expected': [
            '未审批时 job 应处于等待状态，且不可访问 ENV_SECRET',
            '审批通过后 job 才能继续并读取到 ENV_SECRET'
        ],
        'verification_points': [
            '[负向] 未审批时 job 不读取到 ENV_SECRET',
            '[正向] 审批后 job 成功执行'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'with-secrets',
        'secrets': ['ENV_SECRET'],
        'workflow': """  on:
  - push
  jobs:
    deploy:
      name: Deploy to Production
      runs-on: [ubuntu-latest, x64, small]
      environment: production
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Access env secret
        run: |
          VAL="${{ secrets.ENV_SECRET }}"
          if [ -n "$VAL" ]; then
            echo "ENV_SECRET_ACCESS_GRANTED"
          else
            echo "ENV_SECRET_EMPTY"
          fi""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '未审批时 run 状态为 waiting 或 paused'},
            {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'ENV_SECRET'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-031
    cases.append({
        'id': 'SEC-TOCTOU-02-001',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': 'TOCTOU：审批后推送新 commit / 评论触发不绕过审批与代码固定',
        'intent_ref': 'INTENT-SEC-031',
        'mother': '',
        'preconditions': [
            '存在已审批的 PR workflow',
            '审批后 PR 又有新 commit 推送'
        ],
        'steps': [
            'PR workflow 获得审批并开始运行',
            '在运行过程中向 PR 推送新 commit',
            '观察 workflow 是否重新触发并需要重新审批'
        ],
        'expected': [
            '新 commit 推送后应触发新的 workflow run',
            '新 run 不应继承旧审批，应要求重新审批'
        ],
        'verification_points': [
            '[负向] 新 commit 不导致旧 run 执行未审批代码',
            '[正向] 新 run 正确关联最新 commit SHA'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'basic-ci',
        'secrets': [],
        'workflow': """  on:
  - pull_request
  jobs:
    toctou-check:
      name: TOCTOU Check
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Log commit SHA
        run: echo "RUNNING_ON_SHA=${{ atomgit.sha }}"""",
        'trigger_event': 'pr',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志中的 SHA 与最新 commit 一致'},
            {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '旧 run 不会在新 commit 后重新执行'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-032
    cases.append({
        'id': 'SEC-SIDECHAN-02-001',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': 'Secret 不经 output / artifact / step summary 侧信道绕过脱敏外泄',
        'intent_ref': 'INTENT-SEC-032',
        'mother': '',
        'preconditions': [
            '仓库配置了 SIDECHAN_SECRET',
            'workflow 将 secret 写入 output、artifact 与 step summary'
        ],
        'steps': [
            '在 step 中将 secret 写入 $ATOMGIT_OUTPUT',
            '在 step 中将 secret 写入 $ATOMGIT_STEP_SUMMARY',
            '上传包含 secret 的文件作为 artifact'
        ],
        'expected': [
            'output 与 step summary 中的 secret 值应被脱敏为 ***',
            'artifact 中的 secret 明文不应被保留（或被平台拒绝）'
        ],
        'verification_points': [
            '[负向] output 中不含 secret 明文',
            '[负向] step summary 中不含 secret 明文',
            '[负向] artifact 下载内容不含 secret 明文'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'with-secrets',
        'secrets': ['SIDECHAN_SECRET'],
        'workflow': """  on:
  - push
  jobs:
    sidechan:
      name: Side Channel Test
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Write secret to output
        run: echo "secret_val=${{ secrets.SIDECHAN_SECRET }}" >> $ATOMGIT_OUTPUT
      - name: Write secret to summary
        run: echo "secret=${{ secrets.SIDECHAN_SECRET }}" >> $ATOMGIT_STEP_SUMMARY
      - name: Create artifact with secret
        run: echo "${{ secrets.SIDECHAN_SECRET }}" > secret_file.txt
      - name: Upload artifact
        uses: upload-artifact
        with:
          name: secret-artifact
          path: secret_file.txt""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'SIDECHAN_SECRET'},
            {'type': 'negative', 'target': 'step_summary', 'eval': 'deterministic', 'rubric': 'step summary 不含 secret 明文'},
            {'type': 'negative', 'target': 'artifacts', 'eval': 'deterministic', 'rubric': 'artifact 内容不含 secret 明文'}
        ],
        'teardown_reset': 'fixture'
    })

    # SEC-033
    cases.append({
        'id': 'SEC-JOB-ISOLATE-02-001',
        'dimensions': '[security, reliability]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': '同主机 Runner 并发 job 间的隔离（进程/文件/环境互不可见）',
        'intent_ref': 'INTENT-SEC-033',
        'mother': '',
        'preconditions': [
            '同一 runner 上并发执行两个 job',
            'job-1 创建标记文件并写入进程信息'
        ],
        'steps': [
            'job-1 与 job-2 同时运行',
            'job-1 在 /tmp 与 workspace 创建隔离标记',
            'job-2 检查 /tmp 与 workspace 是否存在 job-1 的标记'
        ],
        'expected': [
            '并发 job 之间不应看到对方的进程、文件或环境变量'
        ],
        'verification_points': [
            '[负向] job-2 检测不到 job-1 的进程',
            '[负向] job-2 读取不到 job-1 的文件'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'basic-ci',
        'secrets': [],
        'workflow': """  on:
  - push
  jobs:
    isolate-a:
      name: Isolate A
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Create marker
        run: |
          echo "A_MARKER" > /tmp/isolate_marker.txt
          echo "PID_A=$$"
    isolate-b:
      name: Isolate B
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Check isolation
        run: |
          if [ -f /tmp/isolate_marker.txt ]; then
            echo "ISOLATION_BROKEN"
          else
            echo "ISOLATION_INTACT"
          fi""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 ISOLATION_INTACT'},
            {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志不出现 ISOLATION_BROKEN'}
        ],
        'teardown_reset': 'fixture'
    })

    # 变体 SEC-006-V1 (原 SEC-007)
    cases.append({
        'id': 'SEC-SECRET-MASK-02-002-V1',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P0',
        'title': 'Secret 字符串拼接/分片输出时仍应被脱敏',
        'intent_ref': 'INTENT-SEC-007',
        'mother': 'INTENT-SEC-006',
        'preconditions': [
            '仓库配置了 SPLIT_SECRET',
            'workflow 将 secret 拆分为多段输出'
        ],
        'steps': [
            '在 run step 中将 secret 的前半段与后半段分别 echo',
            '在 run step 中将 secret 与已知字符串拼接后 echo'
        ],
        'expected': [
            '拼接后的完整 secret 仍应被脱敏',
            '分片输出的 secret 片段也应被脱敏'
        ],
        'verification_points': [
            '[负向] 日志不含 SPLIT_SECRET 明文',
            '[负向] 日志不含拼接后的完整 secret'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'with-secrets',
        'secrets': ['SPLIT_SECRET'],
        'workflow': """  on:
  - push
  jobs:
    split-mask:
      name: Split Mask Test
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Echo split parts
        run: |
          SEC="${{ secrets.SPLIT_SECRET }}"
          LEN=${#SEC}
          HALF=$((LEN/2))
          echo "${SEC:0:HALF}"
          echo "${SEC:HALF}"
      - name: Echo concatenated
        run: |
          PREFIX="prefix_"
          SUFFIX="_suffix"
          echo "$PREFIX${{ secrets.SPLIT_SECRET }}$SUFFIX"""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'SPLIT_SECRET'},
            {'type': 'nonfunctional', 'target': 'run_logs', 'eval': 'llm_assisted', 'rubric': '拼接输出中 secret 部分应被遮蔽'}
        ],
        'teardown_reset': 'fixture'
    })

    # 变体 SEC-006-V2 (原 SEC-008)
    cases.append({
        'id': 'SEC-SECRET-MASK-02-002-V2',
        'dimensions': '[security]',
        'dimension': 'security',
        'dimension_label': '安全性',
        'priority': 'P1',
        'title': '多行 Secret 值的逐行脱敏覆盖',
        'intent_ref': 'INTENT-SEC-008',
        'mother': 'INTENT-SEC-006',
        'preconditions': [
            '仓库配置了 MULTILINE_SECRET（值含换行符）',
            'workflow 将多行 secret 输出到日志'
        ],
        'steps': [
            '在 run step 中 echo 多行 secret',
            '观察每一行的脱敏行为'
        ],
        'expected': [
            '多行 secret 的每一行都应被脱敏为 ***',
            '换行不应导致脱敏中断'
        ],
        'verification_points': [
            '[负向] 日志不含 MULTILINE_SECRET 的任意一行明文',
            '[正向] 日志中出现对应行数的 *** 遮蔽'
        ],
        'cleanup': '重置 fixture 仓库',
        'repo_fixture': 'with-secrets',
        'secrets': ['MULTILINE_SECRET'],
        'workflow': """  on:
  - push
  jobs:
    multiline-mask:
      name: Multiline Mask Test
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Echo multiline secret
        run: |
          echo "${{ secrets.MULTILINE_SECRET }}"""",
        'trigger_event': 'push',
        'trigger_as': 'maintainer',
        'trigger_params': {},
        'assertions': [
            {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'MULTILINE_SECRET'},
            {'type': 'nonfunctional', 'target': 'run_logs', 'eval': 'llm_assisted', 'rubric': '多行输出中每一行敏感内容均被遮蔽'}
        ],
        'teardown_reset': 'fixture'
    })

    print(f"Prepared {len(cases)} cases so far (SEC batch).")
    for c in cases:
        write_text_case(c)
        write_yaml_case(c)
    print("SEC batch done.")

if __name__ == '__main__':
    main()
