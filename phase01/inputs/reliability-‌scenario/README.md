# 第一部分：性能测试场景

---

## 场景 PERF-001：Runner 规格真实性验证

**目标**：验证官方资源池 Runner 实际分配的 CPU / 内存 / 磁盘与文档规格一致。

**关联 Gap**：1.1 平台容量边界 / 1.2 缺乏定量基准

### 前置条件
- 测试仓库 `ComputingActionTest/bingo` 已配置可写入权限。
- 目标规格至少包含：`small` (2核8G50GB)、`medium` (4核16G100GB)、`large` (8核32G200GB)。
- 平台提供 `nproc`、`free -h`、`df -h` 或等效命令可用。

### 测试步骤
1. 为每个目标规格分别创建一条 workflow，runs-on 指定该规格。
2. 在 workflow 的 step 中运行系统信息探测命令，并将结果写入 `ATOMGIT_OUTPUT` 或文件。
3. 触发 workflow（`push` 或 `workflow_dispatch`）。
4. 通过 API 获取 run 状态，确认 `conclusion == success`。
5. 下载 job 日志，解析 CPU 核数、内存大小、磁盘可用空间。

### YAML 模板
```yaml
name: PERF-001-runner-spec-{flavor}
on: [workflow_dispatch]
jobs:
  probe:
    runs-on: [ubuntu-latest, x64, {flavor}]
    steps:
      - name: Probe CPU
        run: echo "cpu=$(nproc)" >> "$ATOMGIT_OUTPUT"
      - name: Probe Memory
        run: echo "mem=$(free -m | awk '/Mem:/{print $2}')" >> "$ATOMGIT_OUTPUT"
      - name: Probe Disk
        run: echo "disk=$(df -m / | awk 'NR==2{print $4}')" >> "$ATOMGIT_OUTPUT"
```

### API 观测
- `GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}` → 确认 `status == COMPLETED` 且 `conclusion == success`。
- `GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}/jobs` → 获取 job 日志下载链接。
- `GET .../download-log` → 解析日志中的 `cpu=` / `mem=` / `disk=` 值。

### 断言标准
| 规格 | CPU | 内存 | 磁盘 |
|------|-----|------|------|
| small | == 2 | >= 7800 MB | >= 49000 MB |
| medium | == 4 | >= 15800 MB | >= 99000 MB |
| large | == 8 | >= 31800 MB | >= 199000 MB |

> 允许 ±2% 的误差（容器化环境内存/磁盘可能略小于标称值）。

### 失败判定
- 实际值偏离标称值超过 10% → **FAIL**（平台规格欺诈）。
- 任务未成功完成 → **FAIL**（环境不可用）。

---

## 场景 PERF-002：调度延迟基准

**目标**：测量从 workflow 触发到首个 step 开始执行的等待时间，建立 P50/P95 基准。

**关联 Gap**：1.2 缺乏定量 SLA / 1.3 缺少端到端性能验证

### 前置条件
- 测试仓库空闲（无排队中的 run）。
- 使用 `small` 规格（最常用规格，避免大规格资源稀缺干扰）。

### 测试步骤
1. 创建极简 workflow（仅一个 `echo` step），命名为 `PERF-002-scheduling-latency`。
2. 通过 `workflow_dispatch` 连续触发 **10 次**（每次触发记录客户端时间戳 `T0`）。
3. 每次触发后，轮询 API 获取 run 详情，记录 `start_time`（平台记录的 run 开始时间）与首个 job 的 `start_time`（job 开始时间）。
4. 计算：`调度延迟 = job.start_time - run.start_time`（秒）。
5. 汇总 10 次延迟，计算 P50、P95、最大值。

### YAML 模板
```yaml
name: PERF-002-scheduling-latency
on: [workflow_dispatch]
jobs:
  latency:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "hello"
```

### API 观测
- `POST`（UI 或 API 触发）workflow_dispatch，记录 `T0`。
- `GET /api/v8/repos/{owner}/{repo}/actions/runs?workflow_name=PERF-002-scheduling-latency&per_page=10` → 获取最近 10 条 run。
- 对每条 run：`GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}` → 取 `start_time`。
- `GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}/jobs` → 取首个 job 的 `start_time`。

### 断言标准（初版基线，后续可收紧）
- P50 调度延迟 <= 60 秒
- P95 调度延迟 <= 120 秒
- 单次最大延迟 <= 300 秒（5分钟）

### 失败判定
- P95 > 300 秒 → **FAIL**（调度延迟不可接受）。
- 存在 run 的 `status` 长期为 `RUNNING` 但 job 从未开始 → **FAIL**（调度死锁）。

