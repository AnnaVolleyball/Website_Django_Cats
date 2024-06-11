from django.contrib.auth import authenticate, login

from .forms import RegisterForm, EditProfileForm, TaskForm
from .models import Task

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm

from django.utils import timezone


# business logic
def index_page(request):
    params = {}
    tasks = Task.objects.all()
    params['tasks'] = tasks
    return render(request, 'main/index.html', params)


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        contex = {'form': RegisterForm()}
        return render(request, self.template_name, contex)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print('save')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            # Если данные формы недопустимы, возвращаем страницу регистрации с сообщением об ошибке
            context = {'form': form}
            return render(request, self.template_name, context)


class ChangeUser(View):
    template_name = 'registration/edit_profile.html'

    def get(self, request):
        contex = {'form': EditProfileForm(instance=request.user)}
        return render(request, self.template_name, contex)

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.modified_date = timezone.now()
            user.save()
            return redirect('home')
        else:
            # Если данные формы недопустимы, возвращаем страницу регистрации с сообщением об ошибке
            context = {'form': form}
            return render(request, self.template_name, context)


class Tasks(View):
    template_name = 'tasks/new_task.html'

    def get(self, request):
        contex = {'form': TaskForm()}
        return render(request, self.template_name, contex)

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Присваиваем текущего пользователя
            task.save()
            return redirect('home')
        else:
            # Если данные формы недопустимы, возвращаем страницу регистрации с сообщением об ошибке
            context = {'form': form}
            return render(request, self.template_name, context)











