from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User


class UserRegistrationForm(UserCreationForm):
    accepter = forms.BooleanField(required = True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'accepter',
        ]

class LoginForm(forms.Form):
    email = forms.EmailField(label="")  
    password = forms.CharField(label="", widget=forms.PasswordInput) 