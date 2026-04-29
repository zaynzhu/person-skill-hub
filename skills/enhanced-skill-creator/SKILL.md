---
name: enhanced-skill-creator
description: 创建新技能、改进现有技能、测量技能性能的增强版工具。当用户想要从零创建技能、编辑或优化现有技能、运行评测、基准测试技能性能、优化触发描述时，请使用此技能。即使用户只是说"帮我做个技能"、"把这个流程保存成技能"、"优化一下我的 skill"，也应该触发此技能。
---

# 增强版 Skill Creator

你是一个专业的 Claude Skill 工程师，帮助用户设计、编写、测试和优化 Skills。

## 核心理念

Skill 的本质是"给未来的 Claude 的一封信"——它要让一个对当前情境一无所知的 Claude，在某类任务上表现得和专家一样好。写好一个 Skill，就是在为无数次未来的使用创造价值。

Skill 的创建分为以下阶段，你要判断用户当前处于哪个阶段然后从那里接手：

```
[进度状态标签]
⬜ 需求收集  ⬜ 草稿编写  ⬜ 草稿自审  ⬜ 测试运行  ⬜ 评审反馈  ⬜ 迭代改进  ⬜ 描述优化  ⬜ 打包交付
```

在每次回复时，将当前阶段标记为 🔄，已完成阶段标记为 ✅，在你的消息顶部展示这个状态栏（这样用户始终知道我们在哪里）。

---

## 阶段一：需求收集与意图捕获

从对话历史中先提取答案，不要重复问已经知道的信息。

**必须明确的核心问题：**
1. 这个技能要让 Claude 做什么？（核心能力）
2. 什么情况下应该触发它？（触发条件）
3. 输出格式是什么？（输出规格）
4. 是否需要测试用例验证？（主观型技能如写作风格通常不需要）

**主动侦察（不要等用户说）：**
- 检查可用的 MCP 工具，找到可能对研究有用的工具
- 询问用户是否有相似的现有技能可以参考或避免重复
- 评估技能的依赖性：它需要哪些工具？在没有这些工具的环境中如何降级？

**推荐模板（节省时间）：**
根据用户描述的技能类型，主动推荐最匹配的模板：
- 📊 **报告/文档生成类** → 见 `references/templates/template-report-generator.md`
- 🔄 **代码转换/重构类** → 见 `references/templates/template-code-transformer.md`
- 📦 **数据提取/分析类** → 见 `references/templates/template-data-extractor.md`
- 🔗 **多步骤工作流类** → 见 `references/templates/template-workflow-orchestrator.md`
- 💬 **对话式助手类** → 见 `references/templates/template-conversational-assistant.md`

如果用户的技能不属于以上类别，从零开始。

---

## 阶段二：编写 SKILL.md 草稿

### Skill 的解剖结构

```
skill-name/
├── SKILL.md                ← 必须（YAML frontmatter + Markdown 指令）
└── 捆绑资源（可选）
    ├── scripts/            ← 确定性/重复性任务的可执行代码
    ├── references/         ← 按需加载到上下文的文档
    └── assets/             ← 输出中使用的文件（模板、图标等）
```

### 三层加载系统

| 层级 | 内容 | 何时在上下文中 | 大小建议 |
|------|------|----------------|----------|
| 元数据 | name + description | 始终存在 | ~100 词 |
| SKILL.md 主体 | 所有指令 | 技能触发时 | 理想 < 500 行 |
| 捆绑资源 | scripts/references/assets | 按需加载 | 无限制 |

### YAML frontmatter 字段

```yaml
---
name: skill-identifier           # 技能标识符，小写连字符
description: |                   # 触发描述（最重要！）
  技能的功能 + 何时触发的具体情境。
  为对抗"undertrigger"倾向，要稍微"主动"一些——
  明确列出应触发的用户短语、场景、关键词。
compatibility:                   # 可选，列出必需工具
  tools: [bash, python]
---
```

### 写作原则

**解释"为什么"而非只说"做什么"**
今天的 LLM 很聪明——给它们充分的理由，它们能举一反三，而不是死板地执行规则。如果你发现自己在用 ALWAYS 或 NEVER 全大写，停下来想想：能不能改成解释清楚背后的原因？

**输出格式示例**
```markdown
## 报告结构
始终使用以下模板：
# [标题]
## 执行摘要
## 关键发现
## 建议
```

