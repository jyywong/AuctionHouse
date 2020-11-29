from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.db.models import Q
from auction.models import *
from .forms import *
from dmessages.forms import NewConversationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render (request, 'index.html')

def list(request):
    books=Book.objects.all()
    return render(request, 'item_list.html', {'books':books})

def search_books(request):
    template = 'item_list.html'
    query = request.GET.get('q')
    if not query:
        query = " "
    results = Book.objects.filter(Q(name__icontains=query))
    return render(request, template, {'books': results})

def search_orders(request):
    template = 'order_list.html'
    query = request.GET.get('q')
    if not query:
        query = " "
    results = Order.objects.filter(Q(book__name__icontains=query))
    return render(request, template, {'orders': results})

def book_view(request, pk):
    form = NewConversationForm()
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
        'form':form
        }
    if request.method == 'POST':
        form = NewConversationForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.created_by = request.user
            object.save()
            form = NewConversationForm()
            return render(request, template, context)
    else:
        form = NewConversationForm()
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

def profile(request, pk):
    user = User.objects.get(id=pk)
    buyorders = Order.objects.filter(order_owner = user).filter(buyorsell='Buy')
    sellorders = Order.objects.filter(order_owner = user).filter(buyorsell='Sell')
    order_type = [buyorders, sellorders]
    return render(request, 'order_library.html', {'user':user, 'order_type':order_type})

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
