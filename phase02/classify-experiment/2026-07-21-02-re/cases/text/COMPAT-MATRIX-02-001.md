用例 ID:   COMPAT-MATRIX-02-001
维度标签:   [compatibility, completeness]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-065
标题:      matrix include/exclude 展开语义与动态 runs-on 兼容性——追加变量、排除组合、新组合创建是否与 GitHub 一致

前置条件:
  - 工作流中定义了基础矩阵 + include（含新变量/新组合）+ exclude + 动态 runs-on
  - 平台存在与动态 runs-on 求值结果对应的 Runner 标签

操作步骤:
  1. 触发含基础矩阵 + include + exclude + 动态 runs-on 的工作流
  2. 观测生成的 job 实例数、各实例变量集与调度结果
  3. 检查 include 追加的新组合是否被正确生成且变量注入正确
  4. 检查 exclude 是否精确排除目标组合而不误排
  5. 验证动态 runs-on 引用 matrix 变量后是否正确调度到预期 Runner

预期结果:
  - include/exclude 展开结果（生成多少 job 实例、各实例变量集）与 GitHub 一致
  - 动态 runs-on 引用 matrix 变量后能正确映射到 GitCode runner 标签体系，或至少给出明确报错
  - include 不因「新组合不含基础变量」而被静默忽略

验证点:
  - [正向] 基础矩阵 2×2=4 实例，include 追加 1 个新组合后共 5 实例，且新变量正确注入
  - [正向] exclude 精确排除 1 个组合后剩余 3 实例，非目标组合不被误排除
  - [正向] 动态 runs-on 正确调度到预期 runner
  - [负向] include 不应因新组合不含基础变量而被静默忽略导致实例丢失
  - [负向] exclude 不应因子集匹配而过度排除未声明的组合
  - [负向] 动态 runs-on 解析失败时不应静默挂起无报错

清理:      fixture
