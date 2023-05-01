import factory.django

from ads.models import Category, Ad
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    slug = factory.Faker('ean', length=8)
    name = factory.Faker('name')


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker('name')
    price = 111
    category_id = factory.SubFactory(CategoryFactory)
    author_id = factory.SubFactory(UserFactory)
