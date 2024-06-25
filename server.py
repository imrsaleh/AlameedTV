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

if __name__ == '__main__':
    port = int(os.getenv("PORT", default=5000))
    web.run_app(app, host='0.0.0.0', port=port)
