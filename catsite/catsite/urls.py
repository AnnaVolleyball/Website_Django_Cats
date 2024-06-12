from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='home'),
    path('users/', include('main.urls')),
    path('edit_profile/', views.EditUser.as_view(), name='edit_profile'),
    path('new_task/', views.Tasks.as_view(), name='new_task'),
    path('edit_task/<int:task_id>/', views.EditTask.as_view(), name='edit_task'),
    path('delete_task/<int:task_id>/', views.DeleteTask.as_view(), name='delete_task')
]
