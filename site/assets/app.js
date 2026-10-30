/* AI4Kernel 开源索引 — 站点逻辑
 *
 * 数据来自 build_site.py 生成的 data/site-data.json，架构知识来自 docs/*.md。
 * 无框架、无构建步骤：直接用原生 DOM 与 marked.js 渲染。
 */
(() => {
  'use strict';

  const DATA_URL = './data/site-data.json';
  const DOC_URLS = {
    knowledge: './docs/02-engineering-knowledge.md',
  };

  const ROLE_LABELS = {
    'foundation-runtime': '执行运行时底座',
    'foundation-compiler': '编译器底座',
    'foundation-dsl': 'DSL / kernel 表达层',
    'training-pipeline': '训练流水线',
    'agent-loop': 'Agent 搜索循环',
    'benchmark': '评测基准',
    'dataset-or-model': '数据集 / 模型',
    'listicle': '综述清单',
    'other': '其他',
  };

  const VENDOR_LABELS = {
    NVIDIA: 'NVIDIA',
    AMD: 'AMD',
    Ascend: '华为昇腾',
    TPU: 'Google TPU',
    CPU: 'CPU',
    Intel: 'Intel',
    Other: '其他',
  };

  const HW_ARCH_LABELS = {
    'NVIDIA-GPU-Hopper': 'NVIDIA Hopper (H100/H200)',
    'NVIDIA-GPU-Ampere': 'NVIDIA Ampere (A100)',
    'NVIDIA-GPU-Blackwell': 'NVIDIA Blackwell (B200)',
    'NVIDIA-GPU-Ada': 'NVIDIA Ada (L40S/4090)',
    'NVIDIA-GPU-Volta': 'NVIDIA Volta (V100)',
    'AMD-GPU-CDG': 'AMD CDNA (MI100/MI200)',
    'AMD-GPU-MI300': 'AMD CDNA 3 (MI300X)',
    'AMD-GPU-RDNA': 'AMD RDNA (Radeon)',
    'Ascend-Ascend910B': '昇腾 910B',
    'Ascend-Ascend910C': '昇腾 910C',
    'Ascend-Ascend950': '昇腾 950PR',
    'TPU-v4': 'TPU v4',
    'TPU-v5': 'TPU v5',
    'TPU-v5p': 'TPU v5p',
    'TPU-v6e': 'TPU v6e',
    'CPU-x86': 'x86 CPU',
    'CPU-arm': 'ARM CPU',
    Unknown: '未标注',
  };

  const SHAPE_LABELS = {
    A: '纯评测基准',
    B: '评测 + Agent 平台',
    C: 'Agent 生成闭环',
    D: '训练流水线',
    E: '执行底座',
    F: '综述清单',
    G: '其他 / 单一功能工具',
  };

  const SHAPE_SHORT = {
    A: '纯评测',
    B: '评测+Agent',
    C: 'Agent',
    D: '训练',
    E: '底座',
    F: '清单',
    G: '其他',
  };

  const FILTER_KEYS = ['q', 'group', 'shape', 'vendor', 'feedback', 'license', 'lang'];

  const state = {
    data: null,
    view: 'overview',
    filters: {
      q: '',
      group: '',
      shape: '',
      vendor: '',
      feedback: '',
      license: '',
      lang: '',
    },
    sort: { key: 'canonical', dir: 'asc' },
    selected: null,
    knowledgeLoaded: false,
  };

  // ------------------------------------------------------------------ 工具

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const esc = (value) =>
    String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');

  const repoLink = (repo) =>
    `<a href="${esc(repo.url)}" target="_blank" rel="noopener noreferrer">${esc(repo.canonical)}</a>`;

  const tagList = (items, cls = '') =>
    (items && items.length)
      ? items.map((t) => `<span class="tag ${cls}">${esc(t)}</span>`).join('')
      : '<span class="tag">—</span>';

  function formatNumber(n) {
    if (n === null || n === undefined) return '—';
    if (n >= 10000) return `${(n / 1000).toFixed(1)}k`;
    return String(n);
  }

  function debounce(fn, ms) {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), ms);
    };
  }

  // ------------------------------------------------------------------ 渲染

  function renderBars(target, items, { max, unit = '个', tone } = {}) {
    const el = $(target);
    if (!el) return;
    if (!items.length) {
      el.innerHTML = '<div class="empty">暂无数据</div>';
      return;
    }
    const peak = max || Math.max(...items.map((i) => i.count));
    el.innerHTML = items
      .map((item) => {
        const width = Math.max(2, (item.count / peak) * 100);
        const inner = `
          <span class="bar-label" title="${esc(item.label)}">${esc(item.label)}${
            item.href ? '<span class="bar-hint">→</span>' : ''
          }</span>
          <span class="bar-track"><span class="bar-fill ${tone || ''}" style="width:${width}%"></span></span>
          <span class="bar-value">${item.count}${unit}</span>`;
        return item.href
          ? `<a class="bar-row" href="${esc(item.href)}" title="${esc(item.title || item.label)}">${inner}</a>`
          : `<div class="bar-row">${inner}</div>`;
      })
      .join('');
  }

  function renderOverview() {
    const d = state.data;
    $('#hero-stats').innerHTML = [
      { value: d.counts.repos, label: 'GitHub 仓库' },
      { value: d.counts.total, label: '开源产物总数' },
      { value: d.counts.practices, label: '工程实践条目' },
      { value: d.stats.matrix.roles.length, label: '架构角色' },
      { value: d.counts.with_work, label: '关联研究工作' },
    ]
      .map(
        (s) =>
          `<div class="stat${s.value === d.counts.repos ? ' accent' : ''}">
             <div class="stat-value">${s.value}</div>
             <div class="stat-label">${esc(s.label)}</div>
           </div>`
      )
      .join('');

    renderBars(
      '#shape-bars',
      d.stats.shapes.map((s) => ({
        label: `${s.key} · ${SHAPE_LABELS[s.key] || s.name}`,
        count: s.count,
        href: `#/index?shape=${encodeURIComponent(s.key)}`,
        title: `查看 ${s.count} 个${SHAPE_LABELS[s.key] || s.name}形态的项目`,
      })),
      { tone: 'blue' }
    );
    renderBars(
      '#vendor-bars',
      d.stats.vendors.map((v) => ({
        label: VENDOR_LABELS[v.name] || v.name,
        count: v.count,
        href: `#/index?vendor=${encodeURIComponent(v.name)}`,
        title: `查看 ${v.count} 个支持${VENDOR_LABELS[v.name] || v.name}的项目`,
      })),
      { tone: 'copper' }
    );
    renderBars(
      '#feedback-bars',
      d.stats.feedback.map((f) => ({
        label: f.name,
        count: f.count,
        href: `#/index?feedback=${encodeURIComponent(f.name)}`,
        title: `查看 ${f.count} 个使用${f.name}反馈信号的项目`,
      }))
    );
    renderBars(
      '#license-bars',
      d.stats.licenses.map((l) => ({
        label: l.name,
        count: l.count,
        href: `#/index?license=${encodeURIComponent(l.name)}`,
        title: `查看 ${l.count} 个${l.name}许可的项目`,
      }))
    );
  }

  function fillSelect(id, options, allLabel) {
    const sel = $(id);
    if (!sel) return;
    sel.innerHTML =
      `<option value="">${esc(allLabel)}</option>` +
      options.map((o) => `<option value="${esc(o.value)}">${esc(o.label)}</option>`).join('');
  }

  function initIndexFilters() {
    const d = state.data;
    const uniq = (key, labelFn) => {
      const seen = new Map();
      for (const r of d.repos) {
        for (const v of r[key] || []) {
          if (!seen.has(v)) seen.set(v, labelFn ? labelFn(v) : v);
        }
      }
      return Array.from(seen.entries())
        .map(([value, label]) => ({ value, label }))
        .sort((a, b) => a.label.localeCompare(b.label, 'zh'));
    };

    fillSelect(
      '#idx-group',
      d.stats.groups.map((g) => ({ value: g.name, label: `${g.name} · ${g.label}` })),
      '全部分类'
    );
    fillSelect(
      '#idx-shape',
      d.stats.shapes.map((s) => ({ value: s.key, label: `${s.key} · ${SHAPE_LABELS[s.key] || s.name}` })),
      '全部形态'
    );
    fillSelect('#idx-vendor', uniq('hardware'), '全部厂商');
    fillSelect(
      '#idx-feedback',
      d.stats.feedback.map((f) => ({ value: f.name, label: `${f.name}（${f.count}）` })),
      '全部反馈信号'
    );
    fillSelect('#idx-license', d.stats.licenses.map((l) => ({ value: l.name, label: l.name })), '全部许可');
    fillSelect(
      '#idx-lang',
      d.stats.languages.map((l) => ({ value: l.name, label: l.name })),
      '全部语言'
    );
  }

  function matchesFilters(repo) {
    const f = state.filters;
    if (f.group && repo.group !== f.group) return false;
    if (f.shape && repo.shape !== f.shape) return false;
    if (f.license && (repo.license || '未声明') !== f.license) return false;
    if (f.vendor && !(repo.hardware || []).includes(f.vendor)) return false;
    if (f.lang && repo.primary_language !== f.lang) return false;
    if (f.feedback && !(repo.feedback || []).includes(f.feedback)) return false;
    if (f.q) {
      const haystack = [
        repo.canonical,
        repo.org,
        repo.description,
        repo.task,
        repo.summary,
        repo.group,
        repo.group_label,
        repo.primary_language,
        (repo.hardware || []).join(' '),
        (repo.languages || []).join(' '),
        (repo.methods || []).join(' '),
        (repo.benchmarks || []).join(' '),
        (repo.feedback || []).join(' '),
        repo.architecture ? repo.architecture.arch_pattern : '',
        repo.architecture ? repo.architecture.role_summary_zh : '',
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();
      if (!haystack.includes(f.q.toLowerCase())) return false;
    }
    return true;
  }

  function sortRepos(rows) {
    const { key, dir } = state.sort;
    const sign = dir === 'asc' ? 1 : -1;
    return rows.sort((a, b) => {
      let av = a[key];
      let bv = b[key];
      if (key === 'stars') {
        av = av ?? -1;
        bv = bv ?? -1;
        return (av - bv) * sign;
      }
      av = String(av ?? '').toLowerCase();
      bv = String(bv ?? '').toLowerCase();
      if (av === bv) return a.canonical.localeCompare(b.canonical);
      return av < bv ? -sign : sign;
    });
  }

  const FILTER_LABELS = {
    q: '关键词',
    group: '分类',
    shape: '形态',
    vendor: '厂商',
    feedback: '反馈信号',
    license: '许可',
    lang: '主语言',
  };

  function describeFilters() {
    const parts = [];
    for (const key of FILTER_KEYS) {
      const value = state.filters[key];
      if (!value) continue;
      if (key === 'q') parts.push(`关键词「${value}」`);
      else if (key === 'shape') {
        parts.push(`形态 ${value} · ${SHAPE_LABELS[value] || value}`);
      } else parts.push(`${FILTER_LABELS[key]} ${value}`);
    }
    return parts;
  }

  function renderIndex() {
    const d = state.data;
    const rows = sortRepos(d.repos.filter(matchesFilters));
    const body = $('#idx-body');
    body.innerHTML = rows
      .map(
        (r) => `
        <tr data-canonical="${esc(r.canonical)}" class="${state.selected === r.canonical ? 'selected' : ''}">
          <td class="cell-repo">${esc(r.canonical)}</td>
          <td class="cell-group">${esc(r.group_label || r.group || '—')}</td>
          <td class="cell-group">${
            r.shape
              ? `<span class="tag" title="${esc(SHAPE_LABELS[r.shape] || r.shape)}">${esc(
                  SHAPE_SHORT[r.shape] || r.shape
                )}</span>`
              : '—'
          }</td>
          <td>${r.license ? `<span class="tag">${esc(r.license)}</span>` : '<span class="tag copper">未声明</span>'}</td>
          <td>${esc(r.primary_language || '—')}</td>
          <td>${tagList(r.hardware || [])}</td>
          <td>${tagList(r.feedback || [], 'blue')}</td>
          <td class="cell-desc">${esc(r.description || r.summary || '—')}</td>
          <td class="cell-num">${formatNumber(r.stars)}</td>
        </tr>`
      )
      .join('');
    $('#idx-empty').hidden = rows.length > 0;
    const active = describeFilters();
    $('#idx-clear').hidden = active.length === 0;
    $('#idx-count').textContent = `${rows.length} / ${d.repos.length} 个仓库`;
    $('#index-caption').textContent = active.length
      ? `当前筛选：${active.join(' · ')}`
      : '全部 61 个已开源项目';
  }

  const COMPARE_TABS = [
    { id: 'cmp-arch', slug: 'arch', label: '架构' },
    { id: 'cmp-base', slug: 'base', label: '基础层' },
    { id: 'cmp-vendor', slug: 'vendor', label: '硬件厂商' },
    { id: 'cmp-archchip', slug: 'archchip', label: '硬件架构' },
    { id: 'cmp-matrix', slug: 'matrix', label: '厂商 × 角色' },
  ];

  function activateCompareTab(slug) {
    const tab =
      COMPARE_TABS.find((t) => t.slug === slug) || COMPARE_TABS[0];
    for (const t of $$('#compare-tabs .tab')) {
      t.classList.toggle('active', t.dataset.panel === tab.id);
    }
    for (const p of $$('.tab-panel')) p.hidden = p.id !== tab.id;
    return tab;
  }

  function renderCompare() {
    const d = state.data;

    // 架构形态卡片（可点，跳到按形态筛选的索引）
    $('#cmp-arch-cards').innerHTML = d.stats.shapes
      .map(
        (s) => `
        <a class="card" href="#/index?shape=${encodeURIComponent(s.key)}">
          <span class="card-index">形态 ${esc(s.key)}</span>
          <h3>${esc(SHAPE_LABELS[s.key] || s.name)}</h3>
          <p>${esc(s.blurb)}</p>
          <span class="card-meta">${s.count} 个项目 →</span>
        </a>`
      )
      .join('');

    // 架构全量对照
    $('#cmp-arch-body').innerHTML = d.repos
      .filter((r) => r.architecture)
      .map((r) => {
        const a = r.architecture;
        return `
        <tr data-canonical="${esc(r.canonical)}">
          <td class="cell-repo">${repoLink(r)}</td>
          <td>${esc(ROLE_LABELS[a.role] || a.role)}</td>
          <td class="cell-desc">${esc(a.arch_pattern || '—')}</td>
          <td>${a.eval_harness && a.eval_harness.present ? '有' : '无'}</td>
          <td>${a.agent_loop && a.agent_loop.present ? '有' : '无'}</td>
          <td>${esc((a.verification && a.verification.mechanisms || []).join('、') || '—')}</td>
        </tr>`;
      })
      .join('');

    // 基础层
    $('#cmp-base-body').innerHTML = d.stats.base_layers
      .map(
        (b) => `
        <tr>
          <td class="cell-repo">${esc(b.name)}</td>
          <td class="cell-num">${b.count}</td>
          <td class="cell-desc">${b.members.map((m) => `<span class="tag">${esc(m)}</span>`).join('')}</td>
        </tr>`
      )
      .join('');

    // 硬件厂商
    $('#cmp-vendor-body').innerHTML = d.stats.vendors
      .map(
        (v) => `
        <tr>
          <td class="cell-repo">${esc(VENDOR_LABELS[v.name] || v.name)}</td>
          <td class="cell-num">${v.count}</td>
          <td class="cell-desc">${v.members.map((m) => `<span class="tag">${esc(m)}</span>`).join('')}</td>
        </tr>`
      )
      .join('');

    // 硬件架构
    $('#cmp-chip-body').innerHTML = d.stats.hw_arch
      .map(
        (h) => `
        <tr>
          <td class="cell-repo">${esc(HW_ARCH_LABELS[h.name] || h.name)}</td>
          <td class="cell-num">${h.count}</td>
          <td class="cell-desc">${h.members.map((m) => `<span class="tag">${esc(m)}</span>`).join('')}</td>
        </tr>`
      )
      .join('');

    // 厂商 × 角色
    const roles = d.stats.matrix.roles;
    $('#cmp-matrix-head').innerHTML = `<tr><th>厂商</th>${roles
      .map((r) => `<th style="text-align:right">${esc(ROLE_LABELS[r] || r)}</th>`)
      .join('')}<th style="text-align:right">合计</th></tr>`;
    $('#cmp-matrix-body').innerHTML = d.stats.matrix.rows
      .map(
        (row) => `
        <tr>
          <td class="cell-repo">${esc(VENDOR_LABELS[row.vendor] || row.vendor)}</td>
          ${row.counts.map((c) => `<td class="cell-num">${c || ''}</td>`).join('')}
          <td class="cell-num">${row.total}</td>
        </tr>`
      )
      .join('');
  }

  function renderKnowledge() {
    const target = $('#knowledge-body');
    if (state.knowledgeLoaded) return;
    state.knowledgeLoaded = true;
    target.innerHTML = '<div class="loading">正在载入文档…</div>';
    fetch(DOC_URLS.knowledge)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.text();
      })
      .then((md) => {
        // 文档里的工程实践条目摘自上游 README。生成阶段已转义，这里再过一遍净化器。
        const html = marked.parse(md, { gfm: true, breaks: false });
        target.innerHTML = DOMPurify.sanitize(html, { USE_PROFILES: { html: true } });
      })
      .catch((err) => {
        state.knowledgeLoaded = false;
        target.innerHTML = `<p class="note">文档载入失败：${esc(err.message)}。`
          + '可以直接在 <a href="./docs/02-engineering-knowledge.md">GitHub 上查看 Markdown 原文</a>。</p>';
      });
  }

  // ------------------------------------------------------------------ 抽屉

  function openDrawer(canonical) {
    const repo = state.data.repos.find((r) => r.canonical === canonical);
    if (!repo) return;
    state.selected = canonical;

    const a = repo.architecture || {};
    const parts = [];

    parts.push(`<p class="note">${esc(repo.description || repo.summary || '—')}</p>`);

    parts.push('<h3>基本信息</h3><dl class="kv">');
    parts.push(`<dt>分类</dt><dd>${esc(repo.group_label || repo.group || '—')}</dd>`);
    parts.push(`<dt>组织</dt><dd><a href="https://github.com/${esc(repo.org)}" target="_blank" rel="noopener noreferrer">${esc(repo.org)}</a>${repo.org_type ? ` · ${esc(repo.org_type)}` : ''}</dd>`);
    parts.push(`<dt>许可</dt><dd>${repo.license ? esc(repo.license) : '未声明（需回上游核对）'}</dd>`);
    parts.push(`<dt>主语言</dt><dd>${esc(repo.primary_language || '—')}</dd>`);
    parts.push(`<dt>硬件</dt><dd>${(repo.hardware || []).map((h) => esc(h)).join('、') || '—'}</dd>`);
    parts.push(`<dt>任务</dt><dd>${esc(repo.task || '—')}</dd>`);
    parts.push(`<dt>星标</dt><dd>${repo.stars === null ? '—' : `${repo.stars} 星 · ${repo.forks || 0} fork`}</dd>`);
    parts.push(`<dt>最近推送</dt><dd>${esc((repo.pushed_at || '—').slice(0, 10))}</dd>`);
    parts.push(`<dt>仓库</dt><dd><a href="${esc(repo.url)}" target="_blank" rel="noopener noreferrer">${esc(repo.url)}</a></dd>`);
    if (repo.aliases && repo.aliases.length) {
      parts.push(`<dt>旧地址</dt><dd>${repo.aliases.map((x) => `<code>${esc(x)}</code>`).join('、')}</dd>`);
    }
    parts.push('</dl>');

    if (a.arch_notes_zh) {
      parts.push(`<h3>架构说明</h3><p class="note">${esc(a.arch_notes_zh)}</p>`);
    }
    if (a.arch_pattern) {
      parts.push(`<h3>架构模式</h3><p>${esc(a.arch_pattern)}</p>`);
    }
    if (a.key_modules && a.key_modules.length) {
      parts.push('<h3>主要模块</h3><ul class="list-plain">');
      for (const m of a.key_modules) {
        parts.push(`<li><code>${esc(m.name)}</code> — ${esc(m.purpose_zh)}</li>`);
      }
      parts.push('</ul>');
    }
    if (a.entrypoints && a.entrypoints.length) {
      parts.push('<h3>入口</h3><ul class="list-plain">');
      for (const e of a.entrypoints) parts.push(`<li><code>${esc(e)}</code></li>`);
      parts.push('</ul>');
    }
    if (a.base_layer && a.base_layer.length && a.role !== 'listicle') {
      parts.push(`<h3>基础层</h3><p>${a.base_layer.map((b) => `<span class="tag green">${esc(b)}</span>`).join('')}</p>`);
    }
    if (a.hardware_arch && a.hardware_arch.length) {
      parts.push(
        `<h3>硬件架构</h3><p>${a.hardware_arch
          .map((h) => `<span class="tag blue">${esc(HW_ARCH_LABELS[h] || h)}</span>`)
          .join('')}</p>`
      );
    }
    if (a.eval_harness && a.eval_harness.present) {
      parts.push(`<h3>评测</h3><p class="note">${esc(a.eval_harness.design_zh || '—')}</p>`);
    }
    if (a.verification && (a.verification.mechanisms || []).length) {
      parts.push(
        `<h3>验证机制</h3><p>${a.verification.mechanisms
          .map((m) => `<span class="tag copper">${esc(m)}</span>`)
          .join('')}</p>`
      );
      if (a.verification.notes_zh) {
        parts.push(`<p class="note">${esc(a.verification.notes_zh)}</p>`);
      }
    }
    if (a.agent_loop && a.agent_loop.present) {
      parts.push('<h3>Agent 循环</h3><dl class="kv">');
      parts.push(`<dt>决策</dt><dd>${esc(a.agent_loop.control_zh || '—')}</dd>`);
      parts.push(`<dt>记忆</dt><dd>${esc(a.agent_loop.memory_zh || '—')}</dd>`);
      parts.push(`<dt>反馈</dt><dd>${esc(a.agent_loop.feedback_zh || '—')}</dd>`);
      parts.push('</dl>');
    }
    if (a.engineering_practices && a.engineering_practices.length) {
      parts.push('<h3>工程实践</h3><ul class="list-plain">');
      for (const p of a.engineering_practices) parts.push(`<li>${esc(p)}</li>`);
      parts.push('</ul>');
    }
    if (a.stated_limits && a.stated_limits.length) {
      parts.push('<h3>自述限制</h3><ul class="list-plain">');
      for (const l of a.stated_limits) parts.push(`<li>${esc(l)}</li>`);
      parts.push('</ul>');
    }
    if (repo.root_dirs && repo.root_dirs.length) {
      parts.push(
        `<h3>顶层目录</h3><p>${repo.root_dirs.map((d) => `<span class="tag">${esc(d)}/</span>`).join('')}</p>`
      );
    }

    $('#drawer-title').textContent = repo.canonical;
    $('#drawer-body').innerHTML = parts.join('');
    $('#drawer').classList.add('open');
    $('#drawer').setAttribute('aria-hidden', 'false');
    $('#drawer-backdrop').classList.add('open');
    document.body.style.overflow = 'hidden';
    renderIndex();
  }

  function closeDrawer() {
    state.selected = null;
    $('#drawer').classList.remove('open');
    $('#drawer').setAttribute('aria-hidden', 'true');
    $('#drawer-backdrop').classList.remove('open');
    document.body.style.overflow = '';
    renderIndex();
  }

  // ------------------------------------------------------------------ 路由

  function showView(view) {
    state.view = view;
    for (const name of ['overview', 'index', 'compare', 'knowledge']) {
      $(`#page-${name}`).hidden = name !== view;
    }
    for (const link of $$('#nav a')) {
      link.classList.toggle('active', link.dataset.view === view);
    }
    window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });
  }

  function parseRoute() {
    const raw = window.location.hash.replace(/^#\/?/, '');
    const [path, query] = raw.split('?');
    return { path: path || '', params: new URLSearchParams(query || '') };
  }

  function readFiltersFromUrl(params) {
    for (const key of FILTER_KEYS) {
      state.filters[key] = params.get(key) || '';
    }
  }

  function syncFilterControls() {
    $('#idx-search').value = state.filters.q;
    $('#idx-group').value = state.filters.group;
    $('#idx-shape').value = state.filters.shape;
    $('#idx-vendor').value = state.filters.vendor;
    $('#idx-feedback').value = state.filters.feedback;
    $('#idx-license').value = state.filters.license;
    $('#idx-lang').value = state.filters.lang;
  }

  function writeFiltersToUrl() {
    const params = new URLSearchParams();
    for (const key of FILTER_KEYS) {
      if (state.filters[key]) params.set(key, state.filters[key]);
    }
    const query = params.toString();
    const next = `#/index${query ? `?${query}` : ''}`;
    if (window.location.hash !== next) window.location.hash = next;
  }

  function route() {
    const { path, params } = parseRoute();
    const [name, param] = path.split('/');

    if (name === 'repo' && param) {
      showView('index');
      readFiltersFromUrl(params);
      syncFilterControls();
      renderIndex();
      openDrawer(decodeURIComponent(param));
      return;
    }
    if (name === 'index') {
      showView('index');
      readFiltersFromUrl(params);
      syncFilterControls();
      renderIndex();
      return;
    }
    if (name === 'compare') {
      showView('compare');
      activateCompareTab(params.get('tab') || 'arch');
      return;
    }
    if (name === 'knowledge') {
      showView('knowledge');
      return renderKnowledge();
    }
    return showView('overview');
  }

  // ------------------------------------------------------------------ 主题

  const THEME_KEY = 'ai4kernel-theme';

  function currentTheme() {
    return document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  }

  function applyTheme(theme, persist) {
    document.documentElement.setAttribute('data-theme', theme);
    if (persist) {
      try {
        localStorage.setItem(THEME_KEY, theme);
      } catch {
        /* 隐私模式下写不进去，忽略 */
      }
    }
    const toggle = $('#theme-toggle');
    if (toggle) {
      toggle.setAttribute(
        'aria-label',
        theme === 'light' ? '切换到深色主题' : '切换到浅色主题'
      );
    }
  }

  function initTheme() {
    applyTheme(currentTheme(), false);
    const toggle = $('#theme-toggle');
    if (toggle) {
      toggle.addEventListener('click', () => {
        applyTheme(currentTheme() === 'light' ? 'dark' : 'light', true);
      });
    }
  }

  // ------------------------------------------------------------------ 启动

  function bindEvents() {
    window.addEventListener('hashchange', route);

    $('#drawer-close').addEventListener('click', closeDrawer);
    $('#drawer-backdrop').addEventListener('click', closeDrawer);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && $('#drawer').classList.contains('open')) closeDrawer();
    });

    // 表格行点击 → 抽屉
    document.addEventListener('click', (e) => {
      const row = e.target.closest('tr[data-canonical]');
      if (row) {
        const canonical = row.dataset.canonical;
        if (e.target.tagName === 'A') return;
        openDrawer(canonical);
        return;
      }
      const tab = e.target.closest('.tab');
      if (tab) {
        activateCompareTab(tab.dataset.panel.replace('cmp-', ''));
        // 标签页写进 URL，深链接与前进后退都能还原
        const params = new URLSearchParams();
        params.set('tab', tab.dataset.panel.replace('cmp-', ''));
        const next = `#/compare?${params.toString()}`;
        if (window.location.hash !== next) window.location.hash = next;
      }
    });

    // 索引筛选
    const applyFilters = () => {
      state.filters.group = $('#idx-group').value;
      state.filters.shape = $('#idx-shape').value;
      state.filters.vendor = $('#idx-vendor').value;
      state.filters.feedback = $('#idx-feedback').value;
      state.filters.license = $('#idx-license').value;
      state.filters.lang = $('#idx-lang').value;
      writeFiltersToUrl();
      renderIndex();
    };
    for (const id of [
      '#idx-group',
      '#idx-shape',
      '#idx-vendor',
      '#idx-feedback',
      '#idx-license',
      '#idx-lang',
    ]) {
      $(id).addEventListener('change', applyFilters);
    }

    const onSearch = debounce(() => {
      state.filters.q = $('#idx-search').value.trim();
      writeFiltersToUrl();
      renderIndex();
    }, 160);
    $('#idx-search').addEventListener('input', onSearch);

    $('#idx-clear').addEventListener('click', () => {
      for (const key of FILTER_KEYS) state.filters[key] = '';
      syncFilterControls();
      writeFiltersToUrl();
      renderIndex();
    });

    // 表头排序
    for (const th of $$('#idx-table th.sortable')) {
      th.addEventListener('click', () => {
        const key = th.dataset.sort;
        if (state.sort.key === key) {
          state.sort.dir = state.sort.dir === 'asc' ? 'desc' : 'asc';
        } else {
          state.sort = { key, dir: key === 'stars' ? 'desc' : 'asc' };
        }
        for (const other of $$('#idx-table th.sortable')) {
          const arrow = $('.sort-arrow', other);
          if (arrow) arrow.remove();
        }
        const arrow = document.createElement('span');
        arrow.className = 'sort-arrow';
        arrow.textContent = state.sort.dir === 'asc' ? '↑' : '↓';
        th.appendChild(arrow);
        renderIndex();
      });
    }

    // 顶部全局搜索 → 跳到索引并带上查询
    $('#global-search').addEventListener('keydown', (e) => {
      if (e.key !== 'Enter') return;
      const value = e.target.value.trim();
      if (!value) return;
      state.filters.q = value;
      $('#idx-search').value = value;
      showView('index');
      writeFiltersToUrl();
      renderIndex();
    });
  }

  async function boot() {
    initTheme();
    try {
      const res = await fetch(DATA_URL);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      state.data = await res.json();
    } catch (err) {
      document.querySelector('main').innerHTML =
        `<div class="page"><p class="note">数据载入失败：${esc(err.message)}。`
        + '请通过 HTTP 服务访问本站（直接双击打开 HTML 无法读取本地数据文件）。</p></div>';
      return;
    }

    renderOverview();
    initIndexFilters();
    renderIndex();
    renderCompare();
    bindEvents();
    route();
  }

  document.addEventListener('DOMContentLoaded', boot);
})();
