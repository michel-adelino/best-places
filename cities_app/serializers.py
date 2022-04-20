from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import City
from jwt_auth_app.serializers import UserSerializer
from reviews_app.serializers import ReviewSerializer

User = get_user_model()


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


# class CityWithReviewsSerializer(CitySerializer):
#     reviews = ReviewSerializer(many=True)


# class CityWithUsersSerializer(CitySerializer):
#     users = UserSerializer(many=True)


class PopulatedCitySerializer(CitySerializer):
    reviews = ReviewSerializer(many=True)
    # users = UserSerializer(many=True)
