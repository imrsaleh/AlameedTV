const express = require('express');
const { chromium } = require('playwright');
const app = express();
const PORT = 3000;

async function fetchAndProcessPage(url) {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    const signatureFound = new Promise((resolve, reject) => {
        page.on('response', async response => {
            const requestUrl = response.url();
            if (requestUrl.startsWith('https://api2.shahid.net/proxy/v2.1/playout/new/drm?')) {
                try {
                    if (response.request().method() === 'OPTIONS') {
                        return;
                    }

                    const responseHeaders = response.headers();
                    let responseBody;
                    if (responseHeaders['content-type'] && responseHeaders['content-type'].includes('application/json')) {
                        responseBody = await response.json();
                    } else {
                        responseBody = await response.text();
                        try {
                            responseBody = JSON.parse(responseBody);
                        } catch (error) {
                            console.log(`Response from ${requestUrl} is not JSON, it is ${responseHeaders['content-type'] || 'undefined'}`);
                            return;
                        }
                    }

                    const signature = responseBody.signature;
                    if (signature) {
                        resolve(signature);
                    }
                } catch (error) {
                    console.error(`Error reading response body from ${requestUrl}:`, error);
                    reject(error);
                }
            }
        });
    });

    await page.goto(url, { waitUntil: 'networkidle' });
    const signature = await signatureFound;
    await browser.close();
    return signature;
}

app.get('/', async (req, res) => {
    try {
        const url = 'https://shahid.mbc.net/en/player/episodes/Jak-Al-Elm-season-1-episode-1/id-1018516';
        const signature = await fetchAndProcessPage(url);
        res.json({ signature });
    } catch (error) {
        console.error('Error occurred:', error);  // تسجيل تفاصيل الخطأ في السجل
        res.status(500).json({ error: 'Error occurred while fetching the page', details: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
