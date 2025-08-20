from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from core.response import APIResponse
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
# 注册邮箱验证码发送接口
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.data.get("old_password")):
            return APIResponse.error(msg="Wrong password.", code=400, data={"old_password": ["Wrong password."]})

        user.set_password(serializer.data.get("new_password"))
        user.save()
        return APIResponse.success(msg="Password updated successfully")


@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return JsonResponse({'message': '邮箱不能为空'}, status=400)
        code = str(random.randint(100000, 999999))
        subject = '【Plant Q】您的验证码'
        message = f'您的验证码是：{code}，5分钟内有效。如非本人操作，请忽略此邮件。'
        html_message = f'''<div style="font-family:微软雅黑,Arial,sans-serif;padding:24px;background:#f8f8f8;">
            <div style="max-width:480px;margin:auto;background:#fff;border-radius:8px;padding:32px 24px;box-shadow:0 2px 8px #eee;">
                <h2 style="color:#4caf50;">Plant Q 验证码</h2>
                <p style="font-size:18px;color:#333;">您的验证码是：</p>
                <div style="font-size:32px;font-weight:bold;color:#2196f3;letter-spacing:4px;margin:16px 0;">{code}</div>
                <p style="color:#888;font-size:14px;">5分钟内有效。如非本人操作，请忽略此邮件。</p>
            </div>
        </div>'''
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message)
        except Exception as e:
            return JsonResponse({'message': '邮件发送失败', 'detail': str(e)}, status=500)
        # 使用 Django cache 保存验证码，5分钟过期
        cache_key = f'verification_code_{email}'
        cache.set(cache_key, code, timeout=300)  # 300秒 = 5分钟
        return JsonResponse({'message': '验证码已发送', 'code': 200})
@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')
        if not email or not code:
            return JsonResponse({'message': '邮箱和验证码不能为空'}, status=400)
        
        # 从 cache 获取验证码
        cache_key = f'verification_code_{email}'
        cached_code = cache.get(cache_key)
        
        if not cached_code:
            return JsonResponse({'message': '未发送验证码或验证码已过期'}, status=400)
        
        if code != cached_code:
            return JsonResponse({'message': '验证码错误'}, status=400)
        
        # 验证通过后删除验证码
        cache.delete(cache_key)
        return JsonResponse({'message': '验证通过', 'code': 200})
    return JsonResponse({'message': '仅支持POST请求'}, status=405)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return APIResponse.success(msg="Logout successful", status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(f"Logout error: {e}")
            return APIResponse.error(msg="Logout failed", code=400, status=status.HTTP_400_BAD_REQUEST)
