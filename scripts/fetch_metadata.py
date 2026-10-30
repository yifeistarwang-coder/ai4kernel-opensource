#!/usr/bin/env python3
"""从 GitHub 抓取开源仓库元数据与顶层目录结构。

输出 data/github-metadata.json（提交进仓），README 原文写入 .cache/（不提交，避免第三方版权问题）。
依赖 gh CLI（已认证），用 gh api 而不是裸 curl 以复用用户凭证。
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import time

GH = os.environ.get("GH_BIN", "gh")


def gh_api(path, accept=None):
    cmd = [GH, "api", path]
    if accept:
        cmd += ["-H", f"Accept: {accept}"]
    for attempt in range(4):
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            return json.loads(proc.stdout) if proc.stdout.strip() else None
        if "Not Found" in proc.stderr:
            return None
        if attempt < 3:
            time.sleep(2 * (attempt + 1))
    return None


def gh_raw(path):
    proc = subprocess.run(
        [GH, "api", path, "-H", "Accept: application/vnd.github.raw"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def fetch_repo(slug):
    meta = gh_api(f"repos/{slug}")
    if meta is None:
        return None

    canonical = meta.get("full_name", slug)
    entry = {
        "slug": slug,
        "canonical": canonical,
        "renamed": canonical.lower() != slug.lower(),
        "html_url": meta.get("html_url"),
        "description": meta.get("description"),
        "homepage": meta.get("homepage") or None,
        "license": (meta.get("license") or {}).get("spdx_id"),
        "license_name": (meta.get("license") or {}).get("name"),
        "primary_language": meta.get("language"),
        "languages_url": meta.get("languages_url"),
        "stars": meta.get("stargazers_count"),
        "forks": meta.get("forks_count"),
        "open_issues": meta.get("open_issues_count"),
        "watchers": meta.get("subscribers_count"),
        "size_kb": meta.get("size"),
        "topics": meta.get("topics") or [],
        "created_at": meta.get("created_at"),
        "updated_at": meta.get("updated_at"),
        "pushed_at": meta.get("pushed_at"),
        "archived": meta.get("archived"),
        "disabled": meta.get("disabled"),
        "is_fork": meta.get("fork"),
        "default_branch": meta.get("default_branch"),
        "owner_login": (meta.get("owner") or {}).get("login"),
        "owner_type": (meta.get("owner") or {}).get("type"),
    }

    # 顶层目录结构：判断项目分层与架构形态的最直接证据
    contents = gh_api(f"repos/{canonical}/contents/") or []
    if isinstance(contents, list):
        entry["root_entries"] = sorted(
            [
                {
                    "name": c.get("name"),
                    "type": c.get("type"),
                    "size": c.get("size"),
                }
                for c in contents
            ],
            key=lambda c: (c["type"] != "dir", (c["name"] or "").lower()),
        )

    languages = gh_api(f"repos/{canonical}/languages") or {}
    if isinstance(languages, dict):
        total = sum(languages.values()) or 1
        entry["language_breakdown"] = [
            {"language": k, "bytes": v, "percent": round(100.0 * v / total, 1)}
            for k, v in sorted(languages.items(), key=lambda kv: -kv[1])[:8]
        ]
    return entry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="data/seeds.json")
    ap.add_argument("--out", default="data/github-metadata.json")
    ap.add_argument("--readme-dir", default=".cache/readmes")
    args = ap.parse_args()

    with open(args.seeds, encoding="utf-8") as f:
        seeds = json.load(f)

    os.makedirs(args.readme_dir, exist_ok=True)
    results = []
    for i, seed in enumerate(seeds["github"], 1):
        slug = seed["slug"]
        entry = fetch_repo(slug)
        if entry is None:
            print(f"[{i}/{len(seeds['github'])}] MISS {slug}", file=sys.stderr)
            results.append({"slug": slug, "canonical": None, "error": "not_found_or_unauthorized"})
            continue
        readme = gh_raw(f"repos/{entry['canonical']}/readme")
        if readme:
            safe = entry["canonical"].replace("/", "__")
            with open(os.path.join(args.readme_dir, f"{safe}.md"), "w", encoding="utf-8") as f:
                f.write(readme)
            entry["readme_cached"] = True
            entry["readme_bytes"] = len(readme.encode("utf-8"))
        results.append(entry)
        print(
            f"[{i}/{len(seeds['github'])}] {entry['canonical']:<50} "
            f"{str(entry.get('license')):<12} {entry.get('primary_language')}",
            file=sys.stderr,
        )

    payload = {
        "schema": 1,
        "source": "GitHub REST API v3 via gh api",
        "github": results,
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    ok = sum(1 for r in results if r.get("canonical"))
    print(f"fetched {ok}/{len(results)}", file=sys.stderr)


if __name__ == "__main__":
    main()
