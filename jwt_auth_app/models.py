from django.db import models
from django.contrib.auth.models import AbstractUser


class HoliUser(AbstractUser):
    image = models.CharField(max_length=250, null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'
