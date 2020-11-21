from django import forms
from django.forms import ModelForm
from .models import *

class BookInstanceForm(ModelForm):

    class Meta:
        model = BookInstance
        exclude =['owner']

class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ['buyorsell', 'book', 'price', 'quantity']
