import os
import aiohttp
from aiohttp import web
import time
import binascii
import hashlib
import hmac
import re
import requests
from pyscripts import live, proxy, hadeftvauth, shahiddrm
from pyscripts.aloula import handle_aloula
from pyscripts.rotana_net import (
    handle_rcinemaksa,
    handle_rcinemaeg,
    handle_rcomedy,
    handle_rclassic,
    handle_rdrama,
    handle_rkhalijeah,
    handle_rlbc,
    handle_rclip,
    handle_alressalah,
    handle_alressalahintl
)


ALLOWED_ORIGIN = "https://www.alameedtv.xyz"
ALLOWED_REFERER = "https://www.alameedtv.xyz/"

async def check_origin_middleware(app, handler):
    async def middleware_handler(request):
        origin = request.headers.get('Origin')
        referer = request.headers.get('Referer')
        
        # Allow if either Origin or Referer matches their respective allowed values
        if origin == ALLOWED_ORIGIN or referer == ALLOWED_REFERER:
            return await handler(request)
        
        # If neither matches, deny access
        return web.Response(text="Unauthorized", status=403)
    
    return middleware_handler

async def cors_middleware(app, handler):
    async def middleware_handler(request):
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGIN
        response.headers['Access-Control-Allow-Methods'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        return response
    return middleware_handler

app = web.Application(middlewares=[check_origin_middleware, cors_middleware])

app.router.add_route('*', '/live/{url:.*}', live.handle_live)
app.router.add_get('/proxy/{url:.*}', proxy.handle_proxy)
app.router.add_route('*', '/hadeftv/get/auth', hadeftvauth.hadefauth)
app.router.add_route('*', '/shahid/api/auth', shahiddrm.shahid_api_auth_handler)

#قنوات روتانا
# إضافة المسارات الجديدة
app.router.add_get('/live-hls/rcinemaksa', handle_rcinemaksa)
app.router.add_get('/live-hls/rcinemaeg', handle_rcinemaeg)
app.router.add_get('/live-hls/rcomedy', handle_rcomedy)
app.router.add_get('/live-hls/rclassic', handle_rclassic)
app.router.add_get('/live-hls/rdrama', handle_rdrama)
app.router.add_get('/live-hls/rkhalijeah', handle_rkhalijeah)
app.router.add_get('/live-hls/rlbc', handle_rlbc)
app.router.add_get('/live-hls/rclip', handle_rclip)
app.router.add_get('/live-hls/alressalah', handle_alressalah)
app.router.add_get('/live-hls/alressalahintl', handle_alressalahintl)

#قنوات الاولى 
app.router.add_get('/{path:.*}', handle_aloula)

if __name__ == '__main__':
    port = int(os.getenv("PORT", default=5000))
    web.run_app(app, host='0.0.0.0', port=port)
