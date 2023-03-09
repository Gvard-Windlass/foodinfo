from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Measure(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name
