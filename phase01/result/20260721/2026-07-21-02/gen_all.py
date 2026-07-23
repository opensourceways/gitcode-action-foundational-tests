#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json

RUN_DIR = "."
TEXT_DIR = os.path.join(RUN_DIR, "cases", "text")
YAML_DIR = os.path.join(RUN_DIR, "cases", "yaml")

os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(YAML_DIR, exist_ok=True)

def write_text_case(c):
    path = os.path.join(TEXT_DIR, f"{c['id']}.md")
    mother = c.get('mother','')
    mother_line = f"母意图:    {mother}" if mother else "母意图:    —"
    lines = [
        f"用例 ID:   {c['id']}",
        f"维度标签:   {c['dimensions']}",
        f"维度:      {c['dimension_label']}",
        f"优先级:    {c['priority']}",
        f"溯源意图:  {c['intent_ref']}",
        mother_line,
        f"标题:      {c['title']}",
        "",
        "前置条件:",
    ]
    for p in c['preconditions']:
        lines.append(f"  - {p}")
    lines.append("")
    lines.append("操作步骤:")
    for i, s in enumerate(c['steps'], 1):
        lines.append(f"  {i}. {s}")
    lines.append("")
    lines.append("预期结果:")
    for e in c['expected']:
        lines.append(f"  - {e}")
    lines.append("")
    lines.append("验证点:")
    for v in c['verification_points']:
        lines.append(f"  - {v}")
    lines.append("")
    lines.append(f"清理:      {c['cleanup']}")
    lines.append("")
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"[text] {c['id']}")

