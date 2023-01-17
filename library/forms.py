from django import forms
from .models import Book, Supplier, Order, Pos_order, Cheque

import re
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class BookForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        min_length=2,
        strip=True,
        label='Название фрукта')
    description = forms.CharField(
        max_length=150,
        min_length=2,
        strip=True,
        label='Описание фрукта',
        widget=forms.Textarea,
        initial="Описание")
    price = forms.FloatField(
        min_value=1,
        # step_size=10,
        label='Цена фрукта',
        initial=40)
    date_expired = forms.DateField(
        label='Дата просрочки фрукта',
        # widget=forms.SelectDateWidget,
        help_text='Укажите дату просрочки указанную на упаковке')
    photo = forms.ImageField(
        required=False,
        label='Фотография фрукта')
    supplier = forms.ModelChoiceField(  # Вывод выбора поставщика
        queryset=Supplier.objects.all(),
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # Валидация
    # required=True - обязательное поле
    # max_length - максимальная длина текста
    # min_length - минимальная длина текста
    # max_value - максимальное значение числа
    # max_value - минимальное значение числа
    # step_size - шаг при установки числового значения

    # Стили
    # label - Вывод названия
    # widget - Указания типа поля
    # initial - Значение по умолчанию
    # help_text - подсказка под полем


class SupplierForm(forms.ModelForm):  # Наследование формы для моделей (таблиц)
    class Meta:
        model = Supplier
        fields = '__all__' # Использование всех полей (не реком.)
        # fields = ['title', 'agent_name', 'agent_firstname', 'agent_patronymic', 'exist']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'floatingInput',
                    'placeholder': 'Название'
                }
            ),
            'agent_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя',
                }
            ),
            'agent_firstname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия',

                }
            ),
            'agent_patronymic': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Отчество',
                }
            ),
            'exist': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Поле не должно начинаться с цифры')
        return title

        # r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2}'
        # r'\+7\([0-9][0-9][0-9]\)[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


# email
class ContactForm(forms.Form):
    recipient = forms.EmailField(
        label='Получатель',
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    subject = forms.CharField(
        label='Тема письма',
        widget=forms.TextInput(
            attrs={'class':'form-control'}
        )
    )
    content = forms.CharField(
        label='Тело письма',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 8
            }
        )
    )
