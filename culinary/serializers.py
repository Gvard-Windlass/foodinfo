from tags.serializers import TagSerializer
from .models import (
    Ingredient,
    IngredientUsage,
    Measure,
    Fridge,
    Recipe,
    UtensilConversion,
)
from rest_framework import serializers
from foodinfo.utils import DynamicFieldsModelSerializer


class IngredientSerializer(DynamicFieldsModelSerializer):
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
    shelf = IngredientSerializer(many=True, read_only=True, fields=["id", "name"])

    class Meta:
        model = Fridge
        fields = ["id", "name", "user", "shelf"]


class ConversionSerializer(serializers.ModelSerializer):
    utensil = MeasureSerializer(many=False, read_only=True)
    ingredient = IngredientSerializer(many=False, read_only=True, fields=["id", "name"])

    utensil_id = serializers.PrimaryKeyRelatedField(
        queryset=Measure.objects.all(),
        write_only=True,
        required=False,
        source="utensil",
    )
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        write_only=True,
        required=False,
        source="ingredient",
    )

    class Meta:
        model = UtensilConversion
        fields = [
            "id",
            "standard_value",
            "utensil",
            "utensil_id",
            "ingredient_id",
            "ingredient",
        ]


class IngredientUsageSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False)
    measure = MeasureSerializer(many=False)

    class Meta:
        model = IngredientUsage
        fields = ["id", "amount", "ingredient", "measure"]


class RecipeSerializer(DynamicFieldsModelSerializer):
    ingredients = IngredientSerializer(many=True)
    author = serializers.ReadOnlyField(source="author.username")
    tags = TagSerializer(many=True, fields=["id", "label", "category_name"])

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "thumbnail",
            "favorites",
            "portions",
            "total_time",
            "instructions",
            "ingredients",
            "author",
            "tags",
        ]
