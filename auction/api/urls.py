from django.urls import path
from auction import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('books/', views.book_list.as_view()),
    path('books/<int:pk>', views.book_detail.as_view()),
    path('bookinstances/', views.book_instance_list.as_view()),
    path('bookinstances/<int:pk>', views.book_instance_detail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
