// install requirments: npm install puppeteer

const puppeteer = require('puppeteer');

async function fetchAndProcessPage(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    const signatureFound = new Promise((resolve, reject) => {
        // التنصت على الطلبات واعتراض الردود
        page.on('response', async response => {
            const requestUrl = response.url();
            if (requestUrl.startsWith('https://api2.shahid.net/proxy/v2.1/playout/new/drm?')) {
                try {
                    // تجنب محاولة قراءة نص الطلبات المسبقة
                    if (response.request().method() === 'OPTIONS') {
                        return;
                    }

                    const responseHeaders = response.headers();
                    let responseBody;
                    if (responseHeaders['content-type'] && responseHeaders['content-type'].includes('application/json')) {
                        responseBody = await response.json();  // قراءة الرد ككائن JSON
                    } else {
                        // محاولة قراءة النص مباشرةً إذا كان `Content-Type` غير محدد أو غير متوقع
                        responseBody = await response.text();
                        try {
                            responseBody = JSON.parse(responseBody);  // محاولة تحويل النص إلى JSON
                        } catch (error) {
                            console.log(`Response from ${requestUrl} is not JSON, it is ${responseHeaders['content-type'] || 'undefined'}`);
                            return;
                        }
                    }

                    const signature = responseBody.signature;
                    if (signature) {
                        // طباعة signature وإيقاف السكربت
                        console.log(`${signature}`);
                        resolve();
                    }
                } catch (error) {
                    console.error(`Error reading response body from ${requestUrl}:`, error);
                    reject(error);
                }
            }
        });
    });

    await page.goto(url, { waitUntil: 'networkidle2' });

    // انتظار العثور على signature
    await signatureFound;

    // إغلاق المتصفح بعد العثور على signature
    await browser.close();
    process.exit();  // إنهاء العملية
}

// URL of the target webpage
const url = 'https://shahid.mbc.net/en/player/episodes/Jak-Al-Elm-season-1-episode-1/id-1018516';

// Fetch and process the page
fetchAndProcessPage(url);
