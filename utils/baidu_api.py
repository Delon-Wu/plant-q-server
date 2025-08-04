from django.core.cache import cache
import time

BAIDU_TOKEN_CACHE_KEY = 'baidu_access_token'
BAIDU_TOKEN_EXPIRE_KEY = 'baidu_access_token_expire'

def get_baidu_access_token(api_key, secret_key):
    import requests
    token = cache.get(BAIDU_TOKEN_CACHE_KEY)
    expire = cache.get(BAIDU_TOKEN_EXPIRE_KEY)
    now = int(time.time())
    if token and expire and now < expire:
        return token
    url = f'https://aip.baidubce.com/oauth/2.0/token'
    params = {
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': secret_key
    }
    resp = requests.post(url, params=params)
    data = resp.json()
    token = data.get('access_token')
    expires_in = data.get('expires_in', 0)
    if not token:
        raise Exception('获取百度access_token失败')
    expire = now + int(expires_in) - 60  # 提前1分钟过期
    cache.set(BAIDU_TOKEN_CACHE_KEY, token, timeout=expires_in-60)
    cache.set(BAIDU_TOKEN_EXPIRE_KEY, expire, timeout=expires_in-60)
    return token

def validate_image_file(file):
    allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp']
    max_size = 4 * 1024 * 1024  # 4MB
    if file.content_type not in allowed_types:
        return False, '仅支持png、jpg、jpeg、bmp格式图片'
    if file.size > max_size:
        return False, '图片大小不能超过4MB'
    return True, ''
