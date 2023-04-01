from django.urls import include, path
from rest_framework.routers import DefaultRouter
from tags.views import *

router = DefaultRouter(trailing_slash=False)
router.register(r"tags", TagViewSet, "tags")

urlpatterns = [
    path("", include(router.urls)),
]
