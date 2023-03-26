from django.db.models import Q
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, generics, status
from rest_framework.response import Response
from .serializers import *
from .models import *
from .permissions import (
    HasAccessOrReadOnly,
    HasAccess,
    IsStaffOrReadOnly,
    IsOwnerOrStaff,
)


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
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        filters = []
        name = self.request.query_params.get("name")
        if name:
            filters.append(Q(name__contains=name))
        return Measure.objects.filter(*filters).order_by("name")


class FridgeList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    serializer_class = FridgeSerializer
    permission_classes = [IsOwnerOrStaff]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return Fridge.objects.filter(user_id=user.id)

        return Fridge.objects.all()


class FridgeDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Fridge.objects.all()
    serializer_class = FridgeSerializer
    permission_classes = [IsOwnerOrStaff]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class FridgeEdit(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = Fridge.objects.all()
    serializer_class = FridgeSerializer
    permission_classes = [IsOwnerOrStaff]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ConversionDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = UtensilConversion.objects.all()
    serializer_class = ConversionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        ingredient_id = self.kwargs["ingredient_pk"]
        utensil_id = self.kwargs["utensil_pk"]

        obj = get_object_or_404(
            UtensilConversion, utensil_id=utensil_id, ingredient_id=ingredient_id
        )
        self.check_object_permissions(self.request, obj)

        return obj


class ConversionList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = UtensilConversion.objects.all()
    serializer_class = ConversionSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except IntegrityError:
            content = {
                "error": "Conversion already exist. Ingredient/Utensil combination must be unique"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class ConversionEdit(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = UtensilConversion.objects.all()
    serializer_class = ConversionSerializer
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
