用例 ID:   REL-ART-01-041
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-041
母意图:    —
标题:      超大 artifact——100 MB artifact 上传后下游 job 应成功下载

前置条件:
  - 仓库具备 artifact 使用权限

操作步骤:
  1. 触发含 upload-artifact(100MB) 和 download-artifact 的 workflow

预期结果:
  - upload 成功
  - download 成功
  - 下载后文件 MD5 与上传前一致

验证点:
  - [正向] upload 成功
  - [正向] download 成功
  - [正向] MD5 校验通过

清理:      重置 fixture 仓库
