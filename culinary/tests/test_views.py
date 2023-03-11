from django.urls import reverse
from rest_framework import status
from test.factories import IngredientFactory, MeasureFactory
from test.base_test import BaseTestCases


class TestIngredientViews(BaseTestCases.BaseCRUDViewTests):
    def setUp(self):
        self.factory_count = 21
        IngredientFactory.create_batch(self.factory_count)
        self.endpoint = "ingredients"
        self.default_post_data = {"name": "carrot"}
        self.default_put_data = {"id": 2, "name": "new name"}
        super().setUp()

    def test_filter_by_name(self):
        IngredientFactory.create(name="different name")
        url = reverse("ingredients-list")
        response = self.client.get(url + "?name=different")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)


class TestMeasureViews(BaseTestCases.BaseCRUDViewTests):
    def setUp(self):
        self.factory_count = 21
        MeasureFactory.create_batch(self.factory_count)
        self.endpoint = "measures"
        self.default_post_data = {"name": "ounce"}
        self.default_put_data = {"id": 2, "name": "new name"}
        super().setUp()

    def test_filter_by_name(self):
        MeasureFactory.create(name="ounce")
        url = reverse("measures-list")
        response = self.client.get(url + "?name=ounce")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
