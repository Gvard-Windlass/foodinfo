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


class GetVars:
    single_path_name: str
    list_path_name: str


class GetCompareVars:
    objects_by_staff: int
    objects_by_user1: int
    objects_by_user2: int
    user1_object_id: int
    user2_object_id: int
    staff_object_id: int


class PostVars:
    default_post_data: Dict
    post_path_name: str


class PutVars:
    default_put_data: Dict
    put_path_name: str


class DeleteVars:
    delete_path_name: str


class BaseTestMixins:
    class GuestForbiddenGet(GetVars, APITestCase):
        """Test that anonymous users can't get object or list of objects"""

        def test_get_list_by_guest(self):
            url = reverse(self.list_path_name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_get_specific_by_guest(self):
            url = reverse(self.single_path_name, args=[1])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class GuestPermittedGet(GetVars, APITestCase):
        """Test that anonymous users can get object or list of objects.

        GET - 200, 404"""

        factory_count: int

        def test_get_list_by_guest(self):
            url = reverse(self.list_path_name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), self.factory_count)

        def test_get_specific_by_guest(self):
            url = reverse(self.single_path_name, args=[1])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], 1)

        def test_get_non_existant_by_guest(self):
            url = reverse(self.single_path_name, args=[100])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    class UserPermittedGet(GetVars, APITestCase):
        """Test that non-staff users can get object or list of objects.

        GET - 200, 404"""

        factory_count: int

        def test_get_list_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.list_path_name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), self.factory_count)

        def test_get_specific_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.single_path_name, args=[1])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], 1)

    class StaffPermittedGet(GetVars, APITestCase):
        """Test that staff users can get object or list of objects.

        GET - 200, 404"""

        factory_count: int

        def test_get_list_by_staff(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.list_path_name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), self.factory_count)

        def test_get_specific_by_staff(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.single_path_name, args=[1])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], 1)

    class StaffPermittedPostPutDelete(PostVars, PutVars, DeleteVars, APITestCase):
        """Test that staff can create, update, delete any objects.

        POST - 201, 400

        PUT - 200, 400, 404

        DELETE - 204, 404"""

        def test_post_by_staff(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.post_path_name)
            response = self.client.post(url, data=self.default_post_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_post_bad_data(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.post_path_name)
            data = {"incorrect field": 1}
            response = self.client.post(url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        def test_delete_by_staff(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.delete_path_name, args=[1])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        def test_delete_non_existant(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.delete_path_name, args=[100])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    class UserForbiddenPostPutDelete(PostVars, PutVars, DeleteVars, APITestCase):
        """Test that regular users can't create, update, delete objects"""

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

    class GuestForbiddenPostPutDelete(PostVars, PutVars, DeleteVars, APITestCase):
        """Test that anonymous users can't create, update, delete any objects"""

        def test_post_by_guest(self):
            url = reverse(self.post_path_name)
            response = self.client.post(url, data={"name": "anon"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_update_by_guest(self):
            url = reverse(self.put_path_name, args=[1])
            response = self.client.put(url, data=self.default_put_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_delete_by_guest(self):
            url = reverse(self.delete_path_name, args=[1])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class UserPermittedPost(PostVars, APITestCase):
        """Test that authenticated non-staff users can create objects"""

        def test_post_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.post_path_name)
            response = self.client.post(url, data=self.default_post_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    class OwnerPermittedPutDelete(PutVars, DeleteVars, APITestCase):
        """Test that among non-staff users only those who created objects can update and delete them"""

        user2_object_id: int

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

    class GuestLimitedGet(GetVars, GetCompareVars, APITestCase):
        """Test that anonymous user can get only objects created by staff"""

        def test_get_list_by_guest(self):
            url = reverse(self.list_path_name)
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), self.objects_by_staff)

        def test_get_specific_by_guest(self):
            url = reverse(self.single_path_name, args=[self.staff_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], self.staff_object_id)

            url = reverse(self.single_path_name, args=[self.user1_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class StaffUnlimitedGet(GetVars, GetCompareVars, APITestCase):
        """Test that staff users can get any objects regardless of who created them"""

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

        def test_get_specific_by_staff(self):
            credentials = TestUsers.get_staff_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.single_path_name, args=[self.user1_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], self.user1_object_id)

    class UserLimitedGet(GetVars, GetCompareVars, APITestCase):
        """Test that non-staff users can only get objects created by themselves or staff"""

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

        def test_get_specific_by_user(self):
            credentials = TestUsers.get_user1_credentials()
            self.assertTrue(self.client.login(**credentials))

            url = reverse(self.single_path_name, args=[self.user1_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["id"], self.user1_object_id)

            url = reverse(self.single_path_name, args=[self.staff_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            url = reverse(self.single_path_name, args=[self.user2_object_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
