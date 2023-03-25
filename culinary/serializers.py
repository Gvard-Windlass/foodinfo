from .models import Ingredient, Measure, Fridge, UtensilConversion
from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional 'fields' argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the 'fields' argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


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
