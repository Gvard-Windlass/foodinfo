from typing import Dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUsers:
    """Provides methods for different users logins for testing"""

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
        """Test get object, get list of objects, get 404 object by anonymous user"""

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

    class BaseGetListByUserTestsMixin(APITestCase):
        """Test get list of objects with restriction according to user premissions.

        If anonymous, only objects created by staff users.

        If regular user, only objects created by self and staff.

        If staff, all objects"""

        list_path_name: str
        objects_by_staff: int
        objects_by_user1: int
        objects_by_user2: int

        def test_get_list_by_guest(self):
            url = reverse(self.list_path_name)
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), self.objects_by_staff)

        def test_get_list_by_staff(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.list_path_name)
            staff_response = self.client.get(url)

            self.assertEqual(staff_response.status_code, status.HTTP_200_OK)
            total = sum(
                [self.objects_by_staff, self.objects_by_user1, self.objects_by_user2]
            )
            self.assertEqual(len(staff_response.json()), total)

        def test_get_list_by_user(self):
            url = reverse(self.list_path_name)

            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            user1_response = self.client.get(url)
            self.assertEqual(user1_response.status_code, status.HTTP_200_OK)
            user1_total = sum([self.objects_by_staff, self.objects_by_user1])
            self.assertEqual(len(user1_response.json()), user1_total)

            credentials = TestUsers.get_user2_credentials()
            self.assertTrue(self.client.login(**credentials))

            user2_response = self.client.get(url)
            self.assertEqual(user2_response.status_code, status.HTTP_200_OK)
            user2_total = sum([self.objects_by_staff, self.objects_by_user2])
            self.assertEqual(len(user2_response.json()), user2_total)

            with self.assertRaises(AssertionError):
                self.assertCountEqual(user1_response.json(), user2_response.json())

    class BaseGetObjectByUserTestsMixin(APITestCase):
        """Test get object with restriction according to user premissions.

        If anonymous, only objects created by staff users are available.

        If regular user, only objects created by self and staff are available.

        If staff, all objects are available."""

        single_path_name: str
        staff_object_id: int
        user1_object_id: int

        def test_get_specific_by_guest(self):
            url = reverse(self.single_path_name, args=[self.staff_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], self.staff_object_id)

            url = reverse(self.single_path_name, args=[self.user1_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_get_specific_by_staff(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.single_path_name, args=[self.user1_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], self.user1_object_id)

        def test_get_specific_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.single_path_name, args=[self.user1_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], self.user1_object_id)

    class BaseGetByUserTestsMixin(
        BaseGetListByUserTestsMixin, BaseGetObjectByUserTestsMixin
    ):
        """Test get object and list of objects according to user permissions.

        If anonymous, only staff-created objects are accessible.

        If regular user, only self- and staff-created objects are accessible.

        If staff user, all objects are accessible."""

    class BasePostTestsMixin(APITestCase):
        """Test post correct and incorrect data by staff, correct data by anonymous user."""

        default_post_data: Dict
        post_path_name: str

        def test_post_by_staff(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.post_path_name)
            response = self.client.post(url, data=self.default_post_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_post_by_guest(self):
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
        """Test update with correct and incorrect data by staff, correct data by anonymous user."""

        default_put_data: Dict
        put_path_name: str

        def test_update_by_staff(self):
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

        def test_update_by_guest(self):
            url = reverse(self.put_path_name, args=[1])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class BaseDeleteTestsMixin(APITestCase):
        """Test delete object by staff and anonymous user, delete 404 object by staff."""

        delete_path_name: str

        def test_delete_by_staff(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.delete_path_name, args=[1])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        def test_delete_by_guest(self):
            url = reverse(self.delete_path_name, args=[1])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_delete_non_existant(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.delete_path_name, args=[100])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    class BaseEditByUserTestsMixin(APITestCase):
        """Test put and delete with restriction to those users who created the object."""

        user2_object_id: int
        put_path_name: str
        delete_path_name: str
        default_put_data: Dict

        def test_update_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.put_path_name, args=[self.user2_object_id])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            credentials = TestUsers.get_user2_credentials()
            self.assertTrue(self.client.login(**credentials))

            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_delete_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.delete_path_name, args=[self.user2_object_id])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            credentials = TestUsers.get_user2_credentials()
            self.assertTrue(self.client.login(**credentials))

            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    class BaseGetForbiddenForGuestsTestsMixin(APITestCase):
        """Test that anonymous users can't get object or list of objects"""

        single_path_name: str
        list_path_name: str

        def test_get_list_by_guest(self):
            url = reverse(self.list_path_name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_get_specific_by_guest(self):
            url = reverse(self.single_path_name, args=[1])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class BaseCUDForbiddenForUsersTestsMixin(APITestCase):
        """Test that only users who created the objects can post, put, delete them."""

        post_path_name: str
        delete_path_name: str
        put_path_name: str
        default_post_data: Dict
        default_put_data: Dict

        def test_post_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.post_path_name)
            response = self.client.post(url, data=self.default_post_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_update_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.put_path_name, args=[1])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_delete_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.delete_path_name, args=[1])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class BaseCRUDViewTests(
        BaseGetTestsMixin, BasePostTestsMixin, BasePutTestsMixin, BaseDeleteTestsMixin
    ):
        """Basic tests with successful safe methods calls performed by anonymous user and
        authenticated staff user successfull calls for post, put, delete."""

    class BaseCUDViewTests(BasePostTestsMixin, BasePutTestsMixin, BaseDeleteTestsMixin):
        """Basic test checks, ensuring anonymous users can't use post, put, delete calls."""
