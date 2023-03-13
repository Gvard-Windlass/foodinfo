from django.urls import reverse
from rest_framework import status
from test.factories import IngredientFactory, MeasureFactory
from rest_framework.test import APITestCase
from test.base_test import BaseTestCases, TestUsers


class TestIngredientViews(
    BaseTestCases.BaseCUDViewTests,
    BaseTestCases.BaseGetByUserTestsMixin,
    BaseTestCases.BaseEditByUserTestsMixin,
    APITestCase,
):
    fixtures = ["users.json", "culinary.json"]

    def setUp(self):
        self.list_path_name = "ingredients-list"
        self.single_path_name = "ingredients-detail"

        self.objects_by_staff = 21
        self.objects_by_user1 = 5
        self.objects_by_user2 = 5

        self.staff_object_id = 1
        self.user1_object_id = 26
        self.user2_object_id = 31

        self.post_path_name = "ingredients-list"
        self.default_post_data = {"name": "carrot"}

        self.put_path_name = "ingredients-edit"
        self.default_put_data = {"id": 2, "name": "new name"}

        self.delete_path_name = "ingredients-edit"

    def test_filter_by_name(self):
        IngredientFactory.create(name="different name")
        url = reverse("ingredients-list")
        response = self.client.get(url + "?name=different")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)


class TestMeasureViews(BaseTestCases.BaseCRUDViewTests):
    fixtures = ["users.json", "culinary.json"]

    def setUp(self):
        self.factory_count = 21
        MeasureFactory.create_batch(self.factory_count)
        self.list_path_name = "measures-list"
        self.single_path_name = "measures-detail"

        self.post_path_name = "measures-list"
        self.default_post_data = {"name": "ounce"}

        self.put_path_name = "measures-detail"
        self.default_put_data = {"id": 2, "name": "new name"}

        self.delete_path_name = "measures-detail"

        super().setUp()

    def test_filter_by_name(self):
        MeasureFactory.create(name="ounce")
        url = reverse("measures-list")
        response = self.client.get(url + "?name=ounce")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
