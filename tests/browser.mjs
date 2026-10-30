/* 站点冒烟测试：逐个视图检查渲染、交互与控制台错误。
 *
 * 默认测本地构建产物；传 BASE_URL 可以直接测已部署的站点：
 *   node tests/browser.mjs
 *   BASE_URL=https://yifeistarwang-coder.github.io/ai4kernel-opensource node tests/browser.mjs
 *
 * 需要 playwright：
 *   npm ci && npx playwright install chromium
 */
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const EXTERNAL = process.env.BASE_URL;
const SHOTS = process.env.SHOTS || 'test-results';

const problems = [];
const note = (msg) => problems.push(msg);

function startServer() {
  // 端口用 0 由内核分配，避免撞上机器上已在运行的其它服务
  const proc = spawn('python3', ['-u', '-m', 'http.server', '0', '--directory', 'dist'], {
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return proc;
}

function resolvePort(proc) {
  return new Promise((resolve, reject) => {
    let buffer = '';
    const timer = setTimeout(() => reject(new Error('server did not report a port')), 10000);
    const scan = (chunk) => {
      buffer += chunk.toString();
      const match = buffer.match(/port (\d+)/);
      if (match) {
        clearTimeout(timer);
        resolve(Number(match[1]));
      }
    };
    proc.stdout.on('data', scan);
    proc.stderr.on('data', scan);
    proc.on('exit', (code) => {
      clearTimeout(timer);
      reject(new Error(`server exited with ${code}`));
    });
  });
}

async function waitForServer(base, retries = 40) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(`${base}/index.html`);
      if (res.ok) return true;
    } catch {
      /* 还没起来 */
    }
    await sleep(250);
  }
  return false;
}