---

## 场景 PERF-003：日志加载性能

**目标**：验证大日志（50MB / 200MB）在 UI/API 上的加载时间是否超过可接受阈值。

**关联 Gap**：1.2 日志加载 7min 痛点 / 2.2 日志系统稳定性

### 前置条件
- 测试仓库可正常触发 workflow。
- 客户端具备计时能力（harness 脚本层）。

### 测试步骤
1. 创建生成指定大小日志的 workflow（通过 `yes` 或 `base64 /dev/urandom` 生成文本）。
2. 触发 workflow，等待完成。
3. 通过 API 下载 job 日志，测量下载耗时。
4. 重复 3 次，取平均。

### YAML 模板（50MB 日志）
```yaml
name: PERF-003-log-50mb
on: [workflow_dispatch]
jobs:
  generate-log:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: |
          # 生成约 50MB 日志（约 524288 行 × 100 字节）
          for i in $(seq 1 524288); do
            echo "LOG_LINE_${i}_$(openssl rand -hex 40)"
          done
```

### API 观测
- `GET .../runs/{run_id}/jobs/{job_id}/download-log` → 记录 HTTP 请求耗时（从发送请求到收到完整响应体）。
- 验证响应体大小 ≈ 目标日志大小（允许 gzip 压缩后的差异）。

### 断言标准
| 日志大小 | 下载耗时上限 |
|---------|-------------|
| 50MB | <= 30 秒 |
| 200MB | <= 120 秒 |

### 失败判定
- 下载耗时超过上限 → **FAIL**（日志加载性能退化）。
- 响应体大小远小于预期（如 < 50%）→ **FAIL**（日志截断或丢失）。
- 下载返回 404 或 5xx → **FAIL**（日志 API 可用性）。

---

## 场景 PERF-004：镜像拉取性能

**目标**：测量默认 runner + 自定义 container 镜像时的环境准备耗时（主要为镜像拉取时间）。

**关联 Gap**：1.2 镜像拉取 pending 10min 痛点 / 2.1 自定义镜像稳定性

### 前置条件
- 使用公开可访问的 Docker 镜像（如 `node:20`、`python:3.12`、`maven:3.9-eclipse-temurin-21`）。
- 避免使用需要认证的私有镜像，排除 credentials 耗时干扰。

### 测试步骤
1. 创建 workflow，指定 `container.image` 为测试镜像。
2. 在首个 step 中输出 `docker images` 或简单 `echo`，用于标记镜像已就绪。
3. 触发 workflow，通过 API 获取 job 日志。
4. 解析日志中「环境准备」与「首个 step 开始」的时间差（若平台日志含时间戳则直接计算；否则通过 API 的 `start_time` 与 step 实际开始时间估算）。

### YAML 模板
```yaml
name: PERF-004-image-pull-node20
on: [workflow_dispatch]
jobs:
  pull-test:
    runs-on: [ubuntu-latest, x64, small]
    container:
      image: node:20
    steps:
      - run: echo "image_ready"
```

### API 观测
- `GET .../runs/{run_id}/jobs/{job_id}` → 获取 job 的 `start_time`（平台开始调度该 job 的时间）。
- `GET .../download-log` → 获取日志，搜索 `image_ready` 所在行的时间戳（若日志含时间戳）。
- 若日志无时间戳，则通过 harness 记录「触发时间」与「job 状态变为 RUNNING 后首次 API 返回成功」的时间差作为代理指标。

### 断言标准
- 镜像拉取 + 环境准备总耗时 <= 180 秒（3分钟）。
- 连续触发 5 次，失败次数 <= 1（允许偶发网络抖动）。

### 失败判定
- 单次环境准备 > 600 秒（10分钟）→ **FAIL**（与历史问题 #52 一致）。
- 连续 5 次中失败 >= 3 次 → **FAIL**（镜像拉取 flaky）。
- 日志中出现 `image pull failed` / `backoff` 等错误 → **FAIL**。

---

## 场景 PERF-005：制品传输性能

**目标**：测量大制品（100MB / 500MB / 1GB）上传与下载的耗时和成功率。

**关联 Gap**：1.3 大制品传输 / 1.4 制品性能盲区

### 前置条件
- 测试仓库可正常调用 `upload-artifact` / `download-artifact` 插件。
- 测试仓库磁盘足够生成大文件（在 `large` 规格 runner 上执行，避免 small 规格 50GB 磁盘不足）。

### 测试步骤
1. 创建 workflow，在 step 中生成指定大小的文件（`dd if=/dev/urandom of=artifact.bin bs=1M count=100`）。
2. 使用 `upload-artifact` 上传。
3. 在同一 workflow 的下游 job 中，使用 `download-artifact` 下载，并计算 MD5 校验和。
4. 通过 API 获取 artifact 详情，确认大小。

