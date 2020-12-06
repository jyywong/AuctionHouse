from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    classes = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, default='N/A')
    author = models.CharField(max_length=255, default='N/A')
    isbn = models.CharField(max_length=13, default='0000000000000')

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='Book')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='BookInstance')
    quantity = models.IntegerField(default=1)
    status_choices = [
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Inactive', 'Inactive')
    ]
    status = models.CharField(
        max_length=100,
        choices=status_choices,
        default='Inactive'
    )

    def __str__(self):
        return self.book.name


class Order(models.Model):
    bschoices = [
        ('Buy', 'Buy'),
        ('Sell', 'Sell')
    ]
    quality_choices = [
        ('New', 'New'),
        ('LUsed', 'Lightly Used'),
        ('Used', 'Used'),
        ('Damaged', 'Damaged')
    ]
    order_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Order_Owner')
    buyorsell = models.CharField(
        max_length=50,
        choices=bschoices
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='Order')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    quality = models.CharField(
        max_length=100,
        choices=quality_choices,
        default='Used'
    )
