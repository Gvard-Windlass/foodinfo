from django.contrib import admin

from tags.models import *


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("label", "category")
    search_fields = ("label", "category")


@admin.register(TagCategory)
class TagCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
