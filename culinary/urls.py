from django.urls import include, path
from rest_framework.routers import DefaultRouter
from culinary.views import *

router = DefaultRouter(trailing_slash=False)
router.register(r"measures", measure_views.MeasureViewSet, "measures")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "ingredients/",
        ingredient_views.IngredientList.as_view(),
        name="ingredients-list",
    ),
    path(
        "ingredients/<str:name>/",
        ingredient_views.IngredientList.as_view(),
        name="ingredients-list",
    ),
    path(
        "ingredients/<int:pk>",
        ingredient_views.IngredientDetail.as_view(),
        name="ingredients-detail",
    ),
    path(
        "ingredients/edit/<int:pk>",
        ingredient_views.IngredientEdit.as_view(),
        name="ingredients-edit",
    ),
    path("fridge/", fridge_views.FridgeList.as_view(), name="shelfs-list"),
    path("fridge/<int:pk>", fridge_views.FridgeDetail.as_view(), name="shelfs-detail"),
    path(
        "fridge/edit/<int:pk>",
        fridge_views.FridgeEdit.as_view(),
        name="shelfs-edit",
    ),
    path(
        "conversion/",
        conversion_views.ConversionList.as_view(),
        name="conversion-list",
    ),
    path(
        "conversion/<int:utensil_pk>/<int:ingredient_pk>",
        conversion_views.ConversionDetail.as_view(),
        name="conversion-detail",
    ),
    path(
        "conversion/edit/<int:pk>",
        conversion_views.ConversionEdit.as_view(),
        name="conversion-edit",
    ),
    path("recipes/", recipe_views.RecipeList.as_view(), name="recipe-list"),
    path("recipes/<int:pk>", recipe_views.RecipeDetail.as_view(), name="recipe-detail"),
    path(
        "recipes/edit/<int:pk>", recipe_views.RecipeEdit.as_view(), name="recipe-edit"
    ),
]
