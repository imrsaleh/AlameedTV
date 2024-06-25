import binascii
import hashlib
import hmac
import re
import requests
import time
from aiohttp import web

class shahid_mbc_net:
    CHUNK_JS_URL = 'https://shahid.mbc.net/streaming-pages/_next/static/chunks/{chunk}'
    
    @staticmethod
    def get_site_info():
        try:
            response = requests.get(
                shahid_mbc_net.CHUNK_JS_URL.format(chunk="remoteEntry.js")
            ).content.decode()
            response = re.search(
                r'"static/chunks/"[^({]*\({([^)}]+)}\)[^\"]*"([^\"]+)"',
                response
            )

            r1, r2 = response.group(1), response.group(2)
            r1 = r1.split(",")
            for r in r1:
                r = r.split(":")
                chunk_response = requests.get(shahid_mbc_net.CHUNK_JS_URL.format(
                    chunk=r[0] + "-" + r[1].replace('"', '') + r2
                )).content.decode()

                try:
                    site_info = {
                        "BROWSER_VERSION": re.search(r'BROWSER_VERSION="([^\"]+)"', chunk_response).group(1),
                        "SECRET_KEY": max(re.findall(r'{let t="([^\"]+)";', chunk_response), key=len)
                    }
                    return site_info
                except:
                    pass

            raise "Failed to extract site information"

        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def generate_auth(auth_params):
        site_info = shahid_mbc_net.get_site_info()
        if site_info:
            secret_key = site_info["SECRET_KEY"]
            return binascii.hexlify(hmac.new(
                secret_key.encode('utf-8'),
                ";".join(f"{k}={auth_params[k]}" for k in sorted(auth_params.keys())).encode('utf-8'),
                hashlib.sha256
            ).digest()).decode('utf-8')
        else:
            return None

async def get_response(request):
    auth_params = {
        'request': '{"assetId":999809}',
        'ts': int(time.time() * 1000),
        'country': 'ARE',
    }

    hash_value = shahid_mbc_net.generate_auth(auth_params)
    headers = {
        'authorization': hash_value,
        'browser_name': 'CHROME',
        'browser_version': '126.0.0.0',
        'origin': 'https://shahid.mbc.net',
        'os_version': 'NT 10.0',
        'referer': 'https://shahid.mbc.net/',
        'shahid_os': 'WINDOWS',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    respo = requests.get('https://api2.shahid.net/proxy/v2.1/playout/new/drm', params=auth_params, headers=headers).json()
    return web.json_response(respo)

if __name__ == "__main__":
    respo = get_response()
