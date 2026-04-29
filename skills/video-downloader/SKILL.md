---
name: video-downloader
description: 使用 video_downloader 工具下载 Bilibili（B站）、抖音（Douyin）、TikTok 视频和图集。当用户提到"帮我下载这个视频"、"把这个B站/抖音/TikTok链接下载下来"、"下载视频到本地"、"批量下载"时触发此技能。即使用户只是粘贴了一个 bilibili.com、douyin.com 或 tiktok.com 链接并表达了下载意图，也应该使用此技能。
compatibility:
  tools: [bash, python]
  requires:
    - Python >= 3.8
    - 已安装 video_downloader（pip install -r requirements.txt）
    - Playwright 浏览器（playwright install chromium，抖音/TikTok 必须）
---

# Video Downloader Skill

帮助用户通过命令行或 Python API 下载 B站、抖音、TikTok 的视频和图集。

**技能根目录**：`E:\code\codex\project-y`（以下路径均相对于此目录）

---

## 快速判断

收到用户请求后，先判断场景：

- **单个 URL** → 用命令行，简单快速
- **批量多个 URL** → 命令行批量或从文件读取
- **需要编程控制**（进度回调、自定义逻辑）→ Python API
- **只想查看视频信息不下载** → 加 `--metadata-only`
- **需要高清/4K** → 需要 Cookie + `-q` 参数

---

## 命令行使用（推荐入门）

```bash
# 切换到项目目录
cd E:\code\codex\project-y

# 下载单个视频（最简单）
python -m video_downloader [URL]

# 常用参数组合
python -m video_downloader \
  -o ./downloads \          # 指定保存目录（默认 ./downloads）
  -q 1080P \               # 画质：4K / 1080P60 / 1080P / 720P60 / 720P / 480P / 360P
  -f "{author}_{title}" \  # 文件名模板
  -c cookies.txt \         # Cookie 文件（获取高清或会员内容必须）
  [URL]

# 批量下载（多个 URL）
python -m video_downloader URL1 URL2 URL3

# 从文件批量下载（每行一个 URL）
python -m video_downloader --url-file urls.txt

# 只查看视频信息（不下载）
python -m video_downloader --metadata-only [URL]

# 查看支持的平台
python -m video_downloader --list-platforms
```

**文件名模板变量**：`{title}` 标题 / `{author}` 作者 / `{id}` 视频ID / `{date}` 日期 / `{platform}` 平台

---

## 平台说明

| 平台 | 视频 | 图集 | 画质选择 | Cookie | 反爬状态 |
|------|------|------|---------|--------|---------|
| Bilibili | ✅ | ❌ | ✅ 完整支持 | ✅ | 稳定 |
| 抖音 | ✅ | ✅ | ❌ | ✅ | 测试中，需浏览器自动化 |
| TikTok | ✅ | ❌ | ❌ | ✅ | 测试中，需浏览器自动化 |

**重要**：抖音和 TikTok 需要 X-Bogus/A-Bogus 签名，当前实现通过 Playwright 浏览器自动化绕过，速度较慢但稳定。

---

## Python API 使用

需要 Python 控制时（如进度显示、错误处理、集成到其他脚本）：

```python
import asyncio
from video_downloader import VideoDownloader
from video_downloader.models import DownloadOptions
from video_downloader.config import DownloaderConfig

async def main():
    # 基础下载
    downloader = VideoDownloader()
    result = await downloader.download(
        "https://www.bilibili.com/video/BV1xx411c7mD",
        DownloadOptions(output_dir="./downloads", quality="1080P")
    )
    print(f"{'成功' if result.success else '失败'}: {result.file_path or result.error_message}")

    # 批量下载
    batch = await downloader.batch_download(["url1", "url2"], DownloadOptions())
    print(f"成功 {batch.successful} / 共 {batch.total}")

    # 只提取元数据
    meta = await downloader.extract_metadata("https://www.bilibili.com/video/BV1xx411c7mD")
    print(f"{meta.title} | {meta.author} | {meta.duration}秒 | 可用画质: {meta.available_qualities}")

asyncio.run(main())
```

**自定义配置**（代理、反检测、超时等）：

```python
config = DownloaderConfig(
    output_dir="./downloads",
    cookie_file="./cookies.txt",    # Netscape 格式 Cookie
    filename_template="{author}_{title}",
    timeout=60,
    max_retries=3,
    headless=True,                  # False = 显示浏览器窗口（调试用）
    enable_stealth=True,            # 启用浏览器指纹伪装
    proxy="http://127.0.0.1:7890", # HTTP 或 socks5:// 代理
    user_agent="自定义UA",
)
downloader = VideoDownloader(config)
```

---

## 常见问题处理

### 403 / 反爬虫被拦截
```bash
# 方案1：提供 Cookie（推荐）
python -m video_downloader -c cookies.txt [URL]

# 方案2：使用代理
python -m video_downloader --proxy http://127.0.0.1:7890 [URL]
```

**获取 Cookie**：浏览器安装 "Get cookies.txt" 插件 → 登录目标网站 → 导出 Netscape 格式 → 保存为 cookies.txt

### Playwright 浏览器未安装
```bash
playwright install chromium
```

### Windows 运行报错
- 确认已安装 Visual C++ Redistributable
- 链接：https://aka.ms/vs/17/release/vc_redist.x64.exe

### 超时错误
```bash
python -m video_downloader --timeout 120 [URL]
```

### 视频找不到
- 确认视频未被删除或设为私密
- 会员内容需要提供对应账号的 Cookie

---

## 添加新平台

如需扩展支持新平台，在 `video_downloader/extractors/` 创建新文件，继承 `PlatformExtractor` 基类：

```python
from .base import PlatformExtractor
from ..models import VideoMetadata, DownloadOptions

class NewPlatformExtractor(PlatformExtractor):
    @property
    def platform_name(self) -> str:
        return "new-platform"

    @property
    def url_patterns(self) -> list[str]:
        return [r"https?://(?:www\.)?newplatform\.com/video/[\w-]+"]

    async def extract_metadata(self, url: str) -> VideoMetadata:
        # 实现元数据提取
        pass

    async def get_download_url(self, url: str, options: DownloadOptions) -> str:
        # 实现下载链接获取
        pass
```

然后在 `video_downloader/extractors/__init__.py` 中注册。

---

## MCP Server 模式

如需通过 MCP 协议被 Claude Desktop 或其他 AI 工具调用：

```bash
# 启动 MCP Server（stdio 模式）
python mcp_server.py
```

提供的工具：`download_video` / `batch_download` / `get_video_info` / `list_supported_platforms`

详见 `mcp_server.py`。

---

## 参考文档
- 完整使用示例 → `USAGE.md`
- 快速入口脚本 → `quick_start.py`
- 架构设计文档 → `.kiro/specs/video-downloader-skill/design.md`
- 需求文档 → `.kiro/specs/video-downloader-skill/requirements.md`
