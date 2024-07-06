from django.conf import settings
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
    ide = models.CharField(max_length=100, null=False, blank=False, default='default ide')
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='tasks', default=None, null=True)
    title = models.CharField('Название', max_length=100, null=False, blank=False)
    task = models.TextField('Описание', null=False, blank=False)
    work_size = models.CharField('Время на задачу', max_length=100, null=True)
    start_date = models.DateField('Дата начала', default=None, null=True)
    end_date = models.DateField('Дата окончания', default=None, null=True)
    is_finished = models.BooleanField('Закончена?', default=False)

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()
        if self.is_finished:
            self.end_date = timezone.now().date()
        elif not self.is_finished:
            self.end_date = None
        super().save(*args, **kwargs)

    def __repr__(self):
        return f'<Task> {self.title}, {self.task}, {self.work_size}, {self.start_date}, {self.end_date}, {self.is_finished}'

    def __str__(self):
        return f'<Task> {self.title}, {self.task}, {self.work_size}, {self.start_date}, {self.end_date}, {self.is_finished}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'