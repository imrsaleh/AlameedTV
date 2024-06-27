import requests
from aiohttp import web


def rcinemaksa():
    data = {
        'kwik_key': '58a161c838193cbd8359356414bfee42',
        'mediaUrl': 'rcinemaksa',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/rcinemaksalive/rcinemaksa.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

def rcinemaeg():
    data = {
        'kwik_key': '2bc249e03ad4301994073f4457c985ab',
        'mediaUrl': 'rcinemaeg',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/rcinemaeglive/rcinemaeg.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

def rcomedy():
    data = {
        'kwik_key': 'c4da4eb4f612750f0779b281bc8d67d4',
        'mediaUrl': 'rcomedy',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/rcomedylive/rcomedy.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

def rclassic():
    data = {
        'kwik_key': '2d1d493b5e4cd1c8bfe12416774a0c8d',
        'mediaUrl': 'rclassic',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/rclassiclive/rclassic.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

def rdrama():
    data = {
        'kwik_key': '21813f3166d2c2e20c0b243639cde4dc',
        'mediaUrl': 'rdrama',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/rdramalive/rdrama.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

def rkhalijeah():
    data = {
        'kwik_key': '5c6f48285bb30cc477408af69876cd6b',
        'mediaUrl': 'rkhalijeah',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/rkhalijeahlive/rkhalijeah.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

def rlbc():
    data = {
        'kwik_key': '11a84280d657dad046d1a37756fdcfef',
        'mediaUrl': 'rlbc',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/rlbclive/rlbc.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

def rclip():
    data = {
        'kwik_key': '31073e6759bc9bb6ec299ff1fcec93c8',
        'mediaUrl': 'rclip',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/rcliplive/rclip.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

def alressalah():
    data = {
        'kwik_key': 'e72e95dd21a18d89b696a7737efaebdb',
        'mediaUrl': 'alressalah',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/alressalahlive/alressalah.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

def alressalahintl():
    data = {
        'kwik_key': '174341234aec4deaf71292c0ef58dcab',
        'mediaUrl': 'alressalahintl',
    }

    response = requests.post('https://rotana.net/channels/generateAclToken', data=data).json()
    data = response['data']
    hls = 'https://live.kwikmotion.com/alressalahintllive/alressalahintl.smil/playlist.m3u8?hdnts=' + data
    return {"hls_url": hls}

# دوال التعامل مع الطلبات
async def handle_rcinemaksa(request):
    return web.json_response(rcinemaksa())

async def handle_rcinemaeg(request):
    return web.json_response(rcinemaeg())

async def handle_rcomedy(request):
    return web.json_response(rcomedy())

async def handle_rclassic(request):
    return web.json_response(rclassic())

async def handle_rdrama(request):
    return web.json_response(rdrama())

async def handle_rkhalijeah(request):
    return web.json_response(rkhalijeah())

async def handle_rlbc(request):
    return web.json_response(rlbc())

async def handle_rclip(request):
    return web.json_response(rclip())

async def handle_alressalah(request):
    return web.json_response(alressalah())

async def handle_alressalahintl(request):
    return web.json_response(alressalahintl())
