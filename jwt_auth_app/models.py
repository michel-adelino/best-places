from email.mime import image
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class HoliUser(AbstractUser):
    image = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
