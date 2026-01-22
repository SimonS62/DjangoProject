from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)  # Только email и пароль для регистрации

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label="Email", max_length=254) # Обязательное поле email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_field = User._meta.get_field('email')
