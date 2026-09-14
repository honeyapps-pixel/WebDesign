import { chromium } from 'playwright-core';
import { fileURLToPath } from 'url'; import { dirname, join } from 'path';
const __dirname = dirname(fileURLToPath(import.meta.url));
const out = join(__dirname, 'shots-bauschulz');
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
// 1 · Wheel-Scroll + Reveals
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto('http://localhost:8790/index.html', { waitUntil: 'networkidle' });
  await page.mouse.move(950, 500);
  for (let i = 0; i < 60; i++) { await page.mouse.wheel(0, 400); await page.waitForTimeout(60); }
  await page.waitForTimeout(1500);
  const r = await page.evaluate(() => ({ y: Math.round(window.scrollY), h: document.body.scrollHeight, hidden: [...document.querySelectorAll('[data-reveal]')].filter(e => parseFloat(getComputedStyle(e).opacity) < .95).map(e => e.className) }));
  console.log('wheel', JSON.stringify(r));
  await ctx.close();
}
// 2 · Drawer mobil
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto('http://localhost:8790/index.html', { waitUntil: 'networkidle' });
  await page.click('[data-drawer-toggle]'); await page.waitForTimeout(500);
  const st = await page.evaluate(() => ({ offen: document.querySelector('[data-drawer]').classList.contains('is-offen'), inert: document.querySelector('[data-drawer]').hasAttribute('inert'), fokus: document.activeElement && document.activeElement.textContent.trim().slice(0, 20), body: document.body.className }));
  console.log('drawer', JSON.stringify(st));
  await page.screenshot({ path: join(out, 'drawer-390.png') });
  await page.keyboard.press('Escape'); await page.waitForTimeout(400);
  console.log('drawer nach Esc', await page.evaluate(() => document.querySelector('[data-drawer]').classList.contains('is-offen')));
  // Mobil: Inline-Bilder im Tagebuch sichtbar?
  const inl = await page.evaluate(() => { const p = document.querySelectorAll('.tb__inline'); return { n: p.length, sichtbar: [...p].filter(e => e.offsetParent !== null).length, buehne: getComputedStyle(document.querySelector('.tb__buehne')).display }; });
  console.log('mobil tagebuch', JSON.stringify(inl));
  await ctx.close();
}
// 3 · Reduced motion
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto('http://localhost:8790/index.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  const r = await page.evaluate(() => ({ anim: document.documentElement.className, hidden: [...document.querySelectorAll('[data-reveal]')].filter(e => parseFloat(getComputedStyle(e).opacity) < .95).length, hero: getComputedStyle(document.querySelector('.hero__frame')).animationName, pulse: getComputedStyle(document.querySelector('.wa-fab__pulse')).animationName }));
  console.log('reduced', JSON.stringify(r));
  await page.screenshot({ path: join(out, 'reduced-hero.png') });
  await ctx.close();
}
// 4 · Tastatur: Tab-Reihenfolge Kopf + Fokus sichtbar
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto('http://localhost:8790/index.html', { waitUntil: 'networkidle' });
  const reihe = [];
  for (let i = 0; i < 9; i++) { await page.keyboard.press('Tab'); reihe.push(await page.evaluate(() => { const a = document.activeElement; return a.tagName + ':' + (a.getAttribute('aria-label') || a.textContent.trim().slice(0, 18)); })); }
  console.log('tab', reihe.join(' > '));
  await page.screenshot({ path: join(out, 'fokus-nav.png'), clip: { x: 0, y: 0, width: 1440, height: 160 } });
  // LV Akkordeon
  await page.click('.lv details:nth-of-type(2) summary'); await page.waitForTimeout(200);
  console.log('lv open', await page.evaluate(() => [...document.querySelectorAll('.lv details')].map(d => d.open)));
  // Formular
  await page.fill('#f-name', 'Test'); await page.fill('#f-mail', 'test@example.com');
  await page.evaluate(() => { window.__href = null; const f = document.querySelector('[data-form]'); f.addEventListener('submit', () => {}, true); });
  const [nav] = await Promise.all([page.waitForEvent('framenavigated', { timeout: 3000 }).catch(() => null), page.click('[data-form] button[type=submit]')]);
  console.log('form meldung', await page.evaluate(() => document.querySelector('[data-form-meldung]').textContent.slice(0, 60)));
  await ctx.close();
}
await browser.close();
