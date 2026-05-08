---
name: momoyu-fetch
description: 摸摸鱼公开热榜抓取器，支持在对话中读取、配置平台、去重历史、生成 Markdown 日报和一键打开浏览器功能。触发词包含 /mmy 系列命令。
compatibility:
  tools: [bash, python]
  requires:
    - Python >= 3.8
---

# 摸摸鱼热榜助手 (mmy)

这是一个基于 `momoyu.cc` 公开接口的热榜抓取工具。主要运行脚本位于本 Skill 目录下的 `scripts/momoyu_public_fetch.py`。
执行时产生的数据文件（`mmy_config.json` 和 `mmy_history.json`）也会默认生成在 `scripts/` 目录下，从而保证整个 Skill 的数据内聚且支持跨平台迁移。

> ⚠️ **注意**：
> 下方所有命令示例均使用相对路径。在执行命令前，**请确保当前工作目录（Cwd）已切换至本 Skill 的根目录**（即 `SKILL.md` 所在的目录）。

## 支持的命令

| 命令 | 功能描述 |
| --- | --- |
| `/mmy` | 在对话中打印当前热榜（使用当前激活的关注列表和去重设置） |
| `/mmy:setting` | 交互式配置：选择当前列表关注的平台，并设置是否去重 |
| `/mmy:md` | 生成当前热榜的 Markdown 快照文件到当前目录 |
| `/mmy:daily` | 生成当日所有关注平台的汇总日报（Markdown格式）到当前目录 |
| `/mmy:list` | 管理多套关注列表（查看/新建/切换/删除） |
| `/mmy:open-<N>` | 一键打开当前列表所有平台的前 N 条（如 `/mmy:open-5`） |
| `/mmy:open-<平台>-<N>`| 一键打开指定平台的前 N 条（如 `/mmy:open-zhihu-5`） |

---

## 核心执行流程

> ⚠️ **重要提醒：解决中文乱码**
> Windows PowerShell 环境下执行 Python 脚本抓取包含中文的内容时极易出现乱码。
> **所有**包含 `python` 的 PowerShell 命令执行前，**必须**加上 `[console]::OutputEncoding=[System.Text.Encoding]::UTF8;` 前缀。如果是在 Linux/macOS 环境下，则直接使用 `python` 或 `python3` 即可。

### 1. `/mmy`
执行 `api` 命令并获取 Markdown 输出，直接在对话中渲染给用户。
```powershell
[console]::OutputEncoding=[System.Text.Encoding]::UTF8; python scripts/momoyu_public_fetch.py api --format markdown
```

### 2. `/mmy:setting`
这是一个交互式过程：

**第一步**：执行以下命令获取所有支持的源平台：
```powershell
[console]::OutputEncoding=[System.Text.Encoding]::UTF8; python scripts/momoyu_public_fetch.py sources --limit 200
```
**第二步**：提取前 20 个常用源（或根据用户偏好提取），在对话框中给用户展示带数字序号的列表。
格式要求如下：
> ⚙️ **配置热榜平台**
>
> 1. 知乎热榜 (zhihu)
> 2. 微博热搜 (weibo)
> 3. 虎扑步行街 (hupu)
> ...
> 
> 💬 请回复你想关注的平台**数字序号**（逗号分隔，如：1,3,5）。
> 同时告诉我是否需要**开启历史去重**（开启后近期看过的帖子不再显示，默认关闭）。

**第三步**：用户回复后，你需要读取并修改配置文件 `scripts/mmy_config.json`。
你可以写一个简单的临时 Python 脚本来更新配置，例如：
```python
import json, sys, os
path = os.path.join("scripts", "mmy_config.json")
try:
    with open(path, "r", encoding="utf-8") as f: config = json.load(f)
except:
    config = {"limit_per_source": 10, "deduplicate": False, "active_list": "default", "lists": {"default": ["zhihu"]}}

active = config.get("active_list", "default")
# 更新列表，将下面的列表替换为用户选中的 source_key 或 id 
config["lists"][active] = ["zhihu", "weibo"]
config["deduplicate"] = True # 替换为用户的选择

with open(path, "w", encoding="utf-8") as f: json.dump(config, f, ensure_ascii=False, indent=2)
print("配置更新成功！当前活跃列表:", active)
```

### 3. `/mmy:md` 和 `/mmy:daily`
执行并重定向输出到文件。注意文件名带上日期时间。
```powershell
# 对于 /mmy:md
[console]::OutputEncoding=[System.Text.Encoding]::UTF8; python scripts/momoyu_public_fetch.py api --format markdown > mmy-$(Get-Date -Format 'yyyyMMdd-HHmmss').md

# 对于 /mmy:daily
[console]::OutputEncoding=[System.Text.Encoding]::UTF8; python scripts/momoyu_public_fetch.py api --format markdown > mmy-daily-$(Get-Date -Format 'yyyyMMdd').md
```

### 4. `/mmy:list`
允许用户管理多套配置。
读取 `scripts/mmy_config.json` 中的 `lists` 对象和 `active_list` 字段，展示给用户：
> 📋 **当前关注列表**
> 
> - **default** (当前激活): zhihu, weibo
> - tech: github, v2ex
> 
> 你可以说“新建 tech 列表”、“切换到 tech” 或 “删除 default”。

当用户下达指令后，修改该 JSON 并保存。

### 5. `/mmy:open-N` 和 `/mmy:open-<平台>-N`
解析用户命令，分别调用脚本的 `--open-count` 参数：

- 如果是 **`/mmy:open-5`**（使用当前默认列表打开前 5 条）：
  ```powershell
  [console]::OutputEncoding=[System.Text.Encoding]::UTF8; python scripts/momoyu_public_fetch.py api --open-count 5
  ```

- 如果是 **`/mmy:open-zhihu-5`**（仅打开知乎的前 5 条）：
  ```powershell
  [console]::OutputEncoding=[System.Text.Encoding]::UTF8; python scripts/momoyu_public_fetch.py api --sources zhihu --open-count 5
  ```

---

## 交互规范
1. **反馈及时**：耗时较长的抓取操作前，先安抚用户“正在抓取热榜，请稍候...”。
2. **避免大段乱码**：绝对不能忘记设置 UTF-8 编码。
3. **静默操作**：如果命令是 `/mmy:md`、`/mmy:daily` 或 `/mmy:open-N`，只需要告诉用户“已生成文件”或“已打开浏览器”，**不要**在对话框里把几十条热榜打印出来，以免刷屏。只有 `/mmy` 才需要打印内容。
