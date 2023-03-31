from django.test import TestCase
from tags.models import Tag, TagCategory

from test.factories import TagCategoryFactory, TagFactory


class TestTagCategoryModel(TestCase):
    def test_create_tag_category(self):
        tag_category = TagCategoryFactory.create()
        self.assertIsInstance(tag_category, TagCategory)


class TestTagModel(TestCase):
    def test_create_tag(self):
        tag = TagFactory.create()
        self.assertIsInstance(tag, Tag)
