const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch();
  const [,, dir, scale] = process.argv;
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg') || f.endsWith('.html'))) {
    const full = path.join(dir, f);
    let w, h;
    if (f.endsWith('.svg')) { const m = fs.readFileSync(full,'utf8').match(/viewBox="0 0 (\d+) (\d+)"/); w=+m[1]; h=+m[2]; }
    else { const m = fs.readFileSync(full,'utf8').match(/data-size="(\d+)x(\d+)"/); w=+m[1]; h=+m[2]; }
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: +(scale||1) });
    await p.goto('file://' + full);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    const out = full.replace(/\.(svg|html)$/, '.png');
    if (f.endsWith('.svg')) await p.locator('svg').first().screenshot({ path: out, omitBackground: true });
    else await p.screenshot({ path: out });
    console.log(out);
    await p.close();
  }
  await b.close();
})();
