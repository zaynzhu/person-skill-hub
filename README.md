<div align="center">

# ✦ Skill Hub

**个人 AI 技能合集** · 将专业工作流封装为可复用的指令集

[![Skills](https://img.shields.io/badge/skills-3-6366f1?style=flat-square&logo=sparkles&logoColor=white)](./skills/)
[![License](https://img.shields.io/badge/license-MIT-0ea5e9?style=flat-square)](./LICENSE)

</div>

---

## 什么是 Skill？

Skill 是封装了特定专业知识和工作流程的指令集，让 AI 在垂直任务上达到专家水准。每个 Skill 放在 `skills/` 下的独立目录中，包含一个 `SKILL.md` 主文件和可选的辅助资源。

---

## 技能索引

| &nbsp; | 技能 | 简介 | 状态 |
|:------:|------|------|:----:|
| 🛠️ | [**enhanced-skill-creator**](./skills/enhanced-skill-creator/) | Skill 全生命周期管理工具。支持需求收集、草稿自审、分层测试（L1/L2/L3）、量化评测、描述优化和打包交付，内置 5 类技能模板库 | `stable` |
| 📥 | [**video-downloader**](./skills/video-downloader/) | 多平台视频下载工具。支持 Bilibili / 抖音 / TikTok，具备画质选择、Cookie 认证、批量下载、断点续传和反爬虫绕过能力，并提供 MCP Server 接口 | `stable` |
| 📊 | [**coding-ai-digest**](./skills/coding-ai-digest/) | 实时抓取 star-history.com Coding AI 排行榜，对每个项目进行 GitHub API 查询 + 网络搜索，生成「能不能用上」速查卡报告，包含核心机制、适用场景、真实评价与注意事项 | `stable` |

---

## 如何使用这些 Skill

### 方式一：在支持 Skills 的 AI 工具中安装（推荐）

**适用于**：Claude Code、支持 `.skill` 文件的工具

```bash
# 1. 克隆本仓库
git clone https://github.com/zaynzhu/person-skill-hub.git

# 2. 进入想要使用的 skill 目录
cd person-skill-hub/skills/enhanced-skill-creator

# 3. 将 skill 目录路径告知 AI 工具，或通过工具的 skill 管理界面安装
```

### 方式二：直接读取 SKILL.md（通用）

**适用于**：任意支持自定义系统提示的 AI 工具

```bash
# 克隆仓库
git clone https://github.com/zaynzhu/person-skill-hub.git

# 在对话中告知 AI：
# "请阅读 <path>/skills/<skill-name>/SKILL.md 并按照其中的指令工作"
```

### 方式三：直接复制粘贴（最简单）

打开对应 skill 目录下的 `SKILL.md`，将其内容复制到 AI 工具的系统提示（System Prompt）或对话开头即可。

---

## 各 Skill 依赖说明

| Skill | 运行环境 | 必需工具 | 可选 |
|-------|---------|---------|------|
| `enhanced-skill-creator` | 通用 | 无 | Python（描述优化脚本） |
| `video-downloader` | Python ≥ 3.8 | `aiohttp`、`playwright` | GitHub Token |
| `coding-ai-digest` | Python ≥ 3.8 | 无（搜索服务自动选择） | GitHub Token（速率提升 80x） |

> **video-downloader** 首次使用需执行 `playwright install chromium`（用于抖音/TikTok 反爬）
>
> **coding-ai-digest** 推荐配置 Tavily Search 以获得最佳数据质量

---

## 目录结构

```
skill-hub/
├── README.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md          ← 主指令文件（必须）
        ├── scripts/          ← 辅助脚本（可选）
        ├── agents/           ← 子 agent 指令（可选）
        ├── references/       ← 参考文档（可选）
        └── assets/           ← 静态资源（可选）
```

---

## 添加新技能

```bash
# 1. 新建目录（小写连字符命名）
mkdir skills/my-new-skill

# 2. 创建 SKILL.md（含 YAML frontmatter）
touch skills/my-new-skill/SKILL.md

# 3. 在本文件的技能索引中补充一行记录
```

---

<div align="center">
<sub>持续更新中 · 欢迎 Fork 构建你自己的技能库</sub>
</div>
