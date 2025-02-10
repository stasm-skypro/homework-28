from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс для настройки отображений моделей в админ панели."""

    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс для настройки отображения моделей в админ панели."""

    list_display = ["id", "product", "price", "category"]
    list_filter = ["category"]
    search_fields = ["name", "description"]
