import { chromium } from 'playwright-core';
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
const ctx = await browser.newContext({ viewport:{width:1440,height:900} });
const page = await ctx.newPage();
const log = [];
page.on('pageerror', e => log.push('pageerror: ' + e.message));
page.on('console', m => { if (m.type()==='error') log.push('console: ' + m.text()); });
const B = 'http://localhost:8765/';
await page.goto(B + 'index.html', { waitUntil: 'networkidle' });
// 1 Overlay
await page.click('[data-overlay-toggle]');
await page.waitForTimeout(700);
log.push('overlay open: ' + await page.evaluate(() => document.querySelector('[data-overlay]').classList.contains('is-open') + ' inert=' + document.querySelector('main').hasAttribute('inert')));
await page.screenshot({ path: '/private/tmp/claude-501/-Users-nemo-Desktop-Projekte-Webdesgin/07bcb8c9-80ff-4604-b38e-f58972f4e288/scratchpad/overlay.jpg', type:'jpeg', quality:60 });
await page.keyboard.press('Escape');
await page.waitForTimeout(400);
log.push('overlay closed: ' + await page.evaluate(() => !document.querySelector('[data-overlay]').classList.contains('is-open') + ' focus=' + document.activeElement.className));
// 2 Wege-Schalter
const preisVor = await page.textContent('.hero__anker .preis__w--montage b');
await page.click('.hero .weg [data-weg="selbst"]');
await page.waitForTimeout(200);
log.push('weg=' + await page.evaluate(() => document.documentElement.getAttribute('data-weg') + ' stored=' + sessionStorage.getItem('kt38-weg')));
log.push('hero preis sichtbar: ' + await page.evaluate(() => getComputedStyle(document.querySelector('.hero__anker .preis__w--selbst')).display + '/' + getComputedStyle(document.querySelector('.hero__anker .preis__w--montage')).display));
log.push('bestseller preis: ' + await page.evaluate(() => document.querySelector('#einstieg .pk .preis__w--selbst b').textContent));
// 3 Bento → Rechner
await page.click('[data-raum="dachgeschoss"]');
await page.waitForTimeout(600);
log.push('rechner sit=' + await page.evaluate(() => document.querySelector('#raeume .r-sit').value + ' flaeche=' + document.querySelector('#raeume .r-flaeche').value + ' kw=' + document.getElementById('erg-kw').textContent + ' treffer=' + (document.querySelector('#treffer h4')||{}).textContent + ' trefferKarte=' + document.querySelector('#treffer-karte .pk h3').textContent));
// Raum hinzufügen → multi
await page.click('#raum-hinzu'); await page.waitForTimeout(300);
log.push('2 räume: kw=' + await page.evaluate(() => document.getElementById('erg-kw').textContent + ' treffer=' + (document.querySelector('#treffer h4')||{}).textContent));
// über 6 kW
await page.evaluate(() => { document.querySelectorAll('#raeume .r-flaeche').forEach(i => { i.value = 80; i.dispatchEvent(new Event('input', {bubbles:true})); }); });
await page.waitForTimeout(300);
log.push('grenze: kw=' + await page.evaluate(() => document.getElementById('erg-kw').textContent + ' grenze=' + document.querySelector('#treffer').classList.contains('treffer--grenze')));
// 4 Set anfragen → Kontakt
await page.goto(B + 'set-split-35.html', { waitUntil: 'networkidle' });
log.push('set-seite weg persist=' + await page.evaluate(() => document.documentElement.getAttribute('data-weg')));
await page.evaluate(() => window.scrollTo(0, 900)); await page.waitForTimeout(600);
log.push('unterleiste da=' + await page.evaluate(() => document.querySelector('[data-unterleiste]').classList.contains('is-da')));
await page.click('.produkt-kopf [data-set-anfragen]');
await page.waitForLoadState('networkidle');
log.push('kontakt: url=' + page.url().split('/').pop() + ' thema=' + await page.evaluate(() => document.getElementById('f-thema').value + ' bezug=' + document.getElementById('bezug-text').textContent + ' text=' + document.getElementById('f-text').value.slice(0,60).replace(/\n/g,' | ')));
// 5 Filter
await page.goto(B + 'shop-split.html#flaeche=32', { waitUntil: 'networkidle' });
log.push('filter: ' + await page.evaluate(() => document.getElementById('filter-stand').textContent + ' sichtbar=' + [...document.querySelectorAll('#set-liste [data-set]')].filter(k => !k.hidden).map(k => k.dataset.set).join(',')));
// 6 FAQ
await page.goto(B + 'faq.html', { waitUntil: 'networkidle' });
await page.click('#themen [data-thema="kosten"]');
log.push('faq kosten: ' + await page.evaluate(() => [...document.querySelectorAll('[data-thema-block]')].filter(b => !b.hidden).map(b => b.dataset.themaBlock).join(',')));
// 7 mobile overlay
const m = await browser.newContext({ viewport:{width:390,height:844} }); const mp = await m.newPage();
await mp.goto(B + 'index.html', { waitUntil: 'networkidle' });
await mp.click('[data-overlay-toggle]'); await mp.waitForTimeout(700);
await mp.screenshot({ path: '/private/tmp/claude-501/-Users-nemo-Desktop-Projekte-Webdesgin/07bcb8c9-80ff-4604-b38e-f58972f4e288/scratchpad/overlay-m.jpg', type:'jpeg', quality:60, fullPage:false });
log.push('mobil overlay scrollbar: ' + await mp.evaluate(() => document.querySelector('[data-overlay]').scrollHeight + ' / ' + innerHeight));
await browser.close();
console.log(log.join('\n'));
