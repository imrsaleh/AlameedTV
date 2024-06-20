import os
import aiohttp
from aiohttp import web

from pyscripts.hadeftvauth import hadefauth
from pyscripts.live import handle_live
from pyscripts.proxy import handle_proxy

ALLOWED_ORIGIN = "https://alameedtv.blogspot.com"
ALLOWED_REFERER = "https://alameedtv.blogspot.com/"

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

async def conditional_proxy_handler(request):
    url = request.match_info['url']
    if request.cookies.get('proxied'):
        # User has been proxied before, redirect to original URL
        target_url = f'https://{url}'
        headers = {'Accept-Encoding': 'identity'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(target_url, headers=headers) as response:
                headers = {key: value for key, value in response.headers.items()}
                response_body = await response.read()
                return web.Response(body=response_body, headers=headers)
    else:
        # User has not been proxied before, use proxy handler
        return await handle_proxy(request)

app = web.Application(middlewares=[check_origin_middleware, cors_middleware])

app.router.add_route('*', '/live/{url:.*}', conditional_proxy_handler)
app.router.add_get('/proxy/{url:.*}', handle_proxy)
app.router.add_route('*', '/hadeftv/get/auth', hadefauth)

if __name__ == '__main__':
    port = int(os.getenv("PORT", default=5000))
    web.run_app(app, host='0.0.0.0', port=port)
