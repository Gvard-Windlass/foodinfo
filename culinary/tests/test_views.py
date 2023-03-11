from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from test.factories import IngredientFactory, UserFactory


class TestIngredientViews(APITestCase):
    def setUp(self):
        IngredientFactory.create_batch(21)
        self.user = UserFactory.create()

    def test_get_ingredients_list(self):
        url = reverse("ingredients-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 21)

    def test_filter_by_name(self):
        IngredientFactory.create(name="different name")
        url = reverse("ingredients-list")
        response = self.client.get(url + "?name=different")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_post_new_ingredient_logged_in(self):
        self.client.login(username=UserFactory.username, password=UserFactory.password)
        url = reverse("ingredients-list")
        data = {"name": "carrot"}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_new_ingredient_anonymous(self):
        url = reverse("ingredients-list")
        data = {"name": "carrot"}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_bad_data(self):
        self.client.login(username=UserFactory.username, password=UserFactory.password)
        url = reverse("ingredients-list")
        data = {"incorrect field": 1}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_specific(self):
        url = reverse("ingredients-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 1)

    def test_get_non_existant(self):
        url = reverse("ingredients-detail", args=[100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_ingredient_logged_in(self):
        self.client.login(username=UserFactory.username, password=UserFactory.password)
        url = reverse("ingredients-detail", args=[1])
        data = {"id": 2, "name": "new name"}
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), {"id": 1, "name": "new name"})

    def test_update_bad_data(self):
        self.client.login(username=UserFactory.username, password=UserFactory.password)
        url = reverse("ingredients-detail", args=[1])
        data = {"bad": 1, "data": 2}
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_existant(self):
        self.client.login(username=UserFactory.username, password=UserFactory.password)
        url = reverse("ingredients-detail", args=[100])
        data = {"id": 2, "name": "new name"}
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_ingredient_anonymous(self):
        url = reverse("ingredients-detail", args=[1])
        data = {"id": 2, "name": "new name"}
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ingredient_logged_in(self):
        self.client.login(username=UserFactory.username, password=UserFactory.password)
        url = reverse("ingredients-detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_ingredient_anonymous(self):
        url = reverse("ingredients-detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_non_existant(self):
        self.client.login(username=UserFactory.username, password=UserFactory.password)
        url = reverse("ingredients-detail", args=[100])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
