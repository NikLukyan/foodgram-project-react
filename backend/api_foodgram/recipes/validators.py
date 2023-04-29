import re

from django.core.exceptions import ValidationError


def hex_field_validator(value):
    """Проверка, что содержимое поля в формате HEX."""
    message = (
        'Введите цвет в формате HEX.'
    )
    if not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
        raise ValidationError(message)


def slug_field_validator(value):
    """Проверка, что содержимое поля slug в необходимом формате."""
    message = (
        'Поле slug может содержать только латинские буквы '
        '(строчные и заглавные), цифры и символ _'
    )
    if not re.search(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError(message)
