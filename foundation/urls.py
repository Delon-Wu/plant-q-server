from django.urls import path
from .views import ChatView, PlantRecognizeView
from .track import TrackEventView

urlpatterns = [
    path('chat', ChatView.as_view()),
    path('plant-recognization', PlantRecognizeView.as_view()),
    path('track', TrackEventView.as_view()),
]
