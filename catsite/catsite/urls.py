from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='home'),
    path('users/', include('main.urls')),
    path('edit_profile/', views.ChangeUser.as_view(), name='edit_profile')
]
