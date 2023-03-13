from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name


class Measure(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name
