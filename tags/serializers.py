from django.db.models import F
from rest_framework import serializers

from tags.models import Tag, TagCategory
from foodinfo.utils import DynamicFieldsModelSerializer


class TagSerializer(DynamicFieldsModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TagCategory.objects.all().values_list("id", flat=True), required=False
    )
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Tag
        fields = ["id", "label", "category_id", "category_name"]


class TagCategorySerializer(DynamicFieldsModelSerializer):
    tags = TagSerializer(many=True, source="tag_set", fields=["id", "label"])

    class Meta:
        model = TagCategory
        fields = ["id", "name", "tags"]
