import os
import aiohttp
from aiohttp import web

from pyscripts import live, proxy, hadeftvauth

ALLOWED_URL = "https://alameedtv.blogspot.com"

async def check_origin_middleware(app, handler):
    async def middleware_handler(request):
        origin = request.headers.get('Origin')
        referer = request.headers.get('Referer')
        
        # Allow if either Origin or Referer matches ALLOWED_URL
        if origin == ALLOWED_URL or referer == ALLOWED_URL:
            return await handler(request)
        
        # If neither matches, deny access
        return web.Response(text="Unauthorized", status=403)
    
    return middleware_handler

async def cors_middleware(app, handler):
    async def middleware_handler(request):
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = ALLOWED_URL
        response.headers['Access-Control-Allow-Methods'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        return response
    return middleware_handler

app = web.Application(middlewares=[check_origin_middleware, cors_middleware])

app.router.add_route('*', '/live/{url:.*}', live.handle_live)
app.router.add_get('/proxy/{url:.*}', proxy.handle_proxy)
app.router.add_route('*', '/hadeftv/get/auth', hadeftvauth.hadefauth)

if __name__ == '__main__':
    port = int(os.getenv("PORT", default=5000))
    web.run_app(app, host='0.0.0.0', port=port)
