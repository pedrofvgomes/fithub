from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)

class WeightLog(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    weight = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)

class FoodLog(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
