from datetime import date

# Импортируем ошибку валидации.
from django.core.exceptions import ValidationError


# На вход функция будет принимать дату рождения.
def real_age(value: date) -> None:
    # Считаем разницу между сегодняшним днём и днём рождения в днях
    # и делим на 365.
    age = (date.today() - value).days / 365
    # Если возраст меньше 1 года или больше 120 лет — выбрасываем ошибку.
    if age < 18 or age > 90:
        raise ValidationError(
            'Ожидается возраст от 18 года до 90 лет'
        )
