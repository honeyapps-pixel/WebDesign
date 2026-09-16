// Element-Screenshots: node shot_bwa_el.mjs <seite> <breite> <selector1,selector2,...>
import { chromium } from 'playwright-core';
import { fileURLToPath } from 'url'; import { dirname, join } from 'path';
import { mkdirSync } from 'fs';
const __dirname = dirname(fileURLToPath(import.meta.url));
const outDir = join(__dirname, 'shots-bwa'); mkdirSync(outDir, { recursive: true });
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
const [seite, wS, sels] = process.argv.slice(2);
const w = Number(wS || 1440); const h = w >= 1200 ? 900 : (w >= 700 ? 1112 : 844);
const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1.5 });
const page = await ctx.newPage();
await page.goto('http://localhost:8793/' + seite + '.html', { waitUntil: 'networkidle' });
await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } window.scrollTo(0, 0); });
await page.addStyleTag({ content: '.wa-fab{display:none!important}' });
await page.waitForTimeout(900);
let i = 0;
for (const sel of sels.split(',')) {
  const el = await page.$(sel);
  if (!el) { console.log('fehlt:', sel); continue; }
  await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(400);
  const f = join(outDir, `${seite}-${w}-el${i++}.png`);
  await el.screenshot({ path: f });
  console.log(sel, '→', f);
}
await browser.close();
