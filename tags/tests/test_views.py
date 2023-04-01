from test.base_test import BaseTestMixins
from rest_framework.test import APITestCase


class TestTagViews(
    BaseTestMixins.GuestPermittedGet,
    BaseTestMixins.GuestForbiddenPostPutDelete,
    BaseTestMixins.UserPermittedGet,
    BaseTestMixins.UserForbiddenPostPutDelete,
    BaseTestMixins.StaffPermittedGet,
    BaseTestMixins.StaffPermittedPostPutDelete,
    APITestCase,
):
    fixtures = ["tags.json", "users.json"]

    def setUp(self):
        self.factory_count = 15
        self.list_path_name = "tags-list"
        self.single_path_name = "tags-detail"

        self.post_path_name = "tags-list"
        self.default_post_data = {"label": "new tag", "category_id": 1}

        self.put_path_name = "tags-detail"
        self.default_put_data = {"id": 2, "label": "new label"}

        self.delete_path_name = "tags-detail"
        self.delete_id = 1

        super().setUp()


class TestTagCategoryViews(
    BaseTestMixins.GuestPermittedGet,
    BaseTestMixins.GuestForbiddenPostPutDelete,
    BaseTestMixins.UserPermittedGet,
    BaseTestMixins.UserForbiddenPostPutDelete,
    BaseTestMixins.StaffPermittedGet,
    BaseTestMixins.StaffPermittedPostPutDelete,
    APITestCase,
):
    fixtures = ["tags.json", "users.json"]

    def setUp(self):
        self.factory_count = 3
        self.list_path_name = "tag-categories-list"
        self.single_path_name = "tag-categories-detail"

        self.post_path_name = "tag-categories-list"
        self.default_post_data = {"name": "new category"}

        self.put_path_name = "tag-categories-detail"
        self.default_put_data = {"id": 2, "name": "new name"}

        self.delete_path_name = "tag-categories-detail"
        self.delete_id = 1

        super().setUp()
