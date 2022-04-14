from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import City
from .serializers import CitySerializer
# Create your views here.


# Retrieve is reserved for 'by ID'!
class CityList(ListAPIView):
    """ Get all cities (generic view) """

    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityDetail(APIView):
    """ Get city by id (pk) (class-based view)"""

    def get(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
            serialized_city = CitySerializer(city)
            return Response(data=serialized_city.data, status=status.HTTP_200_OK)
        except City.DoesNotExist:
            raise NotFound(detail="City id not found")
