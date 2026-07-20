<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/examples/python-ci | fetched: 2026-07-20 -->

# Python 项目 CI

完整的 Python 项目持续集成工作流，包含多版本矩阵、pip 缓存、lint、测试和覆盖率。

```yaml
name: Python CI
on:
  push:
    branches:
      - main
      - 'feature/**'
    paths:
      - 'src/**'
      - 'tests/**'
      - 'pyproject.toml'
      - 'setup.py'
      - 'requirements*.txt'
  pull_request:
    branches:
      - main

concurrency:
  max: 1
  exceed-action: QUEUE

permissions:
  repository: read

jobs:
  lint:
    name: 代码质量检查
    runs-on: {ubuntu-24,x64,slim}
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 Python
        uses: setup-python
        with:
          python-version: '3.12'
          cache: 'pip'
      - name: 安装 lint 工具
        run: pip install flake8 black isort mypy
      - name: Flake8 检查
        run: flake8 src/ --max-line-length=120 --statistics
      - name: Black 格式检查
        run: black --check --diff src/
      - name: isort 导入排序检查
        run: isort --check-only --diff src/
      - name: mypy 类型检查
        run: mypy src/ --ignore-missing-imports

  test:
    name: Python ${{ matrix.python-version }} 测试
    runs-on: {ubuntu-24,x64,small}
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
      fail-fast: false
      max-parallel: 3
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 Python ${{ matrix.python-version }}
        uses: setup-python
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - name: 安装依赖
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: 单元测试 + 覆盖率
        run: |
          pytest tests/ \
            --cov=src \
            --cov-report=term-missing \
            --cov-report=xml:coverage.xml \
            --junitxml=test-results.xml \
            -v
      - name: 测试结果摘要
        if: ${{ always }}
        run: |
          echo "## Python 测试结果 - Python ${{ matrix.python-version }}" >> $ATOMGIT_STEP_SUMMARY
          echo "状态: ${{ job.status }}" >> $ATOMGIT_STEP_SUMMARY
      - name: 上传覆盖率报告
        if: ${{ always }}
        uses: upload-artifact
        with:
          name: coverage-py${{ matrix.python-version }}
          path: |
            coverage.xml
            test-results.xml
          retention-days: 7

  build:
    name: 构建打包
    needs: [lint, test]
    runs-on: {ubuntu-24,x64,small}
    if: ${{ atomgit.ref == 'refs/heads/main' }}
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 Python
        uses: setup-python
        with:
          python-version: '3.12'
      - name: 安装构建工具
        run: pip install build twine
      - name: 构建 Python 包
        run: python -m build
      - name: 上传构件
        uses: upload-artifact
        with:
          name: python-package
          path: dist/
          retention-days: 7
```
