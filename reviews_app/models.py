from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from cities_app.models import City

User = get_user_model()

# Create your models here.


class Review(models.Model):

    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, related_name='reviews', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=True)
    rating_food = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_weather = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_culture = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    @property
    def avg_rating(self):
        return (self.rating_food + self.rating_weather + self.rating_food) / 3

    def __str__(self):
        return f'{self.city} by {self.user} average rating: {self.avg_rating}'
