<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/examples/nodejs-ci | fetched: 2026-07-20 -->

# Node.js 项目 CI

完整的 Node.js 项目持续集成工作流，包含安装、构建、测试、缓存和多版本矩阵。

```yaml
name: Node.js CI
on:
  push:
    branches:
      - main
      - 'feature/**'
  pull_request:
    branches:
      - main

concurrency:
  max: 1
  exceed-action: QUEUE

permissions:
  repository: read

env:
  NODE_VERSION_DEFAULT: '20'

jobs:
  test:
    name: Node.js ${{ matrix.node-version }} 测试
    runs-on: {ubuntu-24,x64,small}
    strategy:
      matrix:
        node-version: [18, 20, 22]
      fail-fast: false
      max-parallel: 3
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 Node.js ${{ matrix.node-version }}
        uses: setup-node
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - name: 安装依赖
        run: npm ci
      - name: 代码风格检查
        run: npm run lint
      - name: 构建
        run: npm run build
      - name: 单元测试
        run: npm test
      - name: 集成测试
        run: npm run test:integration
      - name: 测试覆盖率报告
        if: ${{ always }}
        run: |
          echo "## 覆盖率报告 - Node.js ${{ matrix.node-version }}" >> $ATOMGIT_STEP_SUMMARY
          echo "| 指标 | 值 |" >> $ATOMGIT_STEP_SUMMARY
          echo "|------|----|" >> $ATOMGIT_STEP_SUMMARY
          npm run coverage:report >> $ATOMGIT_STEP_SUMMARY

  build-and-package:
    name: 构建与打包
    needs: test
    runs-on: {ubuntu-24,x64,medium}
    if: ${{ atomgit.ref == 'refs/heads/main' && success }}
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 Node.js
        uses: setup-node
        with:
          node-version: ${{ env.NODE_VERSION_DEFAULT }}
          cache: 'npm'
      - name: 安装依赖
        run: npm ci
      - name: 构建生产包
        run: npm run build:prod
      - name: 上传构件
        uses: upload-artifact
        with:
          name: dist-package
          path: dist/
          retention-days: 7
```
