// Resume frame capture from a given frame index (1-based file numbering = f+1)
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const BASE = __dirname;
const FPS = 30;
const START = parseInt(process.argv[2] || '0', 10);   // first MISSING frame index (0-based t frame)

(async () => {
  const TL = JSON.parse(fs.readFileSync(path.join(BASE, 'timeline.json'), 'utf8'));
  const TOTAL = TL.total;
  const N = Math.ceil(TOTAL * FPS);
  console.log(`resuming from frame ${START} to ${N - 1}`);
  const outDir = '/tmp/aimd/frames';

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(BASE, 'renderer_final.html?render=1'));
  await page.waitForFunction('window.READY === true', { timeout: 60000 });

  const t0 = Date.now();
  for (let f = START; f < N; f++) {
    await page.evaluate(tt => window.SEEK(tt), f / FPS);
    await page.screenshot({ path: path.join(outDir, `f${String(f + 1).padStart(6, '0')}.jpg`), type: 'jpeg', quality: 90 });
    if ((f - START) % 300 === 0) {
      const el = (Date.now() - t0) / 1000;
      console.log(`frame ${f + 1}/${N}  ${(el / 60).toFixed(1)}min`);
    }
  }
  await browser.close();
  console.log(`RESUME DONE ${N - START} frames in ${((Date.now() - t0) / 60000).toFixed(1)} min`);
})();