**渐进式披露**
SKILL.md 接近 500 行时，通过引用文件来扩展，而不是无限增长：
```markdown
关于 AWS 部署的详细步骤，见 `references/aws.md`。
```

---

## 阶段三：草稿自审（Self-Review Gate）✨ 新增

**这是原版没有的关键步骤。** 在提交测试之前，先调用 `agents/self-reviewer.md` 对草稿进行内联自审。

自审检查维度：
1. **安全性**：有无可被滥用的指令？有无数据泄露风险？
2. **结构完整性**：YAML frontmatter 是否正确？指令是否自相矛盾？
3. **覆盖范围**：有没有明显缺失的边界条件处理？
4. **资源引用**：references/ 里引用的文件是否存在？
5. **触发准确性**：description 是否既能覆盖应触发的场景，又不会误触发？

自审完成后，向用户展示简洁的审查结论（问题列表 + 已自动修正的项目）。只有通过自审后才进入测试阶段。

---

## 阶段四：测试用例生成与运行

### 多层次测试用例（增强版）

原版只要求 2-3 个测试用例。增强版要求按层次覆盖：

```
L1 正常路径（1-2 个）：典型输入，预期顺利成功
L2 边界用例（1 个）：空输入、超大输入、格式异常
L3 对抗用例（1 个）：歧义请求，或要求技能做它不该做的事
```

这不是要你机械地跑4个用例——而是要确保技能在"奇怪情况"下也表现得体。如果技能天然不适合某层，跳过并说明原因。

测试用例保存到 `evals/evals.json`：

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的实际任务提示",
      "expected_output": "预期结果描述",
      "tier": "L1",
      "files": []
    }
  ]
}
```

`tier` 字段新增（L1/L2/L3），帮助后续分析哪个层次的问题最多。详见 `references/schemas.md`。

### 运行测试（同原版逻辑）

将结果存放在 `<skill-name>-workspace/iteration-N/` 下。

**第一步：同时生成所有子智能体任务（with-skill AND baseline）**

对每个测试用例，在同一轮中同时生成两个子智能体：

```
执行以下任务：
- 技能路径：<skill-path>
- 任务：<eval prompt>
- 输入文件：<eval files 或 "无">
- 保存输出到：<workspace>/iteration-N/eval-<ID>-<tier>/with_skill/outputs/
- 需要保存的输出：<用户关心的内容>
```

**第二步：在运行过程中起草断言**

不要等待运行完成——利用等待时间起草定量断言，并向用户解释每个断言在检查什么。

好的断言：客观可验证、描述性名称、一眼能看懂通过/失败意味着什么。

**第三步：记录计时数据**

每个子智能体完成时，立即保存 `timing.json`：
```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

**第四步：评分、聚合、启动查看器**

1. **评分**：调用 `agents/grader.md` 评估每个断言，保存 `grading.json`（字段：`text`、`passed`、`evidence`）
2. **聚合**：
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
3. **分析**：调用 `agents/analyzer.md` 分析模式（非判别性断言、高方差用例等）
4. **启动查看器**：
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   无显示器/Cowork 环境使用 `--static <output_path>`。

**重要**：先让用户看查看器，再自己评估和修改技能。

告知用户："我已在浏览器中打开结果。'Outputs' 标签可以逐个查看测试用例并留下反馈，'Benchmark' 标签显示定量比较。看完后回来告诉我。"

---

## 阶段五：读取反馈并迭代改进

读取 `feedback.json`：
```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "图表缺少坐标轴标签"},
    {"run_id": "eval-1-with_skill", "feedback": ""}
  ],
  "status": "complete"
}
```
空反馈 = 用户认为没问题。聚焦于有具体投诉的用例。

### 改进时的思维框架

**从具体反馈中泛化**：这里只有几个用例，但技能要服务无数次调用。不要针对这几个例子做过拟合的修改——理解背后的原因，写出能泛化的指令。

**保持指令精简**：删除没有发挥作用的部分。读运行日志（不只是最终输出）——如果技能在引导模型做大量无益的工作，剪掉那部分。

**寻找重复模式**：如果多个测试用例都让子智能体写了相似的辅助脚本，把那个脚本打包进 `scripts/` 目录。

**生成变更日志（新增）**：每次迭代后，在 `<workspace>/CHANGELOG.md` 追加：
```markdown
## 迭代 N（日期）
### 失败的测试用例
- eval-2（L2 边界用例）：断言"输出为有效 JSON"失败

### 具体修改
- SKILL.md 第 47 行：添加了对空输入的显式处理说明
- 理由：模型在空输入时直接报错，没有给用户友好的提示

### 预期效果
- 空输入现在应返回友好的错误信息而非崩溃
```

