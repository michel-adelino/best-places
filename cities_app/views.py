from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from .models import City
from .serializers import CitySerializer
# Create your views here.


# Retrieve is reserved for 'by ID'!
class CityList(ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
