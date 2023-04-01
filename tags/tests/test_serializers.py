import json
from django.test import TestCase

from tags.models import Tag, TagCategory
from tags.serializers import TagCategorySerializer, TagSerializer


class TestTagSerializer(TestCase):
    fixtures = ["tags.json"]

    def test_serializer(self):
        tag = Tag.objects.first()
        serialized = TagSerializer(tag).data
        data = {
            "id": 1,
            "label": "tag 0",
            "category_id": 1,
            "category_name": "test tag category 0",
        }
        self.assertDictEqual(serialized, data)


class TestTagCategorySerializer(TestCase):
    fixtures = ["tags.json"]

    def test_serializer(self):
        category = TagCategory.objects.first()
        serialized = TagCategorySerializer(category).data
        data = {
            "id": 1,
            "name": "test tag category 0",
            "tags": [
                {"id": 1, "label": "tag 0"},
                {"id": 2, "label": "tag 1"},
                {"id": 3, "label": "tag 2"},
                {"id": 4, "label": "tag 3"},
                {"id": 5, "label": "tag 4"},
            ],
        }
        self.assertEqual(json.dumps(serialized), json.dumps(data))
