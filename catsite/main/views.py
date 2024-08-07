import os

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden

from .forms import RegisterForm, EditProfileForm, TaskForm, EditTaskForm
from .models import Task

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.utils import timezone


def index_page(request):
    params = {}
    tasks = Task.objects.all()
    tasks = tasks[::-1]
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            # Если данные формы недопустимы, возвращаем страницу регистрации с сообщением об ошибке
            context = {'form': form}
            return render(request, self.template_name, context)


class EditUser(View):
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


class EditTask(View):
    template_name = 'tasks/edit_task.html'

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        contex = {'form': EditTaskForm(instance=task), 'task': task}
        return render(request, self.template_name, contex)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if task.user != request.user:
            return HttpResponseForbidden("You are not allowed to edit this task.")

        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if request.POST.get('is_finished', None) == 'on':
                task.is_finished = 1
            else:
                if task.is_finished:
                    task.is_finished = 0
            task.save()
            return redirect('home')
        else:
            # Если данные формы недопустимы, возвращаем страницу регистрации с сообщением об ошибке
            context = {'form': form, 'task': task}
            return render(request, self.template_name, context)


class DeleteTask(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if task.user != request.user:
            return HttpResponseForbidden("You are not allowed to delete this task.")
        task.delete()
        return redirect('home')


class Galery(View):
    def get(self, request):
        pictures = [file for file in os.listdir(os.path.join(settings.BASE_DIR, 'main/static/main/img/carousel')) if not file.startswith('.')]
        context = {'pictures': pictures}
        return render(request, 'main/carousel.html', context)

    def post(self, request):
        if 'file' not in request.FILES:
            return redirect('home')

        f = request.FILES['file']
        pictures = os.listdir(os.path.join(settings.BASE_DIR, 'main/static/main/img/carousel'))
        with open(f'main/static/main/img/carousel/{len(pictures) + 1}.jpg', 'wb') as file:
            file.write(f.read())
        return redirect('galery')













