#!/usr/bin/env node
/* Audit jbowman.com against the brand guidelines and WCAG 2.2 AA.
 *
 *   node tools/audit.js                 (expects the site served on :8140)
 *
 * Checks, in order:
 *   1. WCAG AA contrast for every text node, against its real composited
 *      background, with alpha blended properly.
 *   2. The guidelines' contrast law — no Orchid type on Bone, no Plum on Ink.
 *   3. One plum field per page.
 *   4. The Belleza/Montserrat-italic pairing used once per composition.
 *   5. No image rendered above its native resolution.
 *   6. No horizontal pan at any width.
 */
const { chromium } = require('/tmp/claude-0/-home-claude-repo/31cb2b5d-6c32-5a64-9a34-6b7af514686f/scratchpad/node_modules/playwright');

// The pre-installed browser; its path differs from what playwright expects.
const CHROME = require('fs').existsSync('/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
  ? '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'
  : '/opt/pw-browsers/chromium-1243/chrome-linux/chrome';

const BASE = 'http://127.0.0.1:8140/';
const PAGES = ['index.html', 'about.html', 'work.html', 'journal.html', 'connect.html', 'brand/index.html'];
const WIDTHS = [1600, 1280, 900, 600, 390, 320];

const INK = [11, 10, 12], BONE = [241, 236, 225], PLUM = [110, 42, 92], ORCHID = [185, 132, 176];

const AUDIT = `(() => {
  const parse = c => { const m = (c.match(/[\\d.]+/g) || []).map(Number); return { r:m[0]||0, g:m[1]||0, b:m[2]||0, a:m.length>3?m[3]:1 }; };
  const over = (f, b) => ({ r:f.a*f.r+(1-f.a)*b.r, g:f.a*f.g+(1-f.a)*b.g, b:f.a*f.b+(1-f.a)*b.b, a:1 });
  const lum = c => { const t = v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); };
    return 0.2126*t(c.r)+0.7152*t(c.g)+0.0722*t(c.b); };
  const bgOf = el => { let n = el;
    while (n) { const c = parse(getComputedStyle(n).backgroundColor);
      if (c.a > 0) return c.a === 1 ? c : over(c, bgOf(n.parentElement || document.body));
      n = n.parentElement; }
    return { r:255,g:255,b:255,a:1 }; };
  const near = (c, t) => Math.abs(c.r-t[0])<10 && Math.abs(c.g-t[1])<10 && Math.abs(c.b-t[2])<10;

  const contrast = [], law = [];
  document.querySelectorAll('p,span,a,li,h1,h2,h3,h4,label,input,select,textarea,button,em').forEach(el => {
    const txt = (el.textContent||'').trim();
    if (!txt) return;
    const cs = getComputedStyle(el);
    if (cs.display==='none' || cs.visibility==='hidden' || !el.getClientRects().length) return;
    if (el.children.length && !['LABEL','A','BUTTON','LI','EM','H1','H2','H3','H4'].includes(el.tagName)) return;
    // Decorative specimens are captioned and hidden from assistive tech;
    // low contrast is the device being shown, not a defect.
    if (el.closest('[aria-hidden="true"]')) return;
    const fg = parse(cs.color), bg = bgOf(el);
    const eff = fg.a < 1 ? over(fg, bg) : fg;
    const px = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight,10) >= 700;
    const need = (px >= 24 || (px >= 18.66 && bold)) ? 3 : 4.5;
    const L1 = lum(eff), L2 = lum(bg);
    const ratio = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    if (ratio < need) contrast.push({ tag:el.tagName.toLowerCase(), cls:String(el.className).slice(0,34), text:txt.slice(0,40), ratio:+ratio.toFixed(2), need, px:+px.toFixed(1) });

    // Guidelines contrast law
    if (near(eff, [185,132,176]) && near(bg, [241,236,225])) law.push('Orchid type on Bone: "'+txt.slice(0,34)+'"');
    if (near(eff, [110,42,92])  && near(bg, [11,10,12]))    law.push('Plum type on Ink: "'+txt.slice(0,34)+'"');
  });

  // One plum field per page. Colour specimens are documentation of the
  // palette, not compositional use of it, so they carry data-specimen and
  // are excluded — along with anything inside one.
  const plumFields = [...document.querySelectorAll('*')].filter(el => {
    if (el.closest('[data-specimen]')) return false;
    const c = parse(getComputedStyle(el).backgroundColor);
    const r = el.getBoundingClientRect();
    return near(c, [110,42,92]) && r.width * r.height > 40000;
  }).length;

  // Signature type moment: Belleza block containing a Montserrat italic
  const signature = [...document.querySelectorAll('.accent-italic')].length;

  // Images shown above native resolution
  const upscaled = [...document.images].filter(i => i.naturalWidth && i.getBoundingClientRect().width > i.naturalWidth + 1)
    .map(i => ({ src:(i.currentSrc||i.src).split('/').pop(), shown:Math.round(i.getBoundingClientRect().width), native:i.naturalWidth }));

  return { contrast, law, plumFields, signature, upscaled };
})()`;

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  let failures = 0;

  for (const page of PAGES) {
    const p = await browser.newPage({ viewport: { width: 1500, height: 950 } });
    await p.goto(BASE + page, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.evaluate(async () => { for (let y=0; y<document.body.scrollHeight; y+=700) { window.scrollTo(0,y); await new Promise(r=>setTimeout(r,40)); } window.scrollTo(0,0); });
    await p.waitForTimeout(500);

    const r = await p.evaluate(AUDIT);
    const notes = [];
    if (r.contrast.length) { failures += r.contrast.length; notes.push(`${r.contrast.length} below AA`); }
    if (r.law.length)      { failures += r.law.length;      notes.push(`${r.law.length} contrast-law breaches`); }
    if (r.plumFields > 1)  { failures++; notes.push(`${r.plumFields} plum fields (max 1)`); }
    if (r.signature > 1)   { failures++; notes.push(`${r.signature} signature type moments (max 1)`); }
    if (r.upscaled.length) { failures += r.upscaled.length; notes.push(`${r.upscaled.length} upscaled images`); }

    console.log(`\n${page.padEnd(18)} ${notes.length ? '✗ ' + notes.join(' · ') : '✓ clean'}`);
    console.log(`${''.padEnd(18)} plum fields: ${r.plumFields} · signature moments: ${r.signature}`);
    r.contrast.slice(0,6).forEach(f => console.log(`   AA  ${f.ratio}:1 (needs ${f.need}) ${f.px}px <${f.tag} class="${f.cls}"> "${f.text}"`));
    r.law.forEach(l => console.log(`   LAW ${l}`));
    r.upscaled.forEach(u => console.log(`   IMG ${u.src} shown ${u.shown}px, native ${u.native}px`));
    await p.close();
  }

  console.log('\n--- horizontal pan ---');
  for (const w of WIDTHS) {
    const p = await browser.newPage({ viewport: { width: w, height: 900 } });
    let worst = 0;
    for (const page of PAGES) {
      await p.goto(BASE + page, { waitUntil: 'domcontentloaded' });
      await p.waitForTimeout(150);
      const panned = await p.evaluate(() => { window.scrollTo(9999,0); const x = window.scrollX; window.scrollTo(0,0); return x; });
      worst = Math.max(worst, panned);
    }
    if (worst) failures++;
    console.log(`  ${String(w).padStart(5)}px  ${worst ? '✗ pans ' + worst + 'px' : '✓ no pan'}`);
    await p.close();
  }

  await browser.close();
  console.log(`\n${failures ? '✗ ' + failures + ' issue(s)' : '✓ all checks pass'}`);
  process.exit(failures ? 1 : 0);
})();
