from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.db.models import Q
from auction.models import Book
# Create your views here.

def home(request):

    return render (request, 'home.html')

def list(request):
    books=Book.objects.all()

    return render(request, 'item_list.html', {'books':books})

def search(request):
    template = 'item_list.html'

    query = request.GET.get('q')

    results = Book.objects.filter(Q(name__icontains=query))

    return render(request, template, {'books': results})



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

# class BookListView(ListView):
#     template_name='item_list.html'
#     queryset= Item.objects.all()
