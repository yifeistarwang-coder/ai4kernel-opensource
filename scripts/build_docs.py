#!/usr/bin/env python3
"""从合并索引与架构事实生成 Markdown 文档。

输入:
  data/repos.json                  build_index.py 产出
  data/architecture/batch*.json     各 README 批次抽取的架构事实
输出:
  docs/01-repo-index.md            开源仓库索引
  docs/03-comparison.md            项目对比（架构 / 基础 / 硬件厂商 / 硬件架构）
  data/architecture.json           合并后的架构事实（机器可读）
"""

import argparse
import glob
import json
import os
from collections import Counter, defaultdict

GROUP_ORDER = ["foundation", "benchmark", "search", "agent", "training"]
GROUP_LABELS = {
    "benchmark": "评测与验证",
    "search": "搜索与优化",
    "agent": "Agent 与环境",
    "training": "训练、模型与数据",
    "foundation": "执行与知识底座",
}
ROLE_LABELS = {
    "foundation-runtime": "执行运行时底座",
    "foundation-compiler": "编译器底座",
    "foundation-dsl": "DSL / kernel 表达层",
    "training-pipeline": "训练流水线",
    "agent-loop": "Agent 搜索循环",
    "benchmark": "评测基准",
    "dataset-or-model": "数据集 / 模型",
    "listicle": "综述清单",
    "other": "其他",
}
VENDOR_LABELS = {
    "NVIDIA": "NVIDIA",
    "AMD": "AMD",
    "Ascend": "华为昇腾",
    "TPU": "Google TPU",
    "CPU": "CPU",
    "Intel": "Intel",
    "Meta": "Meta",
    "Tenstorrent": "Tenstorrent",
    "Other": "其他",
}
HW_ARCH_LABELS = {
    "NVIDIA-GPU-Hopper": "NVIDIA Hopper (H100/H200)",
    "NVIDIA-GPU-Ampere": "NVIDIA Ampere (A100)",
    "NVIDIA-GPU-Blackwell": "NVIDIA Blackwell (B200)",
    "NVIDIA-GPU-Ada": "NVIDIA Ada (L40S/4090)",
    "NVIDIA-GPU-Volta": "NVIDIA Volta (V100)",
    "AMD-GPU-CDG": "AMD CDNA (MI100/MI200)",
    "AMD-GPU-MI300": "AMD CDNA 3 (MI300X)",
    "AMD-GPU-RDNA": "AMD RDNA (Radeon)",
    "Ascend-Ascend910B": "昇腾 910B",
    "Ascend-Ascend910C": "昇腾 910C",
    "Ascend-Ascend950": "昇腾 950PR",
    "TPU-v4": "TPU v4",
    "TPU-v5": "TPU v5",
    "TPU-v5p": "TPU v5p",
    "TPU-v6e": "TPU v6e",
    "CPU-x86": "x86 CPU",
    "CPU-arm": "ARM CPU",
    "Unknown": "未标注",
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def merge_architecture(repos, batch_files):
    arch = {}
    for path in sorted(batch_files):
        for rec in load(path):
            arch[rec["canonical"].lower()] = rec
    for r in repos:
        r["architecture"] = arch.get(r["canonical"].lower())
    return arch


def esc(text):
    return (text or "").replace("|", "\\|")


def link(url, text=None):
    return f"[{text or url}]({url})"


def repo_label(r):
    return f"`{r['canonical']}`"


def group_of(r):
    return r.get("group") or "other"


def sorted_groups(repos):
    order = {g: i for i, g in enumerate(GROUP_ORDER)}
    return sorted(repos, key=lambda r: (order.get(group_of(r), 99), r["canonical"].lower()))


# ---------------------------------------------------------------- 文档 01


def doc_repo_index(repos, hf, other, snapshot):
    out = []
    out.append("# 开源仓库索引\n")
    out.append(
        "本索引收录 [AI4Kernel Landscape](https://github.com/yifeistarwang-coder/ai4kernel_landscape) "
        f"研究目录中**已公开开源**的全部产物。landscape 快照日期 `{snapshot}`。\n"
    )
    out.append(
        "> **口径说明**：本索引只收录**有可核查公开仓库地址**的条目。"
        "收录不代表代码质量、许可兼容性或可复现性已经过审阅；"
        "许可一列是 GitHub API 对仓库默认许可证的识别结果，"
        "`NOASSERTION` 表示仓库内有许可证文件但 API 未能归一化，"
        "空白表示仓库未声明许可证——使用前必须自行核对上游 `LICENSE`。\n"
    )

    out.append("## 统计\n")
    out.append("| 维度 | 数量 |")
    out.append("| --- | ---: |")
    out.append(f"| GitHub 仓库（去重后） | {len(repos)} |")
    out.append(f"| HuggingFace 模型 / 数据集 | {len(hf)} |")
    out.append(f"| 其他平台仓库 | {len(other)} |")
    out.append(f"| 合计开源产物 | {len(repos) + len(hf) + len(other)} |")
    out.append("")

    lic = Counter(r["license"] or "未声明" for r in repos)
    out.append("## 许可证分布\n")
    out.append("| 许可证 | 仓库数 |")
    out.append("| --- | ---: |")
    for k, v in lic.most_common():
        out.append(f"| `{k}` | {v} |")
    out.append("")

    orgs = Counter(r["org"] for r in repos)
    out.append("## 组织分布\n")
    out.append("| 组织 | 仓库数 |")
    out.append("| --- | ---: |")
    for k, v in orgs.most_common():
        out.append(f"| {link(f'https://github.com/{k}', k)} | {v} |")
    out.append("")

    out.append("## 按分类\n")
    grouped = defaultdict(list)
    for r in sorted_groups(repos):
        grouped[group_of(r)].append(r)
    for g in GROUP_ORDER:
        if g not in grouped:
            continue
        items = grouped[g]
        out.append(f"### {GROUP_LABELS.get(g, g)}（{len(items)}）\n")
        out.append("| 仓库 | 许可 | 主语言 | 硬件 | 任务 | 星标 | 说明 |")
        out.append("| --- | --- | --- | --- | --- | ---: | --- |")
        for r in items:
            hw = "、".join(r["hardware"]) or "—"
            task = esc((r["task"] or "—").replace("\n", " "))
            desc = esc((r["description"] or r["summary"] or "—").replace("\n", " "))
            desc = desc[:110] + ("…" if len(desc) > 110 else "")
            stars = r["stars"] if r["stars"] is not None else "—"
            out.append(
                f"| {link(r['url'], r['canonical'])} | `{r['license'] or '—'}` | "
                f"{r['primary_language'] or '—'} | {hw} | {task} | {stars} | {desc} |"
            )
        out.append("")

    if "other" in grouped:
        out.append(f"### 未归类（{len(grouped['other'])}）\n")
        out.append("| 仓库 | 许可 | 说明 |")
        out.append("| --- | --- | --- |")
        for r in grouped["other"]:
            desc = esc((r["description"] or "—").replace("\n", " "))
            out.append(f"| {link(r['url'], r['canonical'])} | `{r['license'] or '—'}` | {desc} |")
        out.append("")

    out.append("## HuggingFace 模型与数据集\n")
    out.append("模型权重与数据集同样属于开源交付物，但它们不是代码仓库，单列于此。\n")
    out.append("| 产物 | 类型 | 对应工作 | 硬件 | 说明 |")
    out.append("| --- | --- | --- | --- | --- |")
    for h in sorted(hf, key=lambda x: x["canonical"].lower()):
        desc = esc((h["summary"] or "—").replace("\n", " "))
        desc = desc[:100] + ("…" if len(desc) > 100 else "")
        out.append(
            f"| {link(h['url'], h['canonical'])} | {h['kind']} | "
            f"{h['name'] or h['work_id']} | {'、'.join(h['hardware']) or '—'} | {desc} |"
        )
    out.append("")

    if other:
        out.append("## 其他平台仓库\n")
        out.append("| 仓库 | 对应工作 | 说明 |")
        out.append("| --- | --- | --- |")
        for o in other:
            desc = esc((o["summary"] or "—").replace("\n", " "))
            out.append(f"| {link(o['url'], o['url'])} | {o['name'] or o['work_id']} | {desc} |")
        out.append("")

    out.append("## 重定向与改名\n")
    out.append("landscape 数据层里记录的仓库地址有 3 个与 GitHub 当前规范名不一致（组织改名或仓库迁移）。")
    out.append("GitHub 会自动重定向旧地址，但直接用规范名更可靠。\n")
    out.append("| landscape 中记录的地址 | GitHub 规范名 |")
    out.append("| --- | --- |")
    for r in repos:
        for a in r.get("aliases", []):
            out.append(f"| `{a}` | {link(r['url'], r['canonical'])} |")
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- 文档 03


def doc_comparison(repos, snapshot):
    out = []
    out.append("# 项目对比\n")
    out.append(
        "四个对比轴：**架构**（项目怎么搭）、**基础**（构建在什么之上）、"
        "**硬件厂商**（跑在谁的芯片上）、**硬件架构**（具体到哪一代芯片）。\n"
    )
    out.append(
        "表中每一格都来自可核查的公开材料：架构列来自仓库 README 与顶层目录结构，"
        "基础列来自仓库声明的依赖关系，硬件两列来自仓库文档与任务说明。"
        "空白表示公开材料未标注，不等于不支持。\n"
    )

    with_arch = [r for r in repos if r.get("architecture")]
    out.append("## 架构对比\n")
    out.append("### 架构模式分布\n")
    patterns = Counter(
        (r["architecture"].get("arch_pattern") or "未标注") for r in with_arch
    )
    out.append("| 架构模式 | 项目数 |")
    out.append("| --- | ---: |")
    for k, v in patterns.most_common():
        out.append(f"| {esc(k)} | {v} |")
    out.append("")

    out.append("### 项目角色分布\n")
    roles = Counter((r["architecture"].get("role") or "other") for r in with_arch)
    out.append("| 角色 | 项目数 |")
    out.append("| --- | ---: |")
    for k, v in roles.most_common():
        out.append(f"| {ROLE_LABELS.get(k, k)} | {v} |")
    out.append("")

    out.append("### 全量对照\n")
    out.append("| 项目 | 角色 | 架构模式 | 评测 | Agent 循环 | 验证机制 |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for r in sorted_groups(with_arch):
        a = r["architecture"]
        ev = a.get("eval_harness", {})
        al = a.get("agent_loop", {})
        vf = a.get("verification", {})
        out.append(
            f"| {link(r['url'], r['canonical'])} | {ROLE_LABELS.get(a.get('role'), a.get('role'))} | "
            f"{esc(a.get('arch_pattern') or '—')} | {'有' if ev.get('present') else '无'} | "
            f"{'有' if al.get('present') else '无'} | "
            f"{'、'.join(vf.get('mechanisms') or []) or '—'} |"
        )
    out.append("")

    out.append("## 基础层对比\n")
    out.append(
        "「基础」指项目直接构建其上的 kernel 表达层或运行时。"
        "同一个项目可能同时依赖多个（例如以 Triton 为主、同时支持 CUDA C++ 兜底）。\n"
    )
    base = Counter()
    base_map = defaultdict(list)
    for r in with_arch:
        # 综述清单不构建在任何底座上，它列出的基础层是「领域在用什么」，不是「自己建在什么上」
        if (r["architecture"].get("role") or "other") == "listicle":
            continue
        for b in r["architecture"].get("base_layer") or []:
            if b == "None":
                continue
            base[b] += 1
            base_map[b].append(r["canonical"])
    out.append("| 基础层 | 项目数 | 使用该基础的项目 |")
    out.append("| --- | ---: | --- |")
    for k, v in base.most_common():
        names = "、".join(f"`{x}`" for x in sorted(base_map[k]))
        out.append(f"| {k} | {v} | {names} |")
    out.append("")

    out.append("### 项目之间的依赖\n")
    out.append(
        "上表讲的是「构建在哪个底座上」，这里讲的是「直接依赖哪个项目」。"
        "依赖方向几乎全是单向的：生成类项目依赖评测类项目，评测类项目不依赖生成类项目。\n"
    )
    edges = []
    for r in repos:
        for w in r["works"]:
            for rel in w.get("relations") or []:
                edges.append((r["canonical"], rel["type"], rel["to"], w["work_id"]))
    if edges:
        out.append("| 依赖方仓库 | 关系 | 被依赖的工作 |")
        out.append("| --- | --- | --- |")
        for canon, rtype, to, wid in sorted(edges):
            out.append(f"| {link(next(x['url'] for x in repos if x['canonical'] == canon), canon)} | `{rtype}` | `{to}` |")
        out.append("")
        targets = Counter(e[2] for e in edges)
        out.append(
            "被依赖最多的是 "
            + "、".join(f"`{k}`（{v} 次）" for k, v in targets.most_common())
            + "。这说明大部分生成系统的能力度量，最终都落在同一个公共任务集上。\n"
        )
    else:
        out.append("公开材料中未记录开源项目之间的直接依赖关系。\n")

    out.append("## 硬件厂商对比\n")
    out.append(
        "厂商维度回答的是「这条路在哪个生态里被验证过」。"
        "非 NVIDIA 生态的项目数量明显更少，且多数集中在评测而非生成闭环。\n"
    )
    vendor = Counter()
    vendor_map = defaultdict(list)
    for r in repos:
        for h in r["hardware"] or []:
            vendor[h] += 1
            vendor_map[h].append(r["canonical"])
    out.append("| 厂商 | 项目数 | 项目 |")
    out.append("| --- | ---: | --- |")
    for k, v in vendor.most_common():
        names = "、".join(f"`{x}`" for x in sorted(vendor_map[k]))
        out.append(f"| {VENDOR_LABELS.get(k, k)} | {v} | {names} |")
    out.append("")

    out.append("## 硬件架构对比\n")
    out.append(
        "具体到芯片代际的分布。绝大多数项目只写「一张 NVIDIA GPU」，"
        "能定位到具体代际的是少数，这也解释了为什么跨项目对比加速比并不可靠。\n"
    )
    hw_arch = Counter()
    hw_map = defaultdict(list)
    for r in with_arch:
        for h in r["architecture"].get("hardware_arch") or []:
            hw_arch[h] += 1
            hw_map[h].append(r["canonical"])
    out.append("| 硬件架构 | 项目数 | 项目 |")
    out.append("| --- | ---: | --- |")
    for k, v in hw_arch.most_common():
        names = "、".join(f"`{x}`" for x in sorted(hw_map[k]))
        out.append(f"| {HW_ARCH_LABELS.get(k, k)} | {v} | {names} |")
    out.append("")

    out.append("## 厂商 × 角色交叉\n")
    out.append("把「硬件厂商」和「架构角色」交叉，能看出每个生态里开源的是哪一层。\n")
    roles_present = sorted({(r["architecture"].get("role") or "other") for r in with_arch})
    role_cols = [ROLE_LABELS.get(r, r) for r in roles_present]
    out.append("| 厂商 | " + " | ".join(role_cols) + " | 合计 |")
    out.append("| --- |" + " |".join([" ---:"] * len(role_cols)) + " | ---: |")
    vendors = sorted(vendor.keys())
    for v in vendors:
        counts = []
        for role in roles_present:
            n = sum(
                1
                for r in with_arch
                if v in (r["hardware"] or []) and (r["architecture"].get("role") or "other") == role
            )
            counts.append(n)
        out.append(
            f"| {VENDOR_LABELS.get(v, v)} | " + " | ".join(str(c) for c in counts) + f" | {sum(counts)} |"
        )
    out.append("")

    out.append("## 单项目档案\n")
    for r in sorted_groups(with_arch):
        a = r["architecture"]
        out.append(f"### {link(r['url'], r['canonical'])}\n")
        out.append(f"{r['description'] or r['summary'] or '—'}\n")
        is_listicle = (a.get("role") or "other") == "listicle"
        base_display = (
            "—（综述清单，不构建于底座）"
            if is_listicle
            else ("、".join(a.get("base_layer") or []) or "—")
        )
        rows = [
            ("角色", ROLE_LABELS.get(a.get("role"), a.get("role"))),
            ("架构模式", a.get("arch_pattern")),
            ("入口", "、".join(f"`{e}`" for e in a.get("entrypoints") or []) or "—"),
            ("基础层", base_display),
            ("硬件厂商", "、".join(r["hardware"]) or "—"),
            ("硬件架构", "、".join(HW_ARCH_LABELS.get(h, h) for h in a.get("hardware_arch") or []) or "—"),
            ("评测", (a.get("eval_harness") or {}).get("design_zh") if (a.get("eval_harness") or {}).get("present") else "无"),
            ("验证机制", "、".join((a.get("verification") or {}).get("mechanisms") or []) or "—"),
            ("Agent 循环", "有" if (a.get("agent_loop") or {}).get("present") else "无"),
            ("许可", r.get("license") or "未声明"),
            ("星标", str(r.get("stars") if r.get("stars") is not None else "—")),
            ("最近推送", (r.get("pushed_at") or "—")[:10]),
        ]
        out.append("| 项 | 内容 |")
        out.append("| --- | --- |")
        for k, v in rows:
            out.append(f"| {k} | {esc(v) or '—'} |")
        out.append("")
        if a.get("arch_notes_zh"):
            out.append(f"> {a['arch_notes_zh']}\n")
    return "\n".join(out)


def classify_shape(r):
    """从结构化字段推导项目所属的架构形态。"""
    a = r.get("architecture") or {}
    role = a.get("role")
    has_eval = bool((a.get("eval_harness") or {}).get("present"))
    has_agent = bool((a.get("agent_loop") or {}).get("present"))
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


SHAPES = {
    "A": {
        "name": "形态 A：纯评测基准",
        "definition": "只做「给定任务 → 产出结果 → 打分」，不负责生成 kernel 本身。",
        "anatomy": "任务集（目录或 JSON）+ 候选提交入口 + 参考实现 + 判定器 + 基线与指标。",
        "reuse": "把任务集与判定器彻底解耦成两个目录，任务集可以替换而判定逻辑不动；"
        "基线版本必须写进结果文件，否则跨版本不可比。",
    },
    "B": {
        "name": "形态 B：评测 + Agent 平台",
        "definition": "在基准之上叠加可插拔的 Agent 与执行环境，用来横向比较不同 Agent 策略。",
        "anatomy": "基准任务集 + Agent 适配层 + 隔离执行环境 + 统一打分器 + 多次运行的统计。",
        "reuse": "Agent 与任务集通过配置解耦，同一任务集能跑不同 Agent；"
        "执行环境容器化并锁定驱动版本，否则 Agent 之间的差异会被环境差异吃掉。",
    },
    "C": {
        "name": "形态 C：Agent 生成闭环",
        "definition": "自己带生成循环：模型提出候选 → 编译/测试 → 读取反馈 → 迭代。",
        "anatomy": "提示与模板 + 生成器 + 工具接口（编译、跑测试、profile）+ 循环控制器 + 反馈解析。",
        "reuse": "把「工具」抽象成统一接口（输入 kernel 源码，输出结构化反馈），"
        "循环控制器与具体工具解耦，这样换编译器或换硬件只改工具实现。",
    },
    "D": {
        "name": "形态 D：训练流水线",
        "definition": "不只做推理时搜索，而是产出可分发的模型权重或数据集。",
        "anatomy": "数据构造/清洗 + 继续预训练或 SFT + RL 环境与奖励 + 推理配方 + 评测脚本。",
        "reuse": "训练环境和评测环境共用同一套编译执行后端，避免训练时看到的 kernel "
        "在评测时编译行为不同；奖励函数单独成模块以便替换。",
    },
    "E": {
        "name": "形态 E：执行底座",
        "definition": "提供 kernel 的表达层或运行时，本身不负责生成。",
        "anatomy": "DSL/编译器 + 算子库 + 调度/内存层 + 多后端适配 + 基准与文档。",
        "reuse": "底座决定「可生成的 kernel 空间」，"
        "上层生成器的工作量与底座 DSL 的表达能力直接相关；先定底座再写生成器。",
    },
    "F": {
        "name": "形态 F：综述清单",
        "definition": "不提供代码，只提供领域导航。",
        "anatomy": "分类目录 + 条目链接 + 简短说明。",
        "reuse": "作为查表入口，不作为工程依赖；引用其中的条目时回到原始仓库核实。",
    },
    "G": {
        "name": "形态 G：其他 / 单一功能工具",
        "definition": "只覆盖闭环中的一小段，没有形成完整的评测或生成闭环。",
        "anatomy": "视项目而定，通常是单个脚本或单一能力包。",
        "reuse": "适合作为参考实现片段借鉴，不适合作为项目骨架。",
    },
}

LAYERS = [
    (
        "L1 任务与规格层",
        "定义「要优化哪个算子」：参考实现、输入 shape、dtype、语义边界、正确性判据。",
        "判据：仓库里能找到一个可枚举的任务集合，并且任务定义不依赖运行时。",
    ),
    (
        "L2 生成层",
        "产出候选 kernel：专用模型、推理时搜索、Agent 工具循环、或它们的组合。",
        "判据：仓库里存在一个能接受任务并返回 kernel 源码的接口。",
    ),
    (
        "L3 表达层",
        "决定候选写成什么语言/DSL：Triton、CUDA C++、TileLang、HIP、AscendC、MUSA。",
        "判据：仓库的构建产物是编译器、Python 扩展或算子包，而非纯脚本。",
    ),
    (
        "L4 编译与执行层",
        "把源码编译成设备代码并运行：编译器驱动、运行时、内存管理、调度。",
        "判据：仓库能独立完成「编译 → 执行」而不需要上层框架。",
    ),
    (
        "L5 验证层",
        "判断候选是否正确、是否更快：编译检查、参考输出比对、运行时计时、profiling。",
        "判据：仓库里有独立的验证/打分模块，且能对任意候选单独调用。",
    ),
    (
        "L6 评测与度量层",
        "组织任务、跑多次、汇总指标、给出基线与阈值。",
        "判据：仓库能独立产出一份评测报告，而不只是单次运行结果。",
    ),
    (
        "L7 训练层",
        "把数据与反馈变成可分发的模型：继续预训练、SFT、RL、偏好数据。",
        "判据：仓库产出权重或数据集，且带训练脚本与评测脚本。",
    ),
]

PRACTICE_THEMES = [
    (
        "评测与优化分离",
        [
            "评测与优化分离", "评估与优化分离", "生成与评测拆", "评测与生成", "解耦", "分离",
            "独立编译", "平台独立", "优化器产出", "只负责评估", "只负责生成", "grader 与",
            "judger", "judge", "评分器", "grader", "校验与计时", "独立校验",
        ],
        "把「产生候选」和「判定候选」拆成互不信任的两半，是这批项目里最值得抄的一条。",
    ),
    (
        "正确性防线",
        [
            "反作弊", "作弊", "reward-hacking", "reward hacking", "篡改", "tamper", "硬编码",
            "上限", "AST", "对抗", "隐藏", "held-out", "泛化评测", "容差", "tolerance",
            "精度", "数值", "契约", "contract", "语义", "边界用例", "正确性",
        ],
        "正确性判据要和性能判据同等对待，且需要防住「看起来通过」的作弊路径。",
    ),
    (
        "反馈信号升级",
        [
            "profile", "profiler", "ncu", "nsys", "nsight", "热点", "瓶颈", "瓶颈分析",
            "SOL", "指标", "原始指标", "性能计数器", "瓶颈定位", "逐级", "逐层", "精细",
            "Amdahl", "杠杆", "patch", "补丁", "回注", "overlay",
        ],
        "把「跑得通」升级成「知道该改哪里」，是搜索系统从试错走向优化的分水岭。",
    ),
    (
        "Agent 控制与预算",
        [
            "迭代次数", "预算", "budget", "早停", "停止条件", "上限", "并行", "并发",
            "重试", "retry", "工具", "tool", "MCP", "mcp", "角色", "分工", "多智能体",
            "独立 agent", "独立 agent 验证", "记忆", "memory", "知识库", "MCP 服务",
            "规划", "调度", "控制流", "确定性",
        ],
        "Agent 循环必须能被打断、复盘和限制，否则「多试几次」会伪装成「搜索得更聪明」。",
    ),
    (
        "可复现性",
        [
            "docker", "容器", "镜像", "conda", "pin", "锁定", "git SHA", "sha", "版本",
            "环境", "依赖", "install", "setup", "离线", "外网", "缓存隔离", "回滚",
            "还原", "时间戳", "落盘", "resume", "续跑", "回放", "可回放", "目录",
            "脚本", "独立脚本", "notebook", "Jupyter",
        ],
        "固定环境、留痕、可回滚，是这类项目的头号工程债来源。",
    ),
    (
        "评测严谨性",
        [
            "基线", "baseline", "重复", "多次", "统计", "阈值", "预算", "候选数",
            "确定性", "种子", "seed", "warmup", "预热", "计时", "时钟", "方差",
            "对照", "ablation", "消融", "对齐", "性价比", "校准", "口径",
        ],
        "把「跑了几次、基线是谁、预算多少」写进结果，比单纯报一个加速比重要得多。",
    ),
    (
        "可扩展性",
        [
            "配置", "config", "插件", "plugin", "接口", "外置", "json", "yaml",
            "注册", "registry", "分层", "模块化", "扩展", "参数化", "开关", "flag",
            "多后端", "后端", "支持", "抽象", "解耦",
        ],
        "把任务、模型、后端、评分器做成可外置的配置，新任务不应需要改核心代码。",
    ),
    (
        "训练工程",
        [
            "采样", "sample", "奖励", "reward", "过滤", "filter", "拒绝", "reject",
            "配对", "pair", "课程", "curriculum", "数据泄漏", "去重", "SFT",
            "RL", "GRPO", "PPO", "轨迹", "trajectory", "parquet", "预训练",
            "预训练数据", "数据构造", "难例",
        ],
        "训练数据的过滤规则和评测集的划分规则必须一起设计，否则很容易在评测集上泄漏。",
    ),
    (
        "隔离与稳定性",
        [
            "子进程", "隔离", "崩溃", "非法访存", "级联", "进程池", "worker",
            "避免拖垮", "防止", "安全", "只读", "限制", "上限", "沙箱",
        ],
        "生成的 kernel 随时可能编译崩溃或非法访存，隔离执行是让系统能长时间跑下去的前提。",
    ),
    (
        "任务与数据来源",
        [
            "题目", "任务来源", "挖掘", "真实仓库", "生产", "trace", "Trace Schema",
            "prompt 难度", "难度分级", "上下文", "采样策略", "污染", "去重", "相似",
            "统一格式", "格式", "索引", "分类", "taxonomy",
        ],
        "任务从哪来、怎么切分、会不会污染，直接决定评测结论能推广到多远。",
    ),
    (
        "度量口径",
        [
            "roofline", "理论上限", "SOL", "Pass@K", "赛道", "Track", "subset",
            "切分", "分维度", "指标", "口径", "分批", "基准", "对照模型",
        ],
        "度量口径决定了「哪个更好」这个问题有没有唯一答案。",
    ),
    (
        "部署与交付",
        [
            "部署", "生产", "分发", "distributor", "服务框架", "serving",
            "集成", "免安装", "header-only", "pip 包", "Python API", "CLI",
            "库形态", "包形态", "eager", "落地",
        ],
        "能不能被真实服务用上，是「研究有效」和「可交付」之间的分界。",
    ),
]

LIMIT_THEMES = [
    (
        "硬件与架构支持边界",
        ["GPU", "H100", "A100", "Blackwell", "Hopper", "Ampere", "Volta", "MI300", "架构", "arch", "芯片", "显存", "支持"],
        "「支持某张卡」几乎从不等于「支持这一代的全部算子」——检查支持矩阵，不要只看型号。",
    ),
    (
        "环境与依赖门槛",
        ["docker", "conda", "安装", "依赖", "clone", "环境", "镜像", "手动", "版本", "CUDA", "Python", "uv", "sudo"],
        "「一条命令跑起来」是稀缺品。上手成本高意味着复现率低，也意味着结论更难被独立检验。",
    ),
    (
        "评测可信度",
        ["reward", "hacking", "复核", "方差", "波动", "偏差", "不可靠", "误差", "偏移", "漂移"],
        "项目自己写出这类告警的，通常是发现了真实问题——这类告警值得优先读。",
    ),
    (
        "交付不完整",
        ["尚未", "未发布", "还在开发", "仍在", "没有提供", "minimal", "仅", "只提供"],
        "README 明确说「训练流程未发布」的项目，只能用来理解设计，不能用来复现结果。",
    ),
    (
        "规模与定位受限",
        ["有限", "十余", "较少", "小规模", "子集", "仅支持", "部分"],
        "任务集规模小意味着结论的适用范围也小。引用时要把任务集规模一并带上。",
    ),
]

# 分类优先级：越靠前越具体。含泛化关键词的主题放在后面，
# 否则「脚本」「目录」这类词会把几乎所有条目吸走。
PRACTICE_ORDER = [
    "评测与优化分离",
    "正确性防线",
    "反馈信号升级",
    "隔离与稳定性",
    "Agent 控制与预算",
    "任务与数据来源",
    "度量口径",
    "部署与交付",
    "训练工程",
    "可复现性",
    "评测严谨性",
    "可扩展性",
]
PRACTICE_THEME_KEYS = {name: keys for name, keys, _ in PRACTICE_THEMES}


def theme_of(practice):
    p = practice.lower()
    for theme in PRACTICE_ORDER:
        keys = PRACTICE_THEME_KEYS[theme]
        if any(k.lower() in p for k in keys):
            return theme
    return "其他"


def limit_theme_of(limit):
    p = limit.lower()
    for theme, keys, _ in LIMIT_THEMES:
        if any(k.lower() in p for k in keys):
            return theme
    return None


def doc_engineering_knowledge(repos, snapshot):
    out = []
    with_arch = [r for r in repos if r.get("architecture")]
    linked = [r for r in repos if r["work_ids"]]

    out.append("# 抽象知识：工程实践与项目架构搭建\n")
    out.append(
        f"这份文档从 {len(repos)} 个开源项目里提炼**可复用的工程知识**："
        "一个 kernel 优化项目通常由哪些层组成、常见的架构形态有哪几种、"
        "别人已经踩过并且解决掉的工程问题有哪些、以及如果要自己搭一个项目应该怎么起步。\n"
    )
    out.append(
        "> **证据边界**：结论来自仓库 README、顶层目录结构与 GitHub API 元数据。"
        "**没有审计源码实现，没有运行过任何项目，没有复现任何论文数字。**"
        "本文描述的是「公开材料显示项目这样组织」，不是「项目实现正确」。\n"
    )

    # ---- §1 参考分层
    out.append("## 1. kernel 项目的参考分层\n")
    out.append(
        "把这批项目叠在一起看，几乎都能拆进同一套分层里。"
        "分层的价值不在于分类学，而在于**定位缺口**："
        "要判断一个项目离「能交付」还差多远，只需要问它缺哪几层。\n"
    )
    out.append("| 层 | 职责 | 在仓库里长什么样 |")
    out.append("| --- | --- | --- |")
    for name, duty, check in LAYERS:
        out.append(f"| **{name}** | {duty} | {check} |")
    out.append("")
    out.append(
        "缺 L5 的项目只能回答「能不能编译」，缺 L6 的项目只能回答「这一次跑得怎么样」，"
        "缺 L1 的项目则无法回答「在什么任务上」。三样都缺的项目基本只有演示价值。\n"
    )

    out.append("### 各层的项目分布\n")
    role_layer = {
        "foundation-runtime": "L3 / L4",
        "foundation-compiler": "L3 / L4",
        "foundation-dsl": "L3",
        "training-pipeline": "L7",
        "agent-loop": "L2",
        "benchmark": "L1 / L6",
        "dataset-or-model": "L7",
        "listicle": "—",
        "other": "—",
    }
    for role, layer in role_layer.items():
        items = [r for r in with_arch if (r["architecture"].get("role") or "other") == role]
        if not items:
            continue
        names = "、".join(f"`{r['canonical']}`" for r in sorted(items, key=lambda x: x["canonical"]))
        out.append(f"- **{ROLE_LABELS.get(role, role)}**（对应 {layer}，{len(items)} 个）：{names}")
    out.append("")

    # ---- §2 架构形态
    out.append("## 2. 七种架构形态\n")
    out.append(
        "把 61 个项目按「有没有评测闭环、有没有 Agent 闭环、是不是底座、是不是训练流水线」分类，"
        "得到七种形态。形态决定了一个项目的**最小可行交付物**是什么。\n"
    )
    shape_members = defaultdict(list)
    for r in with_arch:
        shape_members[classify_shape(r)].append(r)
    out.append("| 形态 | 项目数 | 项目 |")
    out.append("| --- | ---: | --- |")
    for key in sorted(shape_members):
        items = shape_members[key]
        names = "、".join(f"`{r['canonical']}`" for r in sorted(items, key=lambda x: x["canonical"]))
        out.append(f"| {SHAPES[key]['name']} | {len(items)} | {names} |")
    out.append("")
    for key in sorted(shape_members):
        s = SHAPES[key]
        out.append(f"### {s['name']}\n")
        out.append(f"**是什么**：{s['definition']}\n")
        out.append(f"**骨架**：{s['anatomy']}\n")
        out.append(f"**复用要点**：{s['reuse']}\n")
        notes = [
            f"`{r['canonical']}`——{r['architecture'].get('arch_notes_zh', '')}"
            for r in sorted(shape_members[key], key=lambda x: x["canonical"])
            if r["architecture"].get("arch_notes_zh")
        ]
        if notes:
            out.append("**各项目的具体做法**：\n")
            for n in notes:
                out.append(f"- {n}")
            out.append("")

    # ---- §3 工程实践
    out.append("## 3. 工程实践清单\n")
    out.append(
        "从各项目 README 与目录结构中提炼的具体做法，按主题归类。"
        "括号里是提到该做法并给出具体机制的项目。\n"
    )
    practice_map = defaultdict(list)
    for r in with_arch:
        for p in r["architecture"].get("engineering_practices") or []:
            theme = theme_of(p)
            practice_map[theme].append((r["canonical"], p))

    out.append("| 主题 | 条目数 |")
    out.append("| --- | ---: |")
    for theme in PRACTICE_ORDER:
        if practice_map.get(theme):
            out.append(f"| {theme} | {len(practice_map[theme])} |")
    if practice_map.get("其他"):
        out.append(f"| 其他工程细节 | {len(practice_map['其他'])} |")
    out.append("")

    for theme in PRACTICE_ORDER:
        items = practice_map.get(theme)
        if not items:
            continue
        note = next(n for t, _, n in PRACTICE_THEMES if t == theme)
        out.append(f"### {theme}\n")
        out.append(f"*{note}*\n")
        seen = set()
        for canon, p in sorted(items):
            if p in seen:
                continue
            seen.add(p)
            others = sorted({c for c, q in items if q == p and c != canon})
            src = f"`{canon}`" + ("、" + "、".join(f"`{c}`" for c in others) if others else "")
            out.append(f"- {p}　<sub>（{src}）</sub>")
        out.append("")
    if practice_map.get("其他"):
        out.append("### 其他工程细节\n")
        out.append(
            "这些做法没有归入上面任何一类，但同样具体可复用。"
            "按项目列出，便于按需查阅。\n"
        )
        for canon, p in sorted(practice_map["其他"]):
            out.append(f"- {p}　<sub>（`{canon}`）</sub>")
        out.append("")

    # ---- §4 目录模板
    out.append("## 4. 从零搭建：目录骨架与里程碑\n")
    out.append("### 4.1 目录骨架\n")
    out.append(
        "下面是按出现频次排出来的顶层目录。"
        "括号内是 61 个项目里采用该目录的数量。"
        "这套骨架直接照抄不会错，但**只建需要的**——"
        "没有评测就不要建 `benchmarks/`，没有 Agent 就不要建 `agents/`。\n"
    )
    dir_freq = Counter()
    for r in repos:
        for d in r["root_dirs"]:
            dir_freq[d] += 1
    core = [d for d, _ in dir_freq.most_common(28)]
    out.append("| 目录 | 出现数 | 用途 |")
    out.append("| --- | ---: | --- |")
    purpose = {
        "src": "核心 Python 包",
        "scripts": "可执行脚本入口与数据准备",
        "docs": "使用文档与设计说明",
        "tests": "单元测试",
        "test": "单元测试",
        "examples": "可运行示例",
        "docker": "容器化的评测环境",
        "agents": "Agent 实现与提示",
        "prompts": "提示模板",
        "kb": "知识库 / 经验记忆",
        "tools": "工具封装（编译、profile、校验）",
        "utils": "通用工具",
        "data": "数据集",
        "dataset": "数据集",
        "tasks": "任务定义",
        "benchmark": "评测任务与脚本",
        "graders": "评分器",
        "skills": "技能模块",
        "configs": "配置",
        "assets": "静态资源",
    }
    for d in core:
        out.append(f"| `{d}/` | {dir_freq[d]} | {purpose.get(d, '—')} |")
    out.append("")

    out.append("### 4.2 里程碑\n")
    out.append(
        "按这个顺序做，每一步都能独立交付一个能用的东西，"
        "不会走到一半发现评测跑不通。\n"
    )
    out.append(
        "| 阶段 | 目标 | 交付物 | 验收方式 |\n"
        "| --- | --- | --- | --- |\n"
        "| **M0 任务集** | 定义要优化什么 | 任务定义（目录或 JSON）+ 参考实现 + 正确性判据 | "
        "参考实现自己跑得通，判据能区分正确与错误的实现 |\n"
        "| **M1 评测闭环** | 有一个能信的口径 | 候选提交入口 + 判定器 + 基线 + 多次运行汇总 | "
        "同一个候选重复跑结果稳定，基线版本被记录 |\n"
        "| **M2 生成闭环** | 让模型参与进来 | 提示/模型接口 + 编译与执行工具 + 循环控制器 | "
        "至少能产生一个通过正确性判据的候选 |\n"
        "| **M3 反馈升级** | 让搜索更聪明 | profile 或性能反馈 + 记忆/经验复用 | "
        "在固定预算下比 M2 的随机多试更有效 |\n"
        "| **M4 训练或交付** | 产出可分发的资产 | 训练脚本 + 权重/数据集，或可部署算子包 | "
        "评测脚本与训练环境共用同一套执行后端 |\n"
    )

    out.append("### 4.3 常见陷阱\n")
    out.append(
        "这些不是假想问题，而是这批项目自己写下来、或从其结构里能直接看出来的。\n"
    )
    out.append(
        "1. **只有编译成功当成功**。编译通过不等于算子正确，"
        "必须有参考输出比对；数值算子还要定容差。\n"
        "2. **单次运行比速度**。GPU 计时波动大，必须多次运行并记录分布，"
        "基线与候选必须在同一进程、同一时钟口径下测。\n"
        "3. **版本漂移**。任务集、基线实现、硬件、驱动版本任一变化都会让历史数字失效。"
        "把这些写进结果文件，而不是写进 README 的一段话。\n"
        "4. **训练评测集泄漏**。合成数据与公开 benchmark 高度重叠时，"
        "在 KernelBook 上训练又在 KernelBench 上评测，结论不成立。\n"
        "5. **环境不固定**。10 个项目提供 `docker/`，"
        "说明「Agent 之间的差异」经常被「环境之间的差异」吃掉。\n"
        "6. **只有 `Profile` 反馈的少数派**。在 59 个有工作关联的开源项目里，"
        "只有 13 个声明了 profile 反馈——多数系统的搜索信号仍停留在「编译过 + 跑得通」。\n"
    )

    # ---- §4.4 项目自述的限制
    out.append("### 4.4 项目自己写下来的限制\n")
    out.append(
        "这一节直接来自各项目 README 的自述限制，按主题归类。"
        "**项目主动写出的限制比读者猜出来的限制更有价值**——"
        "它说明作者自己知道边界在哪。\n"
    )
    limit_map = defaultdict(list)
    for r in with_arch:
        for lim in r["architecture"].get("stated_limits") or []:
            theme = limit_theme_of(lim)
            if theme:
                limit_map[theme].append((r["canonical"], lim))
    out.append("| 限制主题 | 条目数 | 涉及项目数 |")
    out.append("| --- | ---: | ---: |")
    for theme, _, _note in LIMIT_THEMES:
        items = limit_map.get(theme)
        if not items:
            continue
        out.append(f"| {theme} | {len(items)} | {len({c for c, _ in items})} |")
    out.append("")
    for theme, _, note in LIMIT_THEMES:
        items = limit_map.get(theme)
        if not items:
            continue
        out.append(f"**{theme}**——{note}\n")
        seen = set()
        for canon, lim in sorted(items):
            if lim in seen:
                continue
            seen.add(lim)
            others = sorted({c for c, q in items if q == lim and c != canon})
            src = f"`{canon}`" + ("、" + "、".join(f"`{c}`" for c in others) if others else "")
            out.append(f"- {lim}　<sub>（{src}）</sub>")
        out.append("")

    # ---- §5 反馈漏斗
    out.append("## 5. 反馈信号漏斗\n")
    out.append(
        "从 landscape 关联的工作字段统计 59 个有开源仓库的工作，"
        "它们声明的反馈信号分布如下。这张表说明**当前开源系统的反馈强度**。\n"
    )
    fb = Counter()
    for r in linked:
        for f in r["feedback"]:
            fb[f] += 1
    out.append("| 反馈信号 | 项目数 | 占比 |")
    out.append("| --- | ---: | ---: |")
    for k, v in fb.most_common():
        out.append(f"| {k} | {v} | {round(100.0 * v / len(linked))}% |")
    out.append("")
    out.append(
        "正确性（49）和运行时（48）几乎是标配，编译（40）稍低，"
        "而真正指导优化的 profile（13）只有四分之一左右。"
        "这解释了为什么大多数开源系统的提升主要来自「多试几次」而不是「知道该改哪里」。\n"
    )

    out.append("### 基准复用\n")
    out.append(
        "同一份任务集被反复复用，是这个领域可比性的来源，也是它的问题来源。\n"
    )
    bench = Counter()
    bench_map = defaultdict(list)
    for r in linked:
        for b in r["benchmarks"]:
            bench[b] += 1
            bench_map[b].append(r["canonical"])
    out.append("| 基准 | 被多少个项目使用 | 使用者 |")
    out.append("| --- | ---: | --- |")
    for k, v in bench.most_common(12):
        names = "、".join(f"`{c}`" for c in sorted(bench_map[k]))
        out.append(f"| {k} | {v} | {names} |")
    out.append("")
    out.append(
        "KernelBench 被 18 个项目用作评测基准，是事实上的公共任务集。"
        "好处是可比，代价是**一个基准上的改进很容易被当成普适能力**——"
        "尤其是当生成系统的训练数据也来自同一来源时。\n"
    )

    out.append("## 6. 证据边界\n")
    out.append(
        "- 本文的工程结论基于 README、目录结构与 API 元数据，**未做源码审计**。\n"
        "- 「某项目具备某能力」指的是**公开材料声明具备**，不代表已验证可用。\n"
        "- 频次统计反映的是**当前收录的 61 个项目**，"
        "不代表领域整体分布——收录本身就有偏（GitHub 可见、英文 README、公开许可）。\n"
        "- 具体的性能、加速比、成功率数字**一律不引用**，因为本仓没有复现它们。\n"
    )
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default="data/repos.json")
    ap.add_argument("--arch-dir", default="data/architecture")
    ap.add_argument("--out-dir", default="docs")
    args = ap.parse_args()

    idx = load(args.index)
    repos = idx["repos"]
    hf = idx["huggingface"]
    other = idx["other_hosts"]
    snapshot = idx.get("landscape_snapshot")

    batch_files = glob.glob(os.path.join(args.arch_dir, "batch*.json"))
    arch = merge_architecture(repos, batch_files)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "01-repo-index.md"), "w", encoding="utf-8") as f:
        f.write(doc_repo_index(repos, hf, other, snapshot))
    with open(os.path.join(args.out_dir, "02-engineering-knowledge.md"), "w", encoding="utf-8") as f:
        f.write(doc_engineering_knowledge(repos, snapshot))
    with open(os.path.join(args.out_dir, "03-comparison.md"), "w", encoding="utf-8") as f:
        f.write(doc_comparison(repos, snapshot))

    merged = [r["architecture"] for r in repos if r.get("architecture")]
    with open("data/architecture.json", "w", encoding="utf-8") as f:
        json.dump({"schema": 1, "architectures": merged}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"docs written; architecture coverage {len(merged)}/{len(repos)}")


if __name__ == "__main__":
    main()
