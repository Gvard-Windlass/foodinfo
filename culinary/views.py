from django.db.models import Q
from rest_framework import viewsets, permissions, mixins, generics
from .serializers import IngredientSerializer, MeasureSerializer
from .models import Ingredient, Measure
from .permissions import HasAccessOrReadOnly, HasAccess


class IngredientEdit(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientSerializer
    permission_classes = [HasAccessOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class IngredientDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientSerializer
    permission_classes = [HasAccess]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class IngredientList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    serializer_class = IngredientSerializer
    permission_classes = [HasAccessOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)

    def get_queryset(self):
        filters = []
        name = self.request.query_params.get("name")
        if name:
            filters.append(Q(name__contains=name))

        user = self.request.user
        if not user.is_staff:
            has_access = Q(user_id=user.id) | Q(user__is_staff=True)
            filters.append(has_access)

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
