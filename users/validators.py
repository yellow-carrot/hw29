from rest_framework.exceptions import ValidationError
import datetime


def check_b_date(value):
    now = datetime.date.today()
    age = (now.year - value.year - 1) + ((now.month, now.day) >= value.month, value.day)
    if age < 9:
        raise ValidationError('age must not be less than 9')


def check_email(value):
    domain = value.split('@')[1]
    if domain == 'rambler.ru':
        raise ValidationError('domain cannot be "rambler.ru"')
