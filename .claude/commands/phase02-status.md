# /phase02-status — 查看执行进度（可中途查看）

## 用途
查看某个 Phase 02 run 的当前进度快照。**可在 `/phase02-exec` 执行过程中随时运行**——因为 `run_batch.py` 每跑完一条就增量更新 `state.json`，本命令只读该状态，不阻塞、不干扰正在进行的执行。

## 如何中途查看
`/phase02-exec` 是一次较长的批量真跑。想看进度时，**另开一个终端/会话**输入 `/phase02-status <run-id>` 即可看到「已完成 n/m、当前正在跑哪条、暂态判定分布」。状态随执行实时推进。

## 确定性内核
`phase02/scripts/status.py`（只读 `state.json` + `summary.json` + `queue.json`）。

## 参数
- `<phase02-run-id>`：要查看的批次 id（必需）

## 执行步骤
```
python phase02/scripts/status.py <phase02-run-id>
```
展示：
- 状态（ready / running / completed）
- 进度条 `done/total` + 百分比
- 当前正在执行的用例（running 时）
- 暂态判定累计（PASS/FAIL/NOT_CONFIGURED/…）
- 最近几条结果

## 输出
- 终端进度快照（不写文件）

## 示例
```
/phase02-status 2026-07-21-10      # 查看进度（执行中或完成后均可）
```
