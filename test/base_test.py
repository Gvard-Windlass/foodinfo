from dataclasses import dataclass
from typing import Dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from test.factories import UserFactory


class BaseTestCases:
    @dataclass
    class BaseViewsConfig:
        endpoint: str
        factory_count: int

    class BaseGetTestsMixin(APITestCase, BaseViewsConfig):
        def test_get_list(self):
            url = reverse(f"{self.endpoint}-list")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), self.factory_count)

        def test_get_specific(self):
            url = reverse(f"{self.endpoint}-detail", args=[1])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], 1)

        def test_get_non_existant(self):
            url = reverse(f"{self.endpoint}-detail", args=[100])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    class BasePostTestsMixin(APITestCase, BaseViewsConfig):
        default_post_data: Dict

        def setUp(self) -> None:
            self.user = UserFactory.create()

        def test_post_new_ingredient_logged_in(self):
            self.client.login(
                username=UserFactory.username, password=UserFactory.password
            )
            url = reverse(f"{self.endpoint}-list")
            response = self.client.post(url, data=self.default_post_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_post_new_ingredient_anonymous(self):
            url = reverse(f"{self.endpoint}-list")
            response = self.client.post(url, data=self.default_post_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_post_bad_data(self):
            self.client.login(
                username=UserFactory.username, password=UserFactory.password
            )
            url = reverse(f"{self.endpoint}-list")
            data = {"incorrect field": 1}
            response = self.client.post(url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    class BasePutTestsMixin(APITestCase, BaseViewsConfig):
        default_put_data: Dict

        def test_update_logged_in(self):
            id = 1
            response_data = self.default_put_data.copy()
            response_data["id"] = id

            self.client.login(
                username=UserFactory.username, password=UserFactory.password
            )
            url = reverse(f"{self.endpoint}-detail", args=[id])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response.json(), response_data)

        def test_update_bad_data(self):
            self.client.login(
                username=UserFactory.username, password=UserFactory.password
            )
            url = reverse(f"{self.endpoint}-detail", args=[1])
            data = {"bad": 1, "data": 2}
            response = self.client.put(url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_update_non_existant(self):
            self.client.login(
                username=UserFactory.username, password=UserFactory.password
            )
            url = reverse(f"{self.endpoint}-detail", args=[100])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_update_anonymous(self):
            url = reverse(f"{self.endpoint}-detail", args=[1])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class BaseDeleteTestsMixin(APITestCase, BaseViewsConfig):
        def setUp(self) -> None:
            self.user = UserFactory.create()

        def test_delete_ingredient_logged_in(self):
            self.client.login(
                username=UserFactory.username, password=UserFactory.password
            )
            url = reverse(f"{self.endpoint}-detail", args=[1])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        def test_delete_ingredient_anonymous(self):
            url = reverse(f"{self.endpoint}-detail", args=[1])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_delete_non_existant(self):
            self.client.login(
                username=UserFactory.username, password=UserFactory.password
            )
            url = reverse(f"{self.endpoint}-detail", args=[100])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    class BaseCRUDViewTests(
        BaseGetTestsMixin, BasePostTestsMixin, BasePutTestsMixin, BaseDeleteTestsMixin
    ):
        pass
