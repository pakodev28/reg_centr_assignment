from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet

app_name = "api"

router = DefaultRouter()
router.register("recipes", RecipeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
