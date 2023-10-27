from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from recipes.models import Recipe, RecipeIngredient

from .serializers import (RecipeCreateUpdateSerializer,
                          RecipeGetDeleteSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет реализует CRUD для рецептов.
    Сортировку по total_cooking_time.
    Фильтрацию по total_cooking_time и ingredients__name.
    """

    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["total_cooking_time", "ingredients__name"]
    ordering_fields = ["total_cooking_time"]

    def get_serializer_class(self):
        """
        Определяет класс сериализатора в зависимости от действия.
        """
        if self.action in ("create", "update", "partial_update"):
            return RecipeCreateUpdateSerializer
        return RecipeGetDeleteSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет рецепт и связанные ингредиенты,
        если они не используются с другими рецептами.
        """
        instance = self.get_object()

        ingredients = instance.ingredients.all()

        for ingredient in ingredients:
            has_other_references = (
                RecipeIngredient.objects.filter(ingredient=ingredient)
                .exclude(recipe=instance)
                .exists()
            )

            if not has_other_references:
                ingredient.delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
