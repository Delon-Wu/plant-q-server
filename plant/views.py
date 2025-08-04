from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Plant, PlantImage
from .serializers import PlantSerializer, PlantImageSerializer
from django.shortcuts import get_object_or_404

class PlantListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        plants = Plant.objects.filter(user_id=str(request.user.id))
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)
    def post(self, request):
        data = request.data.copy()
        data['user_id'] = str(request.user.id)
        serializer = PlantSerializer(data=data)
        if serializer.is_valid():
            plant = serializer.save()
            return Response(PlantSerializer(plant).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlantDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk, user_id=str(request.user.id))
        return Response(PlantSerializer(plant).data)
    def put(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk, user_id=str(request.user.id))
        serializer = PlantSerializer(plant, data=request.data, partial=True)
        if serializer.is_valid():
            plant = serializer.save()
            return Response(PlantSerializer(plant).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk, user_id=str(request.user.id))
        plant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PlantImageAddView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, plant_id):
        plant = get_object_or_404(Plant, pk=plant_id, user_id=str(request.user.id))
        data = request.data.copy()
        data['plant'] = plant.id
        serializer = PlantImageSerializer(data=data)
        if serializer.is_valid():
            image = serializer.save()
            return Response(PlantImageSerializer(image).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
