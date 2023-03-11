from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r"ingredients", views.IngredientViewSet, "ingredients")
router.register(r"measures", views.MeasureViewSet, "measures")

urlpatterns = [
    path("", include(router.urls)),
]
