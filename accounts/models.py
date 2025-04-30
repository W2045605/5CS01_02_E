from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Users(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)