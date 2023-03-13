from .models import Ingredient, Measure
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "user",
            "category",
            "calories",
            "proteins",
            "fats",
            "carbs",
        ]


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ["id", "name"]
