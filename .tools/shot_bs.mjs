import { chromium } from 'playwright-core';
import { fileURLToPath } from 'url'; import { dirname, join } from 'path';
import { mkdirSync } from 'fs';
const __dirname = dirname(fileURLToPath(import.meta.url));
const outDir = join(__dirname, 'shots-bauschulz'); mkdirSync(outDir, { recursive: true });
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
const seiten = process.argv[2] ? process.argv[2].split(',') : ['index','bautagebuch','leistungen','neubau','referenzen','referenz-seniorenwohnanlage-wahrenholz','referenz-bruecke','ueber-uns','kontakt','impressum'];
const breiten = process.argv[3] ? process.argv[3].split(',').map(Number) : [1440, 834, 390];
for (const s of seiten) {
  for (const w of breiten) {
    const h = w >= 1200 ? 900 : (w >= 700 ? 1112 : 844);
    const tag = w === 1440 ? 'desk' : String(w);
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1.5 });
    const page = await ctx.newPage();
    const fehler = [];
    page.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); });
    page.on('pageerror', e => fehler.push('PAGEERROR ' + e.message));
    await page.goto('http://localhost:8790/' + s + '.html', { waitUntil: 'networkidle' });
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(1200);
    const ov = await page.evaluate(() => ({
      docW: document.documentElement.scrollWidth, winW: window.innerWidth,
      breit: [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > window.innerWidth + 2)
        .slice(0, 6).map(e => e.tagName + '.' + (e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className).toString().split(' ')[0])
    }));
    await page.screenshot({ path: join(outDir, s + '-' + tag + '.png'), fullPage: true });
    console.log(s, tag, 'overflow:', ov.docW > ov.winW ? ('JA ' + ov.docW + '>' + ov.winW + ' ' + JSON.stringify(ov.breit)) : 'nein', 'jsFehler:', fehler.length ? fehler.slice(0, 3) : 0);
    await ctx.close();
  }
}
await browser.close();
