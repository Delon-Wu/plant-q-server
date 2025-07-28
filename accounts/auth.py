from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.exceptions import ValidationError
from rest_framework import status
from core.response import APIResponse

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return APIResponse.success(data=response.data, msg="登录成功")
        except TokenError as e:
            return APIResponse.token_expired(msg="令牌错误")
        except InvalidToken as e:
            return APIResponse.auth_error(msg="无效令牌")
        except ValidationError as e:
            error_detail = getattr(e, 'detail', None)
            if isinstance(error_detail, dict) and 'non_field_errors' in error_detail:
                return APIResponse.auth_error(msg="邮箱或密码错误", code=401)
            return APIResponse.error(msg="登录失败", code=401)
        except Exception:
            return APIResponse.error(msg="登录失败，请稍后重试", code=500)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return APIResponse.success(data=response.data, msg="令牌刷新成功")
        except TokenError as e:
            return APIResponse.token_expired(msg="令牌已过期")
        except InvalidToken as e:
            return APIResponse.auth_error(msg="无效的刷新令牌")
        except ValidationError as e:
            return APIResponse.error(msg="刷新令牌格式错误", code=400)
        except Exception as e:
            return APIResponse.error(msg="令牌刷新失败，请重新登录", code=500) 