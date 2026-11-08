// Frame-by-frame deterministic capture: renderer_final.html -> JPEG frames
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const BASE = __dirname;
const FPS = 30;
const QUALITY = 90;

(async () => {
  const TL = JSON.parse(fs.readFileSync(path.join(BASE, 'timeline.json'), 'utf8'));
  TL.fps = FPS;
  fs.writeFileSync(path.join(BASE, 'timeline.json'), JSON.stringify(TL));
  const TOTAL = TL.total;
  const N = Math.ceil(TOTAL * FPS);
  console.log(`total ${TOTAL}s, ${N} frames @ ${FPS}fps`);

  const outDir = '/tmp/aimd/frames';
  fs.rmSync(outDir, { recursive: true, force: true });
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(BASE, 'renderer_final.html?render=1'));
  await page.waitForFunction('window.READY === true', { timeout: 60000 });
  console.log('renderer ready');

  const t0 = Date.now();
  for (let f = 0; f < N; f++) {
    const t = f / FPS;
    await page.evaluate(tt => window.SEEK(tt), t);
    await page.screenshot({ path: path.join(outDir, `f${String(f + 1).padStart(6, '0')}.jpg`), type: 'jpeg', quality: QUALITY });
    if (f % 500 === 0) {
      const el = (Date.now() - t0) / 1000;
      const rate = (f + 1) / el;
      console.log(`frame ${f + 1}/${N}  ${(el / 60).toFixed(1)}min  ${rate.toFixed(1)} f/s  eta ${(((N - f) / rate) / 60).toFixed(1)}min`, flush = true);
    }
  }
  await browser.close();
  const el = (Date.now() - t0) / 1000;
  console.log(`CAPTURE DONE ${N} frames in ${(el / 60).toFixed(1)} min`);
})();
