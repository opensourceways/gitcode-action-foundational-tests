<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/examples/java-maven-ci | fetched: 2026-07-20 -->

# Java Maven 项目 CI

完整的 Java Maven 项目持续集成工作流，包含多 JDK 版本矩阵、构建、测试和打包。

```yaml
name: Java Maven CI
on:
  push:
    branches:
      - main
      - 'release/**'
    paths:
      - 'src/**'
      - 'pom.xml'
  pull_request:
    branches:
      - main

concurrency:
  max: 1
  exceed-action: QUEUE

permissions:
  repository: read

jobs:
  build:
    name: JDK ${{ matrix.java-version }} 构建
    runs-on: {ubuntu-24,x64,small}
    strategy:
      matrix:
        java-version: [8, 11, 17, 21]
      fail-fast: false
      max-parallel: 4
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 JDK ${{ matrix.java-version }}
        uses: setup-java
        with:
          java-version: ${{ matrix.java-version }}
          distribution: 'temurin'
          cache: 'maven'
      - name: Maven 编译
        run: mvn compile -B --no-transfer-progress
      - name: Maven 单元测试
        run: mvn test -B --no-transfer-progress
      - name: Maven 集成测试
        run: mvn verify -B --no-transfer-progress -DskipUnitTests
      - name: 测试结果摘要
        if: ${{ always }}
        run: |
          echo "## Maven 测试结果 - JDK ${{ matrix.java-version }}" >> $ATOMGIT_STEP_SUMMARY
          echo "构建状态: ${{ job.status }}" >> $ATOMGIT_STEP_SUMMARY

  package:
    name: 打包发布
    needs: build
    runs-on: {ubuntu-24,x64,small}
    if: ${{ startsWith(atomgit.ref, 'refs/tags/') }}
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 JDK 17
        uses: setup-java
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: 'maven'
      - name: Maven 打包（跳过测试）
        run: mvn package -B -DskipTests --no-transfer-progress
      - name: 上传 JAR 构件
        uses: upload-artifact
        with:
          name: maven-artifacts
          path: target/*.jar
          retention-days: 30
```
