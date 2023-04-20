from django.contrib import admin

from culinary.models import *


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "category", "calories")
    search_fields = ("name", "user")
    list_filter = ("category",)


@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user")


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(UtensilConversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ("utensil", "ingredient", "standard_value")
    search_fields = ("utensil", "ingredient")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "portions", "calories", "total_time")
    search_fields = ("title", "author")
