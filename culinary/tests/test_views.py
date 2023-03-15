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


class TestMeasureViews(
    BaseTestCases.BaseCRUDViewTests, BaseTestCases.BaseCUDForbiddenForUsersTestsMixin
):
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


class TestFridgeViews(
    BaseTestCases.BaseGetForbiddenForGuestsTestsMixin,
    BaseTestCases.BaseGetObjectByUserTestsMixin,
    APITestCase,
):
    fixtures = ["users.json", "culinary.json"]

    def setUp(self) -> None:
        self.list_path_name = "shelfs-list"
        self.single_path_name = "shelfs-detail"

        self.user1_object_id = 2

    def test_get_list_by_staff(self):
        credentials = TestUsers.get_staff_credentials()
        self.assertTrue(self.client.login(**credentials))

        url = reverse(self.list_path_name)
        response = self.client.get(url)

        self.assertEqual(len(response.json()), 3)
        self.assertEqual(len(response.json()[0]["shelf"]), 21)
        self.assertEqual(len(response.json()[1]["shelf"]), 5)
        self.assertEqual(len(response.json()[2]["shelf"]), 5)

    def test_get_list_by_user(self):
        url = reverse(self.list_path_name)

        credentials = TestUsers.get_user1_credentials()
        self.assertTrue(self.client.login(**credentials))

        user1_response = self.client.get(url)
        user1_data = user1_response.json()
        user1_shelf = user1_data[0]["shelf"]
        self.assertEqual(user1_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user1_data), 1)
        self.assertEqual(len(user1_shelf), 5)

        credentials = TestUsers.get_user2_credentials()
        self.assertTrue(self.client.login(**credentials))

        user2_response = self.client.get(url)
        user2_data = user2_response.json()
        user2_shelf = user2_data[0]["shelf"]
        self.assertEqual(user2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user2_data), 1)
        self.assertEqual(len(user2_shelf), 5)

        with self.assertRaises(AssertionError):
            self.assertCountEqual(user1_shelf, user2_shelf)
