# streams.py
import aiohttp
from aiohttp import web

async def handle_aloula(request):
    path = request.match_info.get('path')

    url_map = {
        'ikhbariya.m3u8': 'https://aloula.faulio.com/api/v1/channels/4',
        'ksa_sport1.m3u8': 'https://aloula.faulio.com/api/v1/channels/9',
        'ksa_sport2.m3u8': 'https://aloula.faulio.com/api/v1/channels/10',
        'ksa_sport3.m3u8': 'https://aloula.faulio.com/api/v1/channels/16',
        'ksa_one.m3u8': 'https://aloula.faulio.com/api/v1/channels/2',
        'ksa_now.m3u8': 'https://aloula.faulio.com/api/v1/channels/17',
        'ksa_quran.m3u8': 'https://aloula.faulio.com/api/v1/channels/7',
        'ksa_sunnah.m3u8': 'https://aloula.faulio.com/api/v1/channels/6',
        'zikryat.m3u8': 'https://aloula.faulio.com/api/v1/channels/3',
    }

    if path in url_map:
        return await fetch_stream(url_map[path])
    else:
        return web.Response(text="Not Found", status=404)

async def fetch_stream(api_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}) as resp:
            data = await resp.json()
            redirect_url = data['streams']['hls']
            return web.Response(status=301, headers={'Location': redirect_url})
