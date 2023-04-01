from django.urls import include, path
from rest_framework.routers import DefaultRouter
from tags.views import *

router = DefaultRouter(trailing_slash=False)
router.register(r"tags", TagViewSet, "tags")
router.register(r"tag-categories", TagCategoryViewsSet, "tag-categories")

urlpatterns = [
    path("", include(router.urls)),
]
