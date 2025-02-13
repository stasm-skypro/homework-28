"""
Контроллеры, определённые внутри приложения catalog.
"""

import logging

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from dotenv import load_dotenv

from catalog.forms import CategoryForm, ProductForm, ProductModeratorForm
from catalog.mixins import OwnerRequiredMixin  # Импортируем кастомный миксин для проверки владельца
from catalog.models import Category, Product

load_dotenv()

logger = logging.getLogger("catalog")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("catalog/logs/reports.log", "a", "utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s"))
logger.addHandler(handler)


# ---- Определяем набор CRUD-операций для модели Category ----
#
class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Определяет отображение добавления категории."""

    model = Category
    context_object_name = "category"
    form_class = CategoryForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """Дополнительная обработка перед сохранением формы."""
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Категория продукта '%s' успешно создана." % self.object.name)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка в случае неверной формы."""
        logger.warning("Ошибка при создании категории продукта: %s" % form.errors)
        return super().form_invalid(form)


# ---- Определяем набор CRUD-операций для модели Product ----
#
class ProductListView(ListView):
    """Определяет отображение страницы со списком продуктов."""

    model = Product
    context_object_name = "product_list"

    def get_context_data(self, **kwargs):
        """Обработка контекста для передачи в шаблон проверки модератора продукта."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["is_product_moderator"] = user.groups.filter(name="Product Moderators").exists()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Определяет отображение детализации (характеристик) продукта."""

    model = Product
    context_object_name = "product"

    def get_object(self, queryset=None):
        """Проверяет количество просмотров статьи и отправляет уведомление администратору."""
        self.object = super().get_object(queryset)
        self.object.views_counter += 1

        # Отправлять уведомление администратору, если количество просмотров превысило 100
        if self.object.views_counter >= 100:
            logger.info("Количество просмотров превысило %s." % self.object.views_counter)
            self.send_info_email("stasm226@gmail.com")
            logger.info("Информационное сообщение отправлено на адрес %s." % "stasm226@gmail.com")

        self.object.save()

        return self.object

    def send_info_email(self, user_email):
        """Отправляет сообщение на email пользователя при успешной регистрации."""
        subject = "Новое достижение!"
        message = "Количество просмотров превысило 100: %s" % self.object.views
        from_email = "stasm226@gmail.com"
        recipients = ["stasm226@gmail.com"]
        send_mail(subject, message, from_email, recipients)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Определяет отображение добавления продукта."""

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """Дополнительная обработка перед сохранением формы."""
        self.object = form.save()  # Сохраняем объект формы в базу
        form.instance.owner = self.request.user  # Назначаем владельца
        logger.info("Продукт '%s' успешно создан. Владелец продукта %s." % (self.object.product, self.request.user))
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка в случае неверной формы."""
        logger.warning("Ошибка при создании продукта: %s" % form.errors)
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, OwnerRequiredMixin,  UpdateView):
    """Определяет отображение обновления продукта."""

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """Дополнительная обработка перед сохранением формы."""
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Продукт '%s' успешно обновлён." % self.object.product)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка в случае неверной формы."""
        logger.warning("Ошибка при обновлении продукта: %s" % form.errors)
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        """Определяем, какую форму использовать и блокируем поле published при необходимости."""

        if form_class is None:
            form_class = ProductForm  # Всегда используем стандартную форму

        form = super().get_form(form_class)
        if not self.request.user.has_perm("catalog.can_unpublish_product"):
            form.fields["publicated"].disabled = True
        else:
            form.fields["product"].disabled = True
            form.fields["category"].disabled = True
            form.fields["price"].disabled = True
            form.fields["description"].disabled = True
            form.fields["image"].disabled = True
            form.fields["created_at"].disabled = True
            form.fields["changed_at"].disabled = True
            form.fields["views_counter"].disabled = True
            form.fields["publicated"].disabled = False
        return form


class ProductDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    """Определяет отображение удаления продукта."""

    model = Product
    form_class = ProductForm
    context_object_name = "product"
    success_url = reverse_lazy("catalog:product_list")

    def post(self, request, *args, **kwargs):
        """Переопределение метода POST для вызова delete."""
        logger.info("Удаление продукта через POST-запрос.")
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Переопределение метода delete для логирования."""
        product = self.get_object()
        logger.info("Продукт '%s' успешно удалён." % product.product)
        return super().delete(request, *args, **kwargs)


