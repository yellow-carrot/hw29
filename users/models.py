from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import check_b_date, check_email


# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class User(AbstractUser):
    ROLE = [
        ('member', 'пользователь'),
        ('moderator', 'модератор'),
        ('admin', 'администратор')
    ]

    role = models.CharField(max_length=9, choices=ROLE, default='member')
    age = models.PositiveSmallIntegerField(null=True)
    location_id = models.ManyToManyField(Location)
    birth_date = models.DateField(validators=[check_b_date], null=True)
    email = models.EmailField(unique=True, null=True, validators=[check_email])

    @property
    def locations(self):
        return self.location_id

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
