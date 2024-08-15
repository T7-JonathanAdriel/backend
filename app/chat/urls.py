from django.urls import path
from .views import get_chat_by_id, get_chat_title, create_chat, create_message

urlpatterns = [
  path('<int:id>/', get_chat_by_id, name='get_chat_by_id'),
  path('title/', get_chat_title, name='get_chat_title'),
  path('create/', create_chat, name='create_chat'),
  path('message/create', create_message, name='create_message'),
]