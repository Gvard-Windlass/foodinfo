from django.urls import reverse
from rest_framework import status
from test.factories import IngredientFactory, MeasureFactory
from rest_framework.test import APITestCase
from test.base_test import BaseTestCases, TestUsers


class TestIngredientViews(
    BaseTestCases.BaseCUDViewTests,
    APITestCase,
):
    fixtures = ["users.json", "culinary.json"]

    def setUp(self):
        self.post_path_name = "ingredients-list"
        self.default_post_data = {"name": "carrot"}

        self.put_path_name = "ingredients-edit"
        self.default_put_data = {"id": 2, "name": "new name"}

        self.delete_path_name = "ingredients-edit"

    def test_get_list_anonymous(self):
        url = reverse(f"ingredients-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 21)

    def test_get_list_staff_access(self):
        credentials = TestUsers.get_staff_credentials()
        self.assertTrue(self.client.login(**credentials))

        url = reverse(f"ingredients-list")
        staff_response = self.client.get(url)

        self.assertEqual(staff_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(staff_response.json()), 31)

    def test_get_list_user_access(self):
        url = reverse(f"ingredients-list")

        credentials = TestUsers.get_user1_credentials()
        self.assertTrue(self.client.login(**credentials))

        user1_response = self.client.get(url)
        self.assertEqual(user1_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user1_response.json()), 26)

        credentials = TestUsers.get_user2_credentials()
        self.assertTrue(self.client.login(**credentials))

        user2_response = self.client.get(url)
        self.assertEqual(user2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user2_response.json()), 26)

        with self.assertRaises(AssertionError):
            self.assertCountEqual(user1_response.json(), user2_response.json())

    def test_filter_by_name(self):
        IngredientFactory.create(name="different name")
        url = reverse("ingredients-list")
        response = self.client.get(url + "?name=different")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_get_specific_anonymous(self):
        url = reverse(f"ingredients-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 1)

        url = reverse(f"ingredients-detail", args=[26])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_specific_staff_acess(self):
        credentials = TestUsers.get_staff_credentials()
        self.assertTrue(self.client.login(**credentials))

        url = reverse(f"ingredients-detail", args=[26])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 26)

    def test_get_specific_user_acess(self):
        credentials = TestUsers.get_user1_credentials()
        self.assertTrue(self.client.login(**credentials))

        url = reverse(f"ingredients-detail", args=[26])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 26)


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
