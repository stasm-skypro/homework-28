"""
Контроллеры, определённые внутри приложения users.
"""

import logging
from django.contrib.auth import logout, login
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import CustomUser


logger = logging.getLogger("catalog")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("users/logs/reports.log", "a", "utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s"))
logger.addHandler(handler)


class UserRegisterView(CreateView):
    """Класс создания представления для регистрации пользователя."""

    model = CustomUser
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """Проверяет статус регистрации пользователя и отправляет уведомление администратору."""
        user = form.save()
        login(self.request, user)
        logger.info("Пользователь '%s' успешно зарегистрирован." % self.object.user_name)
        self.send_welcome_email(user.email)
        logger.info("Приветственное письмо отправлено.")
        return super().form_valid(form)

    # Отправка сообщения на email пользователя при успешной регистрации
    def send_welcome_email(self, user_email):
        """Отправляет сообщение на email пользователя при успешной регистрации."""
        subject = "Добро пожаловать на сайт!"
        message = "Спасибо за регистрацию! Мы рады видеть вас среди нас."
        from_email = "stasm226@gmail.com"
        recipients = [user_email]
        send_mail(subject, message, from_email, recipients)

    def form_invalid(self, form):
        """Обработка в случае неверной формы."""
        logger.warning("Ошибка при регистрации пользователя: %s" % form.errors)
        return super().form_invalid(form)


class UserLoginView(LoginView):
    """Класс для создания представления входа пользователя."""

    template_name = "users/login.html"
    context_object_name = "user"

    def get_success_url(self):
        """Обновляет URL после успешного входа."""
        return reverse_lazy("catalog:product_list")


def custom_logout(requesst):
    """Функция для создания представления выхода пользователя."""
    logout(requesst)
    return redirect(reverse_lazy("catalog:product_list"))


class UserLogoutView(LogoutView):
    """Класс для создания представления выхода пользователя. ПРОВЕРИТЬ!"""

    next_page = "catalog:product_list"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления для редактирования профиля пользователя."""

    model = CustomUser
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """Дополнительная обработка перед сохранением формы."""
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Профиль пользователь '%s' успешно обновлён." % self.object.user_name)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка в случае неверной формы."""
        logger.warning("Ошибка при обновлении профиля пользователя: %s" % form.errors)
        return super().form_invalid(form)
