const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
      executablePath: '/usr/bin/google-chrome',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  // Index.html
  const page1 = await browser.newPage();
  await page1.setViewport({ width: 1920, height: 1080 });
  await page1.goto('file:///home/potato/Documents/unwanted/Optilux%20HTML/index.html');
  await page1.waitForTimeout(1000);
  await page1.screenshot({ path: '/tmp/index_top.png' });
  await page1.evaluate(() => window.scrollBy(0, 400));
  await page1.waitForTimeout(1000);
  await page1.screenshot({ path: '/tmp/index_scrolled.png' });
  
  // Master.html
  const page2 = await browser.newPage();
  await page2.setViewport({ width: 1920, height: 1080 });
  await page2.goto('file:///home/potato/Documents/unwanted/Optilux%20HTML/master.html');
  await page2.waitForTimeout(1000);
  await page2.screenshot({ path: '/tmp/master_top.png' });
  await page2.evaluate(() => window.scrollBy(0, 400));
  await page2.waitForTimeout(1000);
  await page2.screenshot({ path: '/tmp/master_scrolled.png' });

  await browser.close();
  console.log("Screenshots taken.");
})();
