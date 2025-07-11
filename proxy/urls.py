from django.urls import path
from .views import ProxyView

urlpatterns = [
    path('proxy/', ProxyView.as_view(), name='proxy'),
]
