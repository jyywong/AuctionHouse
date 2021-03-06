from rest_framework import serializers
from auction.models import Book, BookInstance, Order
from dmessages.models import Conversation, Message
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
    order_owner_id = serializers.ReadOnlyField(source='order_owner.id')
    book_name = serializers.ReadOnlyField(source='book.name')
    class Meta:
        model = Order
        fields = ['order_owner','order_owner_id','id', 'buyorsell',
                  'book', 'price', 'quantity', 'quality', 'book_name']


class UserSerializer(serializers.ModelSerializer):
    BookInstance = serializers.PrimaryKeyRelatedField(
        many=True, queryset=BookInstance.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'BookInstance']

class RegisterUserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only= True)
    class Meta: 
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self, *args, **kwargs):
        new_user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})

        new_user.set_password(password)
        new_user.save()
        return new_user

class ConversationSerializer(serializers.ModelSerializer):
    send_to_username = serializers.ReadOnlyField(source='send_to.username')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    last_message = serializers.SerializerMethodField(method_name= 'get_last_message')
    class Meta: 
        model = Conversation
        fields = ['id','name', 'send_to','send_to_username',  
        'created_by', 'created_by_username','last_message' ]

    def get_last_message(self, conversation):
        return MessageSerializer(conversation.message.last()).data


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    class Meta:
        model = Message
        fields = ['conversation', 'sender','sender_username', 
        'receiver_username', 'receiver', 'created_at', 'message']