from rest_framework import serializers
from .models import Plant, PlantImage

class PlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ['id', 'image', 'record_time', 'remark', 'created_at']

class PlantSerializer(serializers.ModelSerializer):
    images = PlantImageSerializer(many=True, read_only=True)
    class Meta:
        model = Plant
        fields = ['id', 'user', 'name', 'cover', 'created_at', 'images']