### YAML 模板（100MB）
```yaml
name: PERF-005-artifact-100mb
on: [workflow_dispatch]
jobs:
  upload:
    runs-on: [ubuntu-latest, x64, large]
    steps:
      - run: dd if=/dev/urandom of=artifact.bin bs=1M count=100
      - uses: upload-artifact
        with:
          name: artifact-100mb
          path: artifact.bin
  download:
    runs-on: [ubuntu-latest, x64, large]
    needs: upload
    steps:
      - uses: download-artifact
        with:
          name: artifact-100mb
      - run: md5sum artifact.bin
```

### API 观测
- `GET .../actions/runs/{run_id}/artifacts` → 列出 artifact，确认 `size_in_bytes` 正确。
- `GET .../actions/artifacts/{artifact_id}/zip` → 记录下载耗时。
- Harness 记录：上传 job 耗时（从 step 开始到上传完成）、下载 job 耗时。

### 断言标准
| 制品大小 | 上传耗时 | 下载耗时 | 完整性 |
|---------|---------|---------|--------|
| 100MB | <= 60s | <= 30s | MD5 一致 |
| 500MB | <= 180s | <= 60s | MD5 一致 |
| 1GB | <= 300s | <= 120s | MD5 一致 |

### 失败判定
- 耗时超过上限 → **FAIL**（制品传输性能退化）。
- MD5 不一致 → **FAIL**（制品传输损坏）。
- 上传/下载 step 失败 → **FAIL**。

---

## 场景 PERF-006：缓存加速比

**目标**：验证 `cache` 插件在命中时是否真正减少构建时间，并量化加速比。

**关联 Gap**：1.4 缓存性能盲区 / 1.3 端到端性能验证

### 前置条件
- 测试仓库可调用 `cache` 插件。
- 选择一种依赖安装场景（如 `npm ci` 或 `pip install -r requirements.txt`）。

### 测试步骤
1. **冷启动**：首次运行 workflow，缓存不存在，记录依赖安装耗时 `T_cold`。
2. **热启动**：再次运行同一 workflow，缓存应命中，记录依赖安装耗时 `T_hot`。
3. 计算加速比：`speedup = T_cold / T_hot`。

### YAML 模板（npm 示例）
```yaml
name: PERF-006-cache-speedup
on: [workflow_dispatch]
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - uses: checkout
      - uses: setup-node
        with:
          node-version: '20'
      - uses: cache
        with:
          path: ~/.npm
          key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
          restore-keys: |
            npm-${{ runner.os }}-
      - run: npm ci
      - run: echo "install_done"
```

> 注：需提前在仓库中提交一个包含大量依赖的 `package.json` + `package-lock.json`（或 `requirements.txt`），确保安装耗时 > 30 秒，否则测量误差过大。

### API 观测
- `GET .../download-log` → 解析 `npm ci` 步骤的耗时（若日志含 step 时间戳）。
- 若日志不含 step 级时间戳，则通过 job 总耗时作为代理指标（两次 job 耗时对比）。
- 验证日志中 cache 步骤是否输出 `Cache restored`（命中）或 `Cache not found`（未命中）。

### 断言标准
- 缓存命中时，`T_hot` < `T_cold` 的 50%（即加速比 >= 2x）。
- 缓存命中时，依赖安装耗时减少 >= 30 秒（绝对值，避免小基数噪声）。

### 失败判定
- `T_hot >= T_cold` → **FAIL**（缓存未生效或缓存恢复耗时异常）。
- 缓存步骤报错 → **FAIL**。

---

## 场景 PERF-007：并发压测

**目标**：在 `concurrency.max` 约束下，触发大量 workflow，观测平台队列深度与调度延迟。

**关联 Gap**：1.3 并发压测 / 1.1 全局并发上限未公开

### 前置条件
- 测试 workflow 设置 `concurrency: { enable: true, max: 5 }`。
- 测试仓库允许通过 API 或 UI 快速多次触发 `workflow_dispatch`。

### 测试步骤
1. 创建极简 workflow（仅 sleep 60 秒），配置 `concurrency.max=5`。
2. 在 10 秒内连续触发 **20 次** workflow_dispatch。
3. 通过 API 轮询，记录各 run 的 `status` 变化时间线。
4. 统计：同时处于 `RUNNING` 状态的 run 数峰值、队列中等待的 run 数、全部 20 次完成总耗时。

