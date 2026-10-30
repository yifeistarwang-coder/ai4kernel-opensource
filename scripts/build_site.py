#!/usr/bin/env python3
"""把索引数据与文档装配成可部署的静态站点。

输出 dist/：
  index.html          应用外壳
  assets/             样式、脚本、字体（从 site/ 复制）
  data/site-data.json 站点所需的精简数据
  docs/*.md           文档原文，供站内阅读器渲染
  README.md / LICENSE / ... 便于直接在 Pages 上浏览仓库内容
"""

import argparse
import datetime
import json
import os
import shutil
import sys
from collections import Counter, defaultdict

GROUP_LABELS = {
    "benchmark": "评测与验证",
    "search": "搜索与优化",
    "agent": "Agent 与环境",
    "training": "训练、模型与数据",
    "foundation": "执行与知识底座",
}

VENDOR_LABELS = {
    "NVIDIA": "NVIDIA",
    "AMD": "AMD",
    "Ascend": "华为昇腾",
    "TPU": "Google TPU",
    "CPU": "CPU",
    "Intel": "Intel",
    "Other": "其他",
}

SHAPE_BLURBS = {
    "A": "只做「给定任务 → 产出结果 → 打分」，不负责生成 kernel 本身。",
    "B": "在基准之上叠加可插拔的 Agent 与执行环境，用来横向比较不同 Agent 策略。",
    "C": "自己带生成循环：模型提出候选 → 编译/测试 → 读取反馈 → 迭代。",
    "D": "不只做推理时搜索，而是产出可分发的模型权重或数据集。",
    "E": "提供 kernel 的表达层或运行时，本身不负责生成。",
    "F": "不提供代码，只提供领域导航。",
    "G": "只覆盖闭环中的一小段，没有形成完整的评测或生成闭环。",
}

SHAPE_ORDER = ["A", "B", "C", "D", "E", "F", "G"]

ROOT_FILES = ["README.md", "CHANGELOG.md", "LICENSE", "LICENSE-CONTENT"]


