from django.db import models
from django.contrib.auth import get_user_model

from cities_app.models import City
from reviews_app.serializers import Review

User = get_user_model()


class Holiday(models.Model):
    user = models.ForeignKey(
        User, related_name='holidays', on_delete=models.CASCADE)
    city = models.ForeignKey(
        City, related_name='holidays', on_delete=models.CASCADE)
    date = models.CharField(max_length=7, null=True, blank=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    # review = models.ForeignKey(
    #     Review, related_name='holidays', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.city} by {self.user}'