### YAML 模板
```yaml
name: PERF-007-concurrency-stress
concurrency:
  enable: true
  max: 5
on: [workflow_dispatch]
jobs:
  sleep:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: sleep 60
```

### API 观测
- `GET /api/v8/repos/{owner}/{repo}/actions/runs?status=RUNNING&per_page=100` → 周期性地（每 10 秒）查询，记录 RUNNING 数量。
- `GET /api/v8/repos/{owner}/{repo}/actions/runs?per_page=20` → 获取最近 20 条 run，按 `start_time` / `end_time` 计算各 run 的等待时间（`start_time - T0`）与运行时间。

### 断言标准
- 任意时刻 `RUNNING` 数量 <= 5（严格受 `concurrency.max` 约束）。
- 20 次全部完成总耗时 <= 300 秒（理论最小 240 秒 = 4 批 × 60 秒，允许 25% 调度开销）。
- 无 run 被静默丢弃（20 次触发均能在 API 中查询到）。

### 失败判定
- `RUNNING` 数量 > 5 → **FAIL**（并发控制失效）。
- 存在 run 触发后长期（> 600 秒）未开始且未报错 → **FAIL**（队列死锁）。
- 存在 run 触发后 API 中查询不到 → **FAIL**（任务被静默丢弃）。

---

## 场景 PERF-008：矩阵调度公平性

**目标**：矩阵生成 20 个实例，`max-parallel=4`，验证实际并行度是否等于 4，以及调度是否公平。

**关联 Gap**：1.3 矩阵并行度观测 / 1.1 矩阵组合上限

### 前置条件
- 测试仓库支持 matrix 构建。
- 选用 `small` 规格（避免大规格资源稀缺）。

### 测试步骤
1. 创建矩阵 workflow，20 个实例（如 `os: [ubuntu-latest]` × `idx: [1..20]`），`max-parallel: 4`。
2. 每个实例 sleep 30 秒，记录开始时间。
3. 触发 workflow，通过 API 轮询所有 job 状态。
4. 统计：同一时刻 RUNNING 的 job 数、各 job 的等待时间分布。

### YAML 模板
```yaml
name: PERF-008-matrix-fairness
on: [workflow_dispatch]
jobs:
  matrix-job:
    runs-on: [ubuntu-latest, x64, small]
    strategy:
      matrix:
        idx: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
      max-parallel: 4
    steps:
      - run: |
          echo "job_${{ matrix.idx }}_start=$(date +%s)" >> "$ATOMGIT_OUTPUT"
          sleep 30
```

### API 观测
- `GET .../runs/{run_id}/jobs` → 获取所有 20 个 job 的列表。
- 对每条 job 记录：`status` 变化时间线（通过轮询或日志解析）。
- 计算：每 5 秒时间窗口内 `RUNNING` 的 job 数量。

### 断言标准
- 任意时刻 RUNNING job 数 <= 4（严格受 `max-parallel` 约束）。
- 20 个 job 全部完成总耗时 <= 210 秒（理论最小 150 秒 = 5 批 × 30 秒，允许 40% 调度开销）。
- 各 job 的等待时间（从 run 触发到 job 开始）的 P90 <= 60 秒（公平性，避免个别 job 被饿死）。

### 失败判定
- RUNNING job 数 > 4 → **FAIL**（max-parallel 约束失效）。
- 存在 job 等待时间 > 300 秒 → **FAIL**（调度不公平或饿死）。
- 总耗时 > 300 秒 → **FAIL**（调度效率退化）。

---

# 第二部分：稳定性测试场景

---

## 场景 RELI-001：资源调度状态一致性

**目标**：验证资源池空闲时，job 不会进入无意义的长时间等待或失败。

**关联 Gap**：2.1 #7 / #12（空闲但排队、资源池已释放但 job 仍等待）

### 测试步骤
1. 确保测试仓库/组织下的 Runner 资源池处于空闲状态（无 RUNNING job）。
2. 创建简单 workflow（`runs-on: [ubuntu-latest, x64, small]`），触发 3 个并发实例。
3. 通过 API 持续监控（每 10 秒）：
   - 资源池状态（若 API 支持）或 `RUNNING` job 数量。
   - 各 job 的 `status` 与等待时间。
4. 持续 5 分钟，验证所有 job 在 120 秒内进入 RUNNING 并在 300 秒内完成。

### YAML 模板
```yaml
name: RELI-001-scheduling-consistency
on: [workflow_dispatch]
jobs:
  test-1:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "job1"
  test-2:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "job2"
  test-3:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "job3"
```

### 断言标准
- 3 个 job 均在触发后 120 秒内开始运行。
- 无 job 在资源池空闲时长期处于 `QUEUED` / `WAITING`（> 300 秒）。
- 无 job 因「资源不足」失败（资源池已确认空闲）。

