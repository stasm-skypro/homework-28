from django.db import models


class Category(models.Model):
    """Модель таблицы Категории [товаров]."""

    name = models.CharField(max_length=100, verbose_name="Наименование категории")
    description = models.TextField(verbose_name="Описание")

    def __repl__(self) -> str:
        """Строковое представление для разработчиков."""
        return "%s %s %s" % (self.__class__, self.name, self.description)

    def __str__(self) -> str:
        """Общее строковое представление."""
        return "%s" % self.name

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"
        ordering = [
            "name",
        ]


class Product(models.Model):
    """Модель таблицы Товар."""

    product = models.CharField(max_length=150, verbose_name="Наименование товара")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Изображение", blank=True, null=True, upload_to="catalog/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="goods")
    price = models.FloatField(null=False, default=1.0, verbose_name="Цена товара")
    created_at = models.DateField(verbose_name="Дата производства")
    changed_at = models.DateField(verbose_name="Дата последнего изменения")
    views_counter = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __repl__(self) -> str:
        """Строковое представление для разработчиков."""
        return "%s %s %s %s %s" % (self.__class__, self.product, self.category, self.price, self.created_at)

    def __str__(self) -> str:
        """Общее строковое представление."""
        return "%s %s" % (self.product, self.price)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = [
            "product",
            "price",
        ]


class Contact(models.Model):
    """Класс для создания модели хранения контактных данных."""

    first_name = models.CharField(max_length=35, blank=False, null=False, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=False, null=False, verbose_name="Фамилия")
    phone = models.CharField(max_length=15, blank=False, null=False, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")

    def __repr__(self) -> str:
        """Строковое представление для разработчиков."""
        return "%s %s %s %s %s" % (self.__class__, self.first_name, self.last_name, self.phone, self.message)

    def __str__(self) -> str:
        """Общее строковое представление."""
        return "%s %s %s" % (self.first_name, self.last_name, self.phone)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["first_name", "last_name"]
