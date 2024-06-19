import aiohttp
from aiohttp import web

async def hadefauth(request):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ar,en-GB;q=0.9,en;q=0.8,ar-SA;q=0.7,en-US;q=0.6',
        'authorization': 'Basic RUQzcktWWWNQelR3WklWSnpPMmo0Z1JNaEhtb0xoSWhEZXRMR1RCNUtmcWxCMlFoWnI5RlBYMXU0TVlDOkYwMGhCWGR4WVpVQnp5bDhsb2V4TkszOFBMTGEyQm44VUtJbEVkOXR5MDBlY1lPU3FVVGVOYkpqWW5OZw==',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://www.hadif.tv',
        'priority': 'u=1, i',
        'referer': 'https://www.hadif.tv/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-app-name': 'almajdtv',
        'x-app-platform': 'web',
        'x-app-version': '0.0.0',
        'x-os-version': 'Chrome 126',
    }

    params = {
        'r': '5ddd27762cdc534feb8b4c44',
    }

    data = {
        'grant_type': 'password',
        'username': '117021536425650295505',
        'password': 'p117021536425650295505',
        'scope': 'services',
        'client_id': 'ED3rKVYcPzTwZIVJzO2j4gRMhHmoLhIhDetLGTB5KfqlB2QhZr9FPX1u4MYC',
        'reseller_id': '5ddd27762cdc534feb8b4c44',
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post('https://fapi.streann.com/web/oauth/token', params=params, headers=headers, data=data) as resp:
                response_json = await resp.json()
                return web.json_response({'access_token': response_json['access_token']})
        except aiohttp.ClientError as e:
            return web.Response(text=f"Failed to fetch {target_url}: {str(e)}", status=500)
