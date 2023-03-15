from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r"measures", views.MeasureViewSet, "measures")

urlpatterns = [
    path("", include(router.urls)),
    path("ingredients/", views.IngredientList.as_view(), name="ingredients-list"),
    path(
        "ingredients/<str:name>/",
        views.IngredientList.as_view(),
        name="ingredients-list",
    ),
    path(
        "ingredients/<int:pk>",
        views.IngredientDetail.as_view(),
        name="ingredients-detail",
    ),
    path(
        "ingredients/edit/<int:pk>",
        views.IngredientEdit.as_view(),
        name="ingredients-edit",
    ),
    path("fridge/", views.FridgeList.as_view(), name="shelfs-list"),
    path("fridge/<int:pk>", views.FridgeDetail.as_view(), name="shelfs-detail"),
]
