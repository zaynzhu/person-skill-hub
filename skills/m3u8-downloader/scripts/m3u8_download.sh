#!/usr/bin/env bash
set -euo pipefail

# Defaults
OUTPUT_DIR="$HOME/Downloads"
FILENAME=""
FORMAT="mp4"
HEADERS=()
PROXY=""

usage() {
  cat <<EOF
用法: m3u8_download.sh [选项] <m3u8_url>

选项:
  -o <目录>     保存目录（默认: ~/Downloads）
  -n <文件名>   文件名，不含扩展名（默认: 自动生成）
  -f <格式>     输出格式: mp4 或 ts（默认: mp4）
  -H <header>   添加 HTTP Header，可多次使用
  -p <proxy>    使用 HTTP/SOCKS 代理
  -h            显示帮助信息
EOF
  exit 0
}

while getopts "o:n:f:H:p:h" opt; do
  case "$opt" in
    o) OUTPUT_DIR="$OPTARG" ;;
    n) FILENAME="$OPTARG" ;;
    f) FORMAT="$OPTARG" ;;
    H) HEADERS+=("-header" "$OPTARG") ;;
    p) PROXY="$OPTARG" ;;
    h) usage ;;
    *) usage ;;
  esac
done
shift $((OPTIND - 1))

URL="${1:-}"
if [[ -z "$URL" ]]; then
  echo "错误: 缺少 m3u8 URL" >&2
  usage
fi

# Check ffmpeg
if ! command -v ffmpeg &>/dev/null; then
  echo "错误: ffmpeg 未安装" >&2
  echo "安装方式:" >&2
  echo "  macOS:   brew install ffmpeg" >&2
  echo "  Ubuntu:  sudo apt install ffmpeg" >&2
  echo "  Windows: choco install ffmpeg" >&2
  exit 1
fi

# Validate format
if [[ "$FORMAT" != "mp4" && "$FORMAT" != "ts" ]]; then
  echo "错误: 格式仅支持 mp4 或 ts" >&2
  exit 1
fi

# Auto-generate filename
if [[ -z "$FILENAME" ]]; then
  TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
  FILENAME="m3u8_video_${TIMESTAMP}"
fi

# Sanitize filename (remove problematic characters)
FILENAME=$(echo "$FILENAME" | tr '/\\:*?"<>|' '_')

# Create output directory
mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}.${FORMAT}"

# Avoid overwriting
COUNTER=1
while [[ -f "$OUTPUT_FILE" ]]; do
  OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}_${COUNTER}.${FORMAT}"
  ((COUNTER++))
done

# Build ffmpeg command
FFMPEG_ARGS=(-y -i "$URL")

# Add headers
if [[ ${#HEADERS[@]} -gt 0 ]]; then
  FFMPEG_ARGS+=("${HEADERS[@]}")
fi

# Add proxy
if [[ -n "$PROXY" ]]; then
  FFMPEG_ARGS+=(-http_proxy "$PROXY")
fi

# Codec and format
if [[ "$FORMAT" == "mp4" ]]; then
  FFMPEG_ARGS+=(-c copy -bsf:a aac_adtstoasc)
elif [[ "$FORMAT" == "ts" ]]; then
  FFMPEG_ARGS+=(-c copy)
fi

FFMPEG_ARGS+=("$OUTPUT_FILE")

echo "========================================="
echo "  M3U8 Downloader"
echo "========================================="
echo "  URL:    $URL"
echo "  格式:   $FORMAT"
echo "  保存到: $OUTPUT_FILE"
echo "========================================="
echo ""

# Run ffmpeg
if ffmpeg "${FFMPEG_ARGS[@]}" 2>&1; then
  FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
  echo ""
  echo "✅ 下载完成!"
  echo "   文件: $OUTPUT_FILE"
  echo "   大小: $FILE_SIZE"
else
  echo ""
  echo "❌ 下载失败"
  rm -f "$OUTPUT_FILE" 2>/dev/null
  exit 1
fi