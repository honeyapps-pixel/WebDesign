import { chromium } from 'playwright-core';
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
for (const w of [1440, 834]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1.5 }); const page = await ctx.newPage();
  await page.goto('http://localhost:8793/index.html', { waitUntil: 'networkidle' }); await page.waitForTimeout(1600);
  await page.addStyleTag({ content: '.wa-fab{display:none!important}' });
  for (const nr of ['01', '04', '05', '07']) {
    await page.hover(`.mk-${nr} .mk__k`); await page.waitForTimeout(350);
    const el = await page.$('.schnitt__svg--hero');
    await el.screenshot({ path: `shots-bwa/_hover-${w}-${nr}.png` });
  }
  await ctx.close();
}
await browser.close();
