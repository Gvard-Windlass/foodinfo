from django.db.models import Q
from rest_framework import viewsets
from culinary.permissions import IsStaffOrReadOnly
from tags.models import Tag, TagCategory
from tags.serializers import TagSerializer, TagCategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("label")
    serializer_class = TagSerializer
    permission_classes = [IsStaffOrReadOnly]


class TagCategoryViewsSet(viewsets.ModelViewSet):
    queryset = TagCategory.objects.all().order_by("name")
    serializer_class = TagCategorySerializer
    permission_classes = [IsStaffOrReadOnly]
