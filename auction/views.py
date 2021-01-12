from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.db.models import Q
from auction.models import *
from dmessages.models import Conversation, Message
from .forms import *
from dmessages.forms import NewConversationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auction.api.serializers import BookSerializer, BookInstanceSerializer, OrderSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions
from auction.api.permissions import IsOwnerOrReadOnly, IsOrderOwnerOrReadOnly


# Create your views here.

def search_books(request):
    form = BookForm()
    template = 'item_list.html'
    query = request.GET.get('q')
    if not query:
        query = " "
    results = Book.objects.filter(Q(name__icontains=query))
    context = {
        'books': results,
        'form' : form
    }
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render (request,template,context)


    return render(request, template, context)

def search_orders(request):
    template = 'order_list.html'
    query = request.GET.get('q')
    if not query:
        query = " "
    results = Order.objects.filter(Q(book__name__icontains=query))
    return render(request, template, {'orders': results})

def book_view(request, pk):
    convo_form = NewConversationForm()
    order_form = OrderForm()
    template = 'book_display.html'
    book = Book.objects.get(id=pk)
    buyorders = Order.objects.filter(book = book).filter(buyorsell='Buy')
    sellorders = Order.objects.filter(book = book).filter(buyorsell='Sell')
    order_type = [buyorders, sellorders]
    context = {
        'book': book,
        'order_type':order_type,
        'buyorders':buyorders,
        'sellorders':sellorders,
        'form':convo_form,
        'order_form': order_form
        }
    if request.method == 'POST' and 'convo_form' in request.POST:
        form = NewConversationForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.created_by = request.user
            object.save()
            Message.objects.create(
                conversation=object,
                sender=request.user,
                receiver=form.cleaned_data.get('send_to'),
                message=form.cleaned_data.get('message')
            )
            form = NewConversationForm()
            return render(request, template, context)
    elif request.method == 'POST' and 'order_form' in request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.order_owner = request.user
            object.save()
            form = OrderForm()
        return render(request, template, context)
    else:
        form = NewConversationForm()
        order_form = OrderForm()
    return render(request, template, context)


@login_required
def library(request):
    books = BookInstance.objects.filter(owner = request.user)
    return render(request, 'library.html', {'books':books})

@login_required
def order_library(request):
    template = 'order_library.html'
    owner = request.user
    buyorders = Order.objects.filter(order_owner = owner).filter(buyorsell='Buy')
    sellorders = Order.objects.filter(order_owner = owner).filter(buyorsell='Sell')
    order_type = [buyorders, sellorders]
    return render(request, template, {'user':owner, 'order_type':order_type})

@login_required
def new_book_instance(request):
    form = BookInstanceForm()
    if request.method == 'POST':
        form = BookInstanceForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.owner = request.user
            try:
                existing_book = BookInstance.objects.get(
                    book = object.book,
                    owner = object.owner,
                    quality = object.quality,
                    status = object.status
                )
                existing_book.quantity += object.quantity
                existing_book.save()
            except BookInstance.DoesNotExist:
                None
                object.save()
            form = BookInstanceForm()
            return render(request, 'new_book_instance.html', {'form': form})
    else:
        form = BookInstanceForm()
    return render(request, 'new_book_instance.html', {'form': form})

@login_required
def add_order(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.order_owner = request.user
            object.save()
            form = OrderForm()
            return render(request, 'new_order.html', {'form': form})
    else:
        form = OrderForm()
    return render(request, 'new_order.html', {'form': form})

class delete_order(DeleteView):
    model = Order
    success_url = reverse_lazy('my_profile')
    template_name = 'order_check_delete.html'


def profile(request, pk):
    profile_user = User.objects.get(id=pk)
    buyorders = Order.objects.filter(order_owner = profile_user).filter(buyorsell='Buy')
    sellorders = Order.objects.filter(order_owner = profile_user).filter(buyorsell='Sell')
    totalorders = buyorders.count() + sellorders.count()
    order_type = [buyorders, sellorders]
    return render(request, 'order_library.html', {'profile_user':profile_user, 'order_type':order_type, 'order_total': totalorders})
def my_profile(request):
    user = request.user
    buyorders = Order.objects.filter(order_owner = user).filter(buyorsell='Buy')
    sellorders = Order.objects.filter(order_owner = user).filter(buyorsell='Sell')
    totalorders = buyorders.count() + sellorders.count()
    order_type = [buyorders, sellorders]
    context = {
        'user':user, 
        'order_type':order_type, 
        'order_total': totalorders,
        'buyorders': buyorders,
        'sellorders':sellorders
        }
    
    return render(request, 'my_profile.html', context)
def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            form = UserCreationForm()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})

class book_statistics(DetailView):
    model = Book
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_book = Book.objects.get(id = self.kwargs['pk'])
        context['num_orders'] = list(Order.vol_over_90_days(selected_book).values())
        context['average_prices'] = Order.price_over_90_days(selected_book)
        context['past_90'] = Order.get_past_90_days()



        return context







'''
API Views
'''

class book_list(generics.ListCreateAPIView):
    '''
    List all books registered on the site, or register a new book
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class book_detail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update, or delete a registered book
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class book_instance_list(generics.ListCreateAPIView):
    '''
    List all books in user library
    '''
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class book_instance_detail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update, or delete a book in users library
    '''
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class order_list(generics.ListCreateAPIView):
    '''
    List all orders in user library
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(order_owner=self.request.user)

class order_detail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update, or delete an order in users library
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrderOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(order_owner=self.request.user)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
