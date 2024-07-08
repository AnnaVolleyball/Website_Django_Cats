import os
from catsite import settings

from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from .forms import RegisterForm, EditProfileForm, TaskForm, EditTaskForm
from .models import User, Task


"""Тестирование моделей"""


class UserModelTest(TestCase):
    fixtures = ['user_fixtures.json']

    def test_user_creation(self):
        # Проверка создания пользователя
        self.user = User.objects.get(username='testuser')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.city, 'Test City')

    def test_user_default_values(self):
        # Проверка значений по умолчанию
        default_user = User.objects.create(username='defaultuser')
        self.assertEqual(default_user.name, 'default name')
        self.assertEqual(default_user.email, 'default@example.com')
        self.assertEqual(default_user.city, 'default city')
        self.assertEqual(default_user.ide, 'default ide')

    def test_user_unique_username(self):
        # Проверка уникальности имени пользователя
        with self.assertRaises(Exception):
            User.objects.create(username='testuser', email='unique@example.com')

    def test_user_unique_email(self):
        # Проверка уникальности email
        with self.assertRaises(Exception):
            User.objects.create(username='uniqueuser', email='testuser@example.com')


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser2',
            name='Test2',
            surname='User2',
            email='testuser2@example.com',
            birth_date='2000-02-02',
            city='Test City2',
            ide='Test IDE2',
            modified_date=timezone.now()
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            task='This is a test task',
            work_size='2 hours',
            start_date=timezone.now().date(),
            end_date=None,
            is_finished=False
        )

    def test_task_creation(self):
        # Проверка создания задачи
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.task, 'This is a test task')
        self.assertEqual(self.task.work_size, '2 hours')
        self.assertEqual(self.task.user.username, 'testuser2')

    def test_task_save_method(self):
        # Проверка метода save
        task = Task.objects.create(
            user=self.user,
            title='New Task',
            task='This is another test task',
            work_size='3 hours'
        )
        self.assertIsNotNone(task.start_date)
        self.assertIsNone(task.end_date)
        self.assertFalse(task.is_finished)

        # Проверяем обновление даты окончания при завершении задачи
        task.is_finished = True
        task.save()
        self.assertIsNotNone(task.end_date)
        self.assertTrue(task.is_finished)

        # Проверяем сброс даты окончания при незавершенной задаче
        task.is_finished = False
        task.save()
        self.assertIsNone(task.end_date)

    def test_task_default_values(self):
        # Проверка значений по умолчанию
        task = Task.objects.create(
            user=self.user,
            title='Default Task',
            task='This is a default task'
        )
        self.assertEqual(task.is_finished, False)
        self.assertIsNotNone(task.start_date)
        self.assertIsNone(task.end_date)

    def test_task_start_date_auto_fill(self):
        # Проверка автозаполнения даты начала
        task = Task.objects.create(
            user=self.user,
            title='Auto Start Date Task',
            task='Task with auto start date'
        )
        self.assertIsNotNone(task.start_date)

    def test_task_end_date_auto_fill(self):
        # Проверка автозаполнения даты окончания
        task = Task.objects.create(
            user=self.user,
            title='Auto End Date Task',
            task='Task with auto end date',
            is_finished=True
        )
        self.assertIsNotNone(task.end_date)

    def test_task_without_user(self):
        # Проверка создания задачи без пользователя
        task = Task.objects.create(
            title='No User Task',
            task='This is a task without user'
        )
        self.assertIsNone(task.user)


"""Тестирование представлений"""


class IndexPageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')


class RegisterTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_post_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'paaassword123',
            'password2': 'paaassword123',
            'email': 'testuser@example.com',
            'name': 'Test',
            'surname': 'User',
            'birth_date': '2000-01-01',
            'city': 'Test City',
            'ide': 'Test IDE'
            })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_post_register_invalid_data(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='testuser@example.com').exists())
        self.assertTemplateUsed(response, 'registration/register.html')


class EditUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_get_edit_profile_page(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/edit_profile.html')

    def test_post_edit_profile(self):
        response = self.client.post(reverse('edit_profile'), {
            'username': 'testuser',
            'name': 'New Name',
            'surname': 'New Surname',
            'email': 'newemail@example.com',
            'birth_date': '2000-01-01',
            'city': 'New City',
            'ide': 'New IDE'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'New Name')

    def test_post_edit_profile_invalid_data(self):
        response = self.client.post(reverse('edit_profile'), {
            'username': 'testuser',
            'name': '',
            'surname': 'New Surname',
            'email': 'invalidemail',
            'birth_date': '2000-01-01',
            'city': 'New City',
            'ide': 'New IDE'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/edit_profile.html')


class TasksTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_get_new_task_page(self):
        response = self.client.get(reverse('new_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/new_task.html')

    def test_post_new_task(self):
        response = self.client.post(reverse('new_task'), {
            'title': 'Test Task',
            'task': 'This is a test task',
            'work_size': '2 hours'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='Test Task').exists())

    def test_post_new_task_invalid_data(self):
        response = self.client.post(reverse('new_task'), {
            'title': '',
            'task': 'This is a test task',
            'work_size': '2 hours'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(task='This is a test task').exists())
        self.assertTemplateUsed(response, 'tasks/new_task.html')


class EditTaskTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            task='This is a test task',
            work_size='2 hours',
            start_date=timezone.now().date()
        )

    def test_get_edit_task_page(self):
        response = self.client.get(reverse('edit_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/edit_task.html')

    def test_post_edit_task(self):
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'title': 'Updated Task',
            'task': 'This is an updated test task',
            'work_size': '3 hours'
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_post_edit_task_invalid_data(self):
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'title': '',
            'task': 'This is an updated test task',
            'work_size': '3 hours'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/edit_task.html')

    def test_post_edit_task_unauthorized(self):
        other_user = User.objects.create_user(username='otheruser', password='password123', email='testuser4@example.com')
        other_task = Task.objects.create(
            user=other_user,
            title='Other Task',
            task='This is a task of another user',
            work_size='2 hours',
            start_date=timezone.now().date()
        )
        response = self.client.post(reverse('edit_task', args=[other_task.id]), {
            'title': 'Updated Task',
            'task': 'This is an updated test task',
            'work_size': '3 hours'
        })
        self.assertEqual(response.status_code, 403)


class DeleteTaskTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123', email='testuser5@example.com')
        self.client.login(username='testuser', password='password123')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            task='This is a test task',
            work_size='2 hours',
            start_date=timezone.now().date()
        )

    def test_delete_task(self):
        response = self.client.get(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_unauthorized(self):
        other_user = User.objects.create_user(username='otheruser', password='password123', email='testuser3@example.com')
        other_task = Task.objects.create(
            user=other_user,
            title='Other Task',
            task='This is a task of another user',
            work_size='2 hours',
            start_date=timezone.now().date()
        )
        response = self.client.get(reverse('delete_task', args=[other_task.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(id=other_task.id).exists())


class GaleryTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_galery_page(self):
        response = self.client.get(reverse('galery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/carousel.html')

    def test_post_galery_upload(self):
        with open(os.path.join(settings.BASE_DIR, 'main/static/main/img/carousel/4.jpeg'), 'rb') as test_file:
            response = self.client.post(reverse('galery'), {'file': test_file})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, 'main/static/main/img/carousel/2.jpeg')))

    def test_post_galery_upload_no_file(self):
        response = self.client.post(reverse('galery'), {})
        self.assertEqual(response.status_code, 302)


"""Тестирование форм"""


class RegisterFormTest(TestCase):

    def test_valid_register_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'passsssword123',
            'password2': 'passsssword123',
            'email': 'testuser@example.com',
            'name': 'Test',
            'surname': 'User',
            'birth_date': '2000-01-01',
            'city': 'Test City',
            'ide': 'Test IDE'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_register_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'passsssword123',
            'password2': 'passsssword1234',  # different password
            'email': 'testuser@example.com',
            'name': 'Test',
            'surname': 'User',
            'birth_date': '2000-01-01',
            'city': 'Test City',
            'ide': 'Test IDE'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class EditProfileFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')

    def test_valid_edit_profile_form(self):
        form_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'name': 'New Name',
            'surname': 'New Surname',
            'birth_date': '2000-01-01',
            'city': 'New City',
            'ide': 'New IDE'
        }
        form = EditProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_edit_profile_form(self):
        form_data = {
            'username': '',
            'email': 'newemail@example.com',
            'name': 'New Name',
            'surname': 'New Surname',
            'birth_date': '2000-01-01',
            'city': 'New City',
            'ide': 'New IDE'
        }
        form = EditProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class TaskFormTest(TestCase):

    def test_valid_task_form(self):
        form_data = {
            'title': 'Test Task',
            'task': 'This is a test task description.',
            'work_size': '2 hours'
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_task_form(self):
        form_data = {
            'title': '',
            'task': 'This is a test task description.',
            'work_size': '2 hours'
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class EditTaskFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            task='This is a test task description.',
            work_size='2 hours',
            is_finished=False
        )

    def test_valid_edit_task_form(self):
        form_data = {
            'title': 'Updated Task',
            'task': 'This is an updated test task description.',
            'work_size': '3 hours',
            'is_finished': True
        }
        form = EditTaskForm(data=form_data, instance=self.task)
        self.assertTrue(form.is_valid())

    def test_invalid_edit_task_form(self):
        form_data = {
            'title': '',
            'task': 'This is an updated test task description.',
            'work_size': '3 hours',
            'is_finished': True
        }
        form = EditTaskForm(data=form_data, instance=self.task)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
