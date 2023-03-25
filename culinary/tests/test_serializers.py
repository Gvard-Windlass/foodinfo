import json

from django.test import TestCase

from culinary.models import *
from culinary.serializers import *


class TestIngredientSerializer(TestCase):
    fixtures = ["users.json", "culinary.json"]

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
    fixtures = ["users.json", "culinary.json"]

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
    fixtures = ["users.json", "culinary.json"]

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
    fixtures = ["users.json", "culinary.json"]

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
