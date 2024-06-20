import aiohttp
from aiohttp import web

async def handle_live(request):
    url = request.match_info['url']
    target_url = f'https://{url}'
    headers = {'Accept-Encoding': 'identity'}

    async with aiohttp.ClientSession() as session:
        async with session.get(target_url, headers=headers) as response:
            headers = {key: value for key, value in response.headers.items()}

            # السماح بتمرير البث بشكل مباشر بدون تحميل مسبق
            response_body = await response.read()
            return web.Response(body=response_body, headers=headers)

