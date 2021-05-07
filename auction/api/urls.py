from django.urls import path
from auction import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('books/', views.book_list.as_view()),
    path('books/<int:pk>', views.book_detail.as_view()),
    path('book_orders/<int:pk>', views.book_orders.as_view()),
    path('book_stats_vol/<int:pk>', views.api_book_stats_vol),
    path('book_stats_prices/<int:pk>', views.api_book_stats_prices),
    path('bookinstances/', views.book_instance_list.as_view()),
    path('bookinstances/<int:pk>', views.book_instance_detail.as_view()),
    path('orders/', views.order_list.as_view()),
    path('orders/<int:pk>', views.order_detail.as_view()),
    path('user_orders/<int:pk>', views.UserOrders().as_view()),
    path('user_conversations/<int:pk>', views.UserConversations().as_view()),
    path('conversation_messages/<int:pk>', views.ConversationMessages().as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/register/', views.api_registration_view),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
