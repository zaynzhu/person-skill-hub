# JSON 数据结构参考（Schemas）

本文件定义了 enhanced-skill-creator 中使用的所有 JSON 结构。

---

## evals.json

保存在 `evals/evals.json`，存储技能的测试用例集。

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的任务提示（真实用户会说的话）",
      "expected_output": "预期结果的描述",
      "tier": "L1",
      "files": [],
      "assertions": [
        {
          "name": "断言名称（描述性，一眼能懂通过/失败意味着什么）",
          "check": "断言的具体检查内容描述"
        }
      ]
    }
  ]
}
```

**字段说明：**
- `tier`（增强版新增）：`"L1"` 正常路径 / `"L2"` 边界用例 / `"L3"` 对抗用例
- `files`：任务需要的输入文件路径列表，无则为空数组
- `assertions`：在写断言之前可以为空数组 `[]`

---

## eval_metadata.json

每个评测运行目录中的元数据文件。

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "tier": "L1",
  "prompt": "用户的任务提示",
  "assertions": [
    {
      "name": "输出文件存在",
      "check": "outputs/ 目录中有至少一个文件"
    },
    {
      "name": "输出为有效 JSON",
      "check": "主输出文件可被 json.loads() 解析且不抛出异常"
    }
  ]
}
```

---

## grading.json

评分结果文件，由 `agents/grader.md` 生成。

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "graded_at": "2025-01-01T12:00:00Z",
  "expectations": [
    {
      "text": "断言的文字描述（与 assertions[].name 对应）",
      "passed": true,
      "evidence": "证据：具体说明为何通过或失败"
    }
  ]
}
```

**重要**：字段必须精确为 `text`、`passed`、`evidence`（eval-viewer 依赖这些确切名称）。

---

## timing.json

计时数据，子智能体完成后立即记录。

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

---

## benchmark.json

聚合基准数据，由 `scripts/aggregate_benchmark.py` 生成。

```json
{
  "skill_name": "my-skill",
  "iteration": 1,
  "generated_at": "2025-01-01T12:00:00Z",
  "configurations": [
    {
      "name": "with_skill",
      "label": "With Skill",
      "evals": [
        {
          "eval_id": 0,
          "eval_name": "test-case-name",
          "tier": "L1",
          "pass_rate": 1.0,
          "assertions_total": 3,
          "assertions_passed": 3,
          "duration_ms": 15000,
          "total_tokens": 45000
        }
      ],
      "summary": {
        "pass_rate_mean": 0.85,
        "pass_rate_stddev": 0.12,
        "duration_ms_mean": 18000,
        "total_tokens_mean": 52000
      }
    },
    {
      "name": "without_skill",
      "label": "Baseline (No Skill)",
      "evals": [...],
      "summary": {...}
    }
  ],
  "delta": {
    "pass_rate": 0.23,
    "duration_ms": -2000,
    "total_tokens": 8000
  }
}
```

**注意**：configurations 中，始终将 `with_skill` 版本放在对应 baseline 版本之前。

---

## feedback.json

用户通过 eval-viewer 提交的反馈。

```json
{
  "reviews": [
    {
      "run_id": "eval-0-with_skill",
      "feedback": "图表缺少坐标轴标签",
      "timestamp": "2025-01-01T13:00:00Z"
    },
    {
      "run_id": "eval-1-with_skill",
      "feedback": "",
      "timestamp": "2025-01-01T13:01:00Z"
    }
  ],
  "status": "complete"
}
```

- `feedback` 为空字符串 = 用户认为该用例没问题

---

## 触发评测查询集（trigger eval set）

用于描述优化阶段，保存在 workspace 中。

```json
[
  {
    "query": "具体的、真实的用户提示（有背景、细节、口语化）",
    "should_trigger": true
  },
  {
    "query": "另一个提示",
    "should_trigger": false
  }
]
```
