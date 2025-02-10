# Generated by Django 5.1.4 on 2024-12-24 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_alter_product_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=35, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=50, verbose_name="Фамилия")),
                ("phone", models.CharField(max_length=15, verbose_name="Телефон")),
                ("message", models.TextField(verbose_name="Сообщение")),
            ],
            options={
                "verbose_name": "Контакт",
                "verbose_name_plural": "Контакты",
                "ordering": ["first_name", "last_name"],
            },
        ),
    ]
