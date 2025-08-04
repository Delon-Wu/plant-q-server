from django.urls import path
from .views import PlantListCreateView, PlantDetailView, PlantImageAddView

urlpatterns = [
    path('plants/', PlantListCreateView.as_view()),
    path('plants/<int:pk>/', PlantDetailView.as_view()),
    path('plants/<int:plant_id>/add_image/', PlantImageAddView.as_view()),
]
