#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

TEXT_DIR = "D:/业务/action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases/text"
YAML_DIR = "D:/业务/action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases/yaml"
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(YAML_DIR, exist_ok=True)

CASES = []

def add(id, intent_ref, title, priority, preconditions, steps, expected, verification, teardown_desc, teardown, workflow, assertions, fault_injection=None, dimensions="[reliability]", trigger_event="workflow_dispatch", trigger_as="maintainer", repo_fixture="default", secrets=None):
    CASES.append({
        "id": id, "intent_ref": intent_ref, "title": title, "priority": priority,
        "preconditions": preconditions, "steps": steps, "expected": expected,
        "verification": verification, "teardown_desc": teardown_desc, "teardown": teardown,
        "workflow": workflow, "assertions": assertions, "fault_injection": fault_injection,
        "dimensions": dimensions, "trigger_event": trigger_event, "trigger_as": trigger_as,
        "repo_fixture": repo_fixture, "secrets": secrets or []
    })

# workflow templates
def wfs(sleep=10):
    return f"on:\n  workflow_dispatch:\njobs:\n  test:\n    name: reliability test job\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: sleep step\n        run: |\n          sleep {sleep}"

def wft(timeout, sleep):
    return f"on:\n  workflow_dispatch:\njobs:\n  test:\n    name: timeout test job\n    runs-on: [dedicate-hosted, x64, large]\n    timeout-minutes: {timeout}\n    steps:\n      - name: long sleep step\n        run: |\n          sleep {sleep}"

def wfc(max_val, action, sleep=10):
    return f"on:\n  workflow_dispatch:\nconcurrency:\n  max: {max_val}\n  exceed-action: {action}\njobs:\n  test:\n    name: concurrency test job\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: sleep step\n        run: |\n          sleep {sleep}"

def wfpush(path="src/**"):
    return f"on:\n  push:\n    paths:\n      - '{path}'\njobs:\n  test:\n    name: paths trigger test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: echo triggered\n        run: |\n          echo triggered by paths"

def wfmatrix(versions, fail_fast=None, max_parallel=None):
    strat = "    strategy:\n      matrix:\n        version: " + str(versions).replace("'", "") + "\n"
    if fail_fast is not None:
        strat += f"      fail-fast: {str(fail_fast).lower()}\n"
    if max_parallel is not None:
        strat += f"      max-parallel: {max_parallel}\n"
    return f"on:\n  workflow_dispatch:\njobs:\n  test:\n    name: matrix test job\n    runs-on: [dedicate-hosted, x64, large]\n{strat}    steps:\n      - name: matrix step\n        run: |\n          echo version=${{{{ matrix.version }}}}"

def wfrunner(flavor):
    return f"on:\n  workflow_dispatch:\njobs:\n  test:\n    name: runner spec probe {flavor}\n    runs-on: [ubuntu-latest, x64, {flavor}]\n    steps:\n      - name: probe resources\n        run: |\n          nproc\n          free -m\n          df -BG ${{RUNNER_TEMP}}"

def wfartifact(size_mb):
    return f"on:\n  workflow_dispatch:\njobs:\n  upload:\n    name: upload artifact job\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: generate {size_mb}MB file\n        run: |\n          dd if=/dev/urandom of=artifact.bin bs=1M count={size_mb}\n      - name: upload artifact step\n        uses: upload-artifact\n        with:\n          name: perf-artifact\n          path: artifact.bin\n  download:\n    name: download artifact job\n    runs-on: [dedicate-hosted, x64, large]\n    needs: upload\n    steps:\n      - name: download artifact step\n        uses: download-artifact\n        with:\n          name: perf-artifact\n      - name: verify artifact step\n        run: |\n          ls -la perf-artifact"

def wflog(lines):
    return f"on:\n  workflow_dispatch:\njobs:\n  test:\n    name: log stability test job\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: generate {lines} lines log\n        run: |\n          for i in $(seq 1 {lines}); do echo LOG_LINE_${{i}} $(date +%s%N); done"

def wfneedsfail():
    return "on:\n  workflow_dispatch:\njobs:\n  job_a:\n    name: upstream failing job\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: fail step\n        run: |\n          exit 1\n  job_b:\n    name: downstream dependent job\n    runs-on: [dedicate-hosted, x64, large]\n    needs: job_a\n    steps:\n      - name: should be skipped\n        run: |\n          echo this should not run"

def wfcancel():
    return "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: cancel semantics test job\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: sleep main step\n        run: |\n          sleep 60\n      - name: cleanup always step\n        if: ${{ always() }}\n        run: |\n          echo cleanup executed"

def wfrace():
    return "on:\n  workflow_dispatch:\njobs:\n  job_a:\n    name: job A cancel target\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: sleep step\n        run: |\n          sleep 60\n  job_b:\n    name: job B failure condition\n    runs-on: [dedicate-hosted, x64, large]\n    needs: job_a\n    if: failure()\n    steps:\n      - name: should not run\n        run: |\n          echo this should not run"

def wfcontinue():
    return "on:\n  workflow_dispatch:\njobs:\n  job_a:\n    name: job with continue on error\n    runs-on: [dedicate-hosted, x64, large]\n    continue-on-error: true\n    steps:\n      - name: fail step\n        run: |\n          exit 1\n  job_b:\n    name: downstream after continue\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: success step\n        run: |\n          echo job_b executed"

def wfstage():
    return "on:\n  workflow_dispatch:\nstages:\n  - name: test_stage\n    fail_fast: true\n    jobs:\n      job_a:\n        name: stage job A\n        runs-on: [dedicate-hosted, x64, large]\n        steps:\n          - name: fail step\n            run: |\n              exit 1\n      job_b:\n        name: stage job B\n        runs-on: [dedicate-hosted, x64, large]\n        steps:\n          - name: sleep step\n            run: |\n              sleep 30\n      job_c:\n        name: stage job C\n        runs-on: [dedicate-hosted, x64, large]\n        steps:\n          - name: sleep step\n            run: |\n              sleep 30"

# ===== Cases 1-24 =====

add("REL-CONC-01-001", "INTENT-REL-001", "concurrency.max=5 时同时触发 5 个运行应全部进入执行态", "P1",
    ["仓库已配置 concurrency.max=5 的 workflow"],
    ["同时通过 API 触发 5 次该 workflow"],
    ["5 个运行均进入 in_progress 状态", "全部在合理时间内完成"],
    ["[正向] 5 个运行状态均为 completed(success)", "[非功能] queued→in_progress 调度时延 ≤60 秒"],
    "无需特殊清理", "none", wfc(5, "QUEUE", 10),
    [{"type":"positive","target":"run_status","equals":"completed(success)"},
     {"type":"nonfunctional","target":"queued_to_running_latency","le":"60s"}])

add("REL-CONC-01-002", "INTENT-REL-002", "concurrency.max=6 配置应被系统拒绝", "P1",
    ["仓库具备 workflow 创建权限"],
    ["创建 concurrency.max=6 的 workflow 并保存"],
    ["系统给出明确校验错误", "错误信息包含 max 超出范围提示"],
    ["[正向] YAML 校验失败或保存被拒", "[负向] 不应静默截断为 5"],
    "无需特殊清理", "none", wfc(6, "QUEUE", 10),
    [{"type":"positive","target":"yaml_validation","equals":"rejected"},
     {"type":"negative","target":"run_status","equals":"should_not_start"}])

add("REL-QUEUE-01-003", "INTENT-REL-003", "concurrency QUEUE 策略——超上限运行应排队等待", "P1",
    ["仓库已配置 concurrency.max=2 exceed-action=QUEUE 的 workflow"],
    ["同时触发 4 次该 workflow"],
    ["运行 1-2 进入 in_progress", "运行 3-4 进入 queued", "前 2 个完成后 3-4 自动启动"],
    ["[正向] 4 个运行最终全部 completed(success)", "[负向] 运行 3-4 不应被丢弃"],
    "无需特殊清理", "none", wfc(2, "QUEUE", 30),
    [{"type":"positive","target":"run_status","equals":"completed(success)"},
     {"type":"nonfunctional","target":"queued_count","equals":"2"}])

add("REL-IGNORE-01-004", "INTENT-REL-004", "concurrency IGNORE 策略——超上限运行应直接执行", "P1",
    ["仓库已配置 concurrency.max=2 exceed-action=IGNORE 的 workflow"],
    ["同时触发 4 次该 workflow"],
    ["4 个运行全部进入 in_progress", "无 queued 状态"],
    ["[正向] 4 个运行全部 completed(success)", "[负向] 不应出现 queued 状态"],
    "无需特殊清理", "none", wfc(2, "IGNORE", 30),
    [{"type":"positive","target":"run_status","equals":"completed(success)"},
     {"type":"negative","target":"run_status","equals":"queued"}])

