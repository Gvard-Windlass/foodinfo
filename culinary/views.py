from django.db.models import Q
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import IngredientSerializer, MeasureSerializer
from .models import Ingredient, Measure


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        filters = []
        name = self.request.query_params.get("name")
        if name:
            filters.append(Q(name__contains=name))
        return Ingredient.objects.filter(*filters).order_by("name")


class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all().order_by("name")
    serializer_class = MeasureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        filters = []
        name = self.request.query_params.get("name")
        if name:
            filters.append(Q(name__contains=name))
        return Measure.objects.filter(*filters).order_by("name")
