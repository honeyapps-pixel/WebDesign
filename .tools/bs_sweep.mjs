import { chromium } from 'playwright-core';
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
const seiten = process.argv[2] ? process.argv[2].split(',') : ['index','bautagebuch','leistungen','neubau','gewerbe-industrie','sonderbauten','referenzen','referenz-seniorenwohnanlage-wittingen','referenz-einfamilienhaus-sassenburg','referenz-sozialer-wohnungsbau-knesebeck','referenz-garagenpark-sassenburg','referenz-doppelhaus-gifhorn','referenz-wohnanlage-wolfsburg-ehmen','referenz-seniorenwohnanlage-wahrenholz','referenz-bruecke','ueber-uns','kontakt','impressum','datenschutz'];
const breiten = [320,360,390,480,640,760,834,880,881,980,1100,1160,1280,1440,1920];
let probleme = 0;
for (const s of seiten) {
  const zeile = [];
  for (const w of breiten) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
    const page = await ctx.newPage();
    const fehler = [];
    page.on('pageerror', e => fehler.push(e.message));
    await page.goto('http://localhost:8790/' + s + '.html', { waitUntil: 'load' });
    await page.waitForTimeout(150);
    const r = await page.evaluate(() => {
      const ov = document.documentElement.scrollWidth - window.innerWidth;
      const breit = [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.right > window.innerWidth + 1 && b.width > 0; }).slice(0, 3).map(e => e.tagName.toLowerCase() + '.' + String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className).split(' ')[0]);
      return { ov, breit };
    });
    if (r.ov > 0 || fehler.length) { probleme++; zeile.push(`${w}:+${r.ov}px ${JSON.stringify(r.breit)} ${fehler.join('|')}`); }
    await ctx.close();
  }
  console.log(s, zeile.length ? zeile.join(' · ') : 'ok');
}
console.log('Probleme:', probleme);
await browser.close();
