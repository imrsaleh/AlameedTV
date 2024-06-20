"""
import aiohttp
from aiohttp import web

async def handle_proxy(request):
    target_url = request.match_info.get('url')
    if not target_url:
        return web.Response(text="No target URL provided", status=400)

    target_url = f"http://{target_url}"

    timeout = aiohttp.ClientTimeout(total=10)  # Set a total timeout of 10 seconds
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(target_url) as resp:
                body = await resp.read()
                headers = {k: v for k, v in resp.headers.items() if k.lower() not in ('content-encoding', 'transfer-encoding')}
                return web.Response(body=body, status=resp.status, headers=headers)
        except aiohttp.ClientError as e:
            return web.Response(text=f"Failed to fetch {target_url}: {str(e)}", status=500)
"""
import aiohttp
from aiohttp import web

async def handle_proxy(request):
    url = request.match_info['url']
    target_url = f'http://{url}'
    headers = {'Accept-Encoding': 'identity'}

    async with aiohttp.ClientSession() as session:
        async with session.get(target_url, headers=headers) as response:
            headers = {key: value for key, value in response.headers.items()}

            # السماح بتمرير البث بشكل مباشر بدون تحميل مسبق
            response_body = await response.read()
            # Setting a cookie to indicate that the user has been proxied
            response_obj = web.Response(body=response_body, headers=headers)
            response_obj.set_cookie('proxied', 'true')
            return response_obj
