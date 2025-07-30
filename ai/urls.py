from django.urls import path
from .views import ChatView, PlantRecognizeView

urlpatterns = [
    path('chat', ChatView.as_view()),
    path('plant-recognization', PlantRecognizeView.as_view()),
]
