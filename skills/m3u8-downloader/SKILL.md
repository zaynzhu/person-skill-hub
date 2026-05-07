---
name: m3u8-downloader
description: 使用 ffmpeg 下载 m3u8 视频流并转换为 MP4/TS 格式。当用户提到"下载 m3u8 视频"、"下载这个视频流"、"帮我下载 m3u8"、"m3u8 下载"时触发此技能。即使用户只是粘贴了一个 .m3u8 链接并表达了下载意图，也应该使用此技能。
compatibility:
  tools: [bash]
  requires:
    - ffmpeg（brew install ffmpeg / apt install ffmpeg / choco install ffmpeg）
---

# M3U8 Downloader Skill

通过 ffmpeg 下载 m3u8 视频流，自动转换为 MP4 格式保存到本地。

**技能根目录**：`skills/m3u8-downloader`（以下路径均相对于此目录）

---

## 快速判断

收到用户请求后，先判断场景：

- **提供 m3u8 URL** → 直接下载，最常用
- **提供网页 URL 含 m3u8** → 提示用户先获取 m3u8 直链，或用浏览器开发者工具抓取
- **需要 TS 原始格式** → 加 `-f ts` 参数
- **指定保存目录** → 加 `-o <目录>` 参数
- **指定文件名** → 加 `-n <文件名>` 参数

---

## 使用方式

### 基本下载（最常用）

```bash
bash scripts/m3u8_download.sh "https://example.com/video/index.m3u8"
```

自动生成文件名，保存为 MP4 到 `~/Downloads/` 目录。

### 指定输出格式

```bash
# 保存为 TS 原始格式（不转码，速度最快）
bash scripts/m3u8_download.sh -f ts "https://example.com/video/index.m3u8"
```

### 指定保存目录和文件名

```bash
bash scripts/m3u8_download.sh -o ./videos -n "我的视频" "https://example.com/video/index.m3u8"
```

### 指定 Headers（需要 Referer 或 Cookie 的站点）

```bash
bash scripts/m3u8_download.sh -H "Referer: https://example.com" -H "Cookie: token=abc" "https://example.com/video/index.m3u8"
```

### 全部参数

```
用法: m3u8_download.sh [选项] <m3u8_url>

选项:
  -o <目录>     保存目录（默认: ~/Downloads）
  -n <文件名>   文件名，不含扩展名（默认: 自动生成）
  -f <格式>     输出格式: mp4 或 ts（默认: mp4）
  -H <header>   添加 HTTP Header，可多次使用
  -p <proxy>    使用 HTTP/SOCKS 代理
  -h            显示帮助信息
```

---

## 环境准备

### 检查 ffmpeg

```bash
ffmpeg -version
```

如果未安装：

| 系统 | 安装命令 |
|------|---------|
| macOS | `brew install ffmpeg` |
| Ubuntu/Debian | `sudo apt install ffmpeg` |
| Windows | `choco install ffmpeg` |

### 检查脚本

```bash
bash scripts/m3u8_download.sh -h
```

---

## 常见问题处理

### 下载中断 / 网络不稳定

ffmpeg 默认会重试。如果反复失败：
- 检查网络连接
- 尝试使用代理：`-p socks5://127.0.0.1:1080`
- 保存为 TS 格式避免转码开销：`-f ts`

### 403 Forbidden

站点可能校验 Referer 或 Cookie：
```bash
bash scripts/m3u8_download.sh -H "Referer: https://example.com" "https://example.com/video/index.m3u8"
```

### 视频无法播放

某些 m3u8 流的音频编码需要重编码（而非直接拷贝）：
```bash
ffmpeg -i "https://example.com/video/index.m3u8" -c:v copy -c:a aac -bsf:a aac_adtstoasc output.mp4
```

### 如何获取 m3u8 链接

1. 浏览器打开视频页面
2. F12 打开开发者工具 → Network 标签
3. 筛选 `m3u8`
4. 播放视频，找到 `.m3u8` 请求
5. 复制 Request URL