import aiohttp
from aiohttp import web

async def handle_live(request):
    url = request.match_info['url']
    target_url = f'https://{url}'
    headers = {'Accept-Encoding': 'identity'}

    async with aiohttp.ClientSession() as session:
        async with session.head(target_url, headers=headers) as response:
            if response.status != 200:
                return web.Response(status=response.status)

            original_url = response.url # هذا السطر يحفظ عنوان الرابط الذي ادخله المستخدم
            redirect_url = f'https://{url}'

            return web.HTTPFound(location=redirect_url)

