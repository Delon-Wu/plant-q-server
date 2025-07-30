import os
import requests
from celery import shared_task
import base64

def get_baidu_access_token():
    baidu_api_key = os.environ.get('BAIDU_API_KEY')
    baidu_secret_key = os.environ.get('BAIDU_SECRET_KEY')
    token_url = 'https://aip.baidubce.com/oauth/2.0/token'
    token_params = {
        'grant_type': 'client_credentials',
        'client_id': baidu_api_key,
        'client_secret': baidu_secret_key
    }
    token_resp = requests.post(token_url, data=token_params)
    token_data = token_resp.json()
    return token_data.get('access_token'), token_data

@shared_task
def baidu_plant_recognize_task(image_bytes):
    access_token, token_data = get_baidu_access_token()
    if not access_token:
        return {'error': 'Failed to get access_token', 'detail': token_data}
    img_base64 = base64.b64encode(image_bytes).decode()
    plant_url = f'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token={access_token}'
    plant_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    plant_data = {'image': img_base64}
    plant_resp = requests.post(plant_url, data=plant_data, headers=plant_headers)
    return plant_resp.json()
