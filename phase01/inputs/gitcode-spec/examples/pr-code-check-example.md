<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/examples/pr-code-check-example | fetched: 2026-07-20 -->

# PR 代码检查示例

Pull Request 代码检查工作流，包含代码风格、安全扫描、PR 评论和审查辅助。

```yaml
name: PR 代码检查
on:
  pull_request:
    types:
      - open
      - update
      - reopen

concurrency:
  max: 1
  exceed-action: QUEUE

permissions:
  repository: read
  pr: write
  issue: write

jobs:
  code-style:
    name: 代码风格检查
    runs-on: {ubuntu-24,x64,slim}
    if: ${{ atomgit.event_name == 'pull_request' }}
    steps:
      - name: 检出 PR 代码
        uses: checkout
        with:
          ref: ${{ atomgit.event.pull_request.head.sha }}
          fetch-depth: 0
      - name: 获取变更文件列表
        id: changed-files
        run: |
          files=$(git diff --name-only ${{ atomgit.event.pull_request.base.sha }} ${{ atomgit.event.pull_request.head.sha }})
          echo "files=$files" >> $ATOMGIT_OUTPUT
          echo "## 变更文件" >> $ATOMGIT_STEP_SUMMARY
          for f in $files; do
            echo "- $f" >> $ATOMGIT_STEP_SUMMARY
          done
      - name: 设置 Node.js
        uses: setup-node
        with:
          node-version: '20'
          cache: 'npm'
      - name: 安装依赖
        run: npm ci
      - name: ESLint 检查（仅变更文件）
        run: |
          npx eslint ${{ steps.changed-files.outputs.files }} --format compact || true
      - name: Prettier 格式检查
        run: |
          npx prettier --check ${{ steps.changed-files.outputs.files }} || true

  security-scan:
    name: 安全扫描
    runs-on: {ubuntu-24,x64,slim}
    if: ${{ atomgit.event_name == 'pull_request' }}
    steps:
      - name: 检出 PR 代码
        uses: checkout
        with:
          ref: ${{ atomgit.event.pull_request.head.sha }}
      - name: 设置 Node.js
        uses: setup-node
        with:
          node-version: '20'
      - name: 依赖安全审计
        run: npm audit --audit-level=high || true
      - name: License 检查
        run: npx license-checker --summary || true
      - name: 安全扫描摘要
        if: ${{ always }}
        run: |
          echo "## 安全扫描结果" >> $ATOMGIT_STEP_SUMMARY
          echo "扫描完成于 PR #${{ atomgit.event.pull_request.number }}" >> $ATOMGIT_STEP_SUMMARY

  pr-size-check:
    name: PR 规模检查
    runs-on: {ubuntu-24,x64,slim}
    if: ${{ atomgit.event_name == 'pull_request' }}
    steps:
      - name: 检出 PR 代码
        uses: checkout
        with:
          ref: ${{ atomgit.event.pull_request.head.sha }}
          fetch-depth: 0
      - name: 计算变更规模
        id: size
        run: |
          additions=$(git diff --numstat ${{ atomgit.event.pull_request.base.sha }} ${{ atomgit.event.pull_request.head.sha }} | awk '{sum+=$1} END {print sum}')
          deletions=$(git diff --numstat ${{ atomgit.event.pull_request.base.sha }} ${{ atomgit.event.pull_request.head.sha }} | awk '{sum+=$2} END {print sum}')
          total=$((additions + deletions))
          echo "additions=$additions" >> $ATOMGIT_OUTPUT
          echo "deletions=$deletions" >> $ATOMGIT_OUTPUT
          echo "total=$total" >> $ATOMGIT_OUTPUT

          if [ $total -lt 100 ]; then
            echo "size_label=small" >> $ATOMGIT_OUTPUT
          elif [ $total -lt 500 ]; then
            echo "size_label=medium" >> $ATOMGIT_OUTPUT
          else
            echo "size_label=large" >> $ATOMGIT_OUTPUT
          fi
      - name: PR 规模摘要
        run: |
          echo "## PR 规模统计" >> $ATOMGIT_STEP_SUMMARY
          echo "| 指标 | 值 |" >> $ATOMGIT_STEP_SUMMARY
          echo "|------|----|" >> $ATOMGIT_STEP_SUMMARY
          echo "| 新增行数 | ${{ steps.size.outputs.additions }} |" >> $ATOMGIT_STEP_SUMMARY
          echo "| 删除行数 | ${{ steps.size.outputs.deletions }} |" >> $ATOMGIT_STEP_SUMMARY
          echo "| 总变更行 | ${{ steps.size.outputs.total }} |" >> $ATOMGIT_STEP_SUMMARY
          echo "| 规模标签 | ${{ steps.size.outputs.size_label }} |" >> $ATOMGIT_STEP_SUMMARY
      - name: 添加规模标签
        if: ${{ steps.size.outputs.size_label == 'large' }}
        env:
          ATOMGIT_TOKEN: ${{ atomgit.token }}
        run: |
          curl -X POST \
            "${{ atomgit.api_url }}/repos/${{ atomgit.repository }}/issues/${{ atomgit.event.pull_request.number }}/labels" \
            -H "Authorization: token $ATOMGIT_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{"labels": ["size/large"]}'
```
