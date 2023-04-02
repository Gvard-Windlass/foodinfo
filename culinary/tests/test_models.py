from django.db.utils import IntegrityError
from django.test import TestCase

from culinary.models import *
from test.factories import *


class TestIngredientModel(TestCase):
    def test_create_product(self):
        UserFactory.create()
        product = IngredientFactory.create()
        self.assertIsInstance(product, Ingredient)


class TestMeasureModel(TestCase):
    def test_create_measure(self):
        measure = MeasureFactory.create()
        self.assertIsInstance(measure, Measure)


class TestFridgeModel(TestCase):
    def test_create_fridge(self):
        UserFactory.create()
        fridge = FridgeFactory.create(shelf=IngredientFactory.create_batch(5))
        self.assertIsInstance(fridge, Fridge)
        self.assertIsInstance(Fridge.objects.first().shelf.first(), Ingredient)
        self.assertEqual(len(Fridge.objects.first().shelf.all()), 5)


class TestConversionModel(TestCase):
    def setUp(self):
        UserFactory.create()
        self.conversion = ConversionFactory.create()

    def test_create_conversion(self):
        self.assertIsInstance(self.conversion, UtensilConversion)

    def test_unique_check(self):
        data = {
            "standard_value": 100,
            "utensil_id": self.conversion.utensil_id,
            "ingredient_id": self.conversion.ingredient_id,
        }
        with self.assertRaises(IntegrityError):
            UtensilConversion.objects.create(**data)


class TestRecipeModel(TestCase):
    def test_create_recipe(self):
        UserFactory.create()
        recipe = RecipeFactory.create()
        ingredients = IngredientUsageFactory.create_batch(3, recipe=recipe)

        self.assertIsInstance(recipe, Recipe)
        self.assertIsInstance(ingredients[0], IngredientUsage)

        usage = IngredientUsage.objects.filter(recipe=recipe)
        self.assertEqual(len(usage), 3)
