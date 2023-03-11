from .models import Ingredient, Measure
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ["id", "name"]
