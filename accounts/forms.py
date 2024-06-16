from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
import requests
from .models import Hive

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    widgets = {
            'username':forms.TextInput(attrs={'class':'form-control '}),
            'email':forms.TextInput(attrs={'class':'form-control '}),
            'password1':forms.TextInput(attrs={'class':'form-control'}),
            'password2':forms.EmailInput(attrs={'class':'form-control'}),
            }
        
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class MpesaClient:
    def __init__(self):
        self.base_url = 'https://sandbox.safaricom.co.ke/'
        self.auth_token = 'your_auth_token_here'
        self.headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }

    def stk_push(self, phone_number, amount, account_reference, transaction_desc, callback_url):
        url = f'{self.base_url}/mpesa/stkpush/v1/processrequest'
        payload = {
            'BusinessShortCode': 'your_business_short_code',
            'Password': 'your_password', 
            'Timestamp': 'your_timestamp',  
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': 'your_business_short_code',
            'PhoneNumber': phone_number,
            'CallBackURL': callback_url,
            'AccountReference': account_reference,
            'TransactionDesc': transaction_desc
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

class HiveForm(forms.ModelForm):
    class Meta:
        model = Hive
        fields = ['name', 'temperature', 'humidity', 'sound', 'weight']