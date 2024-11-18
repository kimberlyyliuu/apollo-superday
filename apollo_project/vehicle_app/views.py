from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .models import Vehicle
from .serializers import VehicleSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
from rest_framework.exceptions import ValidationError


# Create your views here.
class VehicleListCreate(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)  # Perform validation
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Return 422 Unprocessable Entity for validation errors
            return Response({"errors": e.detail}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class VehicleDetail(APIView):
    def get(self, request, vin):
        vehicle = get_object_or_404(Vehicle, vin=vin.upper())  # Ensure case-insensitive lookup
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, vin):
        vehicle = get_object_or_404(Vehicle, vin=vin.upper())
        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)  # Perform validation
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            # Return 422 Unprocessable Entity for validation errors
            return Response({"errors": e.detail}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    def delete(self, request, vin):
        vehicle = get_object_or_404(Vehicle, vin=vin.upper())
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)