### 失败判定
- 任意 job 触发后 > 300 秒仍未开始 → **FAIL**（调度死锁或状态不一致）。
- 资源池空闲但 job 报错「资源不足」→ **FAIL**（与 #12 一致）。

---

## 场景 RELI-002：Runner 状态机正确性

**目标**：验证 Runner 在空闲/运行/离线/异常状态间的转换符合预期。

**关联 Gap**：2.1 #78（无任务时 runner 显示运行中）

### 测试步骤
1. 在组织/项目 Runner 管理页面确认至少有一个在线的 `small` 规格 Runner。
2. 触发 workflow，观察该 Runner 状态是否变为「运行中」。
3. workflow 完成后，观察 Runner 状态是否恢复「在线/空闲」。
4. 连续触发 5 次 workflow，重复观察状态转换。
5. 若平台提供 Runner 状态 API，则通过 API 查询；否则记录 UI 观察结果（harness 中标注为「人工复核点」）。

### YAML 模板
```yaml
name: RELI-002-runner-state
on: [workflow_dispatch]
jobs:
  short-job:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: sleep 10
```

### 断言标准
- Workflow 运行期间，目标 Runner 状态 = 运行中。
- Workflow 完成后 60 秒内，目标 Runner 状态 = 在线/空闲。
- 连续 5 次，状态转换正确率 = 100%。

### 失败判定
- Workflow 完成后 Runner 仍显示运行中（> 5 分钟）→ **FAIL**（状态机卡死）。
- 第 6 次触发后 Runner 未进入运行中（但 workflow 仍成功）→ **注意**：可能是多 Runner 调度，需结合日志确认 Runner 名称；若明确调度到该 Runner 但未更新状态 → **FAIL**。

---

## 场景 RELI-003：日志系统稳定性

**目标**：长运行 workflow 生成大量日志，验证日志无乱序、无丢失、无概率性不显示。

**关联 Gap**：2.2 日志乱序/不显示/加载慢 / #14 #80 #81

### 测试步骤
1. 创建 workflow，运行 10 分钟，持续输出带严格递增序号的日志行（每 1 秒输出 100 行）。
2. 触发 workflow，等待完成。
3. 通过 API 下载完整日志。
4. 解析日志，验证：行号是否连续、时间戳是否单调递增、总行数是否符合预期。
5. 重复执行 5 次，统计「日志丢失率」、「乱序率」、「不显示率」。

### YAML 模板
```yaml
name: RELI-003-log-stability
on: [workflow_dispatch]
jobs:
  log-stream:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: |
          for i in $(seq 1 60000); do
            echo "LINE_${i}_$(date +%s%N)"
            # 每 100 行后 sleep 0.01s，控制速率约 100 行/秒，总 60000 行 ≈ 10 分钟
            if [ $((i % 100)) -eq 0 ]; then
              sleep 0.01
            fi
          done
```

> 预期总行数：60,000 行。日志大小约 6~10MB（取决于时间戳长度）。

### API 观测
- `GET .../download-log` → 获取完整日志文本。
- Harness 解析：
  - 搜索 `LINE_1_` 到 `LINE_60000_`，统计缺失行号。
  - 提取时间戳字段，验证是否严格递增。

### 断言标准
- 日志总行数 == 60,000（允许 ±1% 的丢失，即最多缺失 600 行）。
- 乱序率 == 0%（时间戳严格递增，或至少行号严格递增）。
- 5 次执行中，日志下载失败次数 == 0。

### 失败判定
- 丢失率 > 1% → **FAIL**（日志采集丢失）。
- 存在乱序行 → **FAIL**（日志时序一致性破坏）。
- 任意一次日志下载 404 / 5xx → **FAIL**（日志 API 不稳定）。
- 日志行存在但下载后解析为空 → **FAIL**（与 #81 一致）。

---

## 场景 RELI-004：Workflow 缓存失效

**目标**：修改 workflow YAML 后，验证后续运行立即使用新定义，无旧代码缓存。

**关联 Gap**：2.3 #85（yml 缓存未更新）

### 测试步骤
1. 创建初始 workflow `v1`，输出字符串 `"version_1"`。
2. 触发 workflow，确认日志输出 `"version_1"`。
3. 修改 workflow YAML，将输出改为 `"version_2"`，提交并 push。
4. 等待 5 秒后（确保平台同步），再次触发 workflow。
5. 下载日志，确认输出为 `"version_2"`。
6. 重复 3 次（v1 → v2 → v3 → v1），验证无旧版本残留。

