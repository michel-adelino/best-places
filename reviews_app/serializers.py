from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'text', 'user', 'city', 'created_date', 'rating_food',
                  'rating_culture', 'rating_weather', 'avg_rating')
