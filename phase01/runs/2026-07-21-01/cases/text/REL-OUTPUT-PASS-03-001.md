用例 ID:   REL-OUTPUT-PASS-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-050
标题:      ATOMGIT_OUTPUT 写入正常且下游 job 可正确读取——历史 #87/#94 回归

前置条件:
  - job-A 写入 outputs，job-B 通过 needs 读取

操作步骤:
  1. job-A step 写入 echo "key=value123" >> $ATOMGIT_OUTPUT
  2. job-A outputs 映射 key: ${{ steps.gen.outputs.key }}
  3. job-B needs: job-A 后读取 ${{ needs.job-A.outputs.key }}

预期结果:
  - 下游 job echo 输出 value123
  - value 在日志中可见

验证点:
  - [正向] needs.job-A.outputs.key = value123
  - [正向] value 在日志中可见
  - [负向] 不出现 outputs 为空

清理:      none
