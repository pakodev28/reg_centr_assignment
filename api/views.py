from rest_framework import viewsets, status
from rest_framework.response import Response
from recipes.models import Recipe, RecipeIngredient
from .serializers import (
    RecipeGetDeleteSerializer,
    RecipeCreateUpdateSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет реализует CRUD для рецептов.
    """

    queryset = Recipe.objects.all()

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
        если они больше не используются.
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
