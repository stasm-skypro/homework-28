from django.test import TestCase
from django.urls import reverse

from blog.models import Blog


class TestBlogListView(TestCase):

    def test_blog_list(self):
        """Проверяем, что статус-код 200"""
        url = reverse("blog:blog_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_list_template_used(self):
        """Проверяем, что используется правильный шаблон"""
        url = reverse("blog:blog_list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/blog_list.html")

    def test_blog_list_context(self):
        """Проверяем, что объект блога передается в контекст"""
        url = reverse("blog:blog_list")
        response = self.client.get(url)
        self.assertEqual(response.context["blog_list"].count(), Blog.objects.all().count())


class TestBlogDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем тестовый объект Blog
        cls.blog = Blog.objects.create(
            title="Test Blog",
            content="Test Content",
            preview = "blog/default.png",
            created_at ="2023-01-01",
            publicated = True,
            views_counter = 1,
        )

    def test_blog_detail(self):
        """Проверяем, что статус-код 200"""
        url = reverse("blog:blog_detail", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_template_used(self):
        """Проверяем, что используется правильный шаблон"""
        url = reverse("blog:blog_detail", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/blog_detail.html")

    def test_blog_detail_context(self):
        """Проверяем, что объект блога передается в контекст"""
        url = reverse("blog:blog_detail", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.context["blog"].title, self.blog.title)
        self.assertEqual(response.context["blog"].content, self.blog.content)
        self.assertEqual(response.context["blog"].views_counter, self.blog.views_counter + 1)


class TestBlogCreateView(TestCase):

    def test_blog_create(self):
        """Проверяем, что статус-код 200"""
        url = reverse("blog:blog_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_create_template_used(self):
        """Проверяем, что используется правильный шаблон"""
        url = reverse("blog:blog_create")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/blog_form.html")

    def test_blog_create_context(self):
        """Проверяем, что объект блога передается в контекст"""
        url = reverse("blog:blog_create")
        response = self.client.get(url)
        self.assertFalse(response.context["form"].is_bound)


class TestBlogUpdateView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем тестовый объект Blog
        cls.blog = Blog.objects.create(
            title="Test Blog",
            content="Test Content",
            preview = "blog/default.png",
            created_at ="2023-01-01",
            publicated = True,
            views_counter = 1,
        )

    def test_blog_update(self):
        """Проверяем, что статус-код 200"""
        url = reverse("blog:blog_create", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_update_template_used(self):
        """Проверяем, что используется правильный шаблон"""
        url = reverse("blog:blog_create", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/blog_form.html")

    def blog_update_context(self):
        """Проверяем, что объект блога передается в контекст"""
        url = reverse("blog:blog_create", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.context["blog"].title, self.blog.title)
        self.assertEqual(response.context["blog"].content, self.blog.content)
        self.assertEqual(response.context["blog"].views_counter, self.blog.views_counter + 1)


class TestBlogDeleteView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем тестовый объект Blog
        cls.blog = Blog.objects.create(
            title="Test Blog",
            content="Test Content",
            preview = "blog/default.png",
            created_at ="2023-01-01",
            publicated = True,
            views_counter = 1,
        )

    def test_blog_delete(self):
        """Проверяем, что статус-код 200"""
        url = reverse("blog:blog_confirm_delete", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_delete_template_used(self):
        """Проверяем, что используется правильный шаблон"""
        url = reverse("blog:blog_confirm_delete", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/blog_confirm_delete.html")

    def test_blog_delete_context(self):
        """Проверяем, что объект блога передается в контекст"""
        url = reverse("blog:blog_confirm_delete", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.context["blog"].title, self.blog.title)
        self.assertEqual(response.context["blog"].content, self.blog.content)
        self.assertEqual(response.context["blog"].views_counter, self.blog.views_counter)
