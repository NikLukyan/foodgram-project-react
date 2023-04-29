import re

from django.core.exceptions import ValidationError


def hex_field_validator(value):
    """Проверка, что содержимое поля в формате HEX."""
    message = (
        'Введите цвет в формате HEX.'
    )
    if not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
        raise ValidationError(message)