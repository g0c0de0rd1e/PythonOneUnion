from django.urls import path
from .views import UserListView, ChatView

urlpatterns = [
    path('', UserListView.as_view(), name='chat-list'),
    path('chat-with-user/<str:username>/', ChatView.as_view(), name='chat-with-user'),
]
