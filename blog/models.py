from django.db import models

class Blog(models.Model):
    """
    Модель таблицы blog.
    """
    title = models.CharField(max_length=255, verbose_name="Название статьи")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(verbose_name="Миниатюра", blank=True, null=True, upload_to="blog/")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    publicated = models.BooleanField(default=False, verbose_name="Признак публикации")
    views_counter = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{self.__class__} {self.title}"

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ("-created_at",)
