import os
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.response import APIResponse
import base64
import requests
from utils.baidu_api import get_baidu_access_token, validate_image_file

# 1. 转发 openAI api 流式传输的数据
class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return JsonResponse({"message": "This endpoint is not implemented yet."}, status=501)


# 2. 植物识别接口
class PlantRecognizeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            baidu_api_key = os.environ.get('BAIDU_API_KEY')
            baidu_secret_key = os.environ.get('BAIDU_SECRET_KEY')
            if not baidu_api_key or not baidu_secret_key:
                return JsonResponse({'error': '未配置百度API密钥'}, status=500)

            img_b64 = None
            # 1. 支持文件上传
            file = request.FILES.get('image')
            if file:
                valid, msg = validate_image_file(file)
                if not valid:
                    return JsonResponse({'error': msg}, status=400)
                img_bytes = file.read()
                img_b64 = base64.b64encode(img_bytes).decode()
            else:
                # 2. 支持前端直接传base64字符串
                img_b64 = request.POST.get('image') or request.data.get('image') if hasattr(request, 'data') else None
                if not img_b64:
                    return JsonResponse({'error': '请上传图片文件或base64字符串，字段名为image'}, status=400)
                # 校验base64格式
                try:
                    base64.b64decode(img_b64)
                except Exception:
                    return JsonResponse({'error': '图片base64字符串格式错误'}, status=400)

            try:
                access_token = get_baidu_access_token(baidu_api_key, baidu_secret_key)
            except Exception as e:
                return JsonResponse({'error': f'获取access_token失败: {str(e)}'}, status=500)

            url = f'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token={access_token}'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'image': img_b64}

            try:
                resp = requests.post(url, data=data, headers=headers, timeout=30)
                resp.raise_for_status()
                result = resp.json()
            except requests.RequestException as e:
                return JsonResponse({'error': f'百度接口请求失败: {str(e)}'}, status=500)
            except ValueError as e:
                return JsonResponse({'error': '百度接口返回数据格式错误'}, status=500)

            if 'error_code' in result:
                return JsonResponse({'error': result.get('error_msg', '识别失败')}, status=500)

            res_list = result.get('result', [])
            if not res_list:
                return JsonResponse({'result': '抱歉，未能识别出植物信息'}, status=200)

            # 组装自然语言
            descs = []
            for idx, item in enumerate(res_list[:3]):  # 限制最多显示3个结果
                name = item.get('name', '未知')
                score = item.get('score', 0)
                baike = item.get('baike_info', {})
                desc = baike.get('description', '')
                if idx == 0:
                    descs.append(f"识别结果：**{name}**（置信度{score*100:.1f}%）。{desc}")
                else:
                    descs.append(f"其他可能：{name}（置信度{score*100:.1f}%）。{desc}")

            text = '\n\n'.join(descs)  # 使用双换行分隔
            most_likely_kind = res_list[0].get('name', None)
            return JsonResponse({'result': text, 'most_likely_kind': most_likely_kind}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'服务异常: {str(e)}'}, status=500)
        
