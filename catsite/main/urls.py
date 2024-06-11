from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import Register, EditUser, Tasks

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('edit_profile/', EditUser.as_view(), name='edit_profile'),
    path('new_task/', Tasks.as_view(), name='new_task')
]
