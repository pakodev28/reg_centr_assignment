from django.contrib import admin
from .models import Recipe, Ingredient, CookingStep, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class CookingStepInline(admin.TabularInline):
    model = CookingStep
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "get_total_cooking_time")
    list_filter = ("cooking_steps__time_in_minutes",)
    search_fields = ("name",)
    inlines = [RecipeIngredientInline, CookingStepInline]

    def get_total_cooking_time(self, obj):
        return obj.total_cooking_time

    get_total_cooking_time.short_description = "Total Cooking Time"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(CookingStep)
class CookingStepAdmin(admin.ModelAdmin):
    list_display = ("recipe", "description", "time_in_minutes")
    list_filter = ("time_in_minutes",)
    search_fields = ("description",)
