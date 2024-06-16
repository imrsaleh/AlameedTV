from quart import Quart, jsonify
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio

app = Quart(__name__)
HOST = '0.0.0.0'
PORT = 3000

async def fetch_and_process_page(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            page = await browser.new_page()
            signature_event = asyncio.Event()

            signature = None

            async def handle_response(response):
                nonlocal signature
                request_url = response.url
                if request_url.startswith('https://api2.shahid.net/proxy/v2.1/playout/new/drm?'):
                    try:
                        if response.request.method == 'OPTIONS':
                            return

                        response_headers = response.headers
                        if 'application/json' in response_headers.get('content-type', ''):
                            response_body = await response.json()
                        else:
                            response_body = await response.text()
                            try:
                                response_body = response.json()
                            except Exception as e:
                                print(f"Response from {request_url} is not JSON, it is {response_headers.get('content-type', 'undefined')}")
                                return

                        signature = response_body.get('signature')
                        if signature:
                         #   print(f"Signature found: {signature}")
                            signature_event.set()
                    except Exception as e:
                        print(f"Error reading response body from {request_url}: {e}")

            page.on('response', handle_response)
            await page.goto(url, wait_until='networkidle')

            try:
                await asyncio.wait_for(signature_event.wait(), timeout=30)
            except asyncio.TimeoutError:
                print("Timeout while waiting for the response")

            if signature is None:
                print("Signature not found in any response")
            return signature
        except PlaywrightTimeoutError as e:
            print(f"Playwright timeout error: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while processing the page: {e}")
            return None
        finally:
            await browser.close()

@app.route('/')
async def index():
    try:
        url = 'https://shahid.mbc.net/en/player/episodes/Crown-Prince-Mohammed-Bin-Salman-Special-Interview-season-1-episode-1/id-999809'
        signature = await fetch_and_process_page(url)
        if signature:
            return jsonify({'signature': signature})
        else:
            return jsonify({'error': 'Signature not found'}), 404
    except Exception as e:
        print(f"An error occurred in the index route: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
