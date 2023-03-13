from typing import Dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUsers:
    @classmethod
    def _get_credentials(cls, user_n):
        return {"username": f"user {user_n}", "password": f"Bk7^31&3LDXt{user_n}"}

    @classmethod
    def get_staff_credentials(cls):
        return cls._get_credentials(0)

    @classmethod
    def get_user1_credentials(cls):
        return cls._get_credentials(1)

    @classmethod
    def get_user2_credentials(cls):
        return cls._get_credentials(2)


class BaseTestCases:
    class BaseGetTestsMixin(APITestCase):
        single_path_name: str
        list_path_name: str
        factory_count: int

        def test_get_list(self):
            url = reverse(self.list_path_name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), self.factory_count)

        def test_get_specific(self):
            url = reverse(self.single_path_name, args=[1])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], 1)

        def test_get_non_existant(self):
            url = reverse(self.single_path_name, args=[100])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    class BasePostTestsMixin(APITestCase):
        default_post_data: Dict
        post_path_name: str

        def test_post_logged_in(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.post_path_name)
            response = self.client.post(url, data=self.default_post_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_post_anonymous(self):
            url = reverse(self.post_path_name)
            response = self.client.post(url, data={"name": "anon"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_post_bad_data(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.post_path_name)
            data = {"incorrect field": 1}
            response = self.client.post(url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    class BasePutTestsMixin(APITestCase):
        default_put_data: Dict
        put_path_name: str

        def test_update_logged_in(self):
            id = 1
            response_data = self.default_put_data.copy()
            response_data["id"] = id

            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.put_path_name, args=[id])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictContainsSubset(response_data, response.json())

        def test_update_bad_data(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.put_path_name, args=[1])
            data = {"bad": 1, "data": 2}
            response = self.client.put(url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_update_non_existant(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.put_path_name, args=[100])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_update_anonymous(self):
            url = reverse(self.put_path_name, args=[1])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class BaseDeleteTestsMixin(APITestCase):
        delete_path_name: str

        def test_delete_logged_in(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.delete_path_name, args=[1])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        def test_delete_anonymous(self):
            url = reverse(self.delete_path_name, args=[1])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_delete_non_existant(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.delete_path_name, args=[100])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    class BaseCRUDViewTests(
        BaseGetTestsMixin, BasePostTestsMixin, BasePutTestsMixin, BaseDeleteTestsMixin
    ):
        pass

    class BaseCUDViewTests(BasePostTestsMixin, BasePutTestsMixin, BaseDeleteTestsMixin):
        pass
