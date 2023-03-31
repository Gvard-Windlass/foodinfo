from django.db import models


class TagCategory(models.Model):
    name = models.CharField(max_length=25, unique=True)


class Tag(models.Model):
    label = models.CharField(max_length=25, unique=True)
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE)
