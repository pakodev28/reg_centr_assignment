from django.db.models import F
from rest_framework import serializers

from recipes.models import CookingStep, Ingredient, Recipe, RecipeIngredient


class RecipeIngredientGetDeleteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения ингредиентов в рецепте.
    """

    name = serializers.CharField(source="ingredient.name")

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "quantity", "unit_of_measurement")


class CookingStepGetDeleteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения шагов приготовления рецепта.
    """

    class Meta:
        model = CookingStep
        fields = "__all__"


class RecipeGetDeleteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения и удаления рецепта.
    """

    ingredients = RecipeIngredientGetDeleteSerializer(
        many=True, source="recipeingredient_set"
    )
    cooking_steps = CookingStepGetDeleteSerializer(many=True)
    total_cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeIngredientCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления ингредиентов.
    """

    name = serializers.CharField()
    quantity = serializers.FloatField()
    unit_of_measurement = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = ("name", "unit_of_measurement", "quantity")


class CookingStepCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления шагов приготовления.
    """

    class Meta:
        model = CookingStep
        fields = ("description", "time_in_minutes")


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления рецепта.
    """

    ingredients = RecipeIngredientCreateUpdateSerializer(many=True)
    cooking_steps = CookingStepCreateUpdateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ("name", "description", "ingredients", "cooking_steps")

    def validate_ingredients(self, data):
        """
        Проверяет данные ингредиентов и их количество.
        """
        ingredients = self.initial_data.get("ingredients")
        ingredients_set = set()
        if not ingredients:
            raise serializers.ValidationError(
                "Вы не добавили не одного ингредиента"
            )
        for ingredient in ingredients:
            if float(ingredient["quantity"]) <= 0:
                raise serializers.ValidationError(
                    "Колличество ингредиентов должно быть больше нуля"
                )
            id = ingredient.get("id")
            ingredients_set.add(id)
        return data

    def validate_cooking_steps(self, data):
        """
        Проверяет данные шагов приготовления и их время выполнения.
        """
        cooking_steps = self.initial_data.get("cooking_steps")
        if not cooking_steps:
            raise serializers.ValidationError(
                "Вы не добавили ни одного шага приготовления"
            )

        for step in cooking_steps:
            if int(step["time_in_minutes"]) <= 0:
                raise serializers.ValidationError(
                    "Время выполнения шага должно быть больше нуля"
                )

        return data

    def create(self, validated_data):
        """
        Создает новый рецепт, ингредиенты и шаги приготовления.
        """
        ingredients_data = validated_data.pop("ingredients")
        cooking_steps_data = validated_data.pop("cooking_steps")

        recipe = Recipe.objects.create(**validated_data)

        for step_data in cooking_steps_data:
            CookingStep.objects.create(recipe=recipe, **step_data)

        for ingredient_data in ingredients_data:
            ingredient_name = ingredient_data["name"]

            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_name
            )
            quantity = ingredient_data["quantity"]
            unit_of_measurement = ingredient_data["unit_of_measurement"]
            if RecipeIngredient.objects.filter(
                recipe=recipe, ingredient=ingredient
            ).exists():
                quantity += F("quantity")
                unit_of_measurement += F("unit_of_measurement")
            RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient,
                defaults={
                    "quantity": quantity,
                    "unit_of_measurement": unit_of_measurement,
                },
            )
        return recipe

    def update(self, instance, validated_data):
        """
        Обновляет рецепт, ингредиенты и шаги приготовления.
        """
        cooking_steps_data = validated_data.pop("cooking_steps", [])
        ingredients_data = validated_data.pop("ingredients", [])

        if "cooking_steps" in self.initial_data:
            CookingStep.objects.filter(recipe=instance).delete()
            for step_data in cooking_steps_data:
                CookingStep.objects.create(recipe=instance, **step_data)

        if "ingredients" in self.initial_data:
            RecipeIngredient.objects.filter(recipe=instance).delete()
            for ingredient_data in ingredients_data:
                ingredient_name = ingredient_data.get("name")
                if ingredient_name:
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=ingredient_name
                    )
                    quantity = ingredient_data.get("quantity")
                    unit_of_measurement = ingredient_data.get(
                        "unit_of_measurement"
                    )
                    RecipeIngredient.objects.create(
                        recipe=instance,
                        ingredient=ingredient,
                        quantity=quantity,
                        unit_of_measurement=unit_of_measurement,
                    )

        super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        data = RecipeGetDeleteSerializer(
            instance, context={"request": self.context.get("request")}
        ).data
        return data
