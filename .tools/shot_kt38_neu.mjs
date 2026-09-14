import { chromium } from 'playwright-core';
import { fileURLToPath } from 'url'; import { dirname, join } from 'path';
import { mkdirSync, readdirSync } from 'fs';
const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..', 'klimatech38');
const outDir = join(__dirname, 'shots-kt38-neu'); mkdirSync(outDir, { recursive: true });
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
const args = process.argv.slice(2);
const seiten = args.length ? args : readdirSync(root).filter(f => f.endsWith('.html')).map(f => f.replace('.html',''));
const MOBIL = ['index','shop','shop-split','set-split-35','beratung','kontakt','faq','ratgeber-kosten','montage','energetische-beratung'];
const fehler = [];
for (const [w,h,tag] of [[1440,900,'desk'],[834,1112,'834'],[390,844,'390']]) {
  const ctx = await browser.newContext({ viewport:{width:w,height:h}, deviceScaleFactor:1, reducedMotion:'reduce' });
  const page = await ctx.newPage();
  page.on('console', m => { if (m.type()==='error') fehler.push(`${tag} console: ${m.text()}`); });
  page.on('pageerror', e => fehler.push(`${tag} pageerror: ${e.message}`));
  for (const s of seiten) {
    if (tag !== 'desk' && !MOBIL.includes(s) && !args.length) continue;
    await page.goto('http://localhost:8765/' + s + '.html', { waitUntil:'networkidle' });
    await page.evaluate(async () => { const h = document.body.scrollHeight; for (let y = 0; y < h; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(500);
    await page.screenshot({ path: join(outDir, `${s}-${tag}.png`), fullPage: true });
    const ov = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    if (ov.sw > ov.cw + 1) fehler.push(`${s} ${tag}: horizontaler Overflow ${ov.sw}px > ${ov.cw}px`);
  }
  await ctx.close();
}
await browser.close();
console.log(fehler.length ? '\nBEFUNDE:\n' + fehler.join('\n') : '\nkeine Konsolenfehler, kein Overflow');
