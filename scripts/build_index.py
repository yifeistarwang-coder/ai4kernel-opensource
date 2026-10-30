#!/usr/bin/env python3
"""合并 landscape 数据层与 GitHub 元数据，产出开源仓库索引。

输入:
  data/seeds.json             由 build_seeds.py 生成（landscape 侧的仓库/产物线索）
  data/github-metadata.json   由 fetch_metadata.py 生成（GitHub API 快照）
  ../ai4kernel_landscape/data/curation.json   每个 work 的分类、硬件、方法、反馈等
输出:
  data/repos.json  合并后的索引（机器可读）
  data/repos.csv   扁平表格（电子表格/BI 友好）
"""

import argparse
import csv
import glob
import json
import os
import sys
from collections import defaultdict

LANDSCAPE_DEFAULT = "../ai4kernel_landscape"

GROUP_LABELS = {
    "benchmark": "评测与验证",
    "search": "搜索与优化",
    "agent": "Agent 与环境",
    "training": "训练、模型与数据",
    "foundation": "执行与知识底座",
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build(landscape, seeds, gh_meta):
    curation = {w["id"]: w for w in load(os.path.join(landscape, "data", "curation.json"))}
    catalog = load(os.path.join(landscape, "data", "catalog.json"))

    work_by_id = {w["id"]: w for w in catalog["works"]}
    publication = {}
    for pub in load(os.path.join(landscape, "data", "work-publication.json")):
        publication[pub["work_id"]] = pub

    # work 之间的关系：evaluated_on / uses / trained_on，构成项目间的依赖边
    relations = defaultdict(list)
    rel_dir = os.path.join(landscape, "data")
    for path in sorted(glob.glob(os.path.join(rel_dir, "relations-*.json"))):
        for rel in load(path):
            relations[rel["from"]].append(
                {
                    "to": rel["to"],
                    "type": rel["type"],
                    "kind": rel.get("kind"),
                    "note": rel.get("note"),
                }
            )

    # 同一仓库可能以旧 org 名出现在 landscape 数据里；gh API 会把它解析到 canonical 名
    gh_by_slug = {}
    for entry in gh_meta["github"]:
        gh_by_slug[entry["slug"].lower()] = entry
        gh_by_slug[entry["canonical"].lower()] = entry

    repos = []
    merged = {}
    for seed in seeds["github"]:
        slug = seed["slug"]
        gh = gh_by_slug.get(slug.lower())
        canonical = gh["canonical"] if gh else slug
        if canonical in merged:
            merged[canonical]["work_ids"].extend(
                w for w in seed["work_ids"] if w not in merged[canonical]["work_ids"]
            )
            merged[canonical]["referenced_slugs"].append(slug)
            continue
        merged[canonical] = {
            "canonical": canonical,
            "referenced_slugs": [slug],
            "work_ids": list(seed["work_ids"]),
            "gh": gh,
        }

    for canonical, m in merged.items():
        gh = m["gh"]
        work_ids = m["work_ids"]

        works = []
        for wid in work_ids:
            w = work_by_id.get(wid)
            c = curation.get(wid)
            if not w:
                continue
            pub = publication.get(wid, {})
            works.append(
                {
                    "work_id": wid,
                    "name": w.get("name") or c.get("name"),
                    "group": w.get("group") or c.get("group"),
                    "group_label": GROUP_LABELS.get(w.get("group") or c.get("group"), ""),
                    "roles": w.get("roles") or c.get("roles") or [],
                    "task": w.get("task") or c.get("task"),
                    "summary": w.get("summary") or c.get("summary"),
                    "contribution": w.get("contribution") or c.get("contribution"),
                    "limitations": w.get("limitations") or c.get("limitations"),
                    "hardware": w.get("hardware") or c.get("hardware") or [],
                    "languages": w.get("languages") or c.get("languages") or [],
                    "methods": w.get("methods") or c.get("methods") or [],
                    "feedback": w.get("feedback") or c.get("feedback") or [],
                    "benchmarks": w.get("benchmarks") or c.get("benchmarks") or [],
                    "training": w.get("training") or c.get("training"),
                    "budget": w.get("budget") or c.get("budget"),
                    "paper_id": pub.get("source_url"),
                    "paper_venue": pub.get("publication_label"),
                    "relations": relations.get(wid, []),
                }
            )

        primary = works[0] if works else {}
        dirs = [e["name"] for e in (gh or {}).get("root_entries", []) if e["type"] == "dir"]
        aliases = sorted(s for s in set(m["referenced_slugs"]) if s != canonical)

        repos.append(
            {
                "canonical": canonical,
                "referenced_slug": aliases[0] if aliases else None,
                "aliases": aliases,
                "url": (gh or {}).get("html_url") or f"https://github.com/{canonical}",
                "org": (gh or {}).get("owner_login") or canonical.split("/")[0],
                "org_type": (gh or {}).get("owner_type"),
                "description": (gh or {}).get("description"),
                "homepage": (gh or {}).get("homepage"),
                "license": (gh or {}).get("license"),
                "license_name": (gh or {}).get("license_name"),
                "primary_language": (gh or {}).get("primary_language"),
                "language_breakdown": (gh or {}).get("language_breakdown", []),
                "stars": (gh or {}).get("stars"),
                "forks": (gh or {}).get("forks"),
                "open_issues": (gh or {}).get("open_issues"),
                "created_at": (gh or {}).get("created_at"),
                "pushed_at": (gh or {}).get("pushed_at"),
                "archived": (gh or {}).get("archived"),
                "is_fork": (gh or {}).get("is_fork"),
                "topics": (gh or {}).get("topics", []),
                "root_dirs": dirs,
                "group": primary.get("group"),
                "group_label": primary.get("group_label"),
                "task": primary.get("task"),
                "summary": primary.get("summary"),
                "hardware": primary.get("hardware", []),
                "languages": primary.get("languages", []),
                "methods": primary.get("methods", []),
                "feedback": primary.get("feedback", []),
                "benchmarks": primary.get("benchmarks", []),
                "work_ids": work_ids,
                "works": works,
            }
        )

    # HuggingFace 产物：模型与数据集同样属于开源交付
    hf = []
    for seed in seeds["huggingface"]:
        for wid in seed["work_ids"]:
            c = curation.get(wid)
            if not c:
                continue
            hf.append(
                {
                    "canonical": seed["slug"],
                    "url": f"https://huggingface.co/{seed['slug']}",
                    "kind": c.get("hfKind") or "model",
                    "work_id": wid,
                    "name": c.get("name"),
                    "group": c.get("group"),
                    "group_label": GROUP_LABELS.get(c.get("group"), ""),
                    "task": c.get("task"),
                    "summary": c.get("summary"),
                    "hardware": c.get("hardware", []),
                    "languages": c.get("languages", []),
                    "source_ids": seed["source_ids"],
                }
            )

    other = []
    for seed in seeds["other_hosts"]:
        for wid in seed["work_ids"]:
            c = curation.get(wid)
            other.append(
                {
                    "url": seed["slug"],
                    "work_id": wid,
                    "name": (c or {}).get("name"),
                    "group": (c or {}).get("group"),
                    "group_label": GROUP_LABELS.get((c or {}).get("group"), ""),
                    "summary": (c or {}).get("summary"),
                    "hardware": (c or {}).get("hardware", []),
                    "source_ids": seed["source_ids"],
                }
            )

    repos.sort(key=lambda r: (r["group"] or "zzz", r["canonical"].lower()))
    return repos, hf, other


def write_csv(path, repos):
    cols = [
        "canonical",
        "org",
        "org_type",
        "group",
        "group_label",
        "task",
        "license",
        "primary_language",
        "hardware",
        "languages",
        "methods",
        "feedback",
        "benchmarks",
        "work_ids",
        "stars",
        "forks",
        "pushed_at",
        "archived",
        "url",
        "description",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in repos:
            w.writerow(
                {
                    "canonical": r["canonical"],
                    "org": r["org"],
                    "org_type": r["org_type"],
                    "group": r["group"],
                    "group_label": r["group_label"],
                    "task": r["task"],
                    "license": r["license"] or "",
                    "primary_language": r["primary_language"] or "",
                    "hardware": "|".join(r["hardware"]),
                    "languages": "|".join(r["languages"]),
                    "methods": "|".join(r["methods"]),
                    "feedback": "|".join(r["feedback"]),
                    "benchmarks": "|".join(r["benchmarks"]),
                    "work_ids": "|".join(r["work_ids"]),
                    "stars": r["stars"] if r["stars"] is not None else "",
                    "forks": r["forks"] if r["forks"] is not None else "",
                    "pushed_at": r["pushed_at"] or "",
                    "archived": "yes" if r["archived"] else "no",
                    "url": r["url"],
                    "description": (r["description"] or "").replace("\n", " "),
                }
            )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--landscape", default=os.environ.get("LANDSCAPE_DIR", LANDSCAPE_DEFAULT))
    ap.add_argument("--seeds", default="data/seeds.json")
    ap.add_argument("--github", default="data/github-metadata.json")
    ap.add_argument("--out", default="data/repos.json")
    ap.add_argument("--csv", default="data/repos.csv")
    args = ap.parse_args()

    seeds = load(args.seeds)
    gh_meta = load(args.github)
    repos, hf, other = build(args.landscape, seeds, gh_meta)

    payload = {
        "schema": 1,
        "landscape_snapshot": seeds.get("landscape_snapshot"),
        "counts": {
            "github_repos": len(repos),
            "huggingface_artifacts": len(hf),
            "other_host_artifacts": len(other),
        },
        "repos": repos,
        "huggingface": hf,
        "other_hosts": other,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    write_csv(args.csv, repos)
    print(json.dumps(payload["counts"], indent=2))


if __name__ == "__main__":
    main()
