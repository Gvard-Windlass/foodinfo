from django.db.models import Q
from rest_framework import viewsets
from culinary.permissions import IsStaffOrReadOnly
from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("label")
    serializer_class = TagSerializer
    permission_classes = [IsStaffOrReadOnly]
