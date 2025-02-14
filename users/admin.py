from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "username", "avatar", "is_staff"]
    search_fields = ["email", "username"]
    list_filter = ["is_staff"]  # Поле для фильтрации
    group_id = ["groups"]