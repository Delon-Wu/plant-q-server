import os
import httpx
from django.http import StreamingHttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.response import APIResponse
import imghdr
import base64
from django.core.cache import cache
from asgiref.sync import sync_to_async

# 1. 转发 openAI api 流式传输的数据
class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            deepseek_url = os.environ.get('DEEPSEEK_API_URL')
            deepseek_api_key = os.environ.get('DEEPSEEK_API_KEY')
            if not deepseek_url or not deepseek_api_key:
                return JsonResponse({'error': '内部错误，请稍后再试'}, status=500)
            headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}
            headers['Authorization'] = f'Bearer {deepseek_api_key}'
            import requests
            resp = requests.post(deepseek_url, data=request.body, headers=headers, stream=True)
            return StreamingHttpResponse(resp.iter_content(chunk_size=8192), status=resp.status_code, content_type=resp.headers.get('content-type'))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# 2. 植物识别接口
class PlantRecognizeView(APIView):
    permission_classes = [IsAuthenticated]
    async def post(self, request):
        baidu_api_key = os.environ.get('BAIDU_API_KEY')
        baidu_secret_key = os.environ.get('BAIDU_SECRET_KEY')
        if not baidu_api_key or not baidu_secret_key:
            return JsonResponse({'error': '内部错误，请稍后再试'}, status=500)
        # 优先从缓存获取access_token
        access_token = cache.get('baidu_access_token')
        if not access_token:
            token_url = f'https://aip.baidubce.com/oauth/2.0/token'
            token_params = {
                'grant_type': 'client_credentials',
                'client_id': baidu_api_key,
                'client_secret': baidu_secret_key
            }
            async with httpx.AsyncClient() as client:
                token_resp = await client.post(token_url, data=token_params)
                token_data = token_resp.json()
            access_token = token_data.get('access_token')
            expires_in = token_data.get('expires_in')
            if not access_token:
                return JsonResponse({'error': 'Failed to get access_token', 'detail': token_data}, status=500)
            cache.set('baidu_access_token', access_token, timeout=max(10*24*60*60, expires_in - 2*24*60*60))
        img = request.FILES.get('image')
        if not img:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        img_format = imghdr.what(img)
        # 检查图片格式
        if img_format not in ['png', 'jpg', 'jpeg', 'bmp']:
            return JsonResponse({'error': '仅支持png/jpg/jepg/bmp格式'}, status=400)
        img_bytes = img.read()
        img_base64 = base64.b64encode(img_bytes).decode()
        # 检查图片大小
        if len(img_base64.encode('utf-8')) > 4 * 1024 * 1024:
            return JsonResponse({'error': '图片base64编码后大小不能超过4M'}, status=400)
        plant_url = f'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token={access_token}'
        plant_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        plant_data = {'image': img_base64}
        async with httpx.AsyncClient() as client:
            plant_resp = await client.post(plant_url, data=plant_data, headers=plant_headers)
            return JsonResponse(plant_resp.json())
