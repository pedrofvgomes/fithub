from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime, pytz

class User(AbstractUser):
    age = models.IntegerField(default=0)
    starting_weight = models.FloatField(default=0)
    current_weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    gender = models.CharField(max_length=50)
    activity = models.CharField(max_length=100)
    objective = models.CharField(max_length=100)
    bmr = models.IntegerField(default=0)
    daily_calories = models.IntegerField(default=0)

class WeightLog(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    weight = models.FloatField()
    timestamp = models.DateTimeField(default=datetime.datetime.now())

class FoodLog(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories = models.IntegerField(default=0)
    serving = models.CharField(max_length=100)
    meal = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=datetime.datetime.now())

class NutritionalInfo(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    objective = models.FloatField()
    bmr = models.IntegerField()
    activity = models.CharField(max_length=100)
    caloric_need = models.IntegerField()