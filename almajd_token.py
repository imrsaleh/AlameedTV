import requests
from flask import Flask, send_file, redirect, request, abort, jsonify

app = Flask(__name__)
PORT = 3000
ip = '0.0.0.0'

def index():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ar,en-GB;q=0.9,en;q=0.8,ar-SA;q=0.7,en-US;q=0.6',
        'authorization': 'Basic RUQzcktWWWNQelR3WklWSnpPMmo0Z1JNaEhtb0xoSWhEZXRMR1RCNUtmcWxCMlFoWnI5RlBYMXU0TVlDOkYwMGhCWGR4WVpVQnp5bDhsb2V4TkszOFBMTGEyQm44VUtJbEVkOXR5MDBlY1lPU3FVVGVOYkpqWW5OZw==',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://www.hadif.tv',
        'priority': 'u=1, i',
        'referer': 'https://www.hadif.tv/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
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

    response = requests.post('https://fapi.streann.com/web/oauth/token', params=params, headers=headers, data=data)
    return response.json()['access_token']

# الصفحة الرئيسية
@app.route('/get/access_token')
def token():
    referer_header = request.headers.get('Referer')
    if referer_header != 'https://alameedtv.blogspot.com/':
        abort(403)  # إذا لم يتطابق الهيدر، ارجع خطأ 403 Forbidden
    data = {"access_token": index()}
    return jsonify(data)

if __name__ == '__main__':
    print(f'http://127.0.0.1:3000/get/access_token')
    app.run(host=ip, port=PORT)
