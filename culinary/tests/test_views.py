from typing_extensions import override
from django.urls import reverse
from rest_framework import status
from culinary.models import Ingredient
from tags.models import Tag
from test.factories import (
    FridgeFactory,
    IngredientFactory,
    MeasureFactory,
    RecipeFactory,
)
from rest_framework.test import APITestCase
from test.base_test import BaseTestMixins, TestUsers


class TestIngredientViews(
    BaseTestMixins.GuestLimitedGet,
    BaseTestMixins.GuestForbiddenPostPutDelete,
    BaseTestMixins.UserLimitedGet,
    BaseTestMixins.UserPermittedPost,
    BaseTestMixins.OwnerPermittedPutDelete,
    BaseTestMixins.StaffUnlimitedGet,
    BaseTestMixins.StaffPermittedPostPutDelete,
    APITestCase,
):
    fixtures = ["users.json", "tags.json", "culinary.json"]

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
        self.delete_id = 21

    def test_filter_by_name(self):
        IngredientFactory.create(name="different name")
        url = reverse("ingredients-list")
        response = self.client.get(url + "?name=different")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_min_value_constraint(self):
        token = TestUsers.get_staff_token()

        url = reverse(self.post_path_name)
        data = {"name": "carrot", "calories": -100}
        response = self.client.post(
            url, data=data, format="json", HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestMeasureViews(
    BaseTestMixins.GuestPermittedGet,
    BaseTestMixins.GuestForbiddenPostPutDelete,
    BaseTestMixins.UserPermittedGet,
    BaseTestMixins.UserForbiddenPostPutDelete,
    BaseTestMixins.StaffPermittedGet,
    BaseTestMixins.StaffPermittedPostPutDelete,
    APITestCase,
):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self):
        MeasureFactory.create(name="free to delete")

        self.factory_count = 4
        self.list_path_name = "measures-list"
        self.single_path_name = "measures-detail"

        self.post_path_name = "measures-list"
        self.default_post_data = {"name": "ounce"}

        self.put_path_name = "measures-detail"
        self.default_put_data = {"id": 2, "name": "new name"}

        self.delete_path_name = "measures-detail"
        self.delete_id = 4

        super().setUp()

    def test_filter_by_name(self):
        MeasureFactory.create(name="ounce")
        url = reverse("measures-list")
        response = self.client.get(url + "?name=ounce")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)


