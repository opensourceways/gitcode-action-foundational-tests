用例 ID:   USE-SEARCH-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-018
参照来源:  inputs/gitcode-spec/running-pipelines/view-job-logs.md; inputs/gitcode-spec/running-pipelines/view-run-results.md
母意图:    —
标题:      日志搜索与下载功能可用且交互流畅

前置条件:
  - workflow 已产生日志
  - 日志面板可访问

操作步骤:
  1. 在日志面板输入关键词搜索
  2. 点击下载日志按钮

预期结果:
  匹配行高亮显示，下载文件为 UTF-8 纯文本，大文件不崩溃

验证点:
  - [正向] 搜索后匹配行被高亮
  - [正向] 下载的日志文件为 UTF-8 文本
  - [非功能] 搜索响应时间小于 2 秒

清理:      无

