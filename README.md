<div align="center">

# ✦ Skill Hub

**个人 AI 技能合集** · 将专业工作流封装为可复用的指令集

[![Skills](https://img.shields.io/badge/skills-2-6366f1?style=flat-square&logo=sparkles&logoColor=white)](./skills/)
[![License](https://img.shields.io/badge/license-MIT-0ea5e9?style=flat-square)](./LICENSE)

</div>

---

## 什么是 Skill？

Skill 是封装了特定专业知识和工作流程的指令集，让 AI 在垂直任务上达到专家水准。每个 Skill 包含：

- **`SKILL.md`** — 核心指令与工作流程（必须）
- **`agents/`** — 子任务专用指令（可选）
- **`references/`** — 参考文档与数据模板（可选）
- **`assets/`** — 静态资源文件（可选）

---

## 技能索引

| &nbsp; | 技能 | 简介 | 状态 |
|:------:|------|------|:----:|
| 🛠️ | [**enhanced-skill-creator**](./skills/enhanced-skill-creator/) | Skill 全生命周期管理工具。支持需求收集、草稿自审、分层测试（L1/L2/L3）、量化评测、描述优化和打包交付，内置 5 类技能模板库 | `stable` |
| 📥 | [**video-downloader**](./skills/video-downloader/) | 多平台视频下载工具。支持 Bilibili / 抖音 / TikTok，具备画质选择、Cookie 认证、批量下载、断点续传和反爬虫绕过能力，并提供 MCP Server 接口 | `stable` |

---

## 目录结构

```
skill-hub/
├── README.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md          ← 主指令文件（必须）
        ├── agents/           ← 子 agent 指令（可选）
        ├── references/       ← 参考文档（可选）
        └── assets/           ← 静态资源（可选）
```

---

## 添加新技能

```bash
# 1. 在 skills/ 下新建目录（小写连字符命名）
mkdir skills/my-new-skill

# 2. 创建 SKILL.md（含 YAML frontmatter）
touch skills/my-new-skill/SKILL.md

# 3. 在本文件的技能索引中补充一行记录
```

---

<div align="center">
<sub>持续更新中 · 欢迎 Fork 构建你自己的技能库</sub>
</div>
