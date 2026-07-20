<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/examples/go-ci | fetched: 2026-07-20 -->

# Go 项目 CI

完整的 Go 项目持续集成工作流，包含多版本矩阵、构建、测试、vet 和覆盖率。

```yaml
name: Go CI
on:
  push:
    branches:
      - main
      - 'feature/**'
    paths:
      - '**.go'
      - 'go.mod'
      - 'go.sum'
  pull_request:
    branches:
      - main

concurrency:
  max: 1
  exceed-action: QUEUE

permissions:
  repository: read

jobs:
  test:
    name: Go ${{ matrix.go-version }} 测试
    runs-on: {ubuntu-24,x64,small}
    strategy:
      matrix:
        go-version: ['1.21', '1.22', '1.23']
      fail-fast: false
      max-parallel: 3
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 Go ${{ matrix.go-version }}
        uses: setup-go
        with:
          go-version: ${{ matrix.go-version }}
          cache: true
      - name: Go Vet 代码检查
        run: go vet ./...
      - name: Go fmt 格式检查
        run: |
          output=$(gofmt -l .)
          if [ -n "$output" ]; then
            echo "以下文件格式不正确:"
            echo "$output"
            exit 1
          fi
      - name: 下载依赖
        run: go mod download
      - name: 依赖完整性检查
        run: go mod verify
      - name: Go 单元测试
        run: go test -v -race -count=1 ./...
      - name: Go 测试覆盖率
        run: |
          go test -race -coverprofile=coverage.out -covermode=atomic ./...
          go tool cover -func=coverage.out
      - name: 覆盖率摘要
        if: ${{ always }}
        run: |
          echo "## Go 测试覆盖率 - Go ${{ matrix.go-version }}" >> $ATOMGIT_STEP_SUMMARY
          go tool cover -func=coverage.out >> $ATOMGIT_STEP_SUMMARY

  build:
    name: Go 构建
    needs: test
    runs-on: {ubuntu-24,x64,small}
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 Go
        uses: setup-go
        with:
          go-version: '1.23'
          cache: true
      - name: 构建二进制
        run: go build -v -o bin/app ./cmd/app
      - name: 上传构件
        uses: upload-artifact
        with:
          name: go-binary
          path: bin/
          retention-days: 7
```
