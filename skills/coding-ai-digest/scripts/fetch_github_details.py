#!/usr/bin/env python3
"""
fetch_github_details.py
批量获取 GitHub 仓库详细信息，供生成速查卡使用

用法：
  python3 fetch_github_details.py --repos "owner/repo1,owner/repo2"
  python3 fetch_github_details.py --from-file resolved_repos.json
  python3 fetch_github_details.py --repos "..." --token ghp_xxx --output details.json
"""

import argparse
import json
import os
import subprocess
import sys
import time


def fetch_repo(full_name: str, token: str = None) -> dict | None:
    """获取单个仓库详情"""
    url = f"https://api.github.com/repos/{full_name}"
    cmd = ["curl", "-s", url,
           "-H", "Accept: application/vnd.github.v3+json",
           "-H", "User-Agent: coding-ai-digest-skill"]
    if token:
        cmd += ["-H", f"Authorization: token {token}"]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    
    if "message" in data:
        print(f"  [WARN] {full_name}: {data['message']}", file=sys.stderr)
        return None
    
    return {
        "full_name": data.get("full_name"),
        "name": data.get("name"),
        "owner": data.get("owner", {}).get("login"),
        "description": data.get("description", ""),
        "language": data.get("language", ""),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "watchers": data.get("watchers_count", 0),
        "topics": data.get("topics", []),
        "homepage": data.get("homepage", ""),
        "license": (data.get("license") or {}).get("spdx_id", ""),
        "default_branch": data.get("default_branch", "main"),
        "created_at": (data.get("created_at") or "")[:10],
        "updated_at": (data.get("updated_at") or "")[:10],
        "pushed_at": (data.get("pushed_at") or "")[:10],
        "size_kb": data.get("size", 0),
        "is_fork": data.get("fork", False),
        "has_wiki": data.get("has_wiki", False),
        "url": data.get("html_url"),
        "archived": data.get("archived", False),
    }


def fetch_readme_summary(full_name: str, token: str = None) -> str:
    """获取 README 前500字，作为补充描述"""
    url = f"https://api.github.com/repos/{full_name}/readme"
    cmd = ["curl", "-s", url,
           "-H", "Accept: application/vnd.github.v3.raw",
           "-H", "User-Agent: coding-ai-digest-skill"]
    if token:
        cmd += ["-H", f"Authorization: token {token}"]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        return ""
    
    # 只取前 500 字，跳过徽章和图片行
    lines = []
    char_count = 0
    for line in result.stdout.split("\n"):
        if line.startswith("![") or line.startswith("<img") or line.startswith("[!["):
            continue
        lines.append(line)
        char_count += len(line)
        if char_count > 500:
            break
    
    return "\n".join(lines[:20])


def main():
    parser = argparse.ArgumentParser(description="批量获取 GitHub 仓库详情")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--repos", help="逗号分隔的 owner/repo 列表")
    group.add_argument("--from-file", help="从 resolve_repos.py 输出的 JSON 文件读取")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--output", default="github_details.json")
    parser.add_argument("--with-readme", action="store_true", help="同时抓取 README 摘要（消耗更多 API 额度）")
    args = parser.parse_args()

    # 解析 repo 列表
    if args.repos:
        repo_list = [r.strip() for r in args.repos.split(",") if r.strip()]
    else:
        with open(args.from_file) as f:
            resolved = json.load(f)
        repo_list = [r["full_name"] for r in resolved if r.get("full_name")]

    print(f"[INFO] 获取 {len(repo_list)} 个仓库详情...", file=sys.stderr)
    
    if not args.token:
        print(f"[WARN] 未设置 GITHUB_TOKEN，速率限制 60次/h", file=sys.stderr)
        print(f"[WARN] {len(repo_list)} 个项目 + README = {len(repo_list) * 2} 次请求，请注意限额", file=sys.stderr)

    results = []
    for i, full_name in enumerate(repo_list, 1):
        print(f"  [{i}/{len(repo_list)}] {full_name}...", file=sys.stderr, end=" ")
        
        detail = fetch_repo(full_name, args.token)
        if not detail:
            print("失败", file=sys.stderr)
            continue
        
        if args.with_readme:
            time.sleep(0.3)
            detail["readme_preview"] = fetch_readme_summary(full_name, args.token)
        
        results.append(detail)
        print(f"⭐{detail['stars']:,}", file=sys.stderr)
        time.sleep(0.3)  # 避免触发速率限制

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] {len(results)} 个仓库详情已保存到 {args.output}", file=sys.stderr)
    
    # 打印摘要供 Claude 直接读取
    print(f"\n{'#':<3} {'仓库':<40} {'⭐':>8} {'语言':<12} {'更新':<12} 描述")
    print("-" * 110)
    for i, r in enumerate(results, 1):
        desc = (r.get("description") or "")[:35]
        print(f"{i:<3} {r['full_name']:<40} {r['stars']:>8,} {r['language'] or '-':<12} {r['updated_at']:<12} {desc}")
    
    # 输出 JSON 到 stdout（供管道使用）
    if args.output == "-":
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
