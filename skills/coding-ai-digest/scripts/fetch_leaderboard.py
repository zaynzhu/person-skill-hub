#!/usr/bin/env python3
"""
fetch_leaderboard.py
模拟抓取 star-history.com Coding AI Leaderboard

由于页面是动态渲染，本脚本通过 GitHub Search API
抓取最近高速增长的 AI 编程类工具仓库作为近似。

用法：
  python3 fetch_leaderboard.py --mode weekly --top 20
  python3 fetch_leaderboard.py --mode weekly --top 20 --token ghp_xxx
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta


def github_search(query: str, sort: str = "stars", order: str = "desc",
                  per_page: int = 20, token: str = None) -> dict:
    """调用 GitHub Search API"""
    url = (
        f"https://api.github.com/search/repositories"
        f"?q={query}&sort={sort}&order={order}&per_page={per_page}"
    )
    cmd = ["curl", "-s", url, "-H", "Accept: application/vnd.github.v3+json"]
    if token:
        cmd += ["-H", f"Authorization: token {token}"]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"[ERROR] API 返回非 JSON 内容: {result.stdout[:200]}", file=sys.stderr)
        return {"items": []}


def fetch_weekly_trending(top: int = 20, token: str = None) -> list:
    """
    模拟 weekly leaderboard：
    抓取最近7天创建或更新、topic 含 AI 编程相关的高 star 仓库
    """
    since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    # 多个查询组合，覆盖不同类型
    queries = [
        # Claude Code 生态
        f"topic:claude-code pushed:>{since}",
        f"topic:ai-agent pushed:>{since} stars:>500",
        # Skills / 编程 AI 工具
        f"skill claude-code pushed:>{since} stars:>200",
        f"topic:coding-assistant pushed:>{since} stars:>500",
    ]
    
    seen = set()
    results = []
    
    for q in queries:
        data = github_search(q, sort="stars", per_page=10, token=token)
        for item in data.get("items", []):
            if item["full_name"] not in seen:
                seen.add(item["full_name"])
                results.append({
                    "rank": None,
                    "full_name": item["full_name"],
                    "name": item["name"],
                    "description": item.get("description", ""),
                    "stars": item["stargazers_count"],
                    "language": item.get("language", ""),
                    "topics": item.get("topics", []),
                    "updated_at": item.get("updated_at", "")[:10],
                    "created_at": item.get("created_at", "")[:10],
                    "url": item["html_url"],
                    "homepage": item.get("homepage", ""),
                    "forks": item.get("forks_count", 0),
                    "open_issues": item.get("open_issues_count", 0),
                    "license": (item.get("license") or {}).get("spdx_id", ""),
                })
        time.sleep(0.5)
    
    # 按 star 数排序，取 top N
    results.sort(key=lambda x: x["stars"], reverse=True)
    for i, r in enumerate(results[:top], 1):
        r["rank"] = i
    
    return results[:top]


def main():
    parser = argparse.ArgumentParser(description="获取 Coding AI Leaderboard")
    parser.add_argument("--mode", default="weekly", choices=["weekly", "alltime"])
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--output", default="leaderboard.json")
    args = parser.parse_args()

    print(f"[INFO] 抓取 {args.mode} top {args.top} 榜单...", file=sys.stderr)
    
    if not args.token:
        print("[WARN] 未设置 GITHUB_TOKEN，速率限制 60次/h（20个项目足够）", file=sys.stderr)
    
    results = fetch_weekly_trending(top=args.top, token=args.token)
    
    output = {
        "mode": args.mode,
        "fetched_at": datetime.now().isoformat(),
        "count": len(results),
        "repos": results,
    }
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 已保存 {len(results)} 个项目到 {args.output}", file=sys.stderr)
    
    # 输出简要列表到 stdout 供 Claude 直接阅读
    print(f"\n{'排名':<4} {'项目':<40} {'Stars':>8} {'语言':<12} 描述")
    print("-" * 100)
    for r in results:
        desc = (r["description"] or "")[:35]
        print(f"#{r['rank']:<3} {r['full_name']:<40} {r['stars']:>8,} {r['language'] or '-':<12} {desc}")


if __name__ == "__main__":
    main()
