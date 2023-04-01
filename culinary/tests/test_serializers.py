import json

from django.test import TestCase

from culinary.models import *
from culinary.serializers import *


class TestIngredientSerializer(TestCase):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self):
        self.ingredient = Ingredient.objects.first()

    def test_serializer(self):
        serialized = IngredientSerializer(self.ingredient).data
        data = {
            "id": 1,
            "name": "test ingredient 0",
            "user": 1,
            "category": "Other",
            "calories": None,
            "proteins": None,
            "fats": None,
            "carbs": None,
        }
        self.assertDictEqual(serialized, data)

    def test_dynamic_fields(self):
        serialized = IngredientSerializer(self.ingredient, fields=["id", "name"]).data
        data = {"id": 1, "name": "test ingredient 0"}
        self.assertDictEqual(serialized, data)


class TestMeasureSerializer(TestCase):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self):
        self.measure = Measure.objects.first()

    def test_serializer(self):
        serialized = MeasureSerializer(self.measure).data
        data = {
            "id": 1,
            "name": "test measure 0",
        }
        self.assertDictEqual(serialized, data)


class TestFridgeSerializer(TestCase):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self):
        self.fridge = Fridge.objects.all()[2]

    def test_serializer(self):
        serialized = FridgeSerializer(self.fridge).data
        data = {
            "id": 3,
            "name": "test fridge 2",
            "user": 3,
            "shelf": [
                {"id": 27, "name": "test ingredient 26"},
                {"id": 28, "name": "test ingredient 27"},
                {"id": 29, "name": "test ingredient 28"},
                {"id": 30, "name": "test ingredient 29"},
                {"id": 31, "name": "test ingredient 30"},
            ],
        }
        self.assertEqual(json.dumps(serialized), json.dumps(data))


class TestConversionSerializer(TestCase):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self):
        self.conversion = UtensilConversion.objects.first()

    def test_serializer(self):
        serialized = ConversionSerializer(self.conversion).data
        data = {
            "id": 1,
            "standard_value": 10.5,
            "utensil": {"id": 1, "name": "test measure 0"},
            "ingredient": {"id": 1, "name": "test ingredient 0"},
        }
        self.assertEqual(json.dumps(serialized), json.dumps(data))


class TestRecipeSerializer(TestCase):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self):
        self.recipe = Recipe.objects.first()

    def test_serializer(self):
        serialized = RecipeSerializer(self.recipe).data
        data = {
            "id": 1,
            "title": "test recipe 0",
            "thumbnail": None,
            "favorites": [],
            "portions": 6395,
            "total_time": "15:52:05",
            "instructions": "Good woman say man cup. Well drive particularly tend. Within behind perhaps specific. Where can nothing. Along nearly even special beat. Lead blue social. Marriage baby trade work.",
            "ingredients": [
                {
                    "id": 1,
                    "name": "test ingredient 0",
                    "user": 1,
                    "category": "Other",
                    "calories": None,
                    "proteins": None,
                    "fats": None,
                    "carbs": None,
                },
                {
                    "id": 2,
                    "name": "test ingredient 1",
                    "user": 1,
                    "category": "Other",
                    "calories": None,
                    "proteins": None,
                    "fats": None,
                    "carbs": None,
                },
                {
                    "id": 3,
                    "name": "test ingredient 2",
                    "user": 1,
                    "category": "Other",
                    "calories": None,
                    "proteins": None,
                    "fats": None,
                    "carbs": None,
                },
                {
                    "id": 4,
                    "name": "test ingredient 3",
                    "user": 1,
                    "category": "Other",
                    "calories": None,
                    "proteins": None,
                    "fats": None,
                    "carbs": None,
                },
                {
                    "id": 5,
                    "name": "test ingredient 4",
                    "user": 1,
                    "category": "Other",
                    "calories": None,
                    "proteins": None,
                    "fats": None,
                    "carbs": None,
                },
            ],
            "author": "user 0",
            "tags": [
                {"id": 1, "label": "tag 0", "category_name": "test tag category 0"},
                {"id": 4, "label": "tag 3", "category_name": "test tag category 0"},
                {"id": 7, "label": "tag 6", "category_name": "test tag category 1"},
                {"id": 10, "label": "tag 9", "category_name": "test tag category 1"},
                {"id": 13, "label": "tag 12", "category_name": "test tag category 2"},
            ],
        }
        self.assertEqual(json.dumps(serialized), json.dumps(data))

    def test_dynamic_fields(self):
        serialized = RecipeSerializer(
            self.recipe, fields=["id", "title", "thumbnail", "author"]
        ).data
        data = {
            "id": 1,
            "title": "test recipe 0",
            "thumbnail": None,
            "author": "user 0",
        }
        self.assertDictEqual(serialized, data)


class TestIngredientUsageSerializer(TestCase):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def test_serializer(self):
        usage = IngredientUsage.objects.first()
        serialized = IngredientUsageSerializer(usage).data
        data = {
            "id": 1,
            "amount": 57549662635585.4,
            "ingredient": {
                "id": 1,
                "name": "test ingredient 0",
                "user": 1,
                "category": "Other",
                "calories": None,
                "proteins": None,
                "fats": None,
                "carbs": None,
            },
            "measure": {"id": 1, "name": "test measure 0"},
        }
        self.assertEqual(json.dumps(serialized), json.dumps(data))
