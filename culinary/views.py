from rest_framework import viewsets
from rest_framework import permissions
from .serializers import IngredientSerializer
from .models import Ingredient


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        name = self.request.query_params.get("name")
        if name:
            return Ingredient.objects.filter(name__contains=name)
        return Ingredient.objects.all()
