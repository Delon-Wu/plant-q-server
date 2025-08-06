from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Plant, GrowthRecord
from .serializers import PlantSerializer, GrowthRecordSerializer
from django.shortcuts import get_object_or_404

class PlantListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        plants = Plant.objects.filter(user=str(request.user.id))
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)
    def post(self, request):
        data = request.data.copy()
        data['user'] = str(request.user.id)
        serializer = PlantSerializer(data=data)
        if serializer.is_valid():
            plant = serializer.save()
            return Response(PlantSerializer(plant).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlantDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk, user=str(request.user.id))
        return Response(PlantSerializer(plant).data)
    def put(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk, user=str(request.user.id))
        serializer = PlantSerializer(plant, data=request.data, partial=True)
        if serializer.is_valid():
            plant = serializer.save()
            return Response(PlantSerializer(plant).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk, user=str(request.user.id))
        plant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GrowthRecordAddView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, plant_id):
        plant = get_object_or_404(Plant, pk=plant_id, user=str(request.user.id))
        data = request.data.copy()
        data['plant'] = plant.id
        serializer = GrowthRecordSerializer(data=data)
        if serializer.is_valid():
            image = serializer.save()
            return Response(GrowthRecordSerializer(image).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GrowthRecordDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        growth_record = get_object_or_404(GrowthRecord, pk=pk, plant__user=str(request.user.id))
        growth_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
