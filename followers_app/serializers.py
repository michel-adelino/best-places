from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'


class FollowersOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('follower',)


class FollowingsOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('user',)
