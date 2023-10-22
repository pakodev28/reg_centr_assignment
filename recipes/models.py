from django.db import models


class Recipe(models.Model):
    """
    Модель для рецепта.
    """

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        "Ingredient",
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name="Ингредиенты",
    )

    @property
    def total_cooking_time(self):
        """
        Вычисляет и возвращает общее время приготовления
        рецепта на основе времени каждого шага.
        """
        total_time = 0
        for step in self.cooking_steps.all():
            total_time += step.time_in_minutes
        return total_time

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель для ингредиента в рецепте.
    """

    name = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Явная связывающая таблица между рецептами и ингредиентами
    с дополнительными полями quantity и unit_of_measurement.
    """

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент"
    )
    quantity = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Количество"
    )
    unit_of_measurement = models.CharField(
        max_length=25, verbose_name="Единицы измерения"
    )

    def __str__(self):
        return f"{self.quantity} {self.unit_of_measurement} of {self.ingredient} in {self.recipe}"


class CookingStep(models.Model):
    """
    Модель для шага приготовления в рецепте.
    """

    description = models.TextField(verbose_name="Описание")
    time_in_minutes = models.PositiveIntegerField(
        verbose_name="Время выполнения (в минутах)"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="cooking_steps",
        verbose_name="Рецепт",
    )

    def __str__(self):
        return f"Шаг приготовления: {self.description}"
