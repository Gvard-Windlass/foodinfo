from django.test import TestCase

from culinary.models import *
from test.factories import *


class TestIngredientModel(TestCase):
    def test_create_product(self):
        UserFactory.create()
        product = IngredientFactory.create()
        self.assertIsInstance(product, Ingredient)


class TestMeasureModel(TestCase):
    def test_create_product(self):
        product = MeasureFactory.create()
        self.assertIsInstance(product, Measure)


class TestFridgeModel(TestCase):
    def test_create_fridge(self):
        UserFactory.create()
        fridge = FridgeFactory.create(shelf=IngredientFactory.create_batch(5))
        self.assertIsInstance(fridge, Fridge)
        self.assertIsInstance(Fridge.objects.first().shelf.first(), Ingredient)
        self.assertEqual(len(Fridge.objects.first().shelf.all()), 5)
