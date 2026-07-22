用例 ID:   REL-PREEMPT-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-039
标题:      preemption 抢占触发条件——事件匹配范围与作用域边界

前置条件:
  - 仓库配置了 concurrency preemption，参数为 enable=true、max=1、events=[mr_id]
  - 存在可用于触发同一/不同 MR 的 fixture

操作步骤:
  1. 触发运行 A（同一 workflow、同一 MR ID），使其进入 running 状态约 30s
  2. 在同一 workflow、同一 MR ID 上再次 push 触发运行 B
  3. 分别构造并触发以下对比场景：
     (a) 同一 workflow + 同一 MR ID 再次 push — 应抢占 A
     (b) 同一 workflow + 不同 MR ID 触发 — 不应抢占 A
     (c) 不同 workflow（同仓库）+ 同一 MR ID — 观测是否抢占
     (d) 同一 workflow + 同一 MR ID 但由不同用户触发 — 观测是否抢占
  4. 记录各场景下 A 的终态与 B 的调度结果

预期结果:
  - 同一 workflow 且同一 MR ID 的新运行触发时，旧运行 A 被抢占取消
  - 不同 MR ID、不同 workflow 或不同用户触发的运行不应跨边界误杀 A
  - 被抢占运行有明确事件记录或标记

验证点:
  - [正向] 场景 (a) 中 A 被抢占，终态为 cancelled
  - [负向] 场景 (b) 中 A 不应被抢占，应继续运行或正常完成
  - [负向] 场景 (c)(d) 中 A 不应被跨边界抢占；若行为与预期不一致，需记录为调度缺陷
  - [非功能] 被抢占运行有明确「被抢占」标记或事件记录，用户可理解取消原因

清理:      fixture
