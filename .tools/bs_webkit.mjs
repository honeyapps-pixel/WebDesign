// WebKit-(Safari-Engine-)Prüfung der LIVE-Seite: Konsole, Overflow, Fonts, sticky, Karte, Anker, Drawer, Screenshots
import { webkit } from 'playwright-core';
import { fileURLToPath } from 'url'; import { dirname, join } from 'path';
import { mkdirSync } from 'fs';
const __dirname = dirname(fileURLToPath(import.meta.url));
const out = join(__dirname, 'shots-bauschulz', 'webkit'); mkdirSync(out, { recursive: true });
const exe = process.env.HOME + '/Library/Caches/ms-playwright/webkit-2311/pw_run.sh';
const base = process.argv[2] || 'https://bauschulz.vercel.app/';
const seiten = ['index', 'bautagebuch', 'leistungen', 'neubau', 'referenzen', 'referenz-seniorenwohnanlage-wahrenholz', 'referenz-bruecke', 'ueber-uns', 'kontakt', 'impressum'];
const browser = await webkit.launch({ executablePath: exe });
for (const s of seiten) {
  for (const [w, h, tag, mobil] of [[1440, 900, 'desk', false], [390, 844, '390', true]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: mobil, hasTouch: mobil, userAgent: mobil ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' : undefined });
    const page = await ctx.newPage();
    const fehler = [];
    page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') fehler.push(m.type() + ': ' + m.text().slice(0, 120)); });
    page.on('pageerror', e => fehler.push('PAGEERROR ' + e.message));
    page.on('requestfailed', r => fehler.push('REQFAIL ' + r.url().slice(-60)));
    await page.goto(base + s + '.html', { waitUntil: 'networkidle' });
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(1200);
    const r = await page.evaluate(() => {
      const fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v, i, a) => a.indexOf(v) === i);
      const hidden = [...document.querySelectorAll('[data-reveal]')].filter(e => parseFloat(getComputedStyle(e).opacity) < .95).length;
      return { docW: document.documentElement.scrollWidth, winW: innerWidth, fonts, hidden, sticky: getComputedStyle(document.querySelector('.navbar') || document.body).position, karte: !!document.querySelector('.leaflet-container'), marker: document.querySelectorAll('.giebel-marker').length };
    });
    await page.screenshot({ path: join(out, `${s}-${tag}.png`), fullPage: true });
    console.log(s, tag, 'ov:', r.docW > r.winW ? 'JA ' + (r.docW - r.winW) : 'nein', 'fonts:', r.fonts.length, 'hiddenReveal:', r.hidden, 'karte:', r.karte, r.marker, 'fehler:', fehler.length ? fehler.slice(0, 4) : 0);
    await ctx.close();
  }
}
// Interaktion Desktop: Anker + Leiste + Drawer (mobil)
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto(base + 'index.html', { waitUntil: 'networkidle' });
  await page.click('a[href="#bautagebuch"]'); await page.waitForTimeout(1500);
  console.log('anker #bautagebuch top:', await page.evaluate(() => Math.round(document.querySelector('#bautagebuch').getBoundingClientRect().top)));
  await page.click('.tb__leiste a[href="#phase-09"]'); await page.waitForTimeout(1500);
  console.log('anker phase-09 top:', await page.evaluate(() => Math.round(document.querySelector('#phase-09').getBoundingClientRect().top)), 'stand:', await page.evaluate(() => document.querySelector('[data-tb-num]').textContent));
  await ctx.close();
}
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  await page.goto(base + 'index.html', { waitUntil: 'networkidle' });
  await page.tap('[data-drawer-toggle]'); await page.waitForTimeout(500);
  await page.screenshot({ path: join(out, 'drawer-390.png') });
  console.log('drawer offen:', await page.evaluate(() => document.querySelector('[data-drawer]').classList.contains('is-offen')));
  await page.tap('.drawer__zu'); await page.waitForTimeout(400);
  console.log('drawer zu:', await page.evaluate(() => !document.querySelector('[data-drawer]').classList.contains('is-offen')));
  await page.evaluate(() => window.scrollTo(0, 1800)); await page.waitForTimeout(800);
  await page.screenshot({ path: join(out, 'tagebuch-390-view.png') });
  console.log('mobil stand:', await page.evaluate(() => document.querySelector('[data-tb-num]').textContent + ' ' + document.querySelector('[data-tb-titel]').textContent));
  await ctx.close();
}
await browser.close();