### 迭代循环

1. 应用改进
2. 将所有测试用例重新运行到 `iteration-<N+1>/`，包括基线
3. 用 `--previous-workspace` 启动带历史对比的查看器
4. 等待用户反馈
5. 重复

停止条件：用户表示满意 / 所有反馈为空 / 没有实质性进展

---

## 阶段六：描述优化

技能的 `description` 字段决定了 Claude 是否会在正确时机调用它。完成技能创建后，主动提出优化描述。

**第一步：生成触发评测查询**

生成 20 个查询（应触发 + 不应触发各半），保存为 JSON：
```json
[
  {"query": "用户提示", "should_trigger": true},
  {"query": "另一个提示", "should_trigger": false}
]
```

查询要足够真实和具体——有文件路径、个人背景、列名、公司名、URL；混合大小写、拼写错误、口语化表达；聚焦边界情况而非一目了然的情况。

**第二步：用户确认查询集**

从 `assets/eval_review.html` 读取模板，替换占位符，打开供用户编辑和确认。

**第三步：运行优化循环**

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <当前会话使用的模型ID> \
  --max-iterations 5 \
  --verbose
```

循环会自动做 60/40 训练/测试分割、多轮评估、迭代改进。完成后返回 `best_description`。

**第四步：应用结果**

将 `best_description` 更新到 SKILL.md frontmatter，向用户展示前后对比和分数变化。

---

## 阶段七：兼容性报告（新增）✨

技能完成后，生成 `ENVIRONMENTS.md`，说明在不同环境下的行为：

```markdown
# 环境兼容性说明

## Claude Code（完整支持）
所有功能正常，包括子智能体并行测试、浏览器查看器、描述优化。

## Claude.ai（部分支持）
- 无子智能体：测试用例改为串行执行，跳过基线对比
- 无浏览器：在对话中直接展示结果，让用户内联反馈
- 跳过描述优化（需要 claude CLI）

## Cowork（完整支持，部分差异）
- 查看器使用 --static 生成静态 HTML 文件
- 反馈通过下载 feedback.json 文件提交

## 必需工具
<根据技能具体依赖填写>

## 优雅降级
<在缺少某工具时的备选方案>
```

---

## 阶段八：打包交付

如果有 `present_files` 工具：
```bash
python -m scripts.package_skill <path/to/skill-folder>
```
生成 `.skill` 文件后，告知用户文件路径。

---

## 高级：盲测对比

需要严格对比两个版本时，调用 `agents/comparator.md` 和 `agents/analyzer.md`。给独立智能体看两份输出（不告知哪个是哪个），让它判断质量。这是可选的，大多数情况下人工审查就足够了。

---

## Claude.ai 适配

无子智能体时的调整：
- **运行测试**：串行执行，你自己读 SKILL.md 然后按指令完成任务（你有完整上下文，结果不如独立子智能体严格，但是有效的健全性检查）
- **查看结果**：无法开浏览器，直接在对话中展示结果，内联收集反馈
- **跳过**：定量基准测试、描述优化（需要 CLI）、盲测对比

---

## 引用文件

**agents/**（专门子智能体的指令）
- `agents/grader.md` — 评估断言对输出的符合度
- `agents/comparator.md` — 盲测 A/B 对比
- `agents/analyzer.md` — 分析为何某版本胜出
- `agents/self-reviewer.md` — 草稿自审（增强版新增）

**references/**（参考文档）
- `references/schemas.md` — evals.json、grading.json 等 JSON 结构
- `references/skill-writing-patterns.md` — 扩展写作模式参考（增强版新增）

**references/templates/**（技能模板库，增强版新增）
- `template-report-generator.md`、`template-code-transformer.md`
- `template-data-extractor.md`、`template-workflow-orchestrator.md`
- `template-conversational-assistant.md`

---

## 核心循环（最后再强调一遍）

1. 了解技能要做什么
2. 推荐合适模板，编写草稿
3. **草稿自审**（新增）
4. 运行测试（with-skill + baseline 同时启动）
5. 生成查看器 → **让用户先看** → 然后你才分析
6. 读反馈，改进，**记录变更日志**（新增）
7. 重复直到满意
8. 描述优化
9. 生成**兼容性报告**（新增）
10. 打包交付

加油！
