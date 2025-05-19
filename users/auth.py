from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from core.response import APIResponse

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return APIResponse.success(data=response.data, msg="Login successful")
        except TokenError as e:
            return APIResponse.token_expired(msg=str(e))
        except InvalidToken as e:
            return APIResponse.auth_error(msg=str(e))

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return APIResponse.success(data=response.data, msg="Token refreshed successfully")
        except TokenError as e:
            return APIResponse.token_expired(msg=str(e))
        except InvalidToken as e:
            return APIResponse.auth_error(msg=str(e)) 