from django.db import models


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


class User(models.Model):
    ROLE = [
        ('member', 'пользователь'),
        ('moderator', 'модератор'),
        ('admin', 'администратор')
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=9, choices=ROLE, default='member')
    age = models.PositiveSmallIntegerField()
    location_id = models.ManyToManyField(Location)

    @property
    def locations(self):
        return self.location_id

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
