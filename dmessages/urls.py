from django.contrib import admin
from django.urls import path
from dmessages import views
from dmessages.views import inbox

urlpatterns = [
    path('new_conversation', views.new_conversation, name='new_conversation'),
    path('inbox/<int:pk>', inbox, name='inbox')

]
