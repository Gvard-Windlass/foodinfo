from .models import Ingredient, Measure, Fridge
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


class FridgeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    shelf = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Fridge
        fields = ["id", "name", "user", "shelf"]
