from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
import datetime 
import random
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
    created_at = models.DateTimeField(auto_now_add=True)

    '''
    Methods for displaying statistics
    '''
    @staticmethod
    def vol_over_90_days(book):
        '''
        Get all orders within a 90 day period
        '''
        date_difference = datetime.timedelta(days = 90)
        selected_book = book
        qs_filtered = Order.objects.filter(Q(book = selected_book) & Q(created_at__range = (date.today() - date_difference, (date.today() + datetime.timedelta(days=1)))))
        qs_filtered_ordered = qs_filtered.order_by('created_at')
        '''
        Organize data to be plotted out in a graph
        '''
        unique_dates = []
        num_orders = {}
        format = "%b %d, %Y, %I:%M%p"
        for order in qs_filtered_ordered:
            if order.created_at.strftime(format) not in unique_dates:
                unique_dates.append(order.created_at.strftime(format))
                num_orders[order.created_at.strftime(format)] = 1
            else:
                num_orders[order.created_at.strftime(format)] += 1

        return unique_dates, num_orders
    @staticmethod
    def price_over_90_days(book):
        '''
        Get all orders within a 90 day period
        '''
        date_difference = datetime.timedelta(days = 90)
        selected_book = book
        qs_filtered = Order.objects.filter(Q(book = selected_book) & Q(created_at__range = (date.today() - date_difference, date.today() + datetime.timedelta(days=1))))
        print(date.today() - date_difference)
        print('qs_filtered= ')
        print(type(qs_filtered[1].created_at))
        qs_filtered_ordered = qs_filtered.order_by('created_at')
        '''
        Organize data to be plotted out in a graph
        '''
        unique_dates = []
        order_prices_per_date = {}
        format = "%b %d, %Y, %I:%M%p"
        for order in qs_filtered_ordered:
            if order.created_at.date().strftime(format) not in unique_dates:
                unique_dates.append(order.created_at.date().strftime(format))
                order_prices_per_date[order.created_at.date().strftime(format)] = [order.price]
            else:
                order_prices_per_date[order.created_at.date().strftime(format)].append(order.price)
        # print(list(order_prices_per_date.values()))
        print('unique_dates')
        print(unique_dates)
        averages = []
        for day in order_prices_per_date.values():
            print(day)
            averages.append(sum(day)/len(day))
            print(averages)
        return unique_dates, averages


