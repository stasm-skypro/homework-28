# blog/views.py
import logging

from django.urls import reverse_lazy

from django.core.mail import send_mail
from blog.forms import BlogForm
from blog.models import Blog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("blog")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("blog/logs/reports.log", "a", "utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s"))
logger.addHandler(handler)


class BlogListView(ListView):
    """Определяет отображение страницы блога."""

    model = Blog
    context_object_name = "blog_list"

    def get_queryset(self):
        """Возвращает только опубликованные статьи."""
        return Blog.objects.filter(publicated=True)


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Определяет отображение страницы с содержимым статьи."""

    model = Blog

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


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Определяет отображение страницы добавления статьи."""

    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        """Дополнительная обработка перед сохранением формы."""
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Статья '%s' успешно создана." % self.object.title)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка в случае неверной формы."""
        logger.warning("Ошибка при создании статьи: %s" % form.errors)
        return super().form_invalid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Определяет отображение обновления статьи."""

    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        """Дополнительная обработка перед сохранением формы."""
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Статья '%s' успешно обновлена." % self.object.title)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка в случае неверной формы."""
        logger.warning("Ошибка при обновлении статьи: %s" % form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        """Возвращает URL для перехода на страницу с содержимым статьи после успешного удаления."""
        return reverse_lazy("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Определяет отображение удаления статьи."""

    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def post(self, request, *args, **kwargs):
        """Переопределение метода POST для вызова delete."""
        logger.info("Удаление статьи через POST-запрос.")
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Переопределение метода delete для логирования."""
        blog = self.get_object()
        logger.info("Статья '%s' успешно удалена." % blog.title)
        return super().delete(request, *args, **kwargs)