class TestFridgeViews(
    BaseTestMixins.GuestForbiddenGet,
    BaseTestMixins.GuestForbiddenPostPutDelete,
    BaseTestMixins.UserPermittedPost,
    BaseTestMixins.OwnerPermittedPutDelete,
    BaseTestMixins.StaffUnlimitedGet,
    BaseTestMixins.StaffPermittedPostPutDelete,
    APITestCase,
):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self) -> None:
        self.list_path_name = "shelfs-list"
        self.single_path_name = "shelfs-detail"
        self.post_path_name = "shelfs-list"
        self.delete_path_name = "shelfs-edit"
        self.put_path_name = "shelfs-edit"

        self.default_put_data = {"id": 3, "name": "update fridge name"}
        self.default_post_data = {"name": "everyday", "shelf": 2}

        self.staff_object_id = 1
        self.user1_object_id = 2
        self.user2_object_id = 3

    @override
    def test_get_list_by_staff(self):
        token = TestUsers.get_staff_token()

        url = reverse(self.list_path_name)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(len(response.json()), 3)
        self.assertEqual(len(response.json()[0]["shelf"]), 21)
        self.assertEqual(len(response.json()[1]["shelf"]), 5)
        self.assertEqual(len(response.json()[2]["shelf"]), 5)

    def test_get_list_by_user(self):
        url = reverse(self.list_path_name)

        token = TestUsers.get_user1_token()

        user1_response = self.client.get(url, HTTP_AUTHORIZATION=token)
        user1_data = user1_response.json()
        user1_shelf = user1_data[0]["shelf"]
        self.assertEqual(user1_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user1_data), 1)
        self.assertEqual(len(user1_shelf), 5)

        token = TestUsers.get_user2_token()

        user2_response = self.client.get(url, HTTP_AUTHORIZATION=token)
        user2_data = user2_response.json()
        user2_shelf = user2_data[0]["shelf"]
        self.assertEqual(user2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user2_data), 1)
        self.assertEqual(len(user2_shelf), 5)

        with self.assertRaises(AssertionError):
            self.assertCountEqual(user1_shelf, user2_shelf)

    def test_get_specific_by_user(self):
        token = TestUsers.get_user1_token()

        url = reverse(self.single_path_name, args=[self.user1_object_id])
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.user1_object_id)

        url = reverse(self.single_path_name, args=[self.staff_object_id])
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse(self.single_path_name, args=[self.user2_object_id])
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestConversionViews(
    BaseTestMixins.GuestPermittedGet,
    BaseTestMixins.UserPermittedGet,
    BaseTestMixins.GuestForbiddenPostPutDelete,
    BaseTestMixins.UserForbiddenPostPutDelete,
    BaseTestMixins.StaffPermittedGet,
    BaseTestMixins.StaffPermittedPostPutDelete,
    APITestCase,
):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self):
        self.single_path_name = "conversion-detail"
        self.list_path_name = "conversion-list"
        self.post_path_name = "conversion-list"
        self.put_path_name = "conversion-edit"
        self.delete_path_name = "conversion-edit"

        self.factory_count = 3
        self.default_post_data = {
            "standard_value": 205.14,
            "utensil_id": 3,
            "ingredient_id": 1,
        }
        self.default_put_data = {
            "id": 1,
            "standard_value": 20.5,
        }

    def test_unique_check(self):
        token = TestUsers.get_staff_token()

        url = reverse(self.post_path_name)
        data = {
            "standard_value": 100,
            "utensil_id": 1,
            "ingredient_id": 1,
        }
        response = self.client.post(
            url, data=data, format="json", HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override
    def test_get_specific_by_guest(self):
        url = reverse(self.single_path_name, args=[1, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 1)

    @override
    def test_get_non_existant_by_guest(self):
        url = reverse(self.single_path_name, args=[100, 100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override
    def test_get_specific_by_user(self):
        token = TestUsers.get_user1_token()

        url = reverse(self.single_path_name, args=[1, 1])
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 1)

    @override
    def test_get_specific_by_staff(self):
        token = TestUsers.get_staff_token()

        url = reverse(self.single_path_name, args=[1, 1])
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 1)


class TestRecipeViews(
    BaseTestMixins.GuestPermittedGet,
    BaseTestMixins.GuestForbiddenPostPutDelete,
    BaseTestMixins.UserPermittedGet,
    BaseTestMixins.OwnerPermittedPutDelete,
    BaseTestMixins.StaffPermittedGet,
    BaseTestMixins.StaffPermittedPostPutDelete,
    APITestCase,
):
    fixtures = ["users.json", "tags.json", "culinary.json"]

    def setUp(self):
        self.factory_count = 3

        self.single_path_name = "recipe-detail"
        self.list_path_name = "recipe-list"

        self.post_path_name = "recipe-list"
        self.default_post_data = {
            "title": "new recipe",
            "portions": 10,
            "total_time": "1:30:00",
            "instructions": "Recipe steps",
            "ingredients": [
                {
                    "amount": 10,
                    "ingredient": {"id": 1},
                    "measure": {"id": 1},
                },
                {
                    "amount": 100,
                    "ingredient": {"name": "custom ingredient 1", "user_id": 1},
                    "measure": {"id": 2},
                },
            ],
            "author": 1,
            "tags": [1, 5],
        }

        self.put_path_name = "recipe-edit"
        self.default_put_data = {"id": 2, "title": "new_title"}

        self.delete_path_name = "recipe-edit"

    def test_update_by_user(self):
        new_recipe = RecipeFactory.create(title="object to update", author_id=3)
        self.user2_object_id = new_recipe.id
        return super().test_update_by_user()

    def test_delete_by_user(self):
        new_recipe = RecipeFactory.create(title="object to update", author_id=3)
        self.user2_object_id = new_recipe.id
        return super().test_delete_by_user()

    def test_filter_by_title(self):
        RecipeFactory.create(title="title to search for")
        url = reverse(self.list_path_name)
        response = self.client.get(url + "?title=search")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_filter_by_ingredients(self):
        url = reverse(self.list_path_name)
        response = self.client.get(url + "?ingredients=1,2,3,4,5")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    # TODO more tests
    def test_filter_by_precise_ingredients(self):
        url = reverse(self.list_path_name)
        response = self.client.get(url + "?absentLimit=0&ingredients=1,2,3,4,5")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_filter_by_calories(self):
        RecipeFactory.create(title="recipe 100 cal", calories=100)
        RecipeFactory.create(title="recipe 105 cal", calories=105)

        url = reverse(self.list_path_name)
        response = self.client.get(url + "?caloriesAbove=100")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

        url = reverse(self.list_path_name)
        response = self.client.get(url + "?caloriesBelow=105")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_filter_by_user(self):
        # TODO - probubly filter by role
        RecipeFactory.create(title="user recipe", author_id=2)
        url = reverse(self.list_path_name)
        response = self.client.get(url + "?userId=2")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_compact_list(self):
        url = reverse(self.list_path_name)
        response = self.client.get(url + "?expanded=false")

        data = [
            {
                "id": 1,
                "title": "test recipe 0",
                "thumbnail": None,
                "author": "user 0",
                "tags": [
                    {"id": 1, "label": "tag 0", "category_name": "test tag category 0"},
                    {"id": 4, "label": "tag 3", "category_name": "test tag category 0"},
                    {"id": 7, "label": "tag 6", "category_name": "test tag category 1"},
                    {
                        "id": 10,
                        "label": "tag 9",
                        "category_name": "test tag category 1",
                    },
                    {
                        "id": 13,
                        "label": "tag 12",
                        "category_name": "test tag category 2",
                    },
                ],
            },
            {
                "id": 2,
                "title": "test recipe 1",
                "thumbnail": None,
                "author": "user 0",
                "tags": [
                    {"id": 2, "label": "tag 1", "category_name": "test tag category 0"},
                    {"id": 5, "label": "tag 4", "category_name": "test tag category 0"},
                    {"id": 8, "label": "tag 7", "category_name": "test tag category 1"},
                    {
                        "id": 11,
                        "label": "tag 10",
                        "category_name": "test tag category 2",
                    },
                    {
                        "id": 14,
                        "label": "tag 13",
                        "category_name": "test tag category 2",
                    },
                ],
            },
            {
                "id": 3,
                "title": "test recipe 2",
                "thumbnail": None,
                "author": "user 0",
                "tags": [
                    {"id": 3, "label": "tag 2", "category_name": "test tag category 0"},
                    {"id": 6, "label": "tag 5", "category_name": "test tag category 1"},
                    {"id": 9, "label": "tag 8", "category_name": "test tag category 1"},
                    {
                        "id": 12,
                        "label": "tag 11",
                        "category_name": "test tag category 2",
                    },
                    {
                        "id": 15,
                        "label": "tag 14",
                        "category_name": "test tag category 2",
                    },
                ],
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.json(), data)
        self.assertDictEqual(response.json()[0], data[0])

    def test_filter_by_shelf(self):
        token = TestUsers.get_user1_token()

        fridge = FridgeFactory.create(
            name="shelf with recipe 1 ingredients",
            user_id=2,
            shelf=Ingredient.objects.all().order_by("id")[:5],
        )
        url = reverse(self.list_path_name)
        response = self.client.get(
            url + f"?fridgeId={fridge.id}", HTTP_AUTHORIZATION=token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_filter_by_precise_shelf(self):
        token = TestUsers.get_user1_token()

        fridge = FridgeFactory.create(
            name="shelf with recipe 1 ingredients",
            user_id=2,
            shelf=Ingredient.objects.all().order_by("id")[:5],
        )
        url = reverse(self.list_path_name)
        response = self.client.get(
            url + f"?absentLimit=0&fridgeId={fridge.id}", HTTP_AUTHORIZATION=token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_filter_by_tags(self):
        RecipeFactory.create(title="new title", tags=list(Tag.objects.all()[:5]))
        url = reverse(self.list_path_name)
        response = self.client.get(url + "?tags=1,2,4")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
