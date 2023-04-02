from tags.models import Tag
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
    ingredients = IngredientUsageSerializer(many=True, source="ingredientusage_set")
    author = serializers.ReadOnlyField(source="author.username")
    tags = TagSerializer(many=True, fields=["id", "label", "category_name"])
    favorite = serializers.SerializerMethodField()

    def get_favorite(self, obj):
        request = self.context.get("request") or None
        if request and request.user.is_authenticated:
            return obj.favorites.filter(pk=request.user.pk).exists()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "thumbnail",
            "favorite",
            "portions",
            "total_time",
            "instructions",
            "ingredients",
            "author",
            "tags",
            "calories",
            "proteins",
            "fats",
            "carbs",
        ]


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListField(write_only=True)
    tags = serializers.ListField(write_only=True)

    def create(self, validated_data):
        ingredients_usage_data = validated_data.pop("ingredients")
        tag_ids = validated_data.pop("tags")

        recipe = Recipe.objects.create(**validated_data)

        for usage in ingredients_usage_data:
            ingredient_data = usage["ingredient"]
            measure_data = usage["measure"]

            ingr_id = ingredient_data.get("id") or None
            mes_id = measure_data.get("id") or None

            if ingr_id:
                ingredient = Ingredient.objects.get(id=ingr_id)
            else:
                ingredient = Ingredient.objects.create(**ingredient_data)

            if mes_id:
                measure = Measure.objects.get(id=mes_id)
            else:
                measure = Measure.objects.create(**measure_data)

            usage = IngredientUsage.objects.create(
                amount=usage["amount"],
                ingredient=ingredient,
                measure=measure,
                recipe=recipe,
            )

        for id in tag_ids:
            tag = Tag.objects.get(id=id)
            recipe.tags.add(tag)

        return recipe

    class Meta:
        model = Recipe
        fields = [
            "title",
            "thumbnail",
            "portions",
            "total_time",
            "instructions",
            "ingredients",
            "author",
            "tags",
            "calories",
            "proteins",
            "fats",
            "carbs",
        ]
