import { chromium } from 'playwright-core';
const exe = process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const browser = await chromium.launch({ executablePath: exe });
const page = await (await browser.newContext({ viewport:{width:1440,height:900}, reducedMotion:'reduce' })).newPage();
const seiten = process.argv.slice(2).length ? process.argv.slice(2) : ['index','shop','shop-split','set-split-35','beratung','energetische-beratung','faq','kontakt','wartung','montage','klimaanlagen','ratgeber','ratgeber-kosten','impressum'];
const out = {};
for (const s of seiten) {
  await page.goto('http://localhost:8765/' + s + '.html', { waitUntil: 'networkidle' });
  const res = await page.evaluate(() => {
    function lum(c){ const [r,g,b]=c.map(v=>{v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4)}); return 0.2126*r+0.7152*g+0.0722*b; }
    function parse(s){ const m=s.match(/rgba?\(([^)]+)\)/); if(!m) return null; const p=m[1].split(',').map(Number); return {c:p.slice(0,3), a:p.length>3?p[3]:1}; }
    function bgOf(el){ let e=el; while(e){ const cs=getComputedStyle(e); const bg=parse(cs.backgroundColor); if(bg && bg.a>0.85) return bg.c; if(cs.backgroundImage && cs.backgroundImage!=='none' && !cs.backgroundImage.startsWith('linear-gradient')) return 'img'; if(cs.backgroundImage && cs.backgroundImage.startsWith('linear-gradient')) return 'grad'; e=e.parentElement; } return [255,255,255]; }
    const found=[]; const walker=document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n; const seen=new Set();
    while(n=walker.nextNode()){ const t=n.textContent.trim(); if(t.length<2) continue; const el=n.parentElement; if(seen.has(el)) continue; seen.add(el);
      if(el.closest('template, .overlay, [hidden], script, style')) continue;
      const cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none') continue; const r=el.getBoundingClientRect(); if(r.width===0||r.height===0) continue;
      const fg=parse(cs.color); if(!fg) continue; const bg=bgOf(el); if(typeof bg==='string') continue;
      const l1=lum(fg.c), l2=lum(bg); const ratio=(Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
      const size=parseFloat(cs.fontSize); const bold=parseInt(cs.fontWeight)>=700; const large = size>=24 || (size>=18.66 && bold);
      if(ratio < (large?3:4.5)) found.push({el: el.tagName.toLowerCase()+(el.className?'.'+String(el.className).split(' ').slice(0,2).join('.'):''), text:t.slice(0,40), ratio:+ratio.toFixed(2), fg:cs.color, bg:'rgb('+bg.join(',')+')', size}); }
    return found;
  });
  out[s]=res;
}
await browser.close();
for (const [s,r] of Object.entries(out)) { console.log('== '+s+': '+r.length); const uniq=new Map(); r.forEach(x=>{ const k=x.el+'|'+x.fg+'|'+x.bg; if(!uniq.has(k)) uniq.set(k,x); }); [...uniq.values()].forEach(x=>console.log('  ',x.ratio, x.el, x.fg, 'auf', x.bg, x.size+'px', JSON.stringify(x.text))); }
