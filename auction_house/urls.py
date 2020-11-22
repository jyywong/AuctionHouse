"""auction_house URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auction import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search_books, name="home"),
    path('listview', views.list, name="listview"),
    path('book_results', views.search_books, name="search_books"),
    path('order_results', views.search_orders, name="search_orders"),
    path('login', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('signup', views.signup, name='signup'),
    path('logout',auth_views.LogoutView.as_view(), name='logout'),
    path('book_view/<int:pk>', views.book_view, name="book_view"),
    path('new_book_instance', views.new_book_instance, name="new_book_instance"),
    path('library', views.library, name="library"),
    path('add_order', views.add_order, name="add_order"),
    path('order_library', views.order_library, name="order_library"),
    path('profile/<int:pk>', views.profile, name="profile")

]
