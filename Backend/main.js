const puppeteer = require("puppeteer");

(async () => {
  const boardUrl = process.argv[2]; // Get URL from command-line args
  if (!boardUrl) {
    console.error("No Pinterest board URL provided!");
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    headless: false,
  });
  const page = await browser.newPage();

  // Navigate to the Pinterest board
  await page.goto(boardUrl, {
    waitUntil: "domcontentloaded",
  });

  // Set initial viewport size
  await page.setViewport({
    width: 1920,
    height: 2500,
  });

  // Zoom out (e.g., 50% zoom)
  await page.evaluate(() => {
    document.body.style.zoom = "0.5"; // Zoom out to 50%
  });

  // Scroll to load more pins
  await autoScroll(page, 15); // Limit to 15 scrolls

  // Wait for images and network to stabilize
  await page.waitForFunction(
    () => {
      return (
        document.readyState === "complete" &&
        window.performance
          .getEntriesByType("resource")
          .every(
            (e) =>
              e.initiatorType !== "img" ||
              e.responseEnd < performance.now() - 2000
          )
      );
    },
    { timeout: 30000 }
  );

  // Take a full-page screenshot and get it as base64
  let screenshotBase64 = await page.screenshot({
    fullPage: true,
    encoding: "base64",
  });

  screenshotBase64 = fixBase64Padding(screenshotBase64);

  process.stdout.write(screenshotBase64);

  // Send the screenshot to the Flask backend
  const response = await fetch("http://127.0.0.1:5000/process-image", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ image: screenshotBase64 }), // Send base64 image as JSON
  });

  const result = await response.json();
  //console.log("Flask Response:", result);

  await browser.close();
  //console.log("Screenshot successfully sent to Flask backend!");
})();

// Function to fix base64 padding
function fixBase64Padding(base64String) {
  // Calculate padding
  const padding = base64String.length % 4;
  if (padding === 2) {
    return base64String + "=="; // Add two '=' characters
  } else if (padding === 3) {
    return base64String + "="; // Add one '=' character
  } else if (padding === 0) {
    return base64String; // Already properly padded
  } else {
    throw new Error("Invalid base64 string");
  }
}

// Function to scroll down the page
async function autoScroll(page, maxScrolls) {
  await page.evaluate(async (maxScrolls) => {
    await new Promise((resolve) => {
      let totalHeight = 0;
      let distance = 100;
      let scrolls = 0; // Scrolls counter
      let timer = setInterval(() => {
        let scrollHeight = document.body.scrollHeight;
        window.scrollBy(0, distance);
        totalHeight += distance;
        scrolls++; // Increment counter

        // Stop scrolling if reached the end or the max number of scrolls
        if (
          totalHeight >= scrollHeight - window.innerHeight ||
          scrolls >= maxScrolls
        ) {
          clearInterval(timer);
          resolve();
        }
      }, 3500); // Scroll every 3.5 seconds
    });
  }, maxScrolls); // Pass maxScrolls to the function
}
