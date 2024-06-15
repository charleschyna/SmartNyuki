from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import requests
from .models import Hive

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

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