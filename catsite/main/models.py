import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=False, blank=False, default='username')
    name = models.CharField(max_length=100, null=False, blank=False, default='default name')
    surname = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=False, blank=False, default='default@example.com')
    birth_date = models.DateField(null=True)
    city = models.CharField(max_length=100, null=False, blank=False, default='default city')
    toy = models.CharField(max_length=100, null=False, blank=False, default='default toy')
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='tasks')
    title = models.CharField('Название', max_length=100)
    task = models.TextField('Описание')
    date = models.DateField('Дата', default=datetime.date.today())

    def __repr__(self):
        return f'<Task> {self.title}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'