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

class PaySubscription(View):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        amount = 9999.99  # Amount for the subscription

        # Prepare the necessary credentials and endpoint URLs
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        shortcode = settings.MPESA_SHORTCODE
        lipa_na_mpesa_online_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

        # Get the access token
        response = requests.get(token_url, auth=(consumer_key, consumer_secret))
        access_token = response.json().get('access_token')

        # Prepare the headers
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        # Generate the password
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        passkey = settings.MPESA_PASSKEY
        data_to_encode = f'{shortcode}{passkey}{timestamp}'
        encoded_string = base64.b64encode(data_to_encode.encode('utf-8')).decode('utf-8')

        # Prepare the payload
        payload = {
            'BusinessShortCode': shortcode,
            'Password': encoded_string,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': shortcode,
            'PhoneNumber': phone_number,
            'CallBackURL': request.build_absolute_uri(reverse('mpesa_callback')),
            'AccountReference': 'Subscription',
            'TransactionDesc': 'Payment for subscription',
        }

        # Send the STK push request
        response = requests.post(lipa_na_mpesa_online_url, headers=headers, json=payload)
        response_data = response.json()

        if response_data.get('ResponseCode') == '0':
            # Successfully initiated
            return redirect('subscription_success')
        else:
            # Handle the error case
            return redirect('subscription_failed')
        
class MpesaCallback(View):
    def post(self, request):
        # Safaricom sends the data in JSON format
        mpesa_response = json.loads(request.body.decode('utf-8'))

        # Extract useful data from the response
        result_code = mpesa_response['Body']['stkCallback']['ResultCode']
        result_desc = mpesa_response['Body']['stkCallback']['ResultDesc']
        # Save this information to your database as needed

        return JsonResponse({'status': 'ok'})

class HiveForm(forms.ModelForm):
    class Meta:
        model = Hive
        fields = ['name', 'temperature', 'humidity', 'sound', 'weight']