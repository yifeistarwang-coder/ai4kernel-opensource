# AI4Kernel 开源索引

**在线浏览：https://yifeistarwang-coder.github.io/ai4kernel-opensource/**

把 [AI4Kernel Landscape](https://github.com/yifeistarwang-coder/ai4kernel_landscape) 研究目录里
**已经开源**的产物单独整理成一份可检索、可对比的索引。

Landscape 是研究目录，收录 129 个 AI4Kernel 相关工作（论文、框架、模型、数据）。
其中 **61 个有公开 GitHub 仓库**，另有 **10 个 HuggingFace 模型 / 数据集** 和
**1 个其他平台仓库**。本仓把这些开源产物重新组织成三个可用的交付物，并做成一个静态站点。

---

## 三个交付物

| # | 交付物 | 内容 | 文档 | 站点视图 |
| --- | --- | --- | --- | --- |
| 1 | **开源仓库索引** | 61 个 GitHub 仓库 + 11 个模型/数据集产物：许可、组织、语言、硬件、任务、README 摘要、顶部目录结构 | [docs/01-repo-index.md](docs/01-repo-index.md) | 仓库索引 |
| 2 | **抽象知识** | 从 61 个项目里提炼的可复用工程知识：七层参考分层、七种架构形态、340 条工程实践、项目自述限制、从零搭建的脚手架与里程碑 | [docs/02-engineering-knowledge.md](docs/02-engineering-knowledge.md) | 抽象知识 |
| 3 | **项目对比** | 四个对比轴：架构、基础层、硬件厂商、硬件架构；含全量对照表与 61 份单项目档案 | [docs/03-comparison.md](docs/03-comparison.md) | 项目对比 |

站点的 Markdown 版本与仓库里的文档是同一份内容，由 `scripts/build_docs.py` 一次生成。

---

## 站点

静态站点，无框架无构建步骤，部署在 GitHub Pages：

- **概览** — 关键统计、架构形态分布、硬件厂商分布、反馈信号漏斗、许可分布
- **仓库索引** — 61 行可搜索、可按分类/厂商/许可/语言筛选、按列排序的表格；点任意一行打开项目详情抽屉
- **项目对比** — 架构 / 基础层 / 硬件厂商 / 硬件架构四个标签页，外加「厂商 × 角色」交叉表
- **抽象知识** — 完整渲染 `docs/02-engineering-knowledge.md`

深色 / 浅色主题切换在右上角，默认跟随系统偏好，手动切换后保存在浏览器本地。

本地预览：

```bash
python3 scripts/build_site.py
python3 -m http.server 4173 --directory dist
```

---

## 快速上手

```bash
# 只看索引（无需安装依赖）
python3 -c "
import json
d = json.load(open('data/repos.json'))
for r in d['repos'][:10]:
    print(f\"{r['canonical']:<45} {r['license'] or '-':<12} {r['group']}\")
"

# 扁平表格：data/repos.csv，可直接丢进 Excel / Google Sheets
```

想复现整个索引：

```bash
# 1. 从 landscape 数据层提取仓库种子（需要 ai4kernel_landscape 在同级目录）
python3 scripts/build_seeds.py --landscape ../ai4kernel_landscape --out data/seeds.json

# 2. 抓取 GitHub 元数据（需要已认证的 gh CLI）
python3 scripts/fetch_metadata.py --seeds data/seeds.json --out data/github-metadata.json

# 3. 合并索引
python3 scripts/build_index.py --landscape ../ai4kernel_landscape --out data/repos.json --csv data/repos.csv

# 4. 生成文档与站点
python3 scripts/build_docs.py
python3 scripts/build_site.py
```

---

## 仓库结构

```
ai4kernel-opensource/
├── README.md                     # 本文件
├── CHANGELOG.md                  # 结构性变更记录
├── LICENSE                       # 脚本代码 MIT
├── LICENSE-CONTENT               # 编辑内容 CC BY 4.0
├── data/
│   ├── seeds.json                # 从 landscape 提取的仓库/产物线索
│   ├── github-metadata.json      # GitHub API 快照（元数据 + 顶层目录 + README 缓存标记）
│   ├── repos.json                # 合并后的完整索引
│   ├── repos.csv                 # 扁平表格
│   ├── architecture.json         # 61 个项目的结构化架构事实
│   └── architecture/batch*.json  # 架构事实的分批原始记录
├── docs/
│   ├── 01-repo-index.md          # 交付物 1
│   ├── 02-engineering-knowledge.md  # 交付物 2
│   └── 03-comparison.md          # 交付物 3
├── site/                         # 站点源码
│   ├── index.html                # 应用外壳
│   └── assets/                   # 样式、脚本、字体、第三方库（含各自许可）
├── scripts/                      # 可复现的生成管线
└── tests/browser.mjs             # 站点浏览器回归测试
```

---

## 数据口径与证据边界

这份索引**只做索引，不做背书**。请注意以下边界：

- **收录 ≠ 可用**。收录只表示该工作存在一个可核查的公开仓库地址。
- **许可字段来自 GitHub API 的自动识别**。`NOASSERTION` 表示仓库内有许可证文件但 API 未能归一化
  （`NVIDIA/cutlass`、`tile-ai/tilelang`、`ScalingIntelligence/KernelBench` 等属此类），
  空白表示仓库未声明许可证。**商用前必须自行核对上游 `LICENSE` 文件。**
- **没有代码审计，没有跑过一行**。架构事实来自 README 与仓库顶层目录结构，
  不是对实现正确性的判断。
- **星标数是抓取当日的快照**，会变化。
- **仓库会改名、迁移、归档**。landscape 数据层里有 3 个地址与 GitHub 当前规范名不一致，
  已记录在[索引的重定向一节](docs/01-repo-index.md#重定向与改名)。

数据快照日期见 `data/repos.json` 的 `landscape_snapshot` 字段。

---

## 测试

```bash
npm ci
npm run build          # 构建站点到 dist/
npm run test:browser   # 浏览器回归测试（Playwright）
```

浏览器测试会启动本地服务，逐个视图检查渲染、筛选、排序、标签页与详情抽屉，
并断言没有控制台报错与失败请求。CI 里同样跑这一套。

---

## 与 Landscape 的关系

```
ai4kernel_landscape  ──►  build_seeds.py  ──►  seeds.json
      (研究目录)                                      │
                                                      ▼
                    ai4kernel-opensource  ◄── fetch_metadata.py
                        (本仓)                      (GitHub API)
                            │
                            ▼
                     build_index.py ──► repos.json / repos.csv
                            │
                            ▼
                      build_docs.py ──► docs/*.md
                            │
                            ▼
                      build_site.py ──► dist/ ──► GitHub Pages
```

Landscape 仍然保留全部研究笔记、证据分级与阅读记录；本仓只负责其中「已开源」的那一部分，
换一种组织方式：按**可获取性**和**工程结构**重新编排，而不是按研究阅读顺序。

---

## 许可

- `scripts/`、`tests/` 下的代码：[MIT](LICENSE)
- 本仓撰写的文档、索引内容与站点：[CC BY 4.0](LICENSE-CONTENT)
- 索引中出现的第三方仓库名称、URL 与元数据归各自作者所有，此处仅用于标识与比较
- `site/assets/` 下的第三方库各自保留许可文件：
  [marked](site/assets/MARKED-LICENSE)（MIT）、[DOMPurify](site/assets/DOMPURIFY-LICENSE)（MPL-2.0 / Apache-2.0）、
  [Space Grotesk](site/assets/fonts/SPACE-GROTESK-LICENSE)、[JetBrains Mono](site/assets/fonts/JETBRAINS-MONO-LICENSE)（SIL OFL 1.1）
