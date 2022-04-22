from cities_app.serializers import CitySerializer
from .models import Holiday
from rest_framework import serializers
from reviews_app.serializers import ReviewSerializer


class HolidaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Holiday
        fields = '__all__'


# class PopulatedHolidaySerializer(HolidaySerializer):
#     reviews = ReviewSerializer
#     city = CitySerializer
