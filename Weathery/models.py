from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    last_updated = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.city.name}: {self.temperature}°C, {self.description}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
