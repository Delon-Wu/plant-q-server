from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserDetailView, ChangePasswordView, LogoutView
from .auth import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', UserDetailView.as_view(), name='profile'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
] 