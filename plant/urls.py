from django.urls import path
from .views import PlantListCreateView, PlantDetailView, GrowthRecordAddView, GrowthRecordDeleteView

urlpatterns = [
    path('plants/', PlantListCreateView.as_view()),
    path('plants/<int:pk>/', PlantDetailView.as_view()),
    path('plants/record/<int:plant_id>/', GrowthRecordAddView.as_view()),  # 添加成长记录
    path('plants/record/delete/<int:pk>/', GrowthRecordDeleteView.as_view()),  # 删除指定成长记录
]
