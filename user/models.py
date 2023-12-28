from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    image_link = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=200, null=True)
