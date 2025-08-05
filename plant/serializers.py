from rest_framework import serializers
from .models import Plant, GrowthRecord

class GrowthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthRecord
        fields = ['id', 'image', 'record_time', 'remark', 'created_at']

class PlantSerializer(serializers.ModelSerializer):
    records = GrowthRecordSerializer(many=True, read_only=True)
    class Meta:
        model = Plant
        fields = ['id', 'user', 'name', 'cover', 'created_at', 'records']
