from rest_framework import serializers
from auction.models import Book, BookInstance, Order
from django.contrib.auth.models import User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'description',
                  'classes', 'subject', 'author', 'isbn']


class BookInstanceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') 

    class Meta:
        model = BookInstance
        fields = ['book', 'owner', 'quantity', 'status']




class OrderSerializer(serializers.ModelSerializer):
    order_owner = serializers.ReadOnlyField(source='order_owner.username')
    class Meta:
        model = Order
        fields = ['order_owner', 'buyorsell',
                  'book', 'price', 'quantity', 'quality']


class UserSerializer(serializers.ModelSerializer):
    BookInstance = serializers.PrimaryKeyRelatedField(
        many=True, queryset=BookInstance.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'BookInstance']