async function main() {
  let server = null;
  let BASE = EXTERNAL;
  if (!BASE) {
    server = startServer();
    const port = await resolvePort(server);
    BASE = `http://127.0.0.1:${port}`;
    if (!(await waitForServer(BASE))) {
      console.error('server did not start');
      server.kill();
      process.exit(1);
    }
  }

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });

  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', (err) => consoleErrors.push(`pageerror: ${err.message}`));

  const failedRequests = [];
  page.on('response', (res) => {
    if (res.status() >= 400) failedRequests.push(`${res.status()} ${res.url()}`);
  });

  // ---------------------------------------------------------- 概览
  await page.goto(`${BASE}/index.html#/overview`, { waitUntil: 'networkidle' });
  await page.waitForSelector('#hero-stats .stat', { timeout: 10000 });

  const statCount = await page.locator('#hero-stats .stat').count();
  if (statCount !== 5) note(`overview: expected 5 hero stats, got ${statCount}`);

  const shapeBars = await page.locator('#shape-bars .bar-row').count();
  if (shapeBars < 5) note(`overview: shape bars too few (${shapeBars})`);

  const vendorBars = await page.locator('#vendor-bars .bar-row').count();
  if (vendorBars < 3) note(`overview: vendor bars too few (${vendorBars})`);

  const feedbackBars = await page.locator('#feedback-bars .bar-row').count();
  if (feedbackBars < 3) note(`overview: feedback bars too few (${feedbackBars})`);

  await page.screenshot({ path: `${SHOTS}/overview.png`, fullPage: true });

  // ---------------------------------------------------------- 索引
  await page.click('a[data-view="index"]');
  await page.waitForSelector('#idx-body tr', { timeout: 10000 });

  const rowCount = await page.locator('#idx-body tr').count();
  if (rowCount !== 61) note(`index: expected 61 rows, got ${rowCount}`);

  // 搜索
  await page.fill('#idx-search', 'triton');
  await sleep(320);
  const filtered = await page.locator('#idx-body tr').count();
  if (filtered === 0 || filtered >= rowCount) note(`index: search "triton" gave ${filtered} rows`);
  const caption = await page.textContent('#idx-count');
  if (!caption.includes('/ 61')) note(`index: count caption wrong: ${caption}`);

  await page.fill('#idx-search', '');
  await sleep(320);

  // 分类筛选
  const groupOptions = await page.locator('#idx-group option').count();
  if (groupOptions < 6) note(`index: group filter has ${groupOptions} options`);

  await page.selectOption('#idx-group', 'foundation');
  await sleep(220);
  const foundationRows = await page.locator('#idx-body tr').count();
  if (foundationRows !== 9) note(`index: foundation filter gave ${foundationRows} rows, expected 9`);
  await page.selectOption('#idx-group', '');
  await sleep(220);

  // 厂商筛选
  await page.selectOption('#idx-vendor', 'AMD');
  await sleep(220);
  const amdRows = await page.locator('#idx-body tr').count();
  if (amdRows !== 12) note(`index: AMD filter gave ${amdRows} rows, expected 12`);
  await page.selectOption('#idx-vendor', '');
  await sleep(220);

  // 排序
  await page.click('#idx-table th[data-sort="stars"]');
  await sleep(220);
  const firstStar = await page.locator('#idx-body tr').first().locator('td').last().textContent();
  if (!firstStar || firstStar.trim() === '—') note('index: star sort produced empty first row');

  // 空结果
  await page.fill('#idx-search', 'zzzzznotarealrepo');
  await sleep(320);
  if (await page.locator('#idx-empty').isHidden()) note('index: empty state not shown for no matches');
  await page.fill('#idx-search', '');
  await sleep(320);

  await page.screenshot({ path: `${SHOTS}/index.png`, fullPage: true });

  // ---------------------------------------------------------- 抽屉
  await page.locator('#idx-body tr').first().click();
  await page.waitForSelector('#drawer.open', { timeout: 5000 });
  await sleep(400); // 等抽屉滑入动画结束，否则截图停在过渡中间
  const drawerTitle = await page.textContent('#drawer-title');
  if (!drawerTitle || !drawerTitle.includes('/')) note(`drawer: bad title ${drawerTitle}`);
  const drawerBody = await page.textContent('#drawer-body');
  for (const section of ['基本信息', '架构模式', '主要模块']) {
    if (!drawerBody.includes(section)) note(`drawer: missing section ${section}`);
  }
  await page.screenshot({ path: `${SHOTS}/drawer.png` });
  await page.click('#drawer-close');
  await page.waitForSelector('#drawer:not(.open)', { timeout: 5000 });

  // ---------------------------------------------------------- 对比
  await page.click('a[data-view="compare"]');
  await page.waitForSelector('#cmp-arch-body tr', { timeout: 10000 });

  const archRows = await page.locator('#cmp-arch-body tr').count();
  if (archRows !== 61) note(`compare: arch table has ${archRows} rows, expected 61`);

  const shapeCards = await page.locator('#cmp-arch-cards .card').count();
  if (shapeCards !== 7) note(`compare: expected 7 shape cards, got ${shapeCards}`);

  await page.click('.tab[data-panel="cmp-base"]');
  await page.waitForSelector('#cmp-base-body tr', { timeout: 5000 });
  const baseRows = await page.locator('#cmp-base-body tr').count();
  if (baseRows < 10) note(`compare: base layer table has ${baseRows} rows`);

  await page.click('.tab[data-panel="cmp-vendor"]');
  await page.waitForSelector('#cmp-vendor-body tr', { timeout: 5000 });
  const vendorRows = await page.locator('#cmp-vendor-body tr').count();
  if (vendorRows < 4) note(`compare: vendor table has ${vendorRows} rows`);

  await page.click('.tab[data-panel="cmp-archchip"]');
  await page.waitForSelector('#cmp-chip-body tr', { timeout: 5000 });
  const chipRows = await page.locator('#cmp-chip-body tr').count();
  if (chipRows < 6) note(`compare: hw arch table has ${chipRows} rows`);

  await page.click('.tab[data-panel="cmp-matrix"]');
  await page.waitForSelector('#cmp-matrix-body tr', { timeout: 5000 });
  const matrixRows = await page.locator('#cmp-matrix-body tr').count();
  if (matrixRows < 4) note(`compare: matrix has ${matrixRows} rows`);
  const matrixCols = await page.locator('#cmp-matrix-head th').count();
  if (matrixCols < 5) note(`compare: matrix has ${matrixCols} columns`);

  // 标签页写进 URL，深链接能直接落到那个标签页
  if (!page.url().includes('tab=matrix')) {
    note(`compare: tab not in url: ${page.url()}`);
  }
  await page.goto(`${BASE}/index.html#/compare?tab=base`, { waitUntil: 'networkidle' });
  await page.waitForSelector('#cmp-base-body tr', { timeout: 5000 });
  if (await page.locator('#cmp-arch-body').isVisible()) {
    note('compare: deep link to tab=base did not switch panels');
  }

  await page.screenshot({ path: `${SHOTS}/compare.png`, fullPage: true });

  // ---------------------------------------------------------- 抽象知识
  await page.click('a[data-view="knowledge"]');
  await page.waitForSelector('#knowledge-body h1', { timeout: 10000 });
  const proseH1 = await page.textContent('#knowledge-body h1');
  if (!proseH1.includes('抽象知识')) note(`knowledge: unexpected title ${proseH1}`);
  const proseTables = await page.locator('#knowledge-body table').count();
  if (proseTables < 8) note(`knowledge: only ${proseTables} tables rendered`);
  const proseLists = await page.locator('#knowledge-body li').count();
  if (proseLists < 50) note(`knowledge: only ${proseLists} list items rendered`);

  // 渲染结果里不应出现被当成标签执行的第三方标记
  const rawParquet = await page.locator('#knowledge-body script').count();
  if (rawParquet > 0) note('knowledge: script element present in rendered markdown');

  await page.screenshot({ path: `${SHOTS}/knowledge.png`, fullPage: true });

  // ---------------------------------------------------------- 概览 → 索引联动
  await page.goto(`${BASE}/index.html#/overview`, { waitUntil: 'networkidle' });
  await page.waitForSelector('#feedback-bars .bar-row');
  await sleep(300);

  const bars = await page.locator('#feedback-bars a.bar-row').count();
  if (bars < 3) note(`overview: feedback bars are not links (${bars})`);

  // 点击「Profile」应跳到索引并按反馈信号筛选
  await page.locator('#feedback-bars a.bar-row', { hasText: 'Profile' }).click();
  await page.waitForSelector('#idx-body tr', { timeout: 8000 });
  await sleep(300);
  if (await page.locator('#page-index').isHidden()) note('bar click: did not open the index view');
  if (!page.url().includes('feedback=Profile')) {
    note(`bar click: url missing feedback filter: ${page.url()}`);
  }
  const profileRows = await page.locator('#idx-body tr').count();
  if (profileRows !== 13) note(`bar click: Profile filter gave ${profileRows} rows, expected 13`);
  const barCaption = await page.textContent('#index-caption');
  if (!barCaption.includes('Profile')) {
    note(`bar click: caption does not mention the filter: ${barCaption}`);
  }
  const clearVisible = await page.locator('#idx-clear').isVisible();
  if (!clearVisible) note('bar click: clear-filter button not shown');
  // 每一行都必须真的带 Profile 反馈信号
  const allProfile = await page.evaluate(() =>
    Array.from(document.querySelectorAll('#idx-body tr')).every((tr) =>
      tr.children[6].textContent.includes('Profile')
    )
  );
  if (!allProfile) note('bar click: filtered rows do not all carry the Profile signal');

  // 分享链接：直接打开带筛选的 URL 应还原同样的结果
  await page.goto(`${BASE}/index.html#/index?feedback=Profile`, { waitUntil: 'networkidle' });
  await page.waitForSelector('#idx-body tr');
  await sleep(300);
  const sharedRows = await page.locator('#idx-body tr').count();
  if (sharedRows !== 13) note(`shared url: gave ${sharedRows} rows, expected 13`);

  // 清除筛选
  await page.click('#idx-clear');
  await sleep(300);
  const clearedRows = await page.locator('#idx-body tr').count();
  if (clearedRows !== 61) note(`clear filter: gave ${clearedRows} rows, expected 61`);

  // 厂商条形图同样可点
  await page.goto(`${BASE}/index.html#/overview`, { waitUntil: 'networkidle' });
  await page.waitForSelector('#vendor-bars a.bar-row');
  await page.locator('#vendor-bars a.bar-row', { hasText: 'AMD' }).click();
  await page.waitForSelector('#idx-body tr', { timeout: 8000 });
  await sleep(300);
  const amdViaBar = await page.locator('#idx-body tr').count();
  if (amdViaBar !== 12) note(`bar click: AMD filter gave ${amdViaBar} rows, expected 12`);

  // 形态条形图同样可点
  await page.goto(`${BASE}/index.html#/overview`, { waitUntil: 'networkidle' });
  await page.waitForSelector('#shape-bars a.bar-row');
  await page.locator('#shape-bars a.bar-row', { hasText: 'Agent 生成闭环' }).click();
  await page.waitForSelector('#idx-body tr', { timeout: 8000 });
  await sleep(300);
  const shapeRows = await page.locator('#idx-body tr').count();
  if (shapeRows !== 15) note(`bar click: shape C gave ${shapeRows} rows, expected 15`);

  // 形态卡片同样可点
  await page.goto(`${BASE}/index.html#/compare`, { waitUntil: 'networkidle' });
  await page.waitForSelector('#cmp-arch-cards a.card');
  await page.locator('#cmp-arch-cards a.card', { hasText: 'Agent 生成闭环' }).click();
  await page.waitForSelector('#idx-body tr', { timeout: 8000 });
  await sleep(300);
  const cardRows = await page.locator('#idx-body tr').count();
  if (cardRows !== 15) note(`shape card: gave ${cardRows} rows, expected 15`);

  // ---------------------------------------------------------- 主题切换
  await page.goto(`${BASE}/index.html#/overview`, { waitUntil: 'networkidle' });
  await page.waitForSelector('#hero-stats .stat', { timeout: 10000 });
  await sleep(300);
  const initialTheme = await page.getAttribute('html', 'data-theme');
  if (!['light', 'dark'].includes(initialTheme)) {
    note(`theme: unexpected data-theme "${initialTheme}"`);
  }
  const paperBefore = await page.evaluate(
    () => getComputedStyle(document.body).backgroundColor
  );

  await page.click('#theme-toggle');
  await sleep(250);
  const toggled = await page.getAttribute('html', 'data-theme');
  if (toggled === initialTheme) note('theme: toggle did not change data-theme');
  const paperAfter = await page.evaluate(
    () => getComputedStyle(document.body).backgroundColor
  );
  if (paperAfter === paperBefore) note('theme: body background did not change');

  const stored = await page.evaluate(() => localStorage.getItem('ai4kernel-theme'));
  if (stored !== toggled) note(`theme: localStorage holds "${stored}", expected "${toggled}"`);

  await page.screenshot({ path: `${SHOTS}/theme-${toggled}.png`, fullPage: true });

  // 浅色下的关键色值必须真的变了
  const inkAfter = await page.evaluate(
    () => getComputedStyle(document.documentElement).getPropertyValue('--ink').trim()
  );
  if (toggled === 'light' && inkAfter === '#f1f6fb') {
    note('theme: light palette not applied (--ink still the dark value)');
  }

  await page.click('#theme-toggle');
  await sleep(250);
  const back = await page.getAttribute('html', 'data-theme');
  if (back !== initialTheme) note(`theme: toggle back gave "${back}", expected "${initialTheme}"`);

  // 重新加载后应记住选择
  await page.reload({ waitUntil: 'networkidle' });
  await sleep(300);
  const persisted = await page.getAttribute('html', 'data-theme');
  if (persisted !== back) note(`theme: after reload got "${persisted}", expected "${back}"`);

  // ---------------------------------------------------------- 全局搜索
  await page.fill('#global-search', 'tilelang');
  await page.press('#global-search', 'Enter');
  await sleep(400);
  if (await page.locator('#page-index').isHidden()) note('global search: did not navigate to index');
  const globalRows = await page.locator('#idx-body tr').count();
  if (globalRows === 0 || globalRows >= 61) note(`global search: gave ${globalRows} rows`);

  await browser.close();
  if (server) server.kill();

  if (consoleErrors.length) note(`console errors: ${consoleErrors.slice(0, 5).join(' | ')}`);
  if (failedRequests.length) note(`failed requests: ${failedRequests.slice(0, 5).join(' | ')}`);

  if (problems.length) {
    console.error(`\n${problems.length} problem(s):`);
    for (const p of problems) console.error(`  - ${p}`);
    process.exit(1);
  }
  console.log('browser checks passed');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
