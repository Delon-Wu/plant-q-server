from django.urls import path
from .views import PlantListCreateView, PlantDetailView, GrowthRecordAddView

urlpatterns = [
    path('plants/', PlantListCreateView.as_view()),
    path('plants/<int:pk>/', PlantDetailView.as_view()),
    path('plants/<int:plant_id>/add_image/', GrowthRecordAddView.as_view()),
]
