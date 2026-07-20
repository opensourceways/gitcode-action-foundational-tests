<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/examples/java-gradle-ci | fetched: 2026-07-20 -->

# Java Gradle 项目 CI

完整的 Java Gradle 项目持续集成工作流，包含多 JDK 版本矩阵、Gradle 缓存、构建和测试。

```yaml
name: Java Gradle CI
on:
  push:
    branches:
      - main
      - 'feature/**'
    paths:
      - 'src/**'
      - 'build.gradle'
      - 'settings.gradle'
      - 'gradle/**'
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
        java-version: [11, 17, 21]
      fail-fast: false
      max-parallel: 3
    steps:
      - name: 检出代码
        uses: checkout
      - name: 设置 JDK ${{ matrix.java-version }}
        uses: setup-java
        with:
          java-version: ${{ matrix.java-version }}
          distribution: 'temurin'
      - name: 缓存 Gradle 包
        uses: cache
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: gradle-${{ runner.os }}-${{ matrix.java-version }}-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            gradle-${{ runner.os }}-${{ matrix.java-version }}-
      - name: Gradle 编译
        run: ./gradlew compileJava --no-daemon
      - name: Gradle 单元测试
        run: ./gradlew test --no-daemon
      - name: Gradle 集成测试
        run: ./gradlew integrationTest --no-daemon
      - name: Gradle 代码质量检查
        run: ./gradlew checkstyleMain spotbugsMain --no-daemon
      - name: 测试报告摘要
        if: ${{ always }}
        run: |
          echo "## Gradle 测试结果 - JDK ${{ matrix.java-version }}" >> $ATOMGIT_STEP_SUMMARY
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
      - name: 缓存 Gradle 包
        uses: cache
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: gradle-${{ runner.os }}-17-${{ hashFiles('**/*.gradle*') }}
      - name: Gradle 打包
        run: ./gradlew bootJar --no-daemon
      - name: 上传构件
        uses: upload-artifact
        with:
          name: gradle-artifacts
          path: build/libs/*.jar
          retention-days: 30
```
