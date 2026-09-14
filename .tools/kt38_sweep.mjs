// kt38_sweep.mjs — Breakpoint-Sweep: jede Seite auf 11 Breiten von 320 bis 1920 px.
// Faengt Fehler, die ein 3-Breiten-Test uebersieht (z. B. Kopf-Umbruch exakt am Breakpoint).
// Aufruf: node .tools/kt38_sweep.mjs
import { chromium } from 'playwright-core';
import { readdirSync } from 'fs';
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const root = '/Users/nemo/Desktop/Projekte/Webdesgin/klimatech38/';
const seiten = readdirSync(root).filter(f => f.endsWith('.html'));
const b = await chromium.launch({ executablePath: exe });
const befunde = [];
for (const w of [320, 360, 480, 600, 768, 900, 1024, 1080, 1200, 1440, 1920]) {
  const c = await b.newContext({ viewport: { width: w, height: 800 } });
  const p = await c.newPage();
  p.on('pageerror', e => befunde.push(`${w}px pageerror: ${e.message}`));
  for (const s of seiten) {
    await p.goto('http://localhost:8765/' + s, { waitUntil: 'load' });
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    if (sw > w + 1) befunde.push(`${w}px ${s}: Overflow ${sw}`);
  }
  await c.close();
}
await b.close();
console.log(befunde.length ? 'BEFUNDE:\n' + befunde.join('\n') : `Sweep ok: ${seiten.length} Seiten × 11 Breiten (320–1920), kein Overflow, keine JS-Fehler`);
