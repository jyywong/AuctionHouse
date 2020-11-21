from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.db.models import Q
from auction.models import *
from .forms import *
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
    results = Order.objects.filter(Q(book__book__name__icontains=query))
    return render(request, template, {'orders': results})

def book_view(request, pk):
    template = 'book_display.html'
    book = Book.objects.get(id=pk)
    buyorders = Order.objects.filter(book__book = book).filter(buyorsell='buy')
    sellorders = Order.objects.filter(book__book = book).filter(buyorsell='sell')
    return render(request, template, {'book': book, 'buyorders' : buyorders, 'sellorders': sellorders})

@login_required
def library(request):
    books = BookInstance.objects.filter(owner = request.user)
    return render(request, 'library.html', {'books':books})

def order_library(request):
    template = 'order_library.html'
    owner = request.user
    buyorders = Order.objects.filter(book__owner = owner).filter(buyorsell='buy')
    sellorders = Order.objects.filter(book__owner = owner).filter(buyorsell='sell')
    return render(request, template, {'user':owner, 'buyorders': buyorders, 'sellorders':sellorders})

@login_required
def new_book_instance(request):
    form = BookInstanceForm()
    if request.method == 'POST':
        form = BookInstanceForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.owner = request.user
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
            form.save()
            form = OrderForm()
            return render(request, 'new_order.html', {'form': form})
    else:
        form = OrderForm()
    return render(request, 'new_order.html', {'form': form})


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
