from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
  path('auth/', include('app.auth.urls'), name='authentication'),
]
