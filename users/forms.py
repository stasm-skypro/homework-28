import os

from django.contrib.auth.forms import UserCreationForm
from dotenv import load_dotenv

from blog.mixins import StyledFormMixin
from users.models import CustomUser
from django.core.exceptions import ValidationError

load_dotenv()


class UserRegisterForm(StyledFormMixin, UserCreationForm):
    """Класс для создания формы регистрации пользователя с изображением аватара."""

    usable_password = None

    class Meta:
        model = CustomUser
        fields = ("username", "email", "avatar", "password1", "password2")
        labels = {
            "username": "Имя пользователя",
            "email": "Адрес электронной почты",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }

        help_texts = {
            "username": "Введите имя пользователя",
            "email": "Введите адрес электронной почты",
            "password1": "Введите пароль",
            "password2": "Подтвердите пароль",
        }

    def clean_phone_number(self) -> str:
        cleaned_phone_number = self.cleaned_data.get("phone_number", "").strip()

        if cleaned_phone_number and not cleaned_phone_number.isdigit():
            raise ValidationError("Номер телефона должен содержать только цифры!")

        return cleaned_phone_number

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
        max_size = 200 * 1024  # 200 КБ

        if image and image.size > max_size:
            raise ValidationError("Размер изображения не должен превышать 5 МБ.")

        return image

    def clean_user_name(self):
        """Проверяет, что указанные поля формы не содержат запрещённые слова."""
        forbidden_words = os.getenv("FORBIDDEN_WORDS").split(",")
        cleaned_data = super().clean()

        cleaned_words = cleaned_data.get("product").split()
        for word in cleaned_words:
            if word.lower() in forbidden_words:
                self.add_error(
                    "username",
                    "Поле с именем пользователя содержит запрещённое слово %s." % word,
                )
                break


class UserUpdateForm(StyledFormMixin, UserCreationForm):
    """Класс для создания формы редактирования профиля пользователя."""

    class Meta:
        model = CustomUser
        exclude = (
            "password1",
            "password2",
        )
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "phone_number",
            "is_staff",
            "country",
        )

        labels = {
            "avatar": "Аватар",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "phone_number": "Номер телефона",
            "is_staff": "Администратор",
            "country": "Страна",
            # "password1": "Пароль (оставьте пустым, если не хотите изменять)",
            # "password2": "Подтверждение пароля (оставьте пустым, если не хотите изменять)",
        }

        help_texts = {
            "avatar": "Изображение аватара",
            "first_name": "Введите имя",
            "last_name": "Введите фамилию",
            "phone_number": "Введите номер телефона",
            "is_staff": "Установите этот флаг, если вы хотите стать администратором",
            "country": "Введите страну",
            # "password1": "Введите пароль (оставьте пустым, если не хотите изменять)",
            # "password2": "Подтвердите пароль (оставьте пустым, если не хотите изменять)",
        }
