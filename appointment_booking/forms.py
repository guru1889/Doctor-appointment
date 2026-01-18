from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )



class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = [
            'name',
            'username',
            'email',
            'date_of_birth',
            'mobile',
            'image'
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise forms.ValidationError("Password does not match")
