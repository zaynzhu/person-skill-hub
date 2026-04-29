# My Claude Skills

我的私人 Claude Skills 合集。

Skills 是给 Claude 的专项指令包，让它在特定任务上表现得像专家一样。每个 skill 放在 `skills/` 下的独立目录中，包含一个 `SKILL.md` 主文件和可选的辅助资源。

## 技能列表

| 技能 | 描述 | 状态 |
|------|------|------|
| [enhanced-skill-creator](./skills/enhanced-skill-creator/) | 创建、测试、优化 Claude Skills 的增强版工具。支持草稿自审、分层测试用例、技能模板库、变更日志等。 | ✅ 可用 |
| [video-downloader](./skills/video-downloader/) | 下载 Bilibili、抖音、TikTok 视频/图集。支持画质选择、Cookie 登录、批量下载、断点续传、浏览器反爬虫绕过，并提供 MCP Server 接口。 | ✅ 可用 |

## 使用方法

在 Claude Code 或 Claude.ai 中安装对应的 `.skill` 文件，或直接将 `SKILL.md` 的路径传给 Claude。

## 目录结构

```
my-claude-skills/
├── README.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md          ← 主指令文件（必须）
        ├── agents/           ← 子 agent 指令（可选）
        ├── references/       ← 参考文档（可选）
        └── assets/           ← 静态资源（可选）
```

## 添加新技能

1. 在 `skills/` 下创建新目录（小写连字符命名）
2. 至少包含一个 `SKILL.md`（含 YAML frontmatter）
3. 在本文件的技能列表中添加一行记录
