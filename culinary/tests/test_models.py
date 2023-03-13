from django.test import TestCase

from culinary.models import *
from test.factories import IngredientFactory, MeasureFactory, UserFactory


class TestIngredientModel(TestCase):
    def test_create_product(self):
        UserFactory.create()
        product = IngredientFactory.create()
        self.assertIsInstance(product, Ingredient)


class TestMeasureModel(TestCase):
    def test_create_product(self):
        product = MeasureFactory.create()
        self.assertIsInstance(product, Measure)
