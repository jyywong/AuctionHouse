import factory
from faker import Faker
from django.contrib.auth import get_user_model
from auction.models import Book, Order
from random import choice
from decimal import Decimal
from datetime import timedelta as td
from datetime import datetime as dt
from django.utils import timezone
fake = Faker()

Faker.seed(0)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()



    username = factory.LazyFunction(fake.name)
    password = factory.PostGenerationMethodCall('set_password', fake.password())
    email = factory.LazyFunction(fake.email)


class BookFactory(factory.django.DjangoModelFactory):
    class Meta: 
        model = Book

    name = factory.LazyFunction(fake.bs)
    description = factory.LazyFunction(fake.paragraph)
    classes = factory.LazyFunction(fake.job)
    author = factory.LazyFunction(fake.name)

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    order_owner = factory.LazyAttribute(lambda a :choice(get_user_model().objects.all()))
    buyorsell = factory.LazyAttribute(lambda a: choice(['Buy', 'Sell']) )
    book = factory.LazyAttribute(lambda a: choice(Book.objects.all()))
    price = factory.LazyAttribute(lambda a : Decimal(fake.random_int(max=50)))
    quantity = factory.LazyAttribute(lambda a : fake.random_int(max = 10))
    created_at = factory.LazyAttribute(lambda a: fake.date_time_between_dates(
        datetime_start = dt.now() - td(days = 80),
        datetime_end = dt.now(),
        tzinfo = timezone.get_current_timezone()
        ))
