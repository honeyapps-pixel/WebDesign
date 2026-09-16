import { chromium } from 'playwright-core';
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
const out = [];
// 1 Hero-Marker: Hover setzt Zone sichtbar
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } }); const page = await ctx.newPage();
  await page.goto('http://localhost:8793/index.html', { waitUntil: 'networkidle' }); await page.waitForTimeout(1500);
  const vor = await page.evaluate(() => getComputedStyle(document.querySelector('[data-schnitt] use')).getPropertyValue('--z05'));
  await page.hover('.mk-05 .mk__k'); await page.waitForTimeout(350);
  const nach = await page.evaluate(() => ({ z: getComputedStyle(document.querySelector('[data-schnitt] use')).getPropertyValue('--z05').trim(), active: document.querySelector('[data-schnitt]').getAttribute('data-active'), label: getComputedStyle(document.querySelector('.mk-05 .mk__l')).opacity }));
  out.push(['Hover Marker 05 → --z05', vor.trim() || '(leer)', '→', JSON.stringify(nach)]);
  // Tastatur: Tab zu Marker
  await page.mouse.move(5, 5); await page.waitForTimeout(300);
  await page.focus('.mk-03'); await page.waitForTimeout(300);
  out.push(['Fokus Marker 03 → data-active', await page.evaluate(() => document.querySelector('[data-schnitt]').getAttribute('data-active'))]);
  // Legende-Hover
  await page.hover('.legende__liste li:nth-child(7) a'); await page.waitForTimeout(300);
  out.push(['Legende 07 hover → data-active', await page.evaluate(() => document.querySelector('[data-schnitt]').getAttribute('data-active'))]);
  // Klick auf Marker springt zum Kapitel
  await page.click('.mk-04 .mk__k'); await page.waitForTimeout(600);
  out.push(['Klick Marker 04 → hash/scroll', await page.evaluate(() => location.hash + ' scrollY=' + Math.round(scrollY) + ' kapTop=' + Math.round(document.querySelector('#stelle-04').getBoundingClientRect().top))]);
  // FAB-Rücktritt: bis zum Formular scrollen
  await page.evaluate(() => document.querySelector('#kontakt .form').scrollIntoView()); await page.waitForTimeout(700);
  out.push(['FAB is-gedeckt am Formular (1440)', await page.evaluate(() => document.querySelector('.wa-fab').classList.contains('is-gedeckt'))]);
  // Reveals sichtbar nach Scroll?
  const unsichtbar = await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } await new Promise(r => setTimeout(r, 900)); return [...document.querySelectorAll('[data-reveal]')].filter(e => parseFloat(getComputedStyle(e).opacity) < .95).length; });
  out.push(['Reveal-Elemente noch unsichtbar nach Scroll', unsichtbar]);
  // Fremd-Origins / Cookies / Storage
  const hosts = new Set(); page.on('request', r => hosts.add(new URL(r.url()).host));
  await page.goto('http://localhost:8793/kontakt.html?stelle=05', { waitUntil: 'networkidle' });
  out.push(['?stelle=05 → Checkbox 05 vorgewählt', await page.evaluate(() => document.querySelector('input[name=stelle][value^="05 "]').checked)]);
  out.push(['Fremd-Hosts', [...hosts].join(',')]);
  out.push(['Cookies / localStorage / sessionStorage', (await ctx.cookies()).length, await page.evaluate(() => localStorage.length + '/' + sessionStorage.length)]);
  // Formular: Pflichtfeld-Meldung
  await page.click('.form button[type=submit]'); await page.waitForTimeout(200);
  out.push(['Submit ohne Pflichtfelder → Meldung', await page.evaluate(() => { const m = document.querySelector('[data-form-meldung]'); return !m.hidden && m.textContent.slice(0, 40); })]);
  await ctx.close();
}
// 2 Mobil: viewBox-Zuschnitt + Marker-Trefferfläche + FAB
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); const page = await ctx.newPage();
  await page.goto('http://localhost:8793/index.html', { waitUntil: 'networkidle' }); await page.waitForTimeout(1500);
  out.push(['Mobil viewBox', await page.evaluate(() => document.querySelector('[data-schnitt]').getAttribute('viewBox'))]);
  out.push(['Mobil Marker-Trefferfläche (px)', await page.evaluate(() => { const b = document.querySelector('.mk-05 .mk__hit').getBoundingClientRect(); return Math.round(b.width) + '×' + Math.round(b.height); })]);
  out.push(['Mobil Marker-Kreis (px)', await page.evaluate(() => { const b = document.querySelector('.mk-05 .mk__k').getBoundingClientRect(); return Math.round(b.width); })]);
  await page.evaluate(() => document.querySelector('#kontakt .form').scrollIntoView()); await page.waitForTimeout(700);
  out.push(['FAB is-gedeckt am Formular (390)', await page.evaluate(() => document.querySelector('.wa-fab').classList.contains('is-gedeckt'))]);
  await ctx.close();
}
// 3 Reduced Motion: alles sichtbar, keine Pre-Hide
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }); const page = await ctx.newPage();
  await page.goto('http://localhost:8793/index.html', { waitUntil: 'networkidle' }); await page.waitForTimeout(600);
  out.push(['Reduced-Motion: unsichtbare Reveals ohne Scroll', await page.evaluate(() => [...document.querySelectorAll('[data-reveal]')].filter(e => parseFloat(getComputedStyle(e).opacity) < .95).length)]);
  out.push(['Reduced-Motion: Schnitt-Linie sichtbar (dashoffset)', await page.evaluate(() => getComputedStyle(document.querySelector('.sd__linie')).strokeDashoffset)]);
  await ctx.close();
}
out.forEach(z => console.log(...z));
await browser.close();
