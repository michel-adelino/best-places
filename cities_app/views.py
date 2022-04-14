from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from .models import City
from .serializers import CitySerializer

# Create your views here.


class CityList(RetrieveAPIView):
    queryset = City.objets.all()
    serializer_class = CitySerializer