add("REL-PREEMPT-01-005", "INTENT-REL-005", "preemption events 边界值——配置 10 个应正常解析", "P1",
    ["仓库具备 workflow 创建权限"],
    ["创建 concurrency.preemption.events 含 10 个事件的 workflow 并保存"],
    ["workflow YAML 校验通过", "运行正常触发"],
    ["[正向] workflow 保存成功并运行 completed(success)"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\nconcurrency:\n  max: 5\n  exceed-action: QUEUE\n  preemption:\n    events: [push, pull_request, workflow_dispatch, schedule, tag, issue_comment, pull_request_comment, merge_requests, fork_pr, manual]\njobs:\n  test:\n    name: preempt boundary test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: echo step\n        run: |\n          echo test",
    [{"type":"positive","target":"run_status","equals":"completed(success)"}])

add("REL-PREEMPT-01-006", "INTENT-REL-006", "preemption events 越界值——配置 11 个应被拒绝", "P1",
    ["仓库具备 workflow 创建权限"],
    ["创建 concurrency.preemption.events 含 11 个事件的 workflow"],
    ["系统在解析阶段报错", "错误信息包含 events 数量超限提示"],
    ["[正向] 明确报错", "[负向] 不应静默截断"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\nconcurrency:\n  max: 5\n  exceed-action: QUEUE\n  preemption:\n    events: [push, pull_request, workflow_dispatch, schedule, tag, issue_comment, pull_request_comment, merge_requests, fork_pr, manual, pr]\njobs:\n  test:\n    name: preempt invalid test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: echo step\n        run: |\n          echo test",
    [{"type":"positive","target":"yaml_validation","equals":"rejected"}])

add("REL-TIMEOUT-01-007", "INTENT-REL-007", "job timeout 边界值——359 分钟运行应在 360 分钟边界前完成", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发 timeout-minutes=360 的 workflow，job 执行 sleep 21540"],
    ["job 在 359 分钟前成功完成", "状态为 success"],
    ["[正向] job 状态=success", "[负向] 不应在 358 分钟前被强制终止"],
    "无需特殊清理", "none", wft(360, 21540),
    [{"type":"positive","target":"job_status","equals":"success"},
     {"type":"nonfunctional","target":"job_duration_minutes","le":"359"}])

add("REL-TIMEOUT-01-008", "INTENT-REL-008", "job timeout 越界触发——361 分钟应在 360 分钟被强制终止", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发 timeout-minutes=360 的 workflow，job 执行 sleep 21660"],
    ["job 在 360±2 分钟时被终止", "状态为 failure", "日志含超时信息"],
    ["[正向] job 状态=failure", "[正向] 日志含 timeout 或 超时", "[负向] 不应运行超过 365 分钟"],
    "无需特殊清理", "none", wft(360, 21660),
    [{"type":"positive","target":"job_status","equals":"failure"},
     {"type":"positive","target":"run_logs","contains":"timeout"}])

add("REL-TIMEOUT-01-009", "INTENT-REL-009", "自定义短超时——timeout-minutes=1 时 step 运行 2 分钟应被强制终止", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发 timeout-minutes=1 的 workflow，step 执行 sleep 120"],
    ["job 在 60±10 秒时被终止", "状态为 failure", "日志含超时信息"],
    ["[正向] job 状态=failure", "[正向] 实际运行时长 60±10 秒"],
    "无需特殊清理", "none", wft(1, 120),
    [{"type":"positive","target":"job_status","equals":"failure"},
     {"type":"nonfunctional","target":"job_duration_seconds","le":"70"}])

add("REL-TIMEOUT-01-010", "INTENT-REL-010", "默认超时——未声明 timeout-minutes 运行 361 分钟应被强制终止", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发未声明 timeout-minutes 的 workflow，job 执行 sleep 21660"],
    ["job 在 360 分钟时被终止", "状态为 failure", "日志含超时信息"],
    ["[正向] job 状态=failure", "[负向] 不应无限运行"],
    "无需特殊清理", "none", wfs(21660),
    [{"type":"positive","target":"job_status","equals":"failure"},
     {"type":"positive","target":"run_logs","contains":"timeout"}])

add("REL-RERUN-01-011", "INTENT-REL-011", "rerun 边界值——单条运行连续重新运行 3 次应全部成功", "P1",
    ["仓库存在一次失败的 workflow 运行"],
    ["对该运行依次执行 Re-run all jobs 共 3 次"],
    ["第 1-3 次 rerun 均创建新运行", "每次 rerun 的 atomgit.sha/ref 与原始运行一致", "3 次新运行均 success"],
    ["[正向] 运行编号递增", "[正向] 每次 rerun 状态=success", "[负向] 不应复用旧运行记录"],
    "无需特殊清理", "none", wfs(5),
    [{"type":"positive","target":"rerun_count","equals":"3"},
     {"type":"positive","target":"run_status","equals":"completed(success)"}])

add("REL-RERUN-01-012", "INTENT-REL-012", "rerun 越界值——尝试第 4 次重新运行应被系统拒绝", "P1",
    ["已完成 3 次 rerun 的运行记录存在"],
    ["尝试第 4 次 rerun"],
    ["第 4 次 rerun 被拒绝", "系统给出明确错误提示"],
    ["[正向] 第 4 次 rerun 按钮不可用或点击后报错", "[正向] 错误信息含最多 3 次或类似提示"],
    "无需特殊清理", "none", wfs(5),
    [{"type":"positive","target":"rerun_request","equals":"rejected"}])

add("REL-RERUN-01-013", "INTENT-REL-013", "rerun 6 小时年龄限制——超期运行不可重新运行", "P1",
    ["存在一条完成时间超过 6 小时的运行记录"],
    ["6 小时 1 分钟后尝试 rerun"],
    ["rerun 请求被拒绝", "错误信息含 6 小时或已过期"],
    ["[正向] rerun 被拒绝", "[负向] 不应创建新运行"],
    "无需特殊清理", "none", wfs(5),
    [{"type":"positive","target":"rerun_request","equals":"rejected"}])

add("REL-PATHS-01-014", "INTENT-REL-014", "paths 匹配边界值——变更恰好 300 个文件时 paths 过滤应生效", "P1",
    ["仓库已配置 on.push.paths 的 workflow"],
    ["push 变更恰好 300 个文件，其中 1 个匹配 paths 规则"],
    ["workflow 被正确触发"],
    ["[正向] workflow 运行被创建", "[负向] 不应因文件数=300 而判定异常"],
    "无需特殊清理", "none", wfpush("src/**"),
    [{"type":"positive","target":"run_status","equals":"completed(success)"}],
    trigger_event="push")

add("REL-PATHS-01-015", "INTENT-REL-015", "paths 匹配越界值——第 301 个变更文件不参与 paths 匹配判断", "P1",
    ["仓库已配置 on.push.paths 的 workflow"],
    ["push 变更 301 个文件，仅第 301 个匹配 paths 规则"],
    ["workflow 不触发"],
    ["[正向] workflow 不触发", "[负向] 第 301 个文件不应触发 workflow"],
    "无需特殊清理", "none", wfpush("src/**"),
    [{"type":"positive","target":"run_status","equals":"not_triggered"}],
    trigger_event="push")

add("REL-OUTPUT-01-016", "INTENT-REL-016", "step output 边界值——ATOMGIT_OUTPUT 写入 1 MB 参数应成功传递", "P1",
    ["仓库具备 workflow 运行权限"],
    ["job 的 step A 向 ATOMGIT_OUTPUT 写入恰好 1 MB 参数", "step B 读取该参数"],
    ["step B 读取到完整 1 MB 内容", "MD5 校验通过"],
    ["[正向] 下游读取内容长度=1,048,576 bytes", "[负向] 不应截断或丢失"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: output boundary test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: write 1MB output\n        id: writer\n        run: |\n          python3 -c \"print('A'*1048576)\" > out.txt\n          echo \"data=$(cat out.txt)\" >> $ATOMGIT_OUTPUT\n      - name: read 1MB output\n        run: |\n          echo \"${{{{ steps.writer.outputs.data }}}}\"\n          test $(echo \"${{{{ steps.writer.outputs.data }}}}\" | wc -c) -ge 1048576",
    [{"type":"positive","target":"step_output_length","equals":"1048576"}])

add("REL-OUTPUT-01-017", "INTENT-REL-017", "step output 越界值——ATOMGIT_OUTPUT 写入 1 MB+1 byte 应被拒绝或报错", "P1",
    ["仓库具备 workflow 运行权限"],
    ["job 的 step 向 ATOMGIT_OUTPUT 写入 1,048,577 bytes"],
    ["系统报错或截断并给出警告", "不应静默截断"],
    ["[正向] step 状态=failure 或日志含 1MB/超出限制", "[负向] 不应静默截断且无提示"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: output over limit test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: write 1MB+1 output\n        run: |\n          python3 -c \"print('A'*1048577)\" > out.txt\n          echo \"data=$(cat out.txt)\" >> $ATOMGIT_OUTPUT",
    [{"type":"positive","target":"run_logs","contains":"1MB"},
     {"type":"positive","target":"job_status","equals":"failure"}])

add("REL-DISK-01-018", "INTENT-REL-018", "Runner 磁盘边界——small runner 写入 49 GB 应成功", "P1",
    ["仓库具备 small runner 使用权限"],
    ["触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，job 顺序写入 49 GB 文件"],
    ["job 状态=success", "df 显示剩余约 1 GB", "文件完整性校验通过"],
    ["[正向] job 状态=success", "[负向] 不应在 49 GB 时报磁盘满"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: disk boundary test\n    runs-on: [ubuntu-latest, x64, small]\n    steps:\n      - name: write 49GB file\n        run: |\n          fallocate -l 49G testfile || dd if=/dev/zero of=testfile bs=1M count=50176\n      - name: verify disk space\n        run: |\n          df -h .\n          test -f testfile",
    [{"type":"positive","target":"job_status","equals":"success"}])

add("REL-DISK-01-019", "INTENT-REL-019", "Runner 磁盘越界——small runner 写入 51 GB 应失败并报磁盘满", "P1",
    ["仓库具备 small runner 使用权限"],
    ["触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，job 尝试写入 51 GB 文件"],
    ["job 状态=failure", "日志含 No space left on device 或平台等价错误"],
    ["[正向] job 状态=failure", "[正向] 日志含磁盘满错误", "[负向] 不应静默卡死"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: disk over limit test\n    runs-on: [ubuntu-latest, x64, small]\n    steps:\n      - name: write 51GB file\n        run: |\n          fallocate -l 51G testfile || dd if=/dev/zero of=testfile bs=1M count=52224\n        continue-on-error: true\n      - name: check failure\n        run: |\n          echo expecting failure above",
    [{"type":"positive","target":"job_status","equals":"failure"},
     {"type":"positive","target":"run_logs","contains":"No space left on device"}])

add("REL-MEM-01-020", "INTENT-REL-020", "Runner 内存边界——small runner 分配 7.5 GB 应成功", "P1",
    ["仓库具备 small runner 使用权限"],
    ["触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，job 分配 7.5 GB 内存"],
    ["job 状态=success", "内存占用峰值约 7.5 GB"],
    ["[正向] job 状态=success", "[负向] 不应在 7 GB 时 OOM"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: memory boundary test\n    runs-on: [ubuntu-latest, x64, small]\n    steps:\n      - name: allocate 7.5GB\n        run: |\n          python3 -c \"a=bytearray(7680*1024*1024); print(len(a))\"",
    [{"type":"positive","target":"job_status","equals":"success"}])

add("REL-MEM-01-021", "INTENT-REL-021", "Runner 内存越界——small runner 分配 9 GB 应被 OOM kill", "P1",
    ["仓库具备 small runner 使用权限"],
    ["触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，job 分配 9 GB 内存"],
    ["job 状态=failure", "日志含 OOM 或 Killed 信息", "不影响同 Runner 其他 job"],
    ["[正向] job 状态=failure", "[正向] 日志含 OOM 或 Killed", "[负向] 不应导致 Runner 宿主机崩溃"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: memory over limit test\n    runs-on: [ubuntu-latest, x64, small]\n    steps:\n      - name: allocate 9GB\n        run: |\n          python3 -c \"a=bytearray(9216*1024*1024); print(len(a))\"",
    [{"type":"positive","target":"job_status","equals":"failure"},
     {"type":"positive","target":"run_logs","contains":"Killed"}])

add("REL-CPU-01-022", "INTENT-REL-022", "Runner CPU 饱和——small runner 运行 4 个 CPU 密集型进程应完成但耗时延长", "P1",
    ["仓库具备 small runner 使用权限"],
    ["触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，启动 4 个并行 CPU burn 进程，各运行 60 秒"],
    ["job 状态=success", "总耗时约为 120±24 秒", "不应被强制终止"],
    ["[正向] job 状态=success", "[非功能] 总耗时 120±24 秒", "[负向] 不应被系统强制终止"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: CPU saturate test\n    runs-on: [ubuntu-latest, x64, small]\n    steps:\n      - name: burn 4 CPU processes\n        run: |\n          for i in 1 2 3 4; do python3 -c \"import time; end=time.time()+60; [x*x for x in range(10000)] while time.time()<end\" & done\n          wait",
    [{"type":"positive","target":"job_status","equals":"success"},
     {"type":"nonfunctional","target":"job_duration_seconds","ge":"96","le":"144"}])

add("REL-NEST-01-023", "INTENT-REL-023", "workflow_call 嵌套边界——2 层嵌套调用应成功执行", "P1",
    ["fixture 仓库包含 level1.yml 和 level2.yml 两个可重用 workflow"],
    ["触发主 workflow，该 workflow 通过 workflow_call 调用 level1，level1 再调用 level2"],
    ["3 个 workflow 均成功完成", "输入参数在每一层正确传递"],
    ["[正向] 最外层运行状态=success", "[正向] 所有子运行均 success"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  call_level1:\n    name: call level 1 workflow\n    uses: ./.gitcode/workflows/level1.yml",
    [{"type":"positive","target":"run_status","equals":"completed(success)"}])

add("REL-NEST-01-024", "INTENT-REL-024", "workflow_call 嵌套越界——3 层嵌套调用应被拒绝", "P1",
    ["fixture 仓库包含 level1/level2/level3.yml"],
    ["触发主 workflow，尝试 A→B→C→D（3 层嵌套）"],
    ["第 3 层调用失败", "运行状态=failure", "日志含嵌套层数或 2 层提示"],
    ["[正向] 运行状态=failure", "[正向] 日志明确提示嵌套超限", "[负向] 不应死循环或挂起"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  call_level1:\n    name: call level 1 workflow\n    uses: ./.gitcode/workflows/level1_deep.yml",
    [{"type":"positive","target":"run_status","equals":"completed(failure)"},
     {"type":"positive","target":"run_logs","contains":"嵌套"}])

add("REL-NEEDS-01-025", "INTENT-REL-025", "needs 失败传播——上游 job 失败时下游 job 应被 skip", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发含 job_a(失败) 和 job_b(needs: job_a) 的 workflow"],
    ["job_a 状态=failure", "job_b 状态=skipped", "job_b 不应执行"],
    ["[正向] job_a 状态=failure", "[正向] job_b 状态=skipped", "[负向] job_b 不应在 job_a 失败后仍执行"],
    "无需特殊清理", "none", wfneedsfail(),
    [{"type":"positive","target":"job_a_status","equals":"failure"},
     {"type":"positive","target":"job_b_status","equals":"skipped"}])

add("REL-MATRIX-01-026", "INTENT-REL-026", "matrix fail-fast=true——任意 job 实例失败应立即取消其余实例", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发含 3x3 matrix 且 fail-fast=true 的 workflow，其中 1 个实例故意失败"],
    ["失败 job 状态=failure", "其余未完成 jobs 状态=cancelled", "总执行时长显著短于全部跑完"],
    ["[正向] 失败 job 状态=failure", "[正向] 其余未完成 jobs 状态=cancelled", "[负向] 不应继续执行已失败的 matrix 其余实例"],
    "无需特殊清理", "none", wfmatrix([1,2,3], fail_fast=True),
    [{"type":"positive","target":"job_status","equals":"failure"},
     {"type":"positive","target":"cancelled_jobs_count","equals":"8"}])

add("REL-MATRIX-01-027", "INTENT-REL-027", "matrix max-parallel=4——9 个组合应最多同时运行 4 个", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发含 3x3 matrix 且 max-parallel=4 的 workflow"],
    ["任意时刻 in_progress 的 matrix job 数 ≤4", "前 4 个完成后自动启动后续 jobs"],
    ["[正向] 峰值并发≤4", "[正向] 9 个 jobs 全部 completed(success)", "[负向] 不应超过 4 个同时运行"],
    "无需特殊清理", "none", wfmatrix([1,2,3], max_parallel=4),
    [{"type":"positive","target":"max_concurrent_jobs","le":"4"},
     {"type":"positive","target":"run_status","equals":"completed(success)"}])

add("REL-CANCEL-01-028", "INTENT-REL-028", "手动取消 workflow——运行中取消时 always() cleanup step 仍应执行", "P1",
    ["仓库存在一条正在运行的 workflow"],
    ["手动取消该 workflow"],
    ["非 always step 被终止", "if: ${{ always() }} 的 cleanup step 被执行", "workflow 最终状态=cancelled"],
    ["[正向] 非 always step 被终止", "[正向] cleanup step 日志存在且 completed", "[正向] workflow 状态=cancelled"],
    "无需特殊清理", "none", wfcancel(),
    [{"type":"positive","target":"cleanup_step_status","equals":"success"},
     {"type":"positive","target":"run_status","equals":"canceled"}])

add("REL-STAGES-01-029", "INTENT-REL-029", "stages fail_fast 机制——阶段内任一 job 失败应立即终止同阶段其他 jobs", "P1",
    ["仓库具备 stages 使用权限"],
    ["触发含 stage 且 3 个 jobs 并行执行的 workflow，1 个 job 故意失败"],
    ["失败 job 状态=failure", "同阶段其余 jobs 状态=cancelled 或 skipped", "不应进入下一阶段"],
    ["[正向] 失败 job 状态=failure", "[正向] 同阶段其余 jobs 状态∈{cancelled, skipped}", "[负向] 不应进入下一阶段"],
    "无需特殊清理", "none", wfstage(),
    [{"type":"positive","target":"job_status","equals":"failure"},
     {"type":"positive","target":"cancelled_jobs_count","ge":"2"}])

add("REL-CONTINUE-01-030", "INTENT-REL-030", "continue-on-error=true——job 失败后 workflow 不应终止", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发含 continue-on-error=true 的失败 job 和下游 job 的 workflow"],
    ["job_a 状态=failure 但 workflow 不终止", "job_b 正常执行并 success"],
    ["[正向] job_a 状态=failure", "[正向] job_b 状态=success", "[负向] workflow 不应因 job_a 失败而整体 failure"],
    "无需特殊清理", "none", wfcontinue(),
    [{"type":"positive","target":"job_a_status","equals":"failure"},
     {"type":"positive","target":"job_b_status","equals":"success"},
     {"type":"positive","target":"workflow_status","equals":"success"}])

add("REL-FAULT-01-031", "INTENT-REL-031", "故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志", "P1",
    ["具备故障注入能力", "fixture 仓库可接受破坏性测试"],
    ["触发 workflow，在 job 执行到第 3 个 step 时对 runner 进程注入 SIGKILL"],
    ["job 状态=failure", "step 1-2 的日志完整可查看", "step 3 日志不完整或标记为中断"],
    ["[正向] job 状态=failure", "[正向] step 1-2 日志完整", "[负向] 不应状态=in_progress 挂起超过 5 分钟"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: fault injection SIGKILL\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: step one\n        run: |\n          echo step_one_marker\n      - name: step two\n        run: |\n          echo step_two_marker\n      - name: step three\n        run: |\n          sleep 30\n      - name: step four\n        run: |\n          echo step_four_marker\n      - name: step five\n        run: |\n          echo step_five_marker",
    [{"type":"positive","target":"job_status","equals":"failure"},
     {"type":"positive","target":"run_logs","contains":"step_one_marker"},
     {"type":"negative","target":"run_logs","contains":"step_four_marker"}],
    fault_injection={"at":"mid_job","action":"kill_runner","params":{"target_step":3},"recovery_expectation":"retry_and_succeed"})

add("REL-FAULT-01-032", "INTENT-REL-032", "故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误", "P1",
    ["具备故障注入能力", "fixture 仓库可接受破坏性测试"],
    ["触发含 upload-artifact step 的 workflow，在 upload 期间注入网络分区 30 秒"],
    ["upload-artifact step 状态=failure", "日志含 network/connection/timeout 或中文等价词", "不应无限挂起超过 120 秒"],
    ["[正向] upload-artifact step 状态=failure", "[正向] 日志含网络错误", "[负向] 不应无限挂起超过 120 秒"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: fault injection network partition\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: generate artifact file\n        run: |\n          dd if=/dev/urandom of=artifact.bin bs=1M count=10\n      - name: upload artifact step\n        uses: upload-artifact\n        with:\n          name: net-fault-artifact\n          path: artifact.bin",
    [{"type":"positive","target":"step_status","equals":"failure"},
     {"type":"positive","target":"run_logs","contains":"network"}],
    fault_injection={"at":"mid_job","action":"network_partition","params":{"duration_seconds":30,"target_step":2},"recovery_expectation":"explicit_error_and_rerun_success"})

add("REL-FAULT-01-033", "INTENT-REL-033", "故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满", "P1",
    ["具备故障注入能力", "fixture 仓库可接受破坏性测试"],
    ["在 small runner 上预填充 49.5 GB 数据，job 再尝试写入 2 GB artifact"],
    ["写入失败，日志含 No space left on device 或平台等价错误", "job 状态=failure"],
    ["[正向] job 状态=failure", "[正向] 日志含磁盘满错误"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: fault injection disk full\n    runs-on: [ubuntu-latest, x64, small]\n    steps:\n      - name: prefill disk\n        run: |\n          fallocate -l 49.5G prefill.bin || dd if=/dev/zero of=prefill.bin bs=1M count=50688\n      - name: write additional 2GB\n        run: |\n          dd if=/dev/zero of=extra.bin bs=1M count=2048",
    [{"type":"positive","target":"job_status","equals":"failure"},
     {"type":"positive","target":"run_logs","contains":"No space left on device"}],
    fault_injection={"at":"pre_job","action":"disk_full","params":{"pre_fill_gb":49.5,"append_gb":2},"recovery_expectation":"explicit_error_and_user_retry"})

add("REL-FAULT-01-034", "INTENT-REL-034", "故障注入——cache 服务 503 不可用时 job 应优雅降级为 cache miss", "P1",
    ["具备故障注入能力"],
    ["触发含 cache restore step 的 workflow，在 restore 期间注入 cache 服务 503"],
    ["cache step 状态=success(miss) 或 failure 但不阻断 job", "后续 step 正常执行", "job 不应因 cache 不可用而整体 failure"],
    ["[正向] cache step 标记为 miss 或跳过", "[正向] 后续 step 正常执行", "[负向] job 不应因 cache 服务不可用而整体 failure"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: fault injection cache 503\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: restore cache step\n        uses: cache\n        with:\n          path: node_modules\n          key: cache-deps\n      - name: subsequent step\n        run: |\n          echo subsequent step executed",
    [{"type":"positive","target":"job_status","equals":"success"},
     {"type":"positive","target":"run_logs","contains":"cache miss"}],
    fault_injection={"at":"mid_job","action":"concurrent_flood","params":{"service":"cache","response":"503","target_step":1},"recovery_expectation":"graceful_degradation_cache_miss"})

add("REL-FAULT-01-035", "INTENT-REL-035", "故障注入——artifact 下载服务 503 不可用时 job 应失败并报依赖服务错误", "P1",
    ["具备故障注入能力"],
    ["触发含 download-artifact step 的 workflow，在 download 期间注入服务 503"],
    ["download-artifact step 状态=failure", "日志含 503/service unavailable 或中文等价词", "job 状态=failure"],
    ["[正向] download-artifact step 状态=failure", "[正向] 日志含服务不可用错误", "[正向] job 状态=failure"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: fault injection artifact 503\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: download artifact step\n        uses: download-artifact\n        with:\n          name: missing-artifact",
    [{"type":"positive","target":"step_status","equals":"failure"},
     {"type":"positive","target":"run_logs","contains":"503"},
     {"type":"positive","target":"job_status","equals":"failure"}],
    fault_injection={"at":"mid_job","action":"concurrent_flood","params":{"service":"artifact_download","response":"503","target_step":1},"recovery_expectation":"explicit_error_and_rerun_success"})

add("REL-FLOOD-01-036", "INTENT-REL-036", "并发洪泛——同一仓库 10 个 push 同时触发 10 个 workflow 运行应无丢失", "P1",
    ["仓库具备 push 触发权限"],
    ["在 10 秒内对同一仓库 push 10 次，触发 10 个 workflow 运行"],
    ["10 个运行均被创建", "每个运行有独立的 RUN_ID", "10 个运行最终全部 completed"],
    ["[正向] 10 个运行均被创建", "[正向] 每个运行有独立 RUN_ID", "[负向] 不应出现运行数<10 或状态混乱"],
    "无需特殊清理", "none", wfs(5),
    [{"type":"positive","target":"created_runs_count","equals":"10"},
     {"type":"positive","target":"run_status","equals":"completed(success)"}],
    trigger_event="push")

add("REL-FLOOD-01-037", "INTENT-REL-037", "并发洪泛——同一仓库 50 个 push 同时触发应正确排队/限流不崩溃", "P1",
    ["仓库具备 push 触发权限"],
    ["在 30 秒内对同一仓库 push 50 次，触发 50 个 workflow 运行"],
    ["50 个运行均被创建", "系统 API/UI 响应正常", "50 个运行最终全部 completed"],
    ["[正向] 50 个运行均被创建", "[正向] API/UI 无 5xx", "[非功能] 全部完成总时长合理", "[负向] 不应出现运行丢失或重复触发"],
    "无需特殊清理", "none", wfs(5),
    [{"type":"positive","target":"created_runs_count","equals":"50"},
     {"type":"positive","target":"api_status","equals":"200"},
     {"type":"negative","target":"api_status","equals":"500"}],
    trigger_event="push")

add("REL-MATRIX-01-038", "INTENT-REL-038", "大规模 matrix——20 个组合应全部生成并正确调度", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发含 4 维×5 值=20 组合的 matrix workflow"],
    ["20 个 jobs 全部生成", "每个实例获得正确的矩阵变量值", "20 个 jobs 全部 completed(success)"],
    ["[正向] 20 个 jobs 全部生成", "[正向] 矩阵变量校验 100% 通过", "[负向] 不应出现重复组合或遗漏组合"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: matrix 20 combos test\n    runs-on: [dedicate-hosted, x64, large]\n    strategy:\n      matrix:\n        os: [ubuntu, euler]\n        arch: [x64, arm64]\n        compiler: [gcc, clang]\n        mode: [debug, release, profile]\n    steps:\n      - name: verify matrix vars\n        run: |\n          echo os=${{{{ matrix.os }}}} arch=${{{{ matrix.arch }}}} compiler=${{{{ matrix.compiler }}}} mode=${{{{ matrix.mode }}}}",
    [{"type":"positive","target":"generated_jobs_count","equals":"20"},
     {"type":"positive","target":"run_status","equals":"completed(success)"}])

add("REL-MATRIX-01-039", "INTENT-REL-039", "大规模 matrix——50 个组合应全部生成并正确调度", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发含 5 维×10 值=50 组合的 matrix workflow"],
    ["50 个 jobs 全部生成", "无重复/遗漏组合", "调度时延 ≤300 秒"],
    ["[正向] 50 个 jobs 全部生成", "[正向] 无重复/遗漏组合", "[非功能] 调度时延 ≤300 秒"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: matrix 50 combos test\n    runs-on: [dedicate-hosted, x64, large]\n    strategy:\n      matrix:\n        v1: [a,b,c,d,e]\n        v2: [1,2,3,4,5,6,7,8,9,10]\n    steps:\n      - name: verify matrix vars\n        run: |\n          echo v1=${{{{ matrix.v1 }}}} v2=${{{{ matrix.v2 }}}}",
    [{"type":"positive","target":"generated_jobs_count","equals":"50"},
     {"type":"nonfunctional","target":"scheduling_latency_seconds","le":"300"}])

add("REL-LOG-01-040", "INTENT-REL-040", "超长日志——单 job 输出 100 MB 日志应完整保留且可下载查看", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发 job 连续输出 100 MB 日志的 workflow"],
    ["日志总大小约 100 MB", "日志首尾行均可查看无截断", "日志下载 API/页面可正常下载"],
    ["[正向] 日志总大小≈100 MB", "[正向] 首尾行可查看", "[正向] 日志下载正常", "[负向] 不应截断或乱序"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: log size 100MB test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: generate 100MB log\n        run: |\n          for i in $(seq 1 2500); do python3 -c \"print('A'*40960)\"; done",
    [{"type":"positive","target":"log_size_mb","equals":"100"},
     {"type":"positive","target":"log_download","equals":"success"}])

add("REL-ART-01-041", "INTENT-REL-041", "超大 artifact——100 MB artifact 上传后下游 job 应成功下载", "P1",
    ["仓库具备 artifact 使用权限"],
    ["触发含 upload-artifact(100MB) 和 download-artifact 的 workflow"],
    ["upload 成功", "download 成功", "下载后文件 MD5 与上传前一致"],
    ["[正向] upload 成功", "[正向] download 成功", "[正向] MD5 校验通过"],
    "重置 fixture 仓库", "fixture", wfartifact(100),
    [{"type":"positive","target":"upload_status","equals":"success"},
     {"type":"positive","target":"download_status","equals":"success"},
     {"type":"positive","target":"md5_match","equals":"true"}])

# 50 steps workflow generated programmatically after list build
add("REL-STEPS-01-042", "INTENT-REL-042", "超多 step——单 job 内 50 个 step 应全部串行执行无丢失", "P1",
    ["仓库具备 workflow 创建权限"],
    ["创建含单 job 50 个 step 的 workflow 并保存/触发"],
    ["若平台限制≤16，则应明确拒绝或自动拆分", "50 个 step 按顺序执行无丢失"],
    ["[正向] 50 个 step 全部出现在运行详情页", "[正向] 每个 step 日志包含唯一标识", "[负向] 不应出现 step 丢失或顺序错乱"],
    "无需特殊清理", "none", "",  # workflow filled post-build
    [{"type":"positive","target":"step_count","equals":"50"},
     {"type":"positive","target":"step_order","equals":"correct"}])

add("REL-LONG-01-043", "INTENT-REL-043", "长时运行接近 timeout 边界——350 分钟运行应成功且心跳保活正常", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发 timeout-minutes=360 的 workflow，job 运行 350 分钟并每 60 秒输出心跳日志"],
    ["job 状态=success", "运行期间每 60 秒至少输出 1 行日志", "不应在 350 分钟前被误判为死进程"],
    ["[正向] job 状态=success", "[正向] 心跳日志间隔≤60 秒", "[负向] 不应在 350 分钟前被终止"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: long run 350min test\n    runs-on: [dedicate-hosted, x64, large]\n    timeout-minutes: 360\n    steps:\n      - name: heartbeat run\n        run: |\n          for i in $(seq 1 350); do\n            echo heartbeat $i\n            sleep 60\n          done",
    [{"type":"positive","target":"job_status","equals":"success"},
     {"type":"nonfunctional","target":"heartbeat_interval_seconds","le":"60"}])

add("REL-FAIR-01-044", "INTENT-REL-044", "并发资源公平性——2 个 workflow 各 3 个 jobs 应被公平调度", "P1",
    ["仓库具备同时触发多个 workflow 的权限"],
    ["同时触发 workflow X 和 workflow Y，各含 3 个 jobs，每 job sleep 30 秒"],
    ["2 个 workflow 的 jobs 启动时间差 ≤60 秒", "无单个 workflow 独占所有 Runner"],
    ["[正向] 启动时延差≤60 秒", "[负向] 不应出现 workflow X 全部完成后 workflow Y 才开始"],
    "无需特殊清理", "none", wfs(30),
    [{"type":"nonfunctional","target":"startup_time_diff_seconds","le":"60"}])

add("REL-K8S-01-045", "INTENT-REL-045", "自托管 K8s Runner 弹性伸缩——min=1/max=1 时并发 3 个 jobs 应排队执行", "P1",
    ["仓库具备 K8s Runner 使用权限", "K8s Runner 组配置 min=1 max=1"],
    ["并发触发 3 个 jobs 到 K8s Runner 组"],
    ["Runner Pod 数始终=1", "3 个 jobs 顺序执行", "不应创建 2 个及以上 Pod"],
    ["[正向] Pod 数=1", "[正向] 峰值并发=1", "[负向] 不应创建 2 个及以上 Pod"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: K8s runner scaling test\n    runs-on: [self-hosted, kubernetes, small]\n    steps:\n      - name: sleep step\n        run: |\n          sleep 10",
    [{"type":"positive","target":"pod_count","equals":"1"},
     {"type":"positive","target":"max_concurrent_jobs","equals":"1"}])

add("REL-CACHE-01-046", "INTENT-REL-046", "缓存 LRU 淘汰压力——连续写入 10 个大缓存后最旧缓存应被正确淘汰", "P1",
    ["仓库具备 cache 使用权限"],
    ["连续 10 次触发同一 workflow，每次使用不同 cache key 写入 100 MB 缓存"],
    ["最新写入的缓存 key 可命中", "最旧的缓存 key 变为 miss", "不应出现所有 10 个 key 同时命中"],
    ["[正向] 最新 key 状态=hit", "[正向] 最旧 key 状态=miss", "[负向] 不应所有 10 个 key 同时命中"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: cache LRU test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: save cache\n        uses: cache\n        with:\n          path: cache_data\n          key: cache-${{ matrix.index }}\n      - name: generate cache data\n        run: |\n          mkdir -p cache_data\n          dd if=/dev/urandom of=cache_data/data.bin bs=1M count=100",
    [{"type":"positive","target":"latest_cache_status","equals":"hit"},
     {"type":"positive","target":"oldest_cache_status","equals":"miss"}])

add("REL-RETAIN-01-047", "INTENT-REL-047", "artifact 保留期 90 天边界——第 91 天应不可下载", "P1",
    ["仓库具备 artifact 使用权限"],
    ["上传保留期为 90 天的 artifact", "第 90 天尝试下载", "第 91 天尝试下载"],
    ["第 90 天下载成功(HTTP 200)", "第 91 天下载失败(404/403)"],
    ["[正向] 第 90 天可下载", "[正向] 第 91 天不可下载"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: artifact retention test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: create artifact\n        run: |\n          echo retention test > retention.txt\n      - name: upload artifact\n        uses: upload-artifact\n        with:\n          name: retention-artifact\n          path: retention.txt\n          retention-days: 90",
    [{"type":"positive","target":"download_day90_status","equals":"200"},
     {"type":"positive","target":"download_day91_status","equals":"404"}])

add("REL-RACE-01-048", "INTENT-REL-048", "取消与 needs 条件竞态——job A 被取消时 job B(if: failure())应正确判定", "P1",
    ["仓库存在正在运行的 workflow"],
    ["job A 运行中被手动取消，job B needs A 且 if: failure()"],
    ["job A 状态=cancelled", "job B 状态=skipped", "job B 不应执行"],
    ["[正向] job A 状态=cancelled", "[正向] job B 状态=skipped", "[负向] job B 不应执行"],
    "无需特殊清理", "none", wfrace(),
    [{"type":"positive","target":"job_a_status","equals":"canceled"},
     {"type":"positive","target":"job_b_status","equals":"skipped"}])

add("REL-RUNNER-01-049", "INTENT-REL-049", "Runner 规格真实性——small/medium/large 实际 CPU/内存/磁盘 vs 声明值", "P1",
    ["仓库具备多种 flavor runner 使用权限"],
    ["对 small/medium/large 各触发探针 job，读取 /proc/cpuinfo、free -m、df"],
    ["每种 flavor 实际资源不低于声明值的 90%", "各探针在 5 分钟内完成调度"],
    ["[正向] CPU/内存/磁盘最小比率≥0.9", "[负向] 实际资源不应显著低于声明", "[非功能] queued→running ≤5min"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  probe-small:\n    name: probe small runner\n    runs-on: [ubuntu-latest, x64, small]\n    steps:\n      - name: probe small\n        run: |\n          nproc\n          free -m\n          df -BG ${{RUNNER_TEMP}}\n  probe-medium:\n    name: probe medium runner\n    runs-on: [ubuntu-latest, x64, medium]\n    steps:\n      - name: probe medium\n        run: |\n          nproc\n          free -m\n          df -BG ${{RUNNER_TEMP}}\n  probe-large:\n    name: probe large runner\n    runs-on: [ubuntu-latest, x64, large]\n    steps:\n      - name: probe large\n        run: |\n          nproc\n          free -m\n          df -BG ${{RUNNER_TEMP}}",
    [{"type":"positive","target":"resource_ratio","ge":"0.9"},
     {"type":"nonfunctional","target":"queued_to_running_minutes","le":"5"}])

add("REL-RUNNER-01-049-V2", "INTENT-REL-049", "Runner 规格真实性——xlarge/2xlarge 实际 CPU/内存/磁盘 vs 声明值", "P1",
    ["仓库具备大规格 runner 使用权限"],
    ["对 xlarge/2xlarge 各触发探针 job，读取系统资源"],
    ["每种 flavor 实际资源不低于声明值的 90%", "失败时归因清晰"],
    ["[正向] CPU/内存/磁盘最小比率≥0.9", "[负向] 不应因架构不匹配而随机失败"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  probe-xlarge:\n    name: probe xlarge runner\n    runs-on: [ubuntu-latest, x64, xlarge]\n    steps:\n      - name: probe xlarge\n        run: |\n          nproc\n          free -m\n          df -BG ${{RUNNER_TEMP}}\n  probe-2xlarge:\n    name: probe 2xlarge runner\n    runs-on: [ubuntu-latest, x64, 2xlarge]\n    steps:\n      - name: probe 2xlarge\n        run: |\n          nproc\n          free -m\n          df -BG ${{RUNNER_TEMP}}",
    [{"type":"positive","target":"resource_ratio","ge":"0.9"},
     {"type":"positive","target":"failure_attribution","equals":"clear"}])

add("REL-LATENCY-01-050", "INTENT-REL-050", "调度延迟基准——queued→running P50/P95 等待时间", "P1",
    ["仓库具备 workflow 运行权限", "runner 池存在空闲 runner"],
    ["在空闲 runner 条件下连续触发 30 次单 job workflow，记录 queued→running 延迟"],
    ["P95 延迟有界", "形成可复现的基准数据集"],
    ["[正向] P95≤60s", "[负向] 不应出现 runner 空闲但 job 死等>10min"],
    "无需特殊清理", "none", wfs(5),
    [{"type":"nonfunctional","target":"p95_latency_seconds","le":"60"},
     {"type":"nonfunctional","target":"p50_latency_seconds","le":"30"}])

add("REL-LATENCY-01-050-V2", "INTENT-REL-050", "调度延迟压力——并发 20 个 job 的排队延迟与完成率", "P1",
    ["仓库具备 workflow 运行权限"],
    ["并发触发 20 个单 job workflow，各 sleep 60s"],
    ["所有 job 最终完成", "无饿死", "排队延迟可观测"],
    ["[正向] 20 个 job 全部完成", "[负向] 无 job 被无限饿死"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: latency pressure job\n    runs-on: [dedicate-hosted, x64, large]\n    strategy:\n      matrix:\n        index: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]\n    steps:\n      - name: sleep 60s\n        run: |\n          sleep 60",
    [{"type":"positive","target":"completed_jobs_count","equals":"20"},
     {"type":"nonfunctional","target":"max_queued_time_seconds","le":"300"}])

add("REL-LOGPERF-01-051", "INTENT-REL-051", "日志加载性能——50MB 日志下载与查看耗时", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发生成 50MB 日志的 workflow，测量下载与查看耗时"],
    ["50MB 日志可在 ≤30s 内下载完成", "日志内容完整、不乱序、不截断"],
    ["[正向] 下载≤30s", "[正向] 大小/行数 100% 一致", "[负向] 不应 UI 卡死"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: log perf 50MB test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: generate 50MB log\n        run: |\n          for i in $(seq 1 50000); do echo LOG_LINE_${{i}} $(date +%s%N); done",
    [{"type":"nonfunctional","target":"download_time_seconds","le":"30"},
     {"type":"positive","target":"log_integrity","equals":"100%"}])

add("REL-LOGPERF-01-051-V2", "INTENT-REL-051", "日志加载性能——200MB 日志下载与查看耗时", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发生成 200MB 日志的 workflow，测量下载与查看耗时"],
    ["200MB 日志可在 ≤120s 内下载完成", "日志内容完整"],
    ["[正向] 下载≤120s", "[正向] 大小/行数 100% 一致"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: log perf 200MB test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: generate 200MB log\n        run: |\n          for i in $(seq 1 200000); do echo LOG_LINE_${{i}} $(date +%s%N); done",
    [{"type":"nonfunctional","target":"download_time_seconds","le":"120"},
     {"type":"positive","target":"log_integrity","equals":"100%"}])

add("REL-IMAGE-01-052", "INTENT-REL-052", "镜像拉取性能——500MB 自定义 container 环境准备耗时基准", "P1",
    ["仓库具备 container 使用权限"],
    ["触发使用 ~500MB 镜像的 container job，测量拉取耗时"],
    ["500MB 镜像在 2min 内完成拉取并启动", "失败时有明确归因"],
    ["[正向] 拉取≤2min", "[负向] 不应 pending 10min 后无解释失败"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: image pull 500MB test\n    runs-on: [dedicate-hosted, x64, large]\n    container:\n      image: python:3.11-slim\n    steps:\n      - name: check python version\n        run: |\n          python --version",
    [{"type":"nonfunctional","target":"image_pull_time_seconds","le":"120"},
     {"type":"positive","target":"job_status","equals":"success"}])

add("REL-IMAGE-01-052-V2", "INTENT-REL-052", "镜像拉取性能——5GB 自定义 container 环境准备耗时基准", "P1",
    ["仓库具备 container 使用权限"],
    ["触发使用 ~5GB 镜像的 container job，测量拉取耗时"],
    ["5GB 镜像在 10min 内完成拉取并启动", "失败时有明确归因"],
    ["[正向] 拉取≤600s", "[负向] 不应 pending 后无解释失败"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: image pull 5GB test\n    runs-on: [dedicate-hosted, x64, large]\n    container:\n      image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime\n    steps:\n      - name: check environment\n        run: |\n          python --version",
    [{"type":"nonfunctional","target":"image_pull_time_seconds","le":"600"},
     {"type":"positive","target":"job_status","equals":"success"}])

add("REL-ARTPERF-01-053", "INTENT-REL-053", "制品传输性能——100MB artifact 上传下载耗时", "P1",
    ["仓库具备 artifact 使用权限"],
    ["触发含 100MB artifact upload/download 的 workflow"],
    ["上传/下载均成功且 hash 100% 匹配", "上传≤30s 下载≤30s"],
    ["[正向] 上传≤30s", "[正向] 下载≤30s", "[正向] hash 100% 匹配"],
    "重置 fixture 仓库", "fixture", wfartifact(100),
    [{"type":"nonfunctional","target":"upload_time_seconds","le":"30"},
     {"type":"nonfunctional","target":"download_time_seconds","le":"30"},
     {"type":"positive","target":"hash_match","equals":"true"}])

add("REL-ARTPERF-01-053-V2", "INTENT-REL-053", "制品传输性能——1GB artifact 上传下载耗时", "P1",
    ["仓库具备 artifact 使用权限"],
    ["触发含 1GB artifact upload/download 的 workflow"],
    ["上传/下载均成功且 hash 100% 匹配", "上传≤300s 下载≤300s"],
    ["[正向] 上传≤300s", "[正向] 下载≤300s", "[正向] hash 100% 匹配"],
    "重置 fixture 仓库", "fixture", wfartifact(1024),
    [{"type":"nonfunctional","target":"upload_time_seconds","le":"300"},
     {"type":"nonfunctional","target":"download_time_seconds","le":"300"},
     {"type":"positive","target":"hash_match","equals":"true"}])

add("REL-CACHEPERF-01-054", "INTENT-REL-054", "缓存加速比——cache 命中 vs 未命中构建耗时对比", "P2",
    ["仓库具备 cache 使用权限"],
    ["第一轮无 cache 记录安装耗时 T1", "第二轮 cache 命中记录耗时 T2"],
    ["T2 ≤ 0.5 × T1", "restore 耗时≤30s"],
    ["[正向] 加速比≥2x", "[负向] cache 命中后不应仍执行完整安装"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: cache speedup test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: restore cache\n        uses: cache\n        with:\n          path: node_modules\n          key: cache-deps-${{ matrix.run }}\n      - name: install deps\n        run: |\n          npm ci || true\n      - name: save cache\n        uses: cache\n        with:\n          path: node_modules\n          key: cache-deps-${{ matrix.run }}",
    [{"type":"nonfunctional","target":"speedup_ratio","ge":"2"},
     {"type":"nonfunctional","target":"restore_time_seconds","le":"30"}])

add("REL-PRESSURE-01-055", "INTENT-REL-055", "并发压测——concurrency.max=5 时触发 20 个 workflow 的排队与完成率", "P1",
    ["仓库具备 workflow 触发权限"],
    ["在 10s 内并发触发 20 次同一 workflow，每 job sleep 30s"],
    ["20 次触发全部进入终态", "running 峰值≤5", "总耗时≤15min"],
    ["[正向] completed=20", "[负向] running 峰值不应>5", "[负向] 不应出现运行静默消失"],
    "无需特殊清理", "none", wfc(5, "QUEUE", 30),
    [{"type":"positive","target":"completed_count","equals":"20"},
     {"type":"nonfunctional","target":"max_running_count","le":"5"},
     {"type":"nonfunctional","target":"total_duration_seconds","le":"900"}])

add("REL-MATRIXFAIR-01-056", "INTENT-REL-056", "矩阵调度公平性——20 实例 matrix 配 max-parallel=4 的无饿死验证", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发 20 实例 matrix 配 max-parallel=4，每实例 sleep 30s"],
    ["20 实例 100% 完成", "最大 queued 延迟≤3×最小延迟", "总耗时≈3min"],
    ["[正向] 20 实例全部完成", "[非功能] 最大/最小 queued 延迟比≤3", "[负向] 无实例被无限饿死"],
    "无需特殊清理", "none", wfmatrix(list(range(1,21)), max_parallel=4),
    [{"type":"positive","target":"completed_jobs_count","equals":"20"},
     {"type":"nonfunctional","target":"queued_delay_ratio","le":"3"}])

add("REL-SCHED-01-057", "INTENT-REL-057", "资源调度状态一致性——空闲 runner 存在时 job 不应死等", "P1",
    ["runner 池存在空闲 runner"],
    ["连续触发 10 次单 job workflow，每次完成后等待 runner 空闲再触发下一次"],
    ["10 次全部 queued→running ≤60s", "平均≤30s"],
    ["[正向] 10 次全部≤60s", "[非功能] 平均≤30s", "[负向] 不应出现 runner 空闲但 job 死等>5min"],
    "无需特殊清理", "none", wfs(30),
    [{"type":"nonfunctional","target":"max_queued_to_running_seconds","le":"60"},
     {"type":"nonfunctional","target":"avg_queued_to_running_seconds","le":"30"}])

add("REL-STATE-01-058", "INTENT-REL-058", "Runner 状态机正确性——空闲/运行/离线转换与时序一致性", "P1",
    ["仓库具备 runner 状态查询权限"],
    ["对同一 runner 连续执行触发→观察→等待→触发循环 5 轮"],
    ["状态序列符合 idle→running→idle", "转换时延有界"],
    ["[正向] 状态序列正确", "[非功能] idle→running≤30s", "[非功能] running→idle≤60s"],
    "无需特殊清理", "none", wfs(60),
    [{"type":"positive","target":"state_sequence","equals":"idle_running_idle"},
     {"type":"nonfunctional","target":"idle_to_running_seconds","le":"30"},
     {"type":"nonfunctional","target":"running_to_idle_seconds","le":"60"}])

add("REL-LOGSTABLE-01-059", "INTENT-REL-059", "日志系统稳定性——6 万行日志无乱序/无丢失/无截断", "P1",
    ["仓库具备 workflow 运行权限"],
    ["触发生成 6 万行带序号日志的 workflow"],
    ["UI 和下载文件中日志完整", "行号单调递增", "无乱序无丢失"],
    ["[正向] 行数=60000", "[正向] 行号单调递增", "[负向] 不应出现行号跳变或乱序"],
    "无需特殊清理", "none", wflog(60000),
    [{"type":"positive","target":"log_line_count","equals":"60000"},
     {"type":"positive","target":"log_order","equals":"monotonic"}])

add("REL-YAMLCACHE-01-060", "INTENT-REL-060", "Workflow YAML 缓存失效——修改后无旧代码残留", "P1",
    ["仓库具备 workflow 修改与触发权限"],
    ["第一轮执行记录输出 marker_v1", "修改 workflow 输出为 marker_v2 并 push", "立即触发 workflow"],
    ["新触发运行日志中出现 marker_v2", "不应出现 marker_v1 缓存残留"],
    ["[正向] 日志打印 marker_v2", "[负向] 不应打印 marker_v1"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: YAML cache invalidation test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: echo marker\n        run: |\n          echo marker_v1",
    [{"type":"positive","target":"run_logs","contains":"marker_v2"},
     {"type":"negative","target":"run_logs","contains":"marker_v1"}])

add("REL-CANCELREL-01-061", "INTENT-REL-061", "取消操作可靠性——queued/running/post 各阶段取消状态正确过渡", "P1",
    ["仓库具备取消操作权限"],
    ["实验 a: 触发后立即取消(queued 阶段)", "实验 b: running 30s 后取消(running 阶段)", "实验 c: 主 step 完成后 post 执行中取消(post 阶段)"],
    ["queued 取消→终态 cancelled 无 runner 分配", "running 取消→终态 cancelled 且 cleanup 执行", "post 取消→主结论不变 post 被终止"],
    ["[正向] 各阶段取消终态稳定", "[非功能] 取消到终态稳定时间≤60s", "[负向] queued 取消后不应错标 success/failure"],
    "重置 fixture 仓库", "fixture", wfcancel(),
    [{"type":"positive","target":"cancel_queued_status","equals":"canceled"},
     {"type":"positive","target":"cancel_running_status","equals":"canceled"},
     {"type":"positive","target":"cancel_post_main_status","equals":"success"},
     {"type":"nonfunctional","target":"cancel_stabilization_seconds","le":"60"}])

add("REL-NETFAULT-01-062", "INTENT-REL-062", "网络依赖容错——workflow 中访问不可达地址的明确失败与有界超时", "P2",
    ["仓库具备外网访问权限"],
    ["job 内依次 curl 访问: 公网可达端点、不存在域名、RFC5737 黑洞地址、被防火墙 drop 的端口"],
    ["可达地址成功返回", "不可达地址在≤60s 内失败且归因清晰"],
    ["[正向] 可达地址成功", "[负向] 不可达地址不应 hang>60s", "[非功能] 失败归因清晰"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: network fault tolerance test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: curl unreachable addresses\n        run: |\n          curl --connect-timeout 10 --max-time 120 -v http://192.0.2.1/ || true\n          curl --connect-timeout 10 --max-time 120 -v http://nonexistent-domain-test.example/ || true",
    [{"type":"positive","target":"reachable_status","equals":"success"},
     {"type":"positive","target":"unreachable_timeout_seconds","le":"60"},
     {"type":"positive","target":"failure_attribution","equals":"clear"}])

add("REL-ARTCONC-01-063", "INTENT-REL-063", "制品并发写一致性——多 job 同时 upload-artifact 同名 artifact", "P1",
    ["仓库具备 artifact 使用权限"],
    ["matrix 3 实例并行，每实例生成不同内容文件并同时 upload-artifact 到同名 artifact"],
    ["下载内容确定，绝非混合态", "内容完整无损"],
    ["[正向] 下载内容确定", "[负向] 不应出现 ABA/BAB 等混合态"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: artifact concurrent write test\n    runs-on: [dedicate-hosted, x64, large]\n    strategy:\n      matrix:\n        instance: [1,2,3]\n    steps:\n      - name: generate content\n        run: |\n          if [ \"${{{{ matrix.instance }}}}\" = \"1\" ]; then python3 -c \"print('A'*1048576)\" > out.txt; fi\n          if [ \"${{{{ matrix.instance }}}}\" = \"2\" ]; then python3 -c \"print('B'*1048576)\" > out.txt; fi\n          if [ \"${{{{ matrix.instance }}}}\" = \"3\" ]; then python3 -c \"print('C'*1048576)\" > out.txt; fi\n      - name: upload artifact step\n        uses: upload-artifact\n        with:\n          name: concurrent-artifact\n          path: out.txt",
    [{"type":"positive","target":"download_content","in":["AAA","BBB","CCC"]},
     {"type":"negative","target":"download_content","contains_mixed":"false"}])

add("REL-CHILDSTATE-01-064", "INTENT-REL-064", "子任务状态传播——workflow_call 失败时父 workflow 不应假阳性完成", "P0",
    ["fixture 仓库包含可失败的子 workflow"],
    ["触发父 workflow，其通过 workflow_call 调用会失败的子 workflow"],
    ["子 workflow 失败时父 workflow 明确标记 failure", "下游默认 job 被 skip"],
    ["[正向] 父 workflow 状态=failure", "[正向] 下游 job 被 skip", "[负向] 父 workflow 不应显示 success"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  call_child:\n    name: call failing child workflow\n    uses: ./.gitcode/workflows/child_fail.yml\n  downstream:\n    name: downstream job\n    runs-on: [dedicate-hosted, x64, large]\n    needs: call_child\n    steps:\n      - name: should not run\n        run: |\n          echo downstream",
    [{"type":"positive","target":"parent_status","equals":"failure"},
     {"type":"positive","target":"downstream_status","equals":"skipped"},
     {"type":"negative","target":"parent_status","equals":"success"}])

add("REL-CHILDSTATE-01-064-V2", "INTENT-REL-064", "子任务状态传播——workflow_call 未拉起时父 workflow 不应假阳性完成", "P0",
    ["fixture 仓库引用不存在的子 workflow"],
    ["触发父 workflow，其通过 workflow_call 引用不存在的子 workflow"],
    ["父 workflow 明确标记 failure", "下游默认 job 被 skip"],
    ["[正向] 父 workflow 状态=failure", "[正向] 下游 job 被 skip", "[负向] 父 workflow 不应显示 success"],
    "重置 fixture 仓库", "fixture",
    "on:\n  workflow_dispatch:\njobs:\n  call_child:\n    name: call missing child workflow\n    uses: ./.gitcode/workflows/child_missing.yml\n  downstream:\n    name: downstream job\n    runs-on: [dedicate-hosted, x64, large]\n    needs: call_child\n    steps:\n      - name: should not run\n        run: |\n          echo downstream",
    [{"type":"positive","target":"parent_status","equals":"failure"},
     {"type":"positive","target":"downstream_status","equals":"skipped"},
     {"type":"negative","target":"parent_status","equals":"success"}])

add("REL-API-01-065", "INTENT-REL-065", "API 限流与一致性——10 QPS 高频查询 run/job 状态不丢数据", "P2",
    ["具备 API 查询权限与测试脚本环境"],
    ["以 10 QPS 连续查询一个 running 状态的 run 详情 API，持续 60s"],
    ["全部返回 200", "status 字段无矛盾", "P95 响应时间≤2s"],
    ["[正向] 200 占比=100%", "[负向] 不应出现 429/503/500", "[非功能] P95≤2s"],
    "无需特殊清理", "none", wfs(30),
    [{"type":"positive","target":"http_200_ratio","equals":"100%"},
     {"type":"negative","target":"http_error_codes","contains":"429"},
     {"type":"nonfunctional","target":"response_time_p95_seconds","le":"2"}])

add("REL-BIGRUNNER-01-066", "INTENT-REL-066", "大规格资源调度稳定性——xlarge/2xlarge 反复编译成功率", "P1",
    ["仓库具备 xlarge/2xlarge runner 使用权限"],
    ["对 xlarge 和 2xlarge 各触发 10 次编译型 job"],
    ["成功率≥90%", "失败归因 100% 明确", "无 flaky"],
    ["[正向] 成功率≥90%", "[正向] 失败归因明确", "[负向] 不应出现同一规格今天成功明天失败"],
    "无需特殊清理", "none",
    "on:\n  workflow_dispatch:\njobs:\n  compile_xlarge:\n    name: compile on xlarge\n    runs-on: [ubuntu-latest, x64, xlarge]\n    steps:\n      - name: compile step\n        run: |\n          echo compiling\n          sleep 30\n  compile_2xlarge:\n    name: compile on 2xlarge\n    runs-on: [ubuntu-latest, x64, 2xlarge]\n    steps:\n      - name: compile step\n        run: |\n          echo compiling\n          sleep 30",
    [{"type":"positive","target":"success_rate","ge":"90"},
     {"type":"positive","target":"failure_attribution","equals":"clear"}])

# Post-process special cases
for c in CASES:
    if c['id'] == 'REL-STEPS-01-042':
        c['workflow'] = "on:\n  workflow_dispatch:\njobs:\n  test:\n    name: steps count 50 test\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n" + "\n".join([f"      - name: step {i:02d}\n        run: |\n          echo step {i:02d}" for i in range(1, 51)])

def gen():
    total = len(CASES)
    for idx, c in enumerate(CASES, 1):
        print(f"[{idx}/{total}] {c['id']}")
        # text
        with open(os.path.join(TEXT_DIR, f"{c['id']}.md"), 'w', encoding='utf-8') as f:
            f.write(f"用例 ID:   {c['id']}\n")
            f.write(f"维度标签:   {c['dimensions']}\n")
            f.write(f"维度:      稳定性\n")
            f.write(f"优先级:    {c['priority']}\n")
            f.write(f"溯源意图:  {c['intent_ref']}\n")
            f.write(f"母意图:    —\n")
            f.write(f"标题:      {c['title']}\n\n")
            f.write("前置条件:\n")
            for p in c['preconditions']:
                f.write(f"  - {p}\n")
            f.write("\n操作步骤:\n")
            for i, s in enumerate(c['steps'], 1):
                f.write(f"  {i}. {s}\n")
            f.write("\n预期结果:\n")
            for e in c['expected']:
                f.write(f"  - {e}\n")
            f.write("\n验证点:\n")
            for v in c['verification']:
                f.write(f"  - {v}\n")
            f.write(f"\n清理:      {c['teardown_desc']}\n")
        # yaml
        with open(os.path.join(YAML_DIR, f"{c['id']}.yaml"), 'w', encoding='utf-8') as f:
            f.write(f"id: {c['id']}\n")
            f.write(f"dimensions: {c['dimensions']}\n")
            f.write(f"dimension: reliability\n")
            f.write(f"priority: {c['priority']}\n")
            f.write(f'title: "{c["title"]}"\n')
            f.write(f"intent_ref: {c['intent_ref']}\n")
            f.write("setup:\n")
            f.write(f"  repo_fixture: {c['repo_fixture']}\n")
            seclist = str(c['secrets']).replace("'", '"')
            f.write(f"  secrets: {seclist}\n")
            f.write("  variables: {}\n")
            f.write("  branch_protection: default\n")
            if c['workflow']:
                f.write("workflow: |\n")
                for line in c['workflow'].rstrip('\n').split('\n'):
                    f.write(f"  {line}\n")
            else:
                f.write("workflow: null\n")
            f.write("trigger:\n")
            f.write(f"  event: {c['trigger_event']}\n")
            f.write(f"  as: {c['trigger_as']}\n")
            f.write("  params: {}\n")
            if c['fault_injection']:
                fi = c['fault_injection']
                f.write("fault_injection:\n")
                f.write(f"  at: {fi['at']}\n")
                f.write(f"  action: {fi['action']}\n")
                f.write("  params:\n")
                for k, v in fi.get('params', {}).items():
                    f.write(f"    {k}: {v}\n")
                f.write(f"  recovery_expectation: {fi['recovery_expectation']}\n")
            else:
                f.write("fault_injection: null\n")
            f.write("assertions:\n")
            for a in c['assertions']:
                f.write(f"  - type: {a['type']}\n")
                f.write(f"    target: {a['target']}\n")
                for k, v in a.items():
                    if k not in ('type', 'target'):
                        if isinstance(v, str):
                            f.write(f'    {k}: "{v}"\n')
                        else:
                            f.write(f"    {k}: {v}\n")
            f.write("teardown:\n")
            f.write(f"  reset: {c['teardown']}\n")

if __name__ == "__main__":
    gen()
    print(f"Done. Generated {len(CASES)} cases.")

