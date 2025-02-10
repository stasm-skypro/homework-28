"""
Формы для ввода данных.
"""

import os

from blog.mixins import StyledFormMixin
from django import forms
from django.core.exceptions import ValidationError
from dotenv import load_dotenv

from catalog.models import Category, Product

load_dotenv()


class CategoryForm(StyledFormMixin, forms.ModelForm):
    """Форма для ввода данных о категории товаров."""

    class Meta:
        model = Category
        fields = "__all__"
        labels = {
            "name": "Наименование категории",
            "description": "Описание",
        }

    def clean(self):
        forbidden_words = os.getenv("FORBIDDEN_WORDS").split(",")
        cleaned_data = super().clean()

        cleaned_name = cleaned_data.get("name").split()
        for word in cleaned_name:
            if word.lower() in forbidden_words:
                self.add_error(
                    "name",
                    "Поле с наименованием категории содержит запрещённое слово %s." % word,
                )
                break

        cleaned_description = cleaned_data.get("description").split()
        for word in cleaned_description:
            if word.lower() in forbidden_words:
                self.add_error(
                    "description",
                    "Поле с описанием категории содержит запрещённое слово %s." % word,
                )
                break

        return cleaned_data


class ProductForm(StyledFormMixin, forms.ModelForm):
    """
    Форма для ввода данных о продукте.
    """

    class Meta:
        model = Product
        fields = "__all__"
        labels = {
            "name": "Название",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена",
            "created_at": "Дата производства",
            "changed_at": "Дата последнего изменения",
            "views_counter": "Количество просмотров",
        }

    def clean_price(self):
        """Проверяет, что введена неотрицательная цена."""
        cleaned_price = self.cleaned_data.get("price")
        if cleaned_price < 0:
            raise ValidationError("Вы указали недопустимое значение цены! Цена не может быть отрицательной!")

        return cleaned_price

    def clean_image_format(self):
        """
        Проверяет, что загружаемое изображение продукта в формате .jpg или .png.
        """
        image = self.cleaned_data.get("image")
        if image:
            valid_extensions = [".jpg", ".jpeg", ".png"]
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Допустимые форматы изображений: .jpg, .jpeg, .png.")

        return image

    def clean_image_size(self):
        """
        Проверяет, что загружаемый файл изображения не превышает 5 МБ.
        """
        image = self.cleaned_data.get("image")
        max_size = 5 * 1024 * 1024  # 5 MБ

        if image and image.size > max_size:
            raise ValidationError("Размер изображения не должен превышать 5 МБ.")

        return image

    def clean(self):
        """Проверяет, что указанные поля формы не содержат запрещённые слова."""
        forbidden_words = os.getenv("FORBIDDEN_WORDS").split(",")
        cleaned_data = super().clean()

        cleaned_product = cleaned_data.get("product").split()
        for word in cleaned_product:
            if word.lower() in forbidden_words:
                self.add_error(
                    "product",
                    "Поле с наименованием продукта содержит запрещённое слово %s." % word,
                )
                break

        cleaned_description = cleaned_data.get("description").split()
        for word in cleaned_description:
            if word.lower() in forbidden_words:
                self.add_error(
                    "description",
                    "Поле с описанием продукта содержит запрещённое слово %s." % word,
                )
                break

        return cleaned_data
