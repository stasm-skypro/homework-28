from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    """Класс для создания кастомных команд для операций с базой данных."""

    help = "Добавление тестовых продуктов в таблицу catalog_product."

    def handle(self, *args, **kwargs):
        """Создаёт кастомную команду."""

        category, _ = Category.objects.get_or_create(name="Продукты", description="Товары первой необходимости")

        # Перед добавлением новых записей удалим существующие записи из таблицы catalog_product.
        Product.objects.all().delete()

        # Как альтернативный вариант, можно заранее создать фикстуру с товарами и использовать команду loaddata.
        new_products = [
            {
                "product": "Моцарелла",
                "description": "Сыр мягкий",
                "category": category,
                "price": 800.0,
                "created_at": "2024-12-24",
                "changed_at": "2024-12-24",
            },
            {
                "product": "Масло сливочное Домашнее",
                "description": "Натуральное сливочное масло 82.5%",
                "category": category,
                "price": 1200.0,
                "created_at": "2024-12-24",
                "changed_at": "2024-12-24",
            },
            {
                "product": "Творог 9% Простоквашино",
                "description": "Творог натуральный жирность 9%",
                "category": category,
                "price": 1000.0,
                "created_at": "2024-12-24",
                "changed_at": "2024-12-24",
            },
            {
                "product": "Основа для пиццы",
                "description": "Основа для пиццы 30 см из дрожжевого теста",
                "category": category,
                "price": 300.0,
                "created_at": "2024-12-24",
                "changed_at": "2024-12-24",
            },
            {
                "product": "Масло Вегетта",
                "description": "Масло растительное оливковое натуральное",
                "category": category,
                "price": 1200.0,
                "created_at": "2024-12-24",
                "changed_at": "2024-12-24",
            },
        ]

        for new_product in new_products:
            product, created = Product.objects.get_or_create(**new_product)
            if created:
                self.stdout.write(self.style.SUCCESS("Новый товар %s успешно добавлен." % product))
            else:
                self.stdout.write(self.style.WARNING("Товар уже %s существует." % product))
