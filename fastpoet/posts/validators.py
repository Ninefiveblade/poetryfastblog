import re
from datetime import datetime

def check_slug(value):
    if not re.match("^[А-яA-z ]*$", value):
        raise ValueError(
            'допустимы только русские и латинские символы и знак пробела'
        )
    if len(value) < 3 and len(value) > 50:
        raise ValueError(
            'Длина поля должна быть больше 3 и менее 50 символов'
        )
    return value


def check_name(value):
    if not re.match("^[a-z_]*$", value):
        raise ValueError(
            'допустимы только латинские символы и знак подчеркивания _'
        )
    if len(value) < 3 and len(value) > 50:
        raise ValueError(
            'Длина поля должна быть больше 3 и менее 50 символов'
        )
    return value

def check_year(value):
    if value < 0 and value > datetime.date.today().year:
        raise ValueError(
            'Год от 0 до текущего'
        )
    return value