def write_yaml_case(c):
    path = os.path.join(YAML_DIR, f"{c['id']}.yaml")
    wf = c['workflow']
    tp = c.get('trigger_params', {})
    tp_yaml = '\n'.join(f'    {k}: "{v}"' for k,v in tp.items()) + '\n' if tp else ''

    assertions_lines = []
    for a in c['assertions']:
        lines = f"  - type: {a['type']}\n    target: {a['target']}"
        for k,v in a.items():
            if k in ('type','target'): continue
            lines += f'\n    {k}: "{v}"'
        assertions_lines.append(lines)
    assertions_yaml = '\n'.join(assertions_lines)

    fi = c.get('fault_injection')
    if fi:
        params_yaml = '\n'.join(f'    {k}: {v}' for k,v in fi.get('params',{}).items())
        fault_yaml = f"""\n  at: {fi['at']}
  action: {fi['action']}
  params:
{params_yaml}
  recovery_expectation: {fi['recovery_expectation']}"""
    else:
        fault_yaml = "null"

    secrets = c.get('secrets', [])
    secrets_yaml = "[" + ", ".join(f'"{s}"' for s in secrets) + "]" if secrets else "[]"

    content = f'''id: {c['id']}
dimensions: {c['dimensions']}
dimension: {c['dimension']}
priority: {c['priority']}
title: "{c['title']}"
intent_ref: {c['intent_ref']}

setup:
  repo_fixture: {c['repo_fixture']}
  secrets: {secrets_yaml}
  variables: {{}}
  branch_protection: default

workflow: |
{wf}

trigger:
  event: {c['trigger_event']}
  as: {c['trigger_as']}
  params:
{tp_yaml}
fault_injection: {fault_yaml}

assertions:
{assertions_yaml}

teardown:
  reset: {c['teardown_reset']}
'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[yaml] {c['id']}")

cases = []

# ===== SEC batch (14 cases) =====

cases.append({
    'id': 'SEC-CACHE-ISOLATE-02-001',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': 'cache key 跨项目/跨仓库作用域隔离（无横向污染）',
    'intent_ref': 'INTENT-SEC-020',
    'preconditions': ['存在两个独立仓库 repo-A 与 repo-B', '两仓库均配置了同名 cache key'],
    'steps': ['在 repo-A 的 workflow 中写入 cache（key=shared-test-key）', '在 repo-B 的 workflow 中尝试 restore 相同 key', '观察 repo-B 的 cache 命中状态'],
    'expected': ['repo-B 应产生 CACHE_MISS，不应读取到 repo-A 的缓存数据', '缓存作用域应至少隔离到仓库级别'],
    'verification_points': ['[负向] 日志不含 repo-A 写入的缓存内容', '[正向] repo-B 出现 CACHE_MISS'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Cross Repo Cache Isolation
  on:
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
        run: echo "REPO_A_SECRET_DATA" > cached-data.txt''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {'cross_repo_check': 'true'},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '同仓库第二次运行出现 CACHE_HIT'},
        {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '跨仓库运行不出现 REPO_A_SECRET_DATA'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-SHA-REF-02-001',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': 'uses 支持 commit SHA 不可变引用，且 tag/分支重写风险应被识别',
    'intent_ref': 'INTENT-SEC-021',
    'preconditions': ['目标 action 仓库存在已知 commit SHA 与 tag', '测试仓库有权引用该 action'],
    'steps': ['在 workflow 中使用 uses: owner/action@<commit-sha> 引用 action', '观察运行是否成功拉取该 action', '再测试 uses: owner/action@<tag> 在 tag 被强制推送后的行为'],
    'expected': ['commit SHA 引用应始终解析到同一版本', 'tag 被重写后，原 workflow 不应静默执行不同代码'],
    'verification_points': ['[正向] SHA 引用运行成功', '[负向] tag 重写后旧 run 不应静默失败或被劫持'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: SHA Ref Test
  on:
  - push
  jobs:
    sha-ref:
      name: SHA Ref Test
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Use action by SHA
        uses: checkout@a1b2c3d4e5f6''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'run 状态为成功'},
        {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '无 action 被篡改的异常日志'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-ACTION-PERM-02-001',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': '第三方 action 对 ATOMGIT_TOKEN / secret 的隐式获取受最小权限约束',
    'intent_ref': 'INTENT-SEC-022',
    'preconditions': ['仓库配置了 TEST_SECRET', '使用一个非官方第三方 action'],
    'steps': ['在 workflow 中调用第三方 action', '该 action 的代码尝试读取 secrets.TEST_SECRET 或 atomgit.token', '观察运行日志与权限行为'],
    'expected': ['第三方 action 不应默认获得仓库 secrets 访问权', '系统应通过 permissions 或 token 范围限制其权限'],
    'verification_points': ['[负向] 第三方 action 日志不含 TEST_SECRET 明文', '[正向] permissions 声明生效'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'with-secrets',
    'secrets': ['TEST_SECRET'],
    'workflow': '''  name: Third Party Action Permission
  on:
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
          input-param: test''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'TEST_SECRET'},
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '若权限不足则 action 失败或被限制'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-TOKEN-EXPIRE-02-001',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': 'ATOMGIT_TOKEN 运行后失效且不可通过缓存/残留复活',
    'intent_ref': 'INTENT-SEC-023',
    'preconditions': ['仓库配置了 TOKEN_TEST_SECRET', 'workflow 在运行中将 token 写入临时文件'],
    'steps': ['在 run step 中将 ${{ atomgit.token }} 写入 /tmp/token_dump.txt', '在后续 step 中尝试读取该文件并使用 token 调用 API', '在 run 结束后尝试从外部复用该 token'],
    'expected': ['运行期间临时文件中的 token 不应在运行结束后仍然有效', 'runner 工作区应在 job 结束后清理'],
    'verification_points': ['[负向] 运行结束后 token 调用 API 被拒绝', '[正向] 同一 runner 后续 job 读取不到旧 token 文件'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': ['TOKEN_TEST_SECRET'],
    'workflow': '''  name: Token Lifecycle
  on:
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
        run: cat /tmp/token_dump.txt''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '同 job 内可读取 token 文件'},
        {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'TOKEN_TEST_SECRET'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-ENV-POLLUTE-02-001',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': '工作流写协议（ATOMGIT_ENV/OUTPUT/PATH）不被不可信输入污染提权',
    'intent_ref': 'INTENT-SEC-024',
    'preconditions': ['workflow 接收来自 PR 标题/评论等不可信输入', '存在后续高权限 step'],
    'steps': ['在 PR 标题中注入恶意字符串（如包含换行符的伪造 workflow 命令）', '在 workflow 中将 PR 标题写入 $ATOMGIT_ENV', '观察后续 step 的环境变量与行为'],
    'expected': ['不可信输入写入 ATOMGIT_ENV 时不应解析执行注入命令', '后续 step 不应因写协议污染而获得提权'],
    'verification_points': ['[负向] 无注入命令被执行', '[负向] 环境变量不含恶意换行注入内容'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Env Pollute Test
  on:
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
        run: echo "$PR_TITLE"''',
    'trigger_event': 'pr',
    'trigger_as': 'untrusted_contributor',
    'trigger_params': {'pr_title_injection': 'true'},
    'assertions': [
        {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '无额外命令被执行'},
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'run 正常完成或按预期失败'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-RUNNER-LEAK-02-001',
    'dimensions': '[security, reliability]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P0',
    'title': 'Runner 跨 job/跨 run 无敏感残留（工作区/环境/凭据清理）',
    'intent_ref': 'INTENT-SEC-025',
    'preconditions': ['runner 支持多 job 复用', '前一个 job 写入了敏感文件与环境变量'],
    'steps': ['job-1 在 workspace 与 /tmp 写入标记文件与 secret', 'job-2 在相同 runner 上检查 workspace 与 /tmp 是否存在 job-1 残留', 'job-2 检查环境变量中是否残留 job-1 的 secrets'],
    'expected': ['job-2 不应发现 job-1 的文件残留', '环境变量不应包含 job-1 的 secret 值'],
    'verification_points': ['[负向] job-2 日志不含 job-1 的 secret 明文', '[负向] job-2 检查不到 job-1 的标记文件'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'with-secrets',
    'secrets': ['LEAK_TEST_SECRET'],
    'workflow': '''  name: Runner Leak Test
  on:
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
          fi''',
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

cases.append({
    'id': 'SEC-DISK-LEAK-02-001',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': '共享盘（/tmp、workspace）不跨 job 泄露敏感文件',
    'intent_ref': 'INTENT-SEC-026',
    'preconditions': ['job-A 在 /tmp 与 workspace 创建含敏感数据的文件'],
    'steps': ['job-A 写入 /tmp/secret.txt 与 $GITHUB_WORKSPACE/secret.txt', 'job-B 读取 /tmp/secret.txt 与 workspace/secret.txt'],
    'expected': ['job-B 应读取不到 job-A 的敏感文件', '共享盘在 job 切换时应被清理或隔离'],
    'verification_points': ['[负向] job-B 日志不含 job-A 的敏感数据', '[正向] job-B 报告文件不存在'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'with-secrets',
    'secrets': ['DISK_TEST_SECRET'],
    'workflow': '''  name: Disk Leak Test
  on:
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
          fi''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 DISK_NO_LEAK'},
        {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志不出现 DISK_LEAK_FOUND'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-RUNNER-SHARE-02-001',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P0',
    'title': '多项目共享 Runner 的 Secret 与资源隔离（项目 A secret 不达项目 B）',
    'intent_ref': 'INTENT-SEC-028',
    'preconditions': ['同一 runner 组被多个项目共享', '项目 A 配置了 SECRET_A，项目 B 未配置同名 secret'],
    'steps': ['在项目 A 的 workflow 中输出 secrets.SECRET_A', '在项目 B 的 workflow 中尝试读取 secrets.SECRET_A', '观察两项目的运行结果'],
    'expected': ['项目 B 的 workflow 不应读取到项目 A 的 SECRET_A', 'runner 上的 secret 注入应严格按项目隔离'],
    'verification_points': ['[负向] 项目 B 日志不含 SECRET_A 明文', '[正向] 项目 B 中 secrets.SECRET_A 为空或报错'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'with-secrets',
    'secrets': ['SECRET_A'],
    'workflow': '''  name: Cross Project Secret Isolation
  on:
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
          fi''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {'cross_project': 'true'},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 SECRET_EMPTY_AS_EXPECTED'},
        {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'SECRET_A'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-ENV-REVIEW-02-001',
    'dimensions': '[security, usability]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': '环境保护规则（reviewers/wait timer）未审批时环境 Secret 不可访问',
    'intent_ref': 'INTENT-SEC-030',
    'preconditions': ['仓库配置了 environment "production" 与对应 reviewers', '环境配置了环境级 secret ENV_SECRET'],
    'steps': ['触发一个指向 production 环境的 workflow', '在审批通过前观察 workflow 状态', '审批通过后再次观察'],
    'expected': ['未审批时 job 应处于等待状态，且不可访问 ENV_SECRET', '审批通过后 job 才能继续并读取到 ENV_SECRET'],
    'verification_points': ['[负向] 未审批时 job 不读取到 ENV_SECRET', '[正向] 审批后 job 成功执行'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'with-secrets',
    'secrets': ['ENV_SECRET'],
    'workflow': '''  name: Environment Review Gate
  on:
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
          fi''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '未审批时 run 状态为 waiting 或 paused'},
        {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'ENV_SECRET'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-TOCTOU-02-001',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': 'TOCTOU：审批后推送新 commit / 评论触发不绕过审批与代码固定',
    'intent_ref': 'INTENT-SEC-031',
    'preconditions': ['存在已审批的 PR workflow', '审批后 PR 又有新 commit 推送'],
    'steps': ['PR workflow 获得审批并开始运行', '在运行过程中向 PR 推送新 commit', '观察 workflow 是否重新触发并需要重新审批'],
    'expected': ['新 commit 推送后应触发新的 workflow run', '新 run 不应继承旧审批，应要求重新审批'],
    'verification_points': ['[负向] 新 commit 不导致旧 run 执行未审批代码', '[正向] 新 run 正确关联最新 commit SHA'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: TOCTOU Check
  on:
  - pull_request
  jobs:
    toctou-check:
      name: TOCTOU Check
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Log commit SHA
        run: echo "RUNNING_ON_SHA=${{ atomgit.sha }}"''',
    'trigger_event': 'pr',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志中的 SHA 与最新 commit 一致'},
        {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '旧 run 不会在新 commit 后重新执行'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-SIDECHAN-02-001',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': 'Secret 不经 output / artifact / step summary 侧信道绕过脱敏外泄',
    'intent_ref': 'INTENT-SEC-032',
    'preconditions': ['仓库配置了 SIDECHAN_SECRET', 'workflow 将 secret 写入 output、artifact 与 step summary'],
    'steps': ['在 step 中将 secret 写入 $ATOMGIT_OUTPUT', '在 step 中将 secret 写入 $ATOMGIT_STEP_SUMMARY', '上传包含 secret 的文件作为 artifact'],
    'expected': ['output 与 step summary 中的 secret 值应被脱敏为 ***', 'artifact 中的 secret 明文不应被保留（或被平台拒绝）'],
    'verification_points': ['[负向] output 中不含 secret 明文', '[负向] step summary 中不含 secret 明文', '[负向] artifact 下载内容不含 secret 明文'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'with-secrets',
    'secrets': ['SIDECHAN_SECRET'],
    'workflow': '''  name: Side Channel Leak Test
  on:
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
          path: secret_file.txt''',
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

cases.append({
    'id': 'SEC-JOB-ISOLATE-02-001',
    'dimensions': '[security, reliability]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': '同主机 Runner 并发 job 间的隔离（进程/文件/环境互不可见）',
    'intent_ref': 'INTENT-SEC-033',
    'preconditions': ['同一 runner 上并发执行两个 job', 'job-1 创建标记文件并写入进程信息'],
    'steps': ['job-1 与 job-2 同时运行', 'job-1 在 /tmp 与 workspace 创建隔离标记', 'job-2 检查 /tmp 与 workspace 是否存在 job-1 的标记'],
    'expected': ['并发 job 之间不应看到对方的进程、文件或环境变量'],
    'verification_points': ['[负向] job-2 检测不到 job-1 的进程', '[负向] job-2 读取不到 job-1 的文件'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Concurrent Job Isolation
  on:
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
          fi''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 ISOLATION_INTACT'},
        {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志不出现 ISOLATION_BROKEN'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-SECRET-MASK-02-002-V1',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P0',
    'title': 'Secret 字符串拼接/分片输出时仍应被脱敏',
    'intent_ref': 'INTENT-SEC-007',
    'mother': 'INTENT-SEC-006',
    'preconditions': ['仓库配置了 SPLIT_SECRET', 'workflow 将 secret 拆分为多段输出'],
    'steps': ['在 run step 中将 secret 的前半段与后半段分别 echo', '在 run step 中将 secret 与已知字符串拼接后 echo'],
    'expected': ['拼接后的完整 secret 仍应被脱敏', '分片输出的 secret 片段也应被脱敏'],
    'verification_points': ['[负向] 日志不含 SPLIT_SECRET 明文', '[负向] 日志不含拼接后的完整 secret'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'with-secrets',
    'secrets': ['SPLIT_SECRET'],
    'workflow': '''  name: Split Secret Masking
  on:
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
          echo "$PREFIX${{ secrets.SPLIT_SECRET }}$SUFFIX"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'SPLIT_SECRET'},
        {'type': 'nonfunctional', 'target': 'run_logs', 'eval': 'llm_assisted', 'rubric': '拼接输出中 secret 部分应被遮蔽'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-SECRET-MASK-02-002-V2',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': '多行 Secret 值的逐行脱敏覆盖',
    'intent_ref': 'INTENT-SEC-008',
    'mother': 'INTENT-SEC-006',
    'preconditions': ['仓库配置了 MULTILINE_SECRET（值含换行符）', 'workflow 将多行 secret 输出到日志'],
    'steps': ['在 run step 中 echo 多行 secret', '观察每一行的脱敏行为'],
    'expected': ['多行 secret 的每一行都应被脱敏为 ***', '换行不应导致脱敏中断'],
    'verification_points': ['[负向] 日志不含 MULTILINE_SECRET 的任意一行明文', '[正向] 日志中出现对应行数的 *** 遮蔽'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'with-secrets',
    'secrets': ['MULTILINE_SECRET'],
    'workflow': '''  name: Multiline Secret Masking
  on:
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
          echo "${{ secrets.MULTILINE_SECRET }}"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'MULTILINE_SECRET'},
        {'type': 'nonfunctional', 'target': 'run_logs', 'eval': 'llm_assisted', 'rubric': '多行输出中每一行敏感内容均被遮蔽'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'SEC-SECRET-MASK-02-002-V2',
    'dimensions': '[security]',
    'dimension': 'security',
    'dimension_label': '安全性',
    'priority': 'P1',
    'title': '多行 Secret 值的逐行脱敏覆盖',
    'intent_ref': 'INTENT-SEC-008',
    'mother': 'INTENT-SEC-006',
    'preconditions': ['仓库配置了 MULTILINE_SECRET（值含换行符）', 'workflow 将多行 secret 输出到日志'],
    'steps': ['在 run step 中 echo 多行 secret', '观察每一行的脱敏行为'],
    'expected': ['多行 secret 的每一行都应被脱敏为 ***', '换行不应导致脱敏中断'],
    'verification_points': ['[负向] 日志不含 MULTILINE_SECRET 的任意一行明文', '[正向] 日志中出现对应行数的 *** 遮蔽'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'with-secrets',
    'secrets': ['MULTILINE_SECRET'],
    'workflow': '''  name: Multiline Secret Masking
  on:
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
          echo "${{ secrets.MULTILINE_SECRET }}"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_logs', 'must_not_contain_secret': 'MULTILINE_SECRET'},
        {'type': 'nonfunctional', 'target': 'run_logs', 'eval': 'llm_assisted', 'rubric': '多行输出中每一行敏感内容均被遮蔽'}
    ],
    'teardown_reset': 'fixture'
})

# ===== REL batch (4 cases) =====

cases.append({
    'id': 'REL-PUSH-DEDUP-02-001',
    'dimensions': '[reliability]',
    'dimension': 'reliability',
    'dimension_label': '稳定性',
    'priority': 'P1',
    'title': '同一 push 连推的触发去重/幂等与并发触发排队公平性',
    'intent_ref': 'INTENT-REL-030',
    'preconditions': ['仓库已启用 push 触发', '支持快速连续推送'],
    'steps': ['在 10 秒内对同一分支连续推送 3 次 commit', '观察 workflow 触发次数与 run 状态'],
    'expected': ['同一 push 事件不应触发多个重复 run', '若去重失败，则多余 run 应被排队而非丢弃'],
    'verification_points': ['[正向] 3 次连推产生的 run 数 <= 3（期望去重为 1 或 3 个有序 run）', '[负向] 无 run 被静默丢弃', '[nonfunctional] run 排队公平'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Push Dedup Test
  on:
  - push
  jobs:
    dedup:
      name: Push Dedup
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Log run id
        run: echo "RUN_ID=${{ atomgit.run_id }}"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {'simultaneous_pushes': '3', 'window_seconds': '10'},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '所有触发均产生可追踪的 run'},
        {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '无 run 被静默丢弃'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'REL-MANY-STEPS-02-001',
    'dimensions': '[reliability]',
    'dimension': 'reliability',
    'dimension_label': '稳定性',
    'priority': 'P2',
    'title': '超多 step 的单 job 稳定性（接近 16 step 上限）',
    'intent_ref': 'INTENT-REL-031',
    'preconditions': ['runner 资源正常'],
    'steps': ['创建一个包含 15 个 step 的 job', '每个 step 执行简单命令', '观察运行是否成功完成'],
    'expected': ['15 个 step 应全部成功执行', '总耗时应在合理范围内'],
    'verification_points': ['[正向] 所有 15 个 step 状态为 success', '[nonfunctional] 总耗时 < 300 秒'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Many Steps Test
  on:
  - push
  jobs:
    many-steps:
      name: Many Steps
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Step 01
        run: echo "step01"
      - name: Step 02
        run: echo "step02"
      - name: Step 03
        run: echo "step03"
      - name: Step 04
        run: echo "step04"
      - name: Step 05
        run: echo "step05"
      - name: Step 06
        run: echo "step06"
      - name: Step 07
        run: echo "step07"
      - name: Step 08
        run: echo "step08"
      - name: Step 09
        run: echo "step09"
      - name: Step 10
        run: echo "step10"
      - name: Step 11
        run: echo "step11"
      - name: Step 12
        run: echo "step12"
      - name: Step 13
        run: echo "step13"
      - name: Step 14
        run: echo "step14"
      - name: Step 15
        run: echo "step15"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'run 状态为成功'},
        {'type': 'nonfunctional', 'target': 'run_duration', 'eval': 'deterministic', 'rubric': '总耗时 < 300 秒'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'REL-LARGE-REPO-02-001',
    'dimensions': '[reliability]',
    'dimension': 'reliability',
    'dimension_label': '稳定性',
    'priority': 'P2',
    'title': '超大仓库 checkout 的磁盘/时间边界',
    'intent_ref': 'INTENT-REL-032',
    'preconditions': ['存在一个大于 1GB 的测试仓库'],
    'steps': ['触发 workflow 对该大仓库执行 checkout', '观察 checkout 耗时与磁盘占用', '检查是否因超时或磁盘满而失败'],
    'expected': ['checkout 应在合理时间内完成', '磁盘占用不应超出 runner 配额'],
    'verification_points': ['[正向] checkout 成功', '[nonfunctional] 耗时 < 600 秒', '[负向] 无磁盘满报错'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'large-repo',
    'secrets': [],
    'workflow': '''  name: Large Repo Checkout
  on:
  - push
  jobs:
    large-checkout:
      name: Large Checkout
      runs-on: [ubuntu-latest, x64, large]
      steps:
      - name: (TC) checkout large repo
        uses: checkout
        with:
          fetch-depth: 0
      - name: Check disk usage
        run: du -sh .''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'checkout step 成功'},
        {'type': 'nonfunctional', 'target': 'run_duration', 'eval': 'deterministic', 'rubric': 'checkout 耗时 < 600 秒'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'REL-RUNNER-RESIDUE-02-001',
    'dimensions': '[reliability, security]',
    'dimension': 'reliability',
    'dimension_label': '稳定性',
    'priority': 'P1',
    'title': '托管 Runner 跨 job 复用的残留污染——去 flaky 隔离验证',
    'intent_ref': 'INTENT-REL-033',
    'preconditions': ['runner 支持跨 job 复用', 'job-1 在 /tmp 与 workspace 写入状态文件'],
    'steps': ['job-1 写入特定标记文件与进程环境', 'job-2 在相同 runner 上启动并检测残留', '重复多次以去 flaky'],
    'expected': ['job-2 不应检测到 job-1 的标记文件', '环境变量不应跨 job 残留'],
    'verification_points': ['[负向] job-2 检测不到 job-1 的标记', '[正向] 多次运行结果一致'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Runner Residue Check
  on:
  - push
  jobs:
    residue-a:
      name: Residue A
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Write marker
        run: |
          echo "RESIDUE_MARKER" > /tmp/residue_marker.txt
          echo "ENV_A=123" >> $ATOMGIT_ENV
    residue-b:
      name: Residue B
      needs: residue-a
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Check residue
        run: |
          if [ -f /tmp/residue_marker.txt ]; then
            echo "RESIDUE_FOUND"
          else
            echo "NO_RESIDUE"
          fi''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 NO_RESIDUE'},
        {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志不出现 RESIDUE_FOUND'}
    ],
    'teardown_reset': 'fixture'
})

# ===== USE batch (2 cases) =====

cases.append({
    'id': 'USE-PR-CHECKS-02-001',
    'dimensions': '[usability]',
    'dimension': 'usability',
    'dimension_label': '易用性',
    'priority': 'P2',
    'title': 'PR 场景状态回写（Checks/commit status）到 PR 页的可见性与可理解性',
    'intent_ref': 'INTENT-USE-024',
    'preconditions': ['存在打开的 PR', 'workflow 配置了 pull_request 触发'],
    'steps': ['在 PR 上触发 workflow', '观察 PR 页面是否显示 Checks 或 commit status', '检查状态信息的可理解性'],
    'expected': ['PR 页面应显示 workflow 的运行状态', '状态信息应包含 workflow 名称与结果'],
    'verification_points': ['[正向] PR 页面出现 Checks 或状态标签', '[nonfunctional] 状态文本可理解'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: PR Checks Visibility
  on:
  - pull_request
  jobs:
    pr-check:
      name: PR Check
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Run check
        run: echo "PR_CHECK_PASSED"''',
    'trigger_event': 'pr',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'pr_ui', 'eval': 'deterministic', 'rubric': 'PR 页面显示 workflow 运行状态'},
        {'type': 'nonfunctional', 'target': 'pr_ui', 'eval': 'llm_assisted', 'rubric': '状态文本包含 workflow 名称与结果，易于理解'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'USE-INPUTS-DEFAULT-02-001',
    'dimensions': '[usability, compatibility]',
    'dimension': 'usability',
    'dimension_label': '易用性',
    'priority': 'P2',
    'title': 'inputs 默认值在 shell 中以 ${var} 直接引用是否可用/失败可诊断',
    'intent_ref': 'INTENT-USE-025',
    'preconditions': ['workflow 定义了 workflow_dispatch inputs 并带有默认值'],
    'steps': ['通过手动触发 workflow 且不传参', '在 shell 中使用 ${var} 引用 inputs 默认值', '观察运行结果与报错信息'],
    'expected': ['若 GitCode 支持 ${var} 语法，则默认值应正确注入', '若不支持，报错应指明正确引用方式'],
    'verification_points': ['[正向] 默认值正确注入 shell', '[nonfunctional] 错误信息可诊断'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Inputs Default Test
  on:
  - workflow_dispatch
  jobs:
    inputs-test:
      name: Inputs Default
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Use input default
        run: |
          echo "INPUT_VAL=${{ inputs.test_input }}"
          echo "SHELL_VAL=${test_input}"''',
    'trigger_event': 'manual',
    'trigger_as': 'maintainer',
    'trigger_params': {'skip_inputs': 'true'},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 INPUT_VAL 与默认值'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': '若失败，错误信息应指明正确引用方式'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'USE-INPUTS-DEFAULT-02-001',
    'dimensions': '[usability, compatibility]',
    'dimension': 'usability',
    'dimension_label': '易用性',
    'priority': 'P2',
    'title': 'inputs 默认值在 shell 中以 ${var} 直接引用是否可用/失败可诊断',
    'intent_ref': 'INTENT-USE-025',
    'preconditions': ['workflow 定义了 workflow_dispatch inputs 并带有默认值'],
    'steps': ['通过手动触发 workflow 且不传参', '在 shell 中使用 ${var} 引用 inputs 默认值', '观察运行结果与报错信息'],
    'expected': ['若 GitCode 支持 ${var} 语法，则默认值应正确注入', '若不支持，报错应指明正确引用方式'],
    'verification_points': ['[正向] 默认值正确注入 shell', '[nonfunctional] 错误信息可诊断'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Inputs Default Test
  on:
  - workflow_dispatch
  jobs:
    inputs-test:
      name: Inputs Default
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Use input default
        run: |
          echo "INPUT_VAL=${{ inputs.test_input }}"
          echo "SHELL_VAL=${test_input}"''',
    'trigger_event': 'manual',
    'trigger_as': 'maintainer',
    'trigger_params': {'skip_inputs': 'true'},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '日志出现 INPUT_VAL 与默认值'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': '若失败，错误信息应指明正确引用方式'}
    ],
    'teardown_reset': 'fixture'
})

# ===== COMPAT batch (26 cases) =====

cases.append({
    'id': 'COMPAT-SYSENV-MAP-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': '系统环境变量映射差异——GITHUB_* 全集 → ATOMGIT_* 及缺失变量',
    'intent_ref': 'INTENT-COMPAT-032',
    'preconditions': ['workflow 引用 GITHUB_ENV/GITHUB_OUTPUT 等 GitHub 式变量名'],
    'steps': ['在 workflow 中同时输出 GITHUB_ENV 与 ATOMGIT_ENV 的值', '比较两者是否存在及内容一致性'],
    'expected': ['ATOMGIT_* 变量应存在且内容正确', 'GITHUB_* 变量名应被映射或给出迁移提示'],
    'verification_points': ['[正向] ATOMGIT_ENV 非空', '[负向] 无静默空值陷阱', '[nonfunctional] 若 GITHUB_ENV 不被支持，报错应可理解'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Sysenv Map Test
  on:
  - push
  jobs:
    sysenv:
      name: Sysenv Map
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Check ATOMGIT_ENV
        run: echo "ATOMGIT_ENV=$ATOMGIT_ENV"
      - name: Check GITHUB_ENV fallback
        run: echo "GITHUB_ENV=$GITHUB_ENV"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'ATOMGIT_ENV 有值'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': 'GITHUB_ENV 若不可用，报错应指明改用 ATOMGIT_ENV'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-RUNNER-NAME-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': 'RUNNER_OS/ARCH 双命名混乱——RUNNER_* vs ATOMGIT_RUNNER_* 及 GitHub 对齐',
    'intent_ref': 'INTENT-COMPAT-033',
    'preconditions': ['runner 正常可用'],
    'steps': ['在 shell 中输出 RUNNER_OS、ATOMGIT_RUNNER_OS、RUNNER_ARCH、ATOMGIT_RUNNER_ARCH', '比较四者的值与存在性'],
    'expected': ['至少一套命名应返回正确的 os/arch 值', '两套命名若并存，其值应一致'],
    'verification_points': ['[正向] 至少一个 OS 变量返回非空值', '[正向] 至少一个 ARCH 变量返回非空值', '[负向] 无同时为空'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Runner Name Confusion
  on:
  - push
  jobs:
    runner-name:
      name: Runner Name
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Check runner OS names
        run: |
          echo "RUNNER_OS=$RUNNER_OS"
          echo "ATOMGIT_RUNNER_OS=$ATOMGIT_RUNNER_OS"
      - name: Check runner ARCH names
        run: |
          echo "RUNNER_ARCH=$RUNNER_ARCH"
          echo "ATOMGIT_RUNNER_ARCH=$ATOMGIT_RUNNER_ARCH"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '至少一个 OS 变量非空'},
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '至少一个 ARCH 变量非空'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-WF-CMD-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': '工作流日志命令差异——::group::/::error::/::warning::/::notice::/::add-mask:: 支持度',
    'intent_ref': 'INTENT-COMPAT-034',
    'preconditions': ['workflow 使用 GitHub 式日志命令'],
    'steps': ['在 run step 中输出 ::error::、::warning::、::group::、::notice::、::add-mask:: 命令', '观察运行详情页是否识别并渲染这些命令'],
    'expected': ['GitCode 应支持主流的日志命令', '不支持的命令应静默忽略而非报错'],
    'verification_points': ['[正向] 支持的命令在 UI 中可见', '[负向] 不支持的命令不导致 step 失败'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Workflow Commands Support
  on:
  - push
  jobs:
    wf-cmd:
      name: Workflow Commands
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Test error command
        run: echo "::error::This is an error annotation"
      - name: Test warning command
        run: echo "::warning::This is a warning annotation"
      - name: Test group command
        run: |
          echo "::group::My Group"
          echo "inside group"
          echo "::endgroup::"
      - name: Test notice command
        run: echo "::notice::This is a notice"
      - name: Test add-mask command
        run: echo "::add-mask::SECRET_VALUE"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'run 状态为成功'},
        {'type': 'nonfunctional', 'target': 'run_ui', 'eval': 'llm_assisted', 'rubric': '支持的命令在运行详情中可见并正确渲染'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-MULTILINE-DELIM-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': '多行值 delimiter 协议与「不可覆盖默认变量」约束一致性',
    'intent_ref': 'INTENT-COMPAT-035',
    'preconditions': ['workflow 向 ATOMGIT_ENV 写入多行值'],
    'steps': ['使用 delimiter 语法向 ATOMGIT_ENV 写入多行值', '在后续 step 中读取该变量', '测试默认变量是否可被覆盖'],
    'expected': ['多行值应正确传递', '默认变量（如 PATH）不应被 workflow 意外覆盖'],
    'verification_points': ['[正向] 多行值在后续 step 中完整可读', '[负向] 默认变量未被静默覆盖'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Multiline Delimiter Test
  on:
  - push
  jobs:
    multiline:
      name: Multiline Delimiter
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Write multiline value
        run: |
          echo "MY_VAR << EOF" >> $ATOMGIT_ENV
          echo "line1" >> $ATOMGIT_ENV
          echo "line2" >> $ATOMGIT_ENV
          echo "EOF" >> $ATOMGIT_ENV
      - name: Read multiline value
        run: |
          echo "MY_VAR=$MY_VAR"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'MY_VAR 包含 line1 与 line2'},
        {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'PATH 等默认变量未被清空'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-RUNSON-EQUIV-02-001',
    'dimensions': '[compatibility, usability]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': 'runs-on 多种写法等价性——数组 [..] vs 花括号 {..} vs default vs 键值 arch=arm',
    'intent_ref': 'INTENT-COMPAT-037',
    'preconditions': ['runner 池包含对应标签'],
    'steps': ['分别使用数组、花括号、default、键值四种写法定义 runs-on', '触发 workflow 并观察调度结果'],
    'expected': ['等价写法应调度到同一 runner 或同规格 runner', '不支持的写法应给出明确报错'],
    'verification_points': ['[正向] 等价写法运行成功', '[nonfunctional] 报错信息可理解'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Runs On Equivalence
  on:
  - push
  jobs:
    array-form:
      name: Array Form
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Echo
        run: echo "ARRAY_FORM_OK"
    default-form:
      name: Default Form
      runs-on: [default]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Echo
        run: echo "DEFAULT_FORM_OK"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'ARRAY_FORM_OK 出现'},
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'DEFAULT_FORM_OK 出现'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-TOOLCHAIN-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': '预装工具链版本差异——GitHub runner image 与 GitCode ubuntu-latest 预装软件差集',
    'intent_ref': 'INTENT-COMPAT-038',
    'preconditions': ['runner 标签为 ubuntu-latest'],
    'steps': ['在 workflow 中检查常见预装工具（git、node、python、docker、jq）的版本', '与 GitHub ubuntu-latest 的标准列表对比'],
    'expected': ['核心工具（git、bash、curl）应存在', '版本差异应被文档化'],
    'verification_points': ['[正向] git、bash、curl 可用', '[nonfunctional] 缺失工具的报错可理解'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Toolchain Diff
  on:
  - push
  jobs:
    toolchain:
      name: Toolchain Check
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Check git
        run: git --version || echo "GIT_MISSING"
      - name: Check node
        run: node --version || echo "NODE_MISSING"
      - name: Check python
        run: python3 --version || echo "PYTHON_MISSING"
      - name: Check docker
        run: docker --version || echo "DOCKER_MISSING"
      - name: Check jq
        run: jq --version || echo "JQ_MISSING"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'git 版本输出非空'},
        {'type': 'nonfunctional', 'target': 'run_logs', 'eval': 'llm_assisted', 'rubric': '缺失工具的提示清晰可理解'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-NO-WIN-MAC-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': '无 Windows/macOS runner——GitHub 三平台 vs GitCode 仅 Linux 的迁移降级',
    'intent_ref': 'INTENT-COMPAT-039',
    'preconditions': ['workflow 声明了 windows-latest 或 macos-latest'],
    'steps': ['提交包含 windows-latest 或 macos-latest 的 workflow', '观察平台调度行为'],
    'expected': ['不应静默挂起或无提示失败', '应给出明确的「不支持该平台」报错'],
    'verification_points': ['[负向] 不静默挂起超过 300 秒', '[nonfunctional] 报错信息包含平台不支持提示'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: No Win Mac Test
  on:
  - push
  jobs:
    windows-job:
      name: Windows Job
      runs-on: [windows-latest]
      steps:
      - name: Echo
        run: echo "windows"
    macos-job:
      name: macOS Job
      runs-on: [macos-latest]
      steps:
      - name: Echo
        run: echo "macos"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '不静默挂起超过 300 秒'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': '报错信息包含平台不支持提示'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-FLAVOR-LABEL-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': '资源规格标签差异——GitCode flavor（slim~2xlarge）与「large+ 需申请」vs GitHub 标准/大型 runner',
    'intent_ref': 'INTENT-COMPAT-040',
    'preconditions': ['runner 池包含 small/large 标签'],
    'steps': ['使用不同 flavor 标签触发 workflow', '比较各 flavor 的 CPU/内存规格'],
    'expected': ['small/large 等标签应能正确调度', '规格应与文档声明一致'],
    'verification_points': ['[正向] 各 flavor 成功调度', '[nonfunctional] 规格与文档一致'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Flavor Label Test
  on:
  - push
  jobs:
    small-job:
      name: Small Job
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Show CPU count
        run: nproc
    large-job:
      name: Large Job
      runs-on: [ubuntu-latest, x64, large]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Show CPU count
        run: nproc''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'small 与 large job 均成功'},
        {'type': 'nonfunctional', 'target': 'run_logs', 'eval': 'llm_assisted', 'rubric': 'CPU 数与 flavor 规格描述一致'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-UNKNOWN-TOP-02-001',
    'dimensions': '[compatibility, usability]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': '未知/不支持顶层字段的处理——报错 vs 静默忽略（GitHub 有 run-name 等 GitCode 无）',
    'intent_ref': 'INTENT-COMPAT-041',
    'preconditions': ['workflow 包含 GitCode 未声明的顶层字段'],
    'steps': ['在 workflow 中添加 run-name、concurrency.cancel-in-progress 等 GitHub 专有字段', '提交并观察解析行为'],
    'expected': ['不应静默忽略导致用户误以为功能可用', '应给出明确的「不支持字段」报错或警告'],
    'verification_points': ['[负向] 不静默成功运行', '[nonfunctional] 报错精确到字段名与行号'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Unknown Top Field
  run-name: Test Run by ${{ atomgit.actor }}
  on:
  - push
  concurrency:
    group: ${{ atomgit.workflow }}-${{ atomgit.ref }}
    cancel-in-progress: true
  jobs:
    unknown:
      name: Unknown Field
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Echo
        run: echo "unknown_field_test"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '不静默成功运行而忽略不支持的字段'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': '报错或警告精确到不支持的字段名'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-CONCUR-MODEL-02-001',
    'dimensions': '[compatibility, reliability]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': 'concurrency 模型差异——GitHub group+cancel-in-progress vs GitCode enable+max+exceed-action+preemption',
    'intent_ref': 'INTENT-COMPAT-042',
    'preconditions': ['runner 资源正常'],
    'steps': ['使用 GitHub 式 concurrency 语法（group+cancel-in-progress）定义 workflow', '观察平台是否兼容或给出迁移提示'],
    'expected': ['GitHub 式语法不应被静默忽略', '若不兼容，报错应指向 GitCode 的正确语法'],
    'verification_points': ['[负向] 不静默忽略并发控制', '[nonfunctional] 报错包含可操作的迁移建议'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Concurrency Model Diff
  on:
  - push
  concurrency:
    group: ${{ atomgit.workflow }}-${{ atomgit.ref }}
    cancel-in-progress: true
  jobs:
    model-test:
      name: Model Test
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Echo
        run: echo "concurrency_model_test"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '不静默成功而忽略并发配置'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': '报错包含 GitCode 并发语法示例'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-USING-RUNTIME-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': 'action runs.using 运行时差异——GitHub node20/docker/composite vs GitCode 仅 node16',
    'intent_ref': 'INTENT-COMPAT-043',
    'preconditions': ['存在 using: node20 或 docker 的 action 定义'],
    'steps': ['在 workflow 中引用 using: node20 的 action', '观察运行是否成功或给出降级提示'],
    'expected': ['不支持的 using 类型不应静默失败', '应给出明确的运行时不支持报错'],
    'verification_points': ['[负向] 不静默挂起', '[nonfunctional] 报错指明支持的 using 类型'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Using Runtime Diff
  on:
  - push
  jobs:
    using-test:
      name: Using Runtime
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Use action with node20
        uses: node20-action-test
      - name: Use action with docker
        uses: docker-action-test''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '不静默挂起超过 300 秒'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': '报错指明 node16 为支持的运行时'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-USING-RUNTIME-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': 'action runs.using 运行时差异——GitHub node20/docker/composite vs GitCode 仅 node16',
    'intent_ref': 'INTENT-COMPAT-043',
    'preconditions': ['存在 using: node20 或 docker 的 action 定义'],
    'steps': ['在 workflow 中引用 using: node20 的 action', '观察运行是否成功或给出降级提示'],
    'expected': ['不支持的 using 类型不应静默失败', '应给出明确的运行时不支持报错'],
    'verification_points': ['[负向] 不静默挂起', '[nonfunctional] 报错指明支持的 using 类型'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Using Runtime Diff
  on:
  - push
  jobs:
    using-test:
      name: Using Runtime
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Use action with node20
        uses: node20-action-test
      - name: Use action with docker
        uses: docker-action-test''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '不静默挂起超过 300 秒'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': '报错指明 node16 为支持的运行时'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-USES-REF-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': 'uses action 引用方式差异——GitHub owner/repo@ref marketplace vs GitCode 官方短名 + 本地',
    'intent_ref': 'INTENT-COMPAT-044',
    'preconditions': ['workflow 使用 GitHub 式 uses: owner/repo@v1 引用'],
    'steps': ['在 workflow 中使用 GitHub 式 owner/repo@ref 引用 action', '再使用 GitCode 官方短名引用同一 action', '比较两者的行为'],
    'expected': ['GitCode 短名应成功解析', 'GitHub 式引用应给出明确的格式错误或迁移提示'],
    'verification_points': ['[正向] 官方短名运行成功', '[nonfunctional] GitHub 式引用报错可理解'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Uses Ref Diff
  on:
  - push
  jobs:
    ref-test:
      name: Uses Ref Test
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: GitCode short name
        uses: checkout
      - name: GitHub style name
        uses: actions/checkout@v4''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '官方短名 step 成功'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': 'GitHub 式引用报错指明应使用短名'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-DEPRECATED-CMD-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': '废弃命令处理差异——::set-output/::set-env/::add-path 在 GitCode 的降级',
    'intent_ref': 'INTENT-COMPAT-045',
    'preconditions': ['workflow 使用废弃的 ::set-output、::set-env、::add-path 命令'],
    'steps': ['在 run step 中使用废弃命令', '观察平台处理行为与日志输出'],
    'expected': ['废弃命令不应导致 step 失败', '应给出废弃警告或自动映射到新命令'],
    'verification_points': ['[正向] run 状态仍为成功', '[nonfunctional] 出现废弃警告或自动映射提示'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Deprecated Commands
  on:
  - push
  jobs:
    deprecated:
      name: Deprecated Commands
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Old set-output
        run: echo "::set-output name=result::hello"
      - name: Old set-env
        run: echo "::set-env name=MY_VAR::world"
      - name: Old add-path
        run: echo "::add-path::/some/path"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'run 状态为成功'},
        {'type': 'nonfunctional', 'target': 'run_logs', 'eval': 'llm_assisted', 'rubric': '日志出现废弃命令警告或自动映射提示'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-OUTPUT-LIMIT-02-001',
    'dimensions': '[compatibility, reliability]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': 'step 输出/artifact 超限行为差异——1MB output、artifact 上限的降级方式',
    'intent_ref': 'INTENT-COMPAT-046',
    'preconditions': ['workflow 产生超过 1MB 的 step 输出与 artifact'],
    'steps': ['在 step 中输出超过 1MB 的文本', '上传超过上限的 artifact', '观察截断/报错行为'],
    'expected': ['超限输出应被截断或报错', 'artifact 超限应给出明确的降级提示'],
    'verification_points': ['[正向] 超限后 workflow 不崩溃', '[nonfunctional] 降级方式与文档一致'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Output Limit Test
  on:
  - push
  jobs:
    limit-test:
      name: Output Limit
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Generate large output
        run: python3 -c "print('A'*1024*1024)"
      - name: Generate large artifact
        run: dd if=/dev/zero of=bigfile.bin bs=1M count=10
      - name: Upload large artifact
        uses: upload-artifact
        with:
          name: large-artifact
          path: bigfile.bin''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'run 不崩溃'},
        {'type': 'nonfunctional', 'target': 'run_logs', 'eval': 'llm_assisted', 'rubric': '超限后出现截断或报错提示'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-CHECKOUT-EQUIV-02-001',
    'dimensions': '[compatibility, usability]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': 'checkout action 差异——GitCode uses: checkout 参数集与 GitHub actions/checkout@v4 等价性',
    'intent_ref': 'INTENT-COMPAT-047',
    'preconditions': ['仓库存在分支与 PR'],
    'steps': ['使用 GitCode checkout action 并传入 fetch-depth、ref 等参数', '比较检出结果与 GitHub 行为的等价性'],
    'expected': ['常用参数（fetch-depth、ref）应生效', '检出结果应与 GitHub 行为一致'],
    'verification_points': ['[正向] fetch-depth=0 成功获取完整历史', '[正向] ref 参数正确检出指定分支'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Checkout Equivalence
  on:
  - push
  jobs:
    checkout-test:
      name: Checkout Equivalence
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout with fetch-depth
        uses: checkout
        with:
          fetch-depth: 0
      - name: Verify full history
        run: git log --oneline | head -n 5
      - name: (TC) checkout with ref
        uses: checkout
        with:
          ref: main''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'git log 输出非空'},
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'checkout step 成功'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-CACHE-EQUIV-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': 'cache action 差异——key/restore-keys 语义、fork 隔离、跨 run 命中与 GitHub 等价性',
    'intent_ref': 'INTENT-COMPAT-048',
    'preconditions': ['runner 支持 cache'],
    'steps': ['使用 cache action 保存与恢复缓存', '测试 restore-keys 的前缀匹配语义', '验证 fork 隔离'],
    'expected': ['key 精确匹配与 restore-keys 前缀匹配应生效', 'fork PR 不应污染主分支缓存'],
    'verification_points': ['[正向] cache 保存与恢复成功', '[负向] fork PR 不命中主分支缓存'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Cache Equivalence
  on:
  - push
  jobs:
    cache-test:
      name: Cache Equivalence
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Restore cache
        uses: cache
        with:
          key: cache-equiv-exact
          restore-keys: cache-equiv-
          path: ./cache-dir
      - name: Use or create cache
        run: |
          if [ -f cache-dir/data.txt ]; then
            echo "CACHE_HIT"
          else
            echo "CACHE_MISS"
            mkdir -p cache-dir
            echo "data" > cache-dir/data.txt
          fi
      - name: Save cache
        uses: cache
        with:
          key: cache-equiv-exact
          path: ./cache-dir''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'CACHE_HIT 或 CACHE_MISS 出现'},
        {'type': 'negative', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'fork PR 不出现主分支的 CACHE_HIT'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-ARTIFACT-EQUIV-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': 'upload/download-artifact 差异——name 唯一性、path 默认、多 artifact 行为与 GitHub 等价性',
    'intent_ref': 'INTENT-COMPAT-049',
    'preconditions': ['runner 支持 artifact'],
    'steps': ['上传多个同名 artifact', '下载 artifact 并验证 path 默认行为', '测试多 artifact 下载'],
    'expected': ['同名 artifact 应按文档规则处理（覆盖或报错）', 'path 默认行为应与 GitHub 一致'],
    'verification_points': ['[正向] artifact 上传与下载成功', '[nonfunctional] 同名冲突处理与文档一致'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Artifact Equivalence
  on:
  - push
  jobs:
    artifact-test:
      name: Artifact Equivalence
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Create files
        run: |
          echo "file1" > dist/a.txt
          echo "file2" > dist/b.txt
      - name: Upload artifact
        uses: upload-artifact
        with:
          name: build-artifact
          path: dist/
      - name: Download artifact
        uses: download-artifact
        with:
          name: build-artifact
      - name: Verify files
        run: ls -la build-artifact/''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'a.txt 与 b.txt 存在'},
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '上传与下载 step 成功'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-SETUP-STAR-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': 'setup-* action 差异——setup-node/python/java/go 的 version/cache 参数与版本解析',
    'intent_ref': 'INTENT-COMPAT-050',
    'preconditions': ['runner 预装对应 setup action'],
    'steps': ['使用 setup-node 与 setup-python 安装指定版本', '测试 cache 参数是否生效'],
    'expected': ['指定版本应正确安装', 'cache 参数应加速后续运行'],
    'verification_points': ['[正向] node/python 版本与声明一致', '[nonfunctional] cache 参数生效'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Setup Star Test
  on:
  - push
  jobs:
    setup-test:
      name: Setup Star
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Setup Node
        uses: setup-node
        with:
          node-version: '20'
          cache: 'npm'
      - name: Verify Node
        run: node --version
      - name: Setup Python
        uses: setup-python
        with:
          python-version: '3.11'
      - name: Verify Python
        run: python3 --version''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'node --version 包含 v20'},
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'python3 --version 包含 3.11'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-ACTION-INPUTS-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': 'action inputs 环境变量注入差异——INPUT_<NAME> 命名转换与 required 校验',
    'intent_ref': 'INTENT-COMPAT-051',
    'preconditions': ['存在一个带 inputs 定义的自定义 action'],
    'steps': ['在 workflow 中调用该 action 并传入参数', '在 action 的 run 脚本中读取 INPUT_* 环境变量'],
    'expected': ['inputs 应正确映射为 INPUT_* 环境变量', 'required 缺失时应报错'],
    'verification_points': ['[正向] INPUT_TEST_PARAM 值为传入值', '[nonfunctional] required 缺失报错可理解'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Action Inputs Env
  on:
  - push
  jobs:
    inputs-env:
      name: Action Inputs Env
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Call custom action
        uses: custom-action-test
        with:
          test-param: hello''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'INPUT_TEST_PARAM 值为 hello'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': 'required 缺失时报错可理解'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-RECURSIVE-02-001',
    'dimensions': '[compatibility, security]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': 'recursive run 防护一致性——GitCode token 触发的运行是否防递归',
    'intent_ref': 'INTENT-COMPAT-056',
    'preconditions': ['workflow 使用 API token 触发另一个 workflow'],
    'steps': ['在 workflow 中使用 curl + token 触发同一仓库的另一个 workflow', '观察是否产生无限递归'],
    'expected': ['平台应检测到递归并阻止', '不应消耗无限配额'],
    'verification_points': ['[负向] 不产生无限递归 run', '[正向] 首次触发后递归被拦截'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': ['TRIGGER_TOKEN'],
    'workflow': '''  name: Recursive Run Guard
  on:
  - push
  jobs:
    recursive:
      name: Recursive Guard
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Attempt recursive trigger
        run: |
          curl -X POST "${{ atomgit.api_url }}/repos/${{ atomgit.repository }}/actions/workflows/recursive.yml/dispatches" \
            -H "Authorization: token ${{ secrets.TRIGGER_TOKEN }}" \
            -d '{"ref":"main"}' || echo "TRIGGER_BLOCKED"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '不产生无限递归 run'},
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': '出现 TRIGGER_BLOCKED 或等效拦截日志'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-STAGES-ORCH-02-001',
    'dimensions': '[compatibility, usability]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': 'stages 编排层——GitHub 扁平 jobs 迁移到 GitCode 是否需引入 stages 及默认行为',
    'intent_ref': 'INTENT-COMPAT-057',
    'preconditions': ['workflow 使用 stages 结构'],
    'steps': ['定义包含多个 stage 的 workflow', '观察 stage 间串行执行与默认行为'],
    'expected': ['stage 应按顺序串行执行', '默认行为应与文档一致'],
    'verification_points': ['[正向] stage 按顺序执行', '[nonfunctional] 默认行为可预测'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Stages Orchestration
  on:
  - push
  stages:
    - name: build
      jobs:
        - build-job
    - name: test
      jobs:
        - test-job
  jobs:
    build-job:
      name: Build Job
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Build
        run: echo "BUILD_DONE"
    test-job:
      name: Test Job
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Test
        run: echo "TEST_DONE"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'BUILD_DONE 先于 TEST_DONE 出现'},
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '两 job 均成功'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-STAGES-SYNTAX-02-001',
    'dimensions': '[compatibility, usability]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P2',
    'title': 'stages 两种写法 + 缩进瑕疵——列表 - name: vs 映射 stage1: 的解析容错',
    'intent_ref': 'INTENT-COMPAT-058',
    'preconditions': ['workflow 使用 stages 的两种 YAML 写法'],
    'steps': ['使用列表写法（- name:）定义 stages', '使用映射写法（stage1:）定义 stages', '提交并观察解析结果'],
    'expected': ['两种写法应被等价解析', '缩进瑕疵应给出明确报错而非静默失败'],
    'verification_points': ['[正向] 两种写法均成功解析', '[nonfunctional] 缩进错误报错精确到行'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Stages Syntax Test
  on:
  - push
  stages:
    build:
      jobs:
        - build-job
    test:
      jobs:
        - test-job
  jobs:
    build-job:
      name: Build Job
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Build
        run: echo "BUILD_DONE"
    test-job:
      name: Test Job
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Test
        run: echo "TEST_DONE"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'workflow 解析成功且运行'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': '若解析失败，报错精确到行号'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-STAGE-FIELDS-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': 'GitCode 特有 stage 字段——select/pre/fail-fast 无 GitHub 对应的语义确认',
    'intent_ref': 'INTENT-COMPAT-059',
    'preconditions': ['workflow 使用 stage 的 select、pre、fail-fast 字段'],
    'steps': ['定义包含 select、pre、fail-fast 的 stage', '触发并观察各字段的行为'],
    'expected': ['select 应按条件选择执行 job', 'pre 应在 stage 前执行', 'fail-fast 应控制失败传播'],
    'verification_points': ['[正向] select 条件生效', '[正向] pre step 在 stage job 前执行', '[正向] fail-fast 控制失败传播'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: Stage Fields Test
  on:
  - push
  stages:
    - name: build
      pre:
        - name: Pre Build
          runs-on: [ubuntu-latest, x64, small]
          steps:
          - name: Pre step
            run: echo "PRE_BUILD"
      jobs:
        - build-job
      fail-fast: true
  jobs:
    build-job:
      name: Build Job
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Build
        run: echo "BUILD_DONE"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'PRE_BUILD 先于 BUILD_DONE 出现'},
        {'type': 'positive', 'target': 'run_status', 'eval': 'deterministic', 'rubric': 'stage 成功执行'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-YAML-ERROR-02-001',
    'dimensions': '[compatibility, usability]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': '非法 YAML / schema 校验报错质量——错在第几行、可操作提示与 GitHub 对齐',
    'intent_ref': 'INTENT-COMPAT-060',
    'preconditions': ['workflow 包含故意的 YAML 语法错误'],
    'steps': ['提交包含缩进错误、缺少必填字段的 workflow', '观察平台报错信息'],
    'expected': ['报错应指出具体行号', '提示应包含可操作的修改建议'],
    'verification_points': ['[nonfunctional] 报错精确到行号', '[nonfunctional] 提示包含修复建议'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': [],
    'workflow': '''  name: YAML Error Quality
  on:
  - push
  jobs:
    bad-yaml:
      name: Bad YAML
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Missing indent
        run: echo "test"''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': 'YAML 错误报错精确到行号'},
        {'type': 'nonfunctional', 'target': 'error_message', 'eval': 'llm_assisted', 'rubric': '提示包含可操作的修改建议'}
    ],
    'teardown_reset': 'fixture'
})

cases.append({
    'id': 'COMPAT-WF-CALL-02-001',
    'dimensions': '[compatibility]',
    'dimension': 'compatibility',
    'dimension_label': '兼容性',
    'priority': 'P1',
    'title': 'workflow_call 复用差异——嵌套层数、secrets 传递、inputs 类型与 GitHub 对齐',
    'intent_ref': 'INTENT-COMPAT-061',
    'preconditions': ['存在可复用的 callee workflow'],
    'steps': ['定义 workflow_call 的 callee workflow', '在 caller workflow 中调用并传递 secrets 与 inputs', '观察运行结果'],
    'expected': ['workflow_call 应正确传递 inputs 与 secrets', '嵌套层数应受文档限制'],
    'verification_points': ['[正向] inputs 与 secrets 正确传递到 callee', '[负向] 超过 2 层嵌套应被拒绝'],
    'cleanup': '重置 fixture 仓库',
    'repo_fixture': 'basic-ci',
    'secrets': ['CALLEE_SECRET'],
    'workflow': '''  name: Workflow Call Reuse
  on:
  - push
  jobs:
    caller:
      name: Caller Job
      runs-on: [ubuntu-latest, x64, small]
      steps:
      - name: (TC) checkout
        uses: checkout
      - name: Call reusable workflow
        uses: ./.gitcode/workflows/callee.yml
        with:
          input-val: hello
        secrets:
          callee-secret: ${{ secrets.CALLEE_SECRET }}''',
    'trigger_event': 'push',
    'trigger_as': 'maintainer',
    'trigger_params': {},
    'assertions': [
        {'type': 'positive', 'target': 'run_logs', 'eval': 'deterministic', 'rubric': 'callee 正确接收 input-val'},
        {'type': 'negative', 'target': 'run_status', 'eval': 'deterministic', 'rubric': '超过 2 层嵌套被拒绝'}
    ],
    'teardown_reset': 'fixture'
})

for c in cases:
    write_text_case(c)
    write_yaml_case(c)

print(f"Done. Generated {len(cases)} cases.")
