from django.db.models import Q, Count, F
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework import mixins, generics, permissions
from culinary.serializers import RecipeCreateSerializer, RecipeSerializer
from culinary.models import Fridge, Recipe
from culinary.permissions import IsOwnerOrStaff


class RecipeEdit(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = Recipe.objects.all().order_by("title")
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrStaff]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RecipeDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Recipe.objects.all().order_by("title")
    serializer_class = RecipeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RecipeList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RecipeCreateSerializer
        return RecipeSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()

        if serializer_class == RecipeSerializer:
            fields = None
            expanded = self.request.query_params.get("expanded")
            if expanded == "false":
                fields = ["id", "title", "thumbnail", "author", "tags"]

            kwargs["fields"] = fields

        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        filters = []

        calories_above = self.request.query_params.get("caloriesAbove")
        calories_below = self.request.query_params.get("caloriesBelow")

        if calories_above and calories_below and calories_below > calories_above:
            raise ParseError()

        title = self.request.query_params.get("title")
        ingredients = self.request.query_params.get("ingredients")
        user = self.request.query_params.get("userId")
        fridgeId = self.request.query_params.get("fridgeId")
        fridge_ingredients = None
        absent_limit = self.request.query_params.get("absentLimit")
        tags = self.request.query_params.get("tags")

        if title:
            filters.append(Q(title__contains=title))
        if ingredients and not absent_limit:
            filters.append(
                Q(ingredientusage__ingredient__pk__in=ingredients.split(","))
            )
        if calories_above:
            filters.append(Q(calories__gte=calories_above))
        if calories_below:
            filters.append(Q(calories__lte=calories_below))
        if user:
            filters.append(Q(author__id=user))
        if fridgeId:
            fridge = get_object_or_404(Fridge, id=fridgeId)

            if fridge.user.id != self.request.user.id:
                raise PermissionDenied()

            fridge_ingredients = fridge.shelf.all().values_list("id", flat=True)
            if not absent_limit:
                filters.append(
                    Q(ingredientusage__ingredient__pk__in=fridge_ingredients)
                )
        if tags:
            filters.append(Q(tags__pk__in=tags.split(",")))

        if absent_limit:
            if ingredients:
                include = ingredients.split(",")
            elif fridge_ingredients:
                include = fridge_ingredients
            else:
                raise ParseError()

            filters.append(Q(absent__lte=absent_limit))

            return Recipe.objects.annotate(
                all=Count("ingredientusage"),
                present=Count(
                    "ingredientusage",
                    filter=Q(ingredientusage__ingredient__pk__in=include),
                ),
                absent=F("all") - F("present"),
            ).filter(*filters)

        return Recipe.objects.filter(*filters).distinct().order_by("title")
