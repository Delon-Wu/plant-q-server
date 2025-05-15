from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.response import APIResponse

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return APIResponse.success(data=response.data, msg="Login successful")

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return APIResponse.success(data=response.data, msg="Token refreshed successfully") 