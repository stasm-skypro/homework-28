from django import forms
from django.core.exceptions import PermissionDenied


class StyledFormMixin:
    """Миксин для стилизации форм Django."""

    def __init__(self, *args, **kwargs):
        """Осуществляет стилизацию формы."""

        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update(
                    {
                        "class": "form-check-input",
                    }
                )
            else:
                field.widget.attrs.update(
                    {
                        "class": "form-control",
                        "placeholder": field.label,
                        "style": "font-size: 0.9em; width: 100%",
                    }
                )

class OwnerRequiredMixin:
    """Миксин для проверки прав владельца объекта."""

    def get_object(self, queryset=None):
        """Возвращает объект только если текущий пользователь — владелец."""
        obj = super().get_object(queryset)

        # Проверяем, является ли пользователь владельцем
        if obj.owner == self.request.user:
            return obj

        # Проверяем, состоит ли пользователь в группе "Product Moderators"
        if self.request.user.groups.filter(name="Product Moderators").exists():
            return obj

        # Если не владелец и не модератор — запрет
        raise PermissionDenied("Вы не можете удалить этот продукт!")