### YAML 模板（v1）
```yaml
name: RELI-004-yaml-cache
on: [workflow_dispatch]
jobs:
  check:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "version_1"
```

### API 观测
- `GET .../download-log` → 搜索 `version_1` 或 `version_N`。
- `GET .../runs/{run_id}` → 确认 `file_path` 指向最新提交的 workflow 文件。

### 断言标准
- 每次触发后，日志输出必须与当前仓库 HEAD 的 workflow 内容一致。
- 修改后首次触发，输出正确版本的概率 = 100%（3 轮迭代共 6 次触发，全部正确）。

### 失败判定
- 修改 workflow 后，首次触发仍输出旧版本 → **FAIL**（yml 缓存未失效，与 #85 一致）。
- `file_path` 指向的 SHA 与最新提交不一致 → **FAIL**（workflow 版本绑定错误）。

---

## 场景 RELI-005：取消操作可靠性

**目标**：在 job 各阶段（初始化/运行/收尾）执行取消，验证状态正确过渡到 `canceled`。

**关联 Gap**：2.3 #39（取消成功但状态仍是队列中）

### 测试步骤
1. 创建 3 个 workflow：
   - **A**：job 初始阶段立即取消（触发后 5 秒内取消）。
   - **B**：job 运行阶段取消（sleep 300 秒，触发后 30 秒取消）。
   - **C**：job 包含 `post` 阶段（若平台支持），在运行完成后取消（验证 post 是否仍执行）。
2. 通过 API 或 UI 执行取消操作。
3. 轮询 API，记录状态变化时间线：RUNNING → CANCELED（或 FAILED / COMPLETED）。

### YAML 模板（B — 运行中取消）
```yaml
name: RELI-005-cancel-running
on: [workflow_dispatch]
jobs:
  long-job:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: sleep 300
```

### API 观测
- `POST`（或 UI）取消操作，记录取消时间 `T_cancel`。
- `GET .../runs/{run_id}` → 周期轮询，记录 `status` 变为 `CANCELED` 的时间。
- `GET .../runs/{run_id}/jobs` → 确认 job 状态同步为 `CANCELED`。

### 断言标准
- 取消操作后，run 和 job 状态在 60 秒内变为 `CANCELED`。
- 取消后，job 日志中不应出现 sleep 300 完成后的输出（即任务确实被中断）。
- 若平台支持 post 阶段，取消后 post 阶段的行为应可预期（文档声明为准）。

### 失败判定
- 取消后状态长期（> 300 秒）未变为 CANCELED → **FAIL**（取消操作失效）。
- 取消后状态为 FAILED 但无错误日志 → **FAIL**（状态机错误）。
- 取消后状态仍为 RUNNING / QUEUED → **FAIL**（与 #39 一致）。
- 取消后日志显示 job 仍在继续执行（> 30 秒）→ **FAIL**（取消信号未送达）。

---

## 场景 RELI-006：网络依赖容错

**目标**：模拟外部网络下载失败，验证 workflow 的重试/降级/报错行为稳定。

**关联 Gap**：2.5 #42 #15 #65（wget 概率失败、obs 上传失败、无外网）

### 测试步骤
1. 创建 workflow，step 中尝试访问一个**保证不可达**的地址（如 `http://10.255.255.1:12345/fake` 或一个已关闭的服务域名）。
2. 验证该 step 是否**明确失败**（exit code != 0），且错误信息清晰（如 `Connection timed out`、`Could not resolve host`）。
3. 创建第二个 workflow，step 中使用 `wget --timeout=5 --tries=1` 下载一个临时不可用的资源，验证失败后 workflow 是否按预期停止（或 `continue-on-error: true` 时继续）。

### YAML 模板（不可达地址）
```yaml
name: RELI-006-network-fail
on: [workflow_dispatch]
jobs:
  test:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - name: Access unreachable host
        run: |
          wget --timeout=5 --tries=1 http://10.255.255.1:12345/fake || true
          echo "after_fail"
      - name: Should not reach here if strict
        run: echo "step2"
```

> 注：若需测试「失败即停止」，去掉 `|| true`；若需测试「失败继续」，配置 `continue-on-error: true`。

### API 观测
- `GET .../download-log` → 验证错误信息是否包含 `timeout` / `failed` / `Connection` 等关键词。
- `GET .../runs/{run_id}` → 确认 `conclusion` 为 `failure`（或 `success` 若 continue-on-error）。

### 断言标准
- 网络请求失败时，step 的退出码非 0（若未配置 continue-on-error）。
- 日志中必须包含明确的网络错误信息（不允许静默失败或空错误）。
- 重复 10 次，失败信息一致率 = 100%（相同错误类型，无随机异常）。

