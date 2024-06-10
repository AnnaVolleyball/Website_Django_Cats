from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
        label='Никнейм',
        help_text='Обязательное поле. Введите ваше имя.',
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваш уникальный никнейм'})
    )
    email = forms.EmailField(
        max_length=254,
        help_text='Обязательное поле. Введите действительный адрес электронной почты.',
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваш email'})
    )
    # Остальные поля тоже с placeholderами
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Введите вашу дату рождения'}),
        label='Дата рождения',
        help_text='Обязательное поле. Введите вашу дату рождения.'
    )
    name = forms.CharField(
        max_length=100,
        label='Имя',
        help_text='Обязательное поле. Введите ваше имя.',
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя'})
    )
    surname = forms.CharField(
        max_length=100,
        label='Фамилия',
        help_text='Обязательное поле. Введите вашу фамилию.',
        widget=forms.TextInput(attrs={'placeholder': 'Введите вашу фамилию'})
    )
    city = forms.CharField(
        max_length=100,
        label='Город',
        help_text='Обязательное поле. Введите ваш город.',
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваш город'})
    )
    toy = forms.CharField(
        max_length=100,
        label='Любимая игрушка',
        help_text='Обязательное поле. Введите вашу любимую игрушку.',
        widget=forms.TextInput(attrs={'placeholder': 'Введите вашу любимую игрушку'}))

    class Meta:
        model = User
        fields = ('username', 'name', 'surname', 'email', 'birth_date', 'city', 'toy', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя'
        }


class EditProfileForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username', 'email', 'name', 'surname', 'birth_date', 'city', 'toy']

