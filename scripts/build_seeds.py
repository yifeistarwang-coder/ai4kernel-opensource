#!/usr/bin/env python3
"""从 ai4kernel_landscape 的数据层提取开源仓库种子清单。

landscape 仓把仓库 URL 分散在三处：
  - data/catalog.json  的 sources[]（type == "repository"），带 sha256 核查快照
  - data/curation.json 的每个 work 的 repo / repo_url / hf 字段
  - data/catalog.json  的 sources[]（type == "model" / "dataset"），对应 HuggingFace 产物

本脚本把它们合并成一份与 work 关联的种子清单，作为本仓所有下游生成的输入。
"""

import argparse
import json
import os
import re
import sys

GITHUB_REPO_RE = re.compile(r"^https?://github\.com/([^/]+)/([^/#?]+)/?$")
HF_REPO_RE = re.compile(r"^https?://huggingface\.co/([^/]+)/([^/#?]+)/?$")

LANDSCAPE_DEFAULT = "../ai4kernel_landscape"


def strip_github_suffix(slug):
    """GitHub API 接受 owner/repo 或 owner/repo/path，本仓只取前两段。"""
    return "/".join(slug.split("/")[:2])


def collect(catalog, curation):
    """返回 (github_seeds, hf_seeds, non_github_seeds)。"""
    github = {}
    hf = {}
    other = {}

    def add(bucket, key, entry):
        bucket.setdefault(key, {"slug": key, "work_ids": [], "source_ids": []})
        for field in ("work_ids", "source_ids"):
            for item in entry.get(field) or []:
                if item not in bucket[key][field]:
                    bucket[key][field].append(item)

    for src in catalog.get("sources", []):
        stype = src.get("type")
        url = src.get("url") or ""
        if stype == "repository":
            m = GITHUB_REPO_RE.match(url.rstrip("/"))
            if m:
                slug = f"{m.group(1)}/{m.group(2)}"
                add(github, slug, {"source_ids": [src["id"]]})
            else:
                add(other, url, {"source_ids": [src["id"]]})
        elif stype in ("model", "dataset"):
            m = HF_REPO_RE.match(url.rstrip("/"))
            if m:
                slug = f"{m.group(1)}/{m.group(2)}"
                add(hf, slug, {"source_ids": [src["id"]]})

    for work in curation:
        wid = work["id"]
        repo = work.get("repo")
        if repo:
            add(github, strip_github_suffix(repo), {"work_ids": [wid]})
        repo_url = work.get("repo_url")
        if repo_url and not GITHUB_REPO_RE.match(repo_url.rstrip("/")):
            add(other, repo_url, {"work_ids": [wid]})
        hf_id = work.get("hf")
        if hf_id:
            add(hf, hf_id.strip("/"), {"work_ids": [wid]})

    # work -> repository source 反向关联，让 github 种子也能挂到 work 上
    work_by_id = {w["id"]: w for w in curation}
    for src in catalog.get("sources", []):
        if src.get("type") != "repository":
            continue
        m = GITHUB_REPO_RE.match((src.get("url") or "").rstrip("/"))
        if not m:
            continue
        slug = f"{m.group(1)}/{m.group(2)}"
        for work in catalog.get("works", []):
            if src["id"] in (work.get("source_ids") or []):
                if work["id"] not in github[slug]["work_ids"]:
                    github[slug]["work_ids"].append(work["id"])

    # work 侧的 repo 字段可能与 source 侧 slug 不同（仓库换 org），用 work 关联兜底
    src_to_work = {}
    for work in catalog.get("works", []):
        for sid in work.get("source_ids") or []:
            src_to_work.setdefault(sid, []).append(work["id"])
    for slug, entry in list(github.items()):
        for sid in entry["source_ids"]:
            for wid in src_to_work.get(sid, []):
                if wid not in entry["work_ids"]:
                    entry["work_ids"].append(wid)

    return github, hf, other


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--landscape", default=os.environ.get("LANDSCAPE_DIR", LANDSCAPE_DEFAULT))
    ap.add_argument("--out", default="data/seeds.json")
    args = ap.parse_args()

    catalog_path = os.path.join(args.landscape, "data", "catalog.json")
    curation_path = os.path.join(args.landscape, "data", "curation.json")
    for p in (catalog_path, curation_path):
        if not os.path.exists(p):
            sys.exit(f"missing landscape data file: {p}")

    with open(catalog_path, encoding="utf-8") as f:
        catalog = json.load(f)
    with open(curation_path, encoding="utf-8") as f:
        curation = json.load(f)

    github, hf, other = collect(catalog, curation)

    # 一个 work 可能同时声明 repo 与 hf，或只有其一；把 work 列表一并记录
    out = {
        "landscape_snapshot": catalog.get("snapshot"),
        "landscape_version": catalog.get("version"),
        "github": sorted(github.values(), key=lambda e: e["slug"].lower()),
        "huggingface": sorted(hf.values(), key=lambda e: e["slug"].lower()),
        "other_hosts": sorted(other.values(), key=lambda e: e["slug"].lower()),
        "counts": {
            "github": len(github),
            "huggingface": len(hf),
            "other_hosts": len(other),
            "works_with_repo": sum(1 for w in curation if w.get("repo") or w.get("repo_url")),
            "works_total": len(curation),
        },
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps(out["counts"], indent=2))


if __name__ == "__main__":
    main()
