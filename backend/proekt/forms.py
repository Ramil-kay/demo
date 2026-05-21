from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from .models import UserProfile, Booking, Review, Hall

class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        min_length=6,
        label='Логин',
        validators=[
            RegexValidator(regex=r'^[a-zA-Z0-9]+$', message='Логин должен содержать только латиницу и цифры'),
            MinLengthValidator(6)
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин (минимум 6 символов)'})
    )
    password = forms.CharField(
        min_length=8,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль (минимум 8 символов)'})
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )
    full_name = forms.CharField(
        max_length=200,
        label='ФИО',
        validators=[
            RegexValidator(regex=r'^[А-Яа-яЁё\s]+$', message='ФИО должно содержать только буквы кириллицы и пробелы')
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'})
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        validators=[
            RegexValidator(regex=r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', message='Формат: 8(XXX)XXX-XX-XX')
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8(999)123-45-67'})
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['hall', 'event_date', 'start_time', 'duration_hours', 'payment_method']
        widgets = {
            'hall': forms.Select(attrs={'class': 'form-select'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
    
    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        from django.utils import timezone
        if event_date and event_date < timezone.now().date():
            raise forms.ValidationError('Дата проведения не может быть в прошлом')
        return event_date

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Поделитесь впечатлениями о мероприятии...'}),
        }