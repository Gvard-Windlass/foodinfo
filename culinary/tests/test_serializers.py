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
            "favorite": None,
            "portions": 6395,
            "total_time": "15:52:05",
            "instructions": "Good woman say man cup. Well drive particularly tend. Within behind perhaps specific. Where can nothing. Along nearly even special beat. Lead blue social. Marriage baby trade work.",
            "ingredients": [
                {
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
                },
                {
                    "id": 2,
                    "amount": 39997078.888215,
                    "ingredient": {
                        "id": 2,
                        "name": "test ingredient 1",
                        "user": 1,
                        "category": "Other",
                        "calories": None,
                        "proteins": None,
                        "fats": None,
                        "carbs": None,
                    },
                    "measure": {"id": 1, "name": "test measure 0"},
                },
                {
                    "id": 3,
                    "amount": 4.94152069866164,
                    "ingredient": {
                        "id": 3,
                        "name": "test ingredient 2",
                        "user": 1,
                        "category": "Other",
                        "calories": None,
                        "proteins": None,
                        "fats": None,
                        "carbs": None,
                    },
                    "measure": {"id": 1, "name": "test measure 0"},
                },
                {
                    "id": 4,
                    "amount": 119448218085.71,
                    "ingredient": {
                        "id": 4,
                        "name": "test ingredient 3",
                        "user": 1,
                        "category": "Other",
                        "calories": None,
                        "proteins": None,
                        "fats": None,
                        "carbs": None,
                    },
                    "measure": {"id": 1, "name": "test measure 0"},
                },
                {
                    "id": 5,
                    "amount": 446.536884244799,
                    "ingredient": {
                        "id": 5,
                        "name": "test ingredient 4",
                        "user": 1,
                        "category": "Other",
                        "calories": None,
                        "proteins": None,
                        "fats": None,
                        "carbs": None,
                    },
                    "measure": {"id": 1, "name": "test measure 0"},
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
            "calories": None,
            "proteins": None,
            "fats": None,
            "carbs": None,
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


class TestRecipeCreateSerializer(TestCase):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self):
        return super().setUp()

    def test_serializer(self):
        data = {
            "title": "new recipe",
            "portions": 10,
            "total_time": "1:30:00",
            "instructions": "Recipe steps",
            "ingredients": [
                {
                    "amount": 10,
                    "ingredient": {"id": 1},
                    "measure": {"id": 1},
                },
                {
                    "amount": 100,
                    "ingredient": {"name": "custom ingredient 1", "user_id": 1},
                    "measure": {"id": 2},
                },
            ],
            "author": 1,
            "tags": [1, 5],
        }
        creation_serializer = RecipeCreateSerializer(data=data)
        self.assertTrue(creation_serializer.is_valid())

        recipe = creation_serializer.save()
        recipe.refresh_from_db()
        serialized = RecipeSerializer(recipe).data

        db_data = {
            "id": 4,
            "title": "new recipe",
            "thumbnail": None,
            "favorite": None,
            "portions": 10,
            "total_time": "01:30:00",
            "instructions": "Recipe steps",
            "ingredients": [
                {
                    "id": 16,
                    "amount": 10.0,
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
                },
                {
                    "id": 17,
                    "amount": 100.0,
                    "ingredient": {
                        "id": 32,
                        "name": "custom ingredient 1",
                        "user": 1,
                        "category": "Other",
                        "calories": None,
                        "proteins": None,
                        "fats": None,
                        "carbs": None,
                    },
                    "measure": {"id": 2, "name": "test measure 1"},
                },
            ],
            "author": "user 0",
            "tags": [
                {"id": 1, "label": "tag 0", "category_name": "test tag category 0"},
                {"id": 5, "label": "tag 4", "category_name": "test tag category 0"},
            ],
            "calories": None,
            "proteins": None,
            "fats": None,
            "carbs": None,
        }
        self.assertEqual(json.dumps(serialized), json.dumps(db_data))


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