### 失败判定
- 网络请求失败后 step 仍显示成功 → **FAIL**（错误掩盖）。
- 日志中无错误信息 → **FAIL**（与 #54 一致：静默失败）。
- 10 次中错误类型不一致（如有时 timeout、有时 404、有时 success）→ **FAIL**（flaky 行为）。

---

## 场景 RELI-007：制品并发写一致性

**目标**：多个 job 同时写入同一 artifact name，验证无数据损坏或静默覆盖。

**关联 Gap**：2.4 制品并发读写 / 1.4 制品性能盲区

### 测试步骤
1. 创建 workflow，包含 3 个并行 job（`job-a`, `job-b`, `job-c`），每个 job 生成不同的文件内容，但使用**相同的 artifact name** 上传。
2. 下游 job 下载该 artifact，检查内容是否可预期（平台应拒绝并发同名写入，或最后写入者生效，但**不应损坏**）。
3. 若平台支持，查询 artifact 元数据，确认上传者/时间戳。

### YAML 模板
```yaml
name: RELI-007-artifact-concurrent-write
on: [workflow_dispatch]
jobs:
  job-a:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "content_from_a" > result.txt
      - uses: upload-artifact
        with:
          name: shared-artifact
          path: result.txt
  job-b:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "content_from_b" > result.txt
      - uses: upload-artifact
        with:
          name: shared-artifact
          path: result.txt
  job-c:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "content_from_c" > result.txt
      - uses: upload-artifact
        with:
          name: shared-artifact
          path: result.txt
  check:
    runs-on: [ubuntu-latest, x64, small]
    needs: [job-a, job-b, job-c]
    steps:
      - uses: download-artifact
        with:
          name: shared-artifact
      - run: cat result.txt
```

### API 观测
- `GET .../actions/runs/{run_id}/artifacts` → 确认 artifact 数量与名称。
- `GET .../download-log` → 查看 `cat result.txt` 输出。
- 可选：下载 artifact zip，检查文件内容是否为 `content_from_a` / `b` / `c` 之一（平台允许覆盖，但不应损坏）。

### 断言标准
- 3 个 upload 步骤均不报错（或按文档声明的行为报错）。
- 若均成功，下游下载的内容必须是完整的 `content_from_a` 或 `b` 或 `c` 之一（不允许乱码、截断、空文件）。
- 若平台不支持并发同名写入，应有明确的冲突错误信息。

### 失败判定
- 下游下载的文件为空或损坏（乱码、截断）→ **FAIL**（并发写入数据损坏）。
- 3 个 upload 均成功但 artifact 元数据异常（如大小为 0 或负数）→ **FAIL**。
- 无错误信息但行为不符合预期 → **FAIL**（缺乏冲突提示）。

---

## 场景 RELI-008：子任务状态传播

**目标**：`workflow_call` 拉起子任务，验证父任务状态严格反映子任务真实状态，禁止「假阳性完成」。

**关联 Gap**：2.3 #30（workflow_call 无法拉起子任务，但显示已完成）

### 前置条件
- 平台支持 `workflow_call`（若不支持，本场景标注为 `NOT_APPLICABLE`）。
- 主仓库与子 workflow 仓库已配置可访问（或同一仓库内 `.gitcode/workflows/` 下存在子 workflow）。

### 测试步骤
1. 创建子 workflow `sub.yml`，包含一个必然失败的 step（如 `exit 1`）。
2. 创建主 workflow `main.yml`，通过 `workflow_call` 调用 `sub.yml`。
3. 触发主 workflow，观察父 run 的状态。
4. 创建第二个子 workflow `sub-success.yml`，包含必然成功的 step，验证正向传播。

### YAML 模板（主 workflow）
```yaml
name: RELI-008-parent-fail
on: [workflow_dispatch]
jobs:
  call-sub:
    uses: ./.gitcode/workflows/sub-fail.yml
```

### 子 workflow（sub-fail.yml）
```yaml
name: sub-fail
on: [workflow_call]
jobs:
  fail-job:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: exit 1
```

### API 观测
- `GET .../runs/{parent_run_id}` → 确认 `conclusion` = `failure`（子任务失败必须传播到父任务）。
- `GET .../runs/{parent_run_id}/jobs` → 确认 job 状态与子任务一致。
- 若平台支持查询子 run，则同时查询子 run 状态，确认父子状态一致。

### 断言标准
- 子 workflow 失败 → 父 workflow 必须失败（`conclusion == failure`）。
- 子 workflow 成功 → 父 workflow 必须成功。
- 父 workflow 的完成时间 >= 子 workflow 的完成时间（禁止子任务未完成时父任务已标记完成）。

