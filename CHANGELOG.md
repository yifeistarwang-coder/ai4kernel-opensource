# Changelog

本文件记录本仓的结构性变化。数据快照的变化不在此逐条列出，
以 `data/repos.json` 的 `landscape_snapshot` 字段与各文件内容为准。

## 2026-10-30 — 浅色主题

站点新增浅色主题，与深色主题共用同一套设计令牌。

- 右上角主题切换按钮，默认跟随系统 `prefers-color-scheme`，手动切换后写入 `localStorage`
- 首帧前由内联脚本定好主题，避免深浅切换时闪一下
- 补上深色主题漏定义的 `--copper-block`（引用块背景此前是透明的）
- 把 hero 渐变、页面底色、斑马纹行底色、滚动条颜色改为随主题变化的令牌
- 浏览器回归测试新增主题用例：切换生效、背景色变化、写入 localStorage、刷新后保持

## 2026-10-30 — 站点版

把三个交付物做成静态站点，部署在 GitHub Pages。

### 新增

- **站点**（`site/` → `dist/`）：四个视图——概览、仓库索引、项目对比、抽象知识。
  - 仓库索引可搜索，按分类 / 厂商 / 许可 / 主语言筛选，按列排序，点行打开项目详情抽屉
  - 项目对比四个标签页（架构 / 基础层 / 硬件厂商 / 硬件架构）外加「厂商 × 角色」交叉表
  - 抽象知识页渲染 `docs/02-engineering-knowledge.md`
- **站点生成**（`scripts/build_site.py`）：装配 `dist/`，含 `robots.txt`、`sitemap.xml`、`.nojekyll`。
- **浏览器回归测试**（`tests/browser.mjs`）：逐视图检查渲染、筛选、排序、标签页、抽屉，
  并断言无控制台报错与失败请求；CI 中执行。
- **Pages 部署**（`.github/workflows/deploy-pages.yml`）。

### 安全

- 上游 README 与 GitHub 描述里的 `<`、`>`、`&` 在写进 Markdown 前统一转义
  （`scripts/sanitize.py`），避免第三方仓库的 README 注入标记。
- 站点渲染 Markdown 时再过一遍 DOMPurify。
- CI 增加两项断言：Markdown 中不得出现未转义标记；粗体标记的闭合位置不得导致 CommonMark 解析失败。

## 2026-10-30 — 首版

从 [AI4Kernel Landscape](https://github.com/yifeistarwang-coder/ai4kernel_landscape)
（快照 `2026-10-30`）中筛出已开源部分，整理为独立索引仓。

### 新增

- **开源仓库索引**（`docs/01-repo-index.md`）：61 个 GitHub 仓库 + 10 个 HuggingFace
  模型/数据集 + 1 个其他平台仓库，按分类、组织、许可分表，并记录仓库改名/迁移。
- **抽象知识**（`docs/02-engineering-knowledge.md`）：七层参考分层、七种架构形态、
  340 条按主题归类的工程实践、项目自述限制归类、目录骨架与搭建里程碑。
- **项目对比**（`docs/03-comparison.md`）：架构、基础层、硬件厂商、硬件架构四个对比轴，
  含全量对照表、项目间依赖边与 61 份单项目档案。
- **数据层**：
  - `data/seeds.json` — 从 landscape 数据层提取的仓库与产物线索
  - `data/github-metadata.json` — GitHub API 快照（元数据 + 顶层目录结构）
  - `data/repos.json` / `data/repos.csv` — 合并后的完整索引与扁平表格
  - `data/architecture.json` / `data/architecture/batch*.json` — 结构化架构事实
- **生成管线**（`scripts/`）：`build_seeds.py` → `fetch_metadata.py` →
  `build_index.py` → `build_docs.py`，全流程可复现。
- **CI**（`.github/workflows/check.yml`）：校验 JSON 可解析、文档重生成无漂移、索引完整性。

### 已知边界

- 许可字段是 GitHub API 的自动识别结果，`NOASSERTION` 与空白项必须回到上游 `LICENSE` 核对。
- 架构结论来自 README 与顶层目录结构，未做源码审计，未运行任何项目。
- README 原文缓存写入 `.cache/` 且不进版本库，避免第三方版权与再分发问题。
