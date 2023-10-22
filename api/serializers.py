from rest_framework import serializers
from recipes.models import Recipe, Ingredient, CookingStep


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class CookingStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingStep
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    cooking_steps = CookingStepSerializer(many=True, read_only=True)

    total_cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = "__all__"