def classify_shape(repo):
    arch = repo.get("architecture") or {}
    role = arch.get("role")
    has_eval = bool((arch.get("eval_harness") or {}).get("present"))
    has_agent = bool((arch.get("agent_loop") or {}).get("present"))
    if role == "listicle":
        return "F"
    if role and role.startswith("foundation"):
        return "E"
    if role == "training-pipeline":
        return "D"
    if role == "agent-loop":
        return "C"
    if has_agent and has_eval:
        return "B"
    if has_eval:
        return "A"
    return "G"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_payload(index, architecture):
    repos = []
    arch_by_canonical = {a["canonical"].lower(): a for a in architecture["architectures"]}

    for r in index["repos"]:
        # 站点数据不做转义：JSON 以 application/json 提供，不会被当成 HTML 执行；
        # 渲染时由 app.js 的 esc() 负责转义，避免二次转义把 &lt; 显示成字面量。
        repo = {
            "canonical": r["canonical"],
            "url": r["url"],
            "org": r["org"],
            "org_type": r["org_type"],
            "description": r["description"],
            "license": r["license"],
            "primary_language": r["primary_language"],
            "stars": r["stars"],
            "forks": r["forks"],
            "pushed_at": r["pushed_at"],
            "group": r["group"],
            "group_label": r["group_label"],
            "task": r["task"],
            "summary": r["summary"],
            "hardware": r["hardware"],
            "languages": r["languages"],
            "methods": r["methods"],
            "feedback": r["feedback"],
            "benchmarks": r["benchmarks"],
            "root_dirs": r["root_dirs"],
            "aliases": r.get("aliases", []),
            "architecture": arch_by_canonical.get(r["canonical"].lower()),
        }
        repos.append(repo)

    shapes = defaultdict(list)
    for r in repos:
        shapes[classify_shape(r)].append(r["canonical"])
    shape_stats = [
        {
            "key": key,
            "name": key,
            "blurb": SHAPE_BLURBS.get(key, ""),
            "count": len(shapes.get(key, [])),
            "members": sorted(shapes.get(key, [])),
        }
        for key in SHAPE_ORDER
        if shapes.get(key)
    ]

    vendors = defaultdict(list)
    for r in repos:
        for h in r["hardware"]:
            vendors[h].append(r["canonical"])
    vendor_stats = [
        {"name": k, "count": len(v), "members": sorted(v)}
        for k, v in sorted(vendors.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    ]

    licenses = Counter(r["license"] or "未声明" for r in repos)
    license_stats = [
        {"name": k, "count": v} for k, v in licenses.most_common()
    ]

    languages = Counter(r["primary_language"] for r in repos if r["primary_language"])
    language_stats = [{"name": k, "count": v} for k, v in languages.most_common()]

    groups = Counter(r["group"] for r in repos if r["group"])
    group_stats = [
        {"name": k, "label": GROUP_LABELS.get(k, k), "count": v}
        for k, v in groups.most_common()
    ]

    feedback = Counter()
    for r in repos:
        for f in r["feedback"]:
            feedback[f] += 1
    feedback_stats = [{"name": k, "count": v} for k, v in feedback.most_common()]

    base_layers = defaultdict(list)
    for r in repos:
        arch = r.get("architecture") or {}
        if (arch.get("role") or "other") == "listicle":
            continue
        for b in arch.get("base_layer") or []:
            if b == "None":
                continue
            base_layers[b].append(r["canonical"])
    base_stats = [
        {"name": k, "count": len(v), "members": sorted(v)}
        for k, v in sorted(base_layers.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    ]

    hw_arch = defaultdict(list)
    for r in repos:
        for h in (r.get("architecture") or {}).get("hardware_arch") or []:
            hw_arch[h].append(r["canonical"])
    hw_stats = [
        {"name": k, "count": len(v), "members": sorted(v)}
        for k, v in sorted(hw_arch.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    ]

    roles = sorted(
        {
            (r.get("architecture") or {}).get("role") or "other"
            for r in repos
            if r.get("architecture")
        }
    )
    matrix_rows = []
    for vendor in sorted(vendors):
        counts = [
            sum(
                1
                for r in repos
                if vendor in r["hardware"]
                and ((r.get("architecture") or {}).get("role") or "other") == role
            )
            for role in roles
        ]
        matrix_rows.append(
            {"vendor": vendor, "counts": counts, "total": sum(counts)}
        )

    practices = {
        r["canonical"]: len((r.get("architecture") or {}).get("engineering_practices") or [])
        for r in repos
    }
    practice_total = sum(practices.values())

    return {
        "meta": {
            "landscape_snapshot": index.get("landscape_snapshot"),
            "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
            "source": "AI4Kernel Landscape",
        },
        "counts": {
            "repos": len(repos),
            "hf": len(index["huggingface"]),
            "other": len(index["other_hosts"]),
            "total": len(repos) + len(index["huggingface"]) + len(index["other_hosts"]),
            "practices": practice_total,
            "with_work": sum(1 for r in repos if r["group"]),
        },
        "repos": repos,
        "huggingface": index["huggingface"],
        "other_hosts": index["other_hosts"],
        "stats": {
            "shapes": shape_stats,
            "vendors": vendor_stats,
            "licenses": license_stats,
            "languages": language_stats,
            "groups": group_stats,
            "feedback": feedback_stats,
            "base_layers": base_stats,
            "hw_arch": hw_stats,
            "matrix": {"roles": roles, "rows": matrix_rows},
        },
    }


def build_site(root, out_dir, site_url):
    index = load(os.path.join(root, "data", "repos.json"))
    architecture = load(os.path.join(root, "data", "architecture.json"))
    payload = build_payload(index, architecture)

    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "docs"), exist_ok=True)

    shutil.copytree(
        os.path.join(root, "site", "assets"),
        os.path.join(out_dir, "assets"),
    )
    shutil.copyfile(os.path.join(root, "site", "index.html"), os.path.join(out_dir, "index.html"))

    for name in ROOT_FILES:
        src = os.path.join(root, name)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(out_dir, name))

    for name in os.listdir(os.path.join(root, "docs")):
        if name.endswith(".md"):
            shutil.copyfile(
                os.path.join(root, "docs", name), os.path.join(out_dir, "docs", name)
            )

    with open(os.path.join(out_dir, "data", "site-data.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")

    with open(os.path.join(out_dir, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")

    robots = f"User-agent: *\nAllow: /\nSitemap: {site_url.rstrip('/')}/sitemap.xml\n"
    with open(os.path.join(out_dir, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{site_url.rstrip('/')}/</loc></url>
  <url><loc>{site_url.rstrip('/')}/docs/01-repo-index.md</loc></url>
  <url><loc>{site_url.rstrip('/')}/docs/02-engineering-knowledge.md</loc></url>
  <url><loc>{site_url.rstrip('/')}/docs/03-comparison.md</loc></url>
</urlset>
"""
    with open(os.path.join(out_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    return payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="dist")
    ap.add_argument(
        "--site-url",
        default="https://yifeistarwang-coder.github.io/ai4kernel-opensource",
    )
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    out_dir = os.path.abspath(os.path.join(root, args.out))
    payload = build_site(root, out_dir, args.site_url)

    size = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, _, fs in os.walk(out_dir)
        for f in fs
    )
    print(
        f"site built: {len(payload['repos'])} repos, "
        f"{payload['counts']['practices']} practices, "
        f"{size / 1024:.0f} KiB -> {out_dir}"
    )


if __name__ == "__main__":
    main()