### 失败判定
- 子任务失败但父任务成功 → **FAIL**（假阳性完成，与 #30 一致）。
- 子任务未完成但父任务已标记完成 → **FAIL**（状态传播延迟或缺失）。
- 父任务状态为 `completed` 但子任务状态为 `running` → **FAIL**。

---

## 场景 RELI-009：API 限流与一致性

**目标**：高频查询运行状态 API，验证无异常限流、返回数据前后一致。

**关联 Gap**：2.4 API 并发查询 / 1.3 并发下 API 响应时间

### 测试步骤
1. 触发一个长时间运行的 workflow（如 sleep 300 秒）。
2. 使用脚本以 **10 QPS** 的频率连续查询 `GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}`，持续 60 秒（共 600 次请求）。
3. 记录每次请求的：HTTP 状态码、响应时间、返回的 `status` 字段。
4. 验证：
   - 是否存在 429（Too Many Requests）或 503（Service Unavailable）。
   - 响应时间是否出现显著退化（P95 > 2 秒）。
   - 同一 run_id 的 `status` 是否出现逻辑不一致（如 RUNNING → COMPLETED → RUNNING）。

### 断言标准
- 600 次请求中，HTTP 200 占比 >= 99%（允许最多 6 次网络抖动）。
- 无 429 / 503（若存在，需确认是否为平台限流策略，并记录限流阈值）。
- P95 响应时间 <= 2 秒。
- `status` 变化符合状态机：QUEUED → RUNNING → COMPLETED / FAILED / CANCELED（无倒退）。

### 失败判定
- 429/503 次数 > 6 → **FAIL**（限流策略过于严格或 API 不稳定）。
- P95 响应时间 > 5 秒 → **FAIL**（API 性能退化）。
- 出现 status 倒退（如 RUNNING 后又变回 QUEUED）→ **FAIL**（数据一致性缺陷）。

---

## 场景 RELI-010：大规格资源调度稳定性

**目标**：在 `xlarge` / `2xlarge` 规格上反复触发编译任务，验证资源申请成功率与任务完成率。

**关联 Gap**：2.1 #96（2xlarge arm 任务申请资源错误）/ 1.1 大规格可用性

### 前置条件
- 测试仓库/组织已开通 `xlarge` 或 `2xlarge` 规格访问权限（文档声明需咨询客服）。
- 若未开通，本场景降级为 `large` 规格，并在结果中标注。

### 测试步骤
1. 创建资源密集型 workflow（如编译大型 C++ 项目或运行 `stress-ng`），指定 `runs-on: [ubuntu-latest, x64, xlarge]`。
2. 连续触发 10 次，每次间隔 30 秒。
3. 通过 API 监控每次触发的状态：
   - 是否成功申请到资源（job 是否开始运行）。
   - 是否成功完成（`conclusion == success`）。
   - 耗时是否稳定（无剧烈抖动）。

### YAML 模板
```yaml
name: RELI-010-large-spec-stability
on: [workflow_dispatch]
jobs:
  stress:
    runs-on: [ubuntu-latest, x64, xlarge]
    steps:
      - run: |
          sudo apt-get update && sudo apt-get install -y stress-ng
          stress-ng --cpu 8 --timeout 30s --metrics-brief
```

> 注：`xlarge` 为 16 核，但 `stress-ng --cpu 8` 即可验证资源可用；若实际分配不足，stress-ng 会报错或性能异常。

### API 观测
- `GET .../runs/{run_id}/jobs` → 确认 job 状态为 `RUNNING`（资源申请成功）。
- `GET .../runs/{run_id}` → 确认 `conclusion`。
- `GET .../download-log` → 查看 `stress-ng` 输出，确认 `bogo-ops-per-second` 无异常跌落。

### 断言标准
- 10 次触发中，资源申请成功率 >= 90%（即 <= 1 次因「资源不足」排队或失败）。
- 10 次触发中，任务完成成功率 >= 90%。
- stress-ng 的 `bogo-ops-per-second` 在 10 次执行中的变异系数（CV）<= 20%（资源稳定性）。

### 失败判定
- 资源申请成功率 < 80% → **FAIL**（大规格资源不稳定）。
- 任务完成成功率 < 80% → **FAIL**（大规格环境存在运行时缺陷）。
- 单次 stress-ng 输出显示 CPU 数量远低于 8 → **FAIL**（资源规格欺诈或调度错误）。
- 出现 `arm` 架构被错误调度到 `x64` 请求（或反之）→ **FAIL**（异构调度错误，与 #96 一致）。


