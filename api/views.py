from rest_framework import viewsets, filters
from recipes.models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["total_cooking_time"]
