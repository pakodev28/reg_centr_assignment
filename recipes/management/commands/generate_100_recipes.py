import random

from django.core.management.base import BaseCommand

from recipes.models import CookingStep, Ingredient, Recipe, RecipeIngredient


class Command(BaseCommand):
    help = "Generate 100 recipes in the database"

    def handle(self, *args, **options):
        for i in range(100):
            recipe = Recipe.objects.create(
                name=f"Рецепт {i}",
                description=f"Описание для рецепта {i}",
            )

            for i in range(random.randint(3, 10)):
                ingredient, created = Ingredient.objects.get_or_create(
                    name=f"Ингредиент {i}"
                )

                quantity = round(random.uniform(0.1, 2.0), 2)
                unit_of_measurement = random.choice(
                    ["г", "кг", "мл", "л", "ч.л."]
                )

                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity,
                    unit_of_measurement=unit_of_measurement,
                )

            for i in range(random.randint(1, 5)):
                description = f"Шаг {i}: Как приготовить что-то"
                time_in_minutes = random.randint(5, 60)
                CookingStep.objects.create(
                    description=description,
                    time_in_minutes=time_in_minutes,
                    recipe=recipe,
                )

        self.stdout.write(
            self.style.SUCCESS("Successfully generated 100 recipes")
        )
