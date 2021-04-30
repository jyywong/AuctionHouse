from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from django.utils import timezone
import datetime 
import random
# Create your models here.


class Book(models.Model):
    '''
    The Book class creates an entry on the website of an existence of a book
    '''
    name = models.CharField(max_length=50)
    description = models.TextField()
    classes = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, default='N/A')
    author = models.CharField(max_length=255, default='N/A')
    isbn = models.CharField(max_length=13, default='0000000000000')

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    '''
    Unnecesary model. Wanted to implement a sort of library for each user but decided that it wouldn't add much value to the website.
    Could delete, but it might mess up a lot of stuff.
    '''
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
    '''
    Each order is tied to the owner of the order, and the book this order is made for
    '''
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
    created_at = models.DateTimeField(default = timezone.now())

    '''
    Methods for displaying statistics
    '''
    @staticmethod
    def get_past_90_days():
        past_90 = []
        today = date.today()
        start = date.today() - datetime.timedelta(days = 90)
        for i in range(datetime.timedelta(days=90).days):
            past_90.append((start + datetime.timedelta(days = i)).strftime("%d/%m/%Y"))
        return past_90
    @staticmethod
    def get_orders_90_days(book):
        '''
        Get all orders within a 90 day period
        '''
        date_difference = datetime.timedelta(days = 90)
        selected_book = book
        '''
        qs_filtered selects all orders for the given book that were created in the past 90 days
        '''
        qs_filtered = Order.objects.filter(
            Q(book = selected_book) & 
                Q(created_at__range = 
                    (date.today() - date_difference, 
                    (date.today() + datetime.timedelta(days=1))))
            )

        qs_filtered_ordered = qs_filtered.order_by('created_at')
        return qs_filtered_ordered




    '''
    Methods for organizing data to be plotted out in chart.js
    '''
    @staticmethod
    def vol_over_90_days(book):
        qs_filtered_ordered = Order.get_orders_90_days(book)
        '''
        num_orders is a dictionary that has a key for each date for the past 90 days.
        Each date has a number associated with that date which is the # of orders for that date
        I used a dictionary in this case because there may or may not be orders on a certain date, or there may be mulitple orders on a certain date.
        If I used a list or an array, it would have been more difficult to deal with multiple orders on a date or no orders
        '''
        past_90 = Order.get_past_90_days()
        num_orders = dict((day, 0) for day in past_90)
        
        for order in qs_filtered_ordered:
            for key in num_orders:
                    if key == order.created_at.date().strftime("%d/%m/%Y"):
                        num_orders[key] += 1
        return  num_orders
    @staticmethod
    def price_over_90_days(book):
        qs_filtered_ordered = Order.get_orders_90_days(book)
        '''
        Organizing data to be plotted out in a graph:
  
        prices_per_day is a dictionary with each date for the past 90 days as a key.
        Each date has an empty list to begin.
        '''
        past_90 = Order.get_past_90_days()
        prices_per_day = dict((day, []) for day in past_90)

        '''
        Below, we go through every order in the past 90 days for this book.
        For each date, we append the price of each order within a date to the empty list associated with each key/date.
        '''
        for order in qs_filtered_ordered:
            for key in prices_per_day:
                    if key == order.created_at.date().strftime("%d/%m/%Y"):
                        prices_per_day[key].append(order.price)

        '''
        We now calculate the average price of the book on each day for the past 90 days and append this to a new list.
        '''

        for day in prices_per_day.values():
            if day:
                newday = int(sum(day)/len(day))
                day.clear()
                day.append(newday)
            else:
                day.append(0)
        return  prices_per_day


