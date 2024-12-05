const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  // Navigate to the Pinterest board (or your target page)
  await page.goto('https://www.pinterest.com/NoMyCheesy/f-l-o-w-e-r-s/');
  
  // Wait for the sticky bar element using XPath
  const xpath = 'html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div';
  
  // Wait for the element using XPath, page.$x returns an array of elements
  const elements = await page.waitForSelector(xpath);

  // Check if any elements were found
  if (elements.length > 0) {
      const element = elements[0]; // Get the first matched element
      await element.evaluate(el => el.remove()); // Remove it from the DOM
  } else {
      console.log("Element not found");
  }
    // Zoom out (e.g., 50% zoom)
    await page.evaluate(() => {
        document.body.style.zoom = '0.5'; // Zoom out to 50%
    });

    // Scroll to load more pins
    await autoScroll(page, 15);  // Limit to 15 scrolls

    // Wait for images and network to stabilize
    await page.waitForFunction(() => {
        return document.readyState === 'complete' && window.performance.getEntriesByType('resource').every(e => e.initiatorType !== 'img' || e.responseEnd < performance.now() - 2000);
    }, { timeout: 20000 });

    // Take a full-page screenshot
    await page.screenshot({
        path: 'yoursite.png',
        fullPage: true
    });

    await browser.close();
    console.log('Screenshot saved as yoursite.png');
})();

// Function to scroll down the page
async function autoScroll(page, maxScrolls) {
    await page.evaluate(async (maxScrolls) => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            let distance = 100;
            let scrolls = 0;  // Scrolls counter
            let timer = setInterval(() => {
                let scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;
                scrolls++;  // Increment counter

                // Stop scrolling if reached the end or the max number of scrolls
                if (totalHeight >= scrollHeight - window.innerHeight || scrolls >= maxScrolls) {
                    clearInterval(timer);
                    resolve();
                }
            }, 3500);  // Scroll every 3.5 seconds
        });
    }, maxScrolls);  // Pass maxScrolls to the function
}
