from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, mixins, generics, status
from rest_framework.response import Response
from culinary.serializers import ConversionSerializer
from culinary.models import UtensilConversion
from culinary.permissions import IsStaffOrReadOnly


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
