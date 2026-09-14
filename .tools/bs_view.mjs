// Viewport-Aufnahmen an bestimmten Scrollpositionen (echtes Wheel-Scrollen, Lenis aktiv)
import { chromium } from 'playwright-core';
import { fileURLToPath } from 'url'; import { dirname, join } from 'path';
import { mkdirSync } from 'fs';
const __dirname = dirname(fileURLToPath(import.meta.url));
const outDir = join(__dirname, 'shots-bauschulz'); mkdirSync(outDir, { recursive: true });
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
const seite = process.argv[2] || 'index';
const w = Number(process.argv[3] || 1440), h = w >= 1200 ? 900 : (w >= 700 ? 1112 : 844);
const sel = process.argv[4] || '#bautagebuch';
const schritte = Number(process.argv[5] || 6);
const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1.5 });
const page = await ctx.newPage();
const fehler = [];
page.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); });
page.on('pageerror', e => fehler.push('PAGEERROR ' + e.message));
await page.goto('http://localhost:8790/' + seite + '.html', { waitUntil: 'networkidle' });
await page.mouse.move(w / 2, h / 2);
const top = await page.evaluate(s => { const el = document.querySelector(s); return el ? el.getBoundingClientRect().top + window.scrollY : 0; }, sel);
const hoehe = await page.evaluate(s => { const el = document.querySelector(s); return el ? el.getBoundingClientRect().height : 0; }, sel);
// per Wheel zur Sektion scrollen
let y = 0;
while (y < top - 40) { await page.mouse.wheel(0, 300); y += 300; await page.waitForTimeout(40); }
await page.waitForTimeout(900);
for (let i = 0; i < schritte; i++) {
  await page.screenshot({ path: join(outDir, `${seite}-${w}-view-${i}.png`) });
  const stand = await page.evaluate(() => ({ y: Math.round(window.scrollY), num: document.querySelector('[data-tb-num]')?.textContent, on: [...document.querySelectorAll('.tb__img.is-on')].map(i => i.getAttribute('src')), plan: !!document.querySelector('[data-plan].is-on') }));
  console.log(i, JSON.stringify(stand));
  const d = Math.max(300, Math.round(hoehe / schritte));
  for (let k = 0; k < d; k += 150) { await page.mouse.wheel(0, 150); await page.waitForTimeout(30); }
  await page.waitForTimeout(800);
}
console.log('jsFehler', fehler);
await browser.close();
