from django import forms
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from datetime import datetime
import base64
import json
from .models import Hive

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    remember_me = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
        
class LoginForm(AuthenticationForm):
        Email = forms.EmailField(widget=forms.TextInput(attrs={'autocomplete': 'email'}), required=True)
        password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}), required=True)



''' class HiveForm(forms.ModelForm):
    class Meta:
        model = Hive
        fields = ['name', 'temperature', 'humidity', 'sound', 'weight'] '''