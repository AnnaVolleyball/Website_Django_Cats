from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from main import views, api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='home'),
    path('users/', include('main.urls')),
    path('edit_profile/', views.EditUser.as_view(), name='edit_profile'),
    path('new_task/', views.Tasks.as_view(), name='new_task'),
    path('edit_task/<int:task_id>/', views.EditTask.as_view(), name='edit_task'),
    path('delete_task/<int:task_id>/', views.DeleteTask.as_view(), name='delete_task'),
    path('galery/', views.Galery.as_view(), name='galery'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/tasks/', api.TaskListView.as_view(), name="tasks_api"),
    path('api/tasks/<int:pk>/', api.TaskDetailView.as_view(), name="task_api"),
    path('api/users/', api.UserListView.as_view(), name="users_api")

]
