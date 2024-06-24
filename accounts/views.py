from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json, base64
from django.urls import reverse
from django.views.generic import View
import requests
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth import logout
from .models import Hive
from .forms import HiveForm, LoginForm


def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def signup(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! - You are successflly SignUped!")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
        return redirect('signin')
    else:
        form = LoginForm()
    return render(request, 'signup.html',{'form':form})

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('dashboard')
        return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'signin.html', {'form': form})


def hives(request):
    return render(request, 'hives.html')

def subscription(request):
    return render(request, 'subscription.html')

def profile(request):
    return render(request, 'profile.html')


def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('logout')
    return render(request, 'signin.html')

def settings(request):
    return render(request, 'settings.html')

@csrf_exempt
def mpesa_stk_push(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')  # Assuming amount is passed from the form
        phone_number = request.POST.get('phone_number')  # Get phone number from form or session

        # Construct the request payload for M-Pesa STK push
        payload = {
            'BusinessShortCode': settings.MPESA_SHORTCODE,
            'Password': settings.MPESA_PASSWORD,
            'Timestamp': datetime.now().strftime('%Y%m%d%H%M%S'),
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,  # Customer's phone number
            'PartyB': settings.MPESA_SHORTCODE,
            'PhoneNumber': phone_number,  # Customer's phone number
            'CallBackURL': settings.MPESA_CALLBACK_URL,
            'AccountReference': 'YourAppName',
            'TransactionDesc': 'Payment for Premium Plan',
        }

        # Make request to M-Pesa API
        response = requests.post(settings.MPESA_STK_PUSH_URL, json=payload, headers={
            'Authorization': 'Bearer {}'.format(get_access_token()),  # Implement get_access_token() function
            'Content-Type': 'application/json'
        })

        # Process M-Pesa API response
        if response.status_code == 200:
            # Payment request successfully initiated
            return HttpResponse("Payment request initiated successfully.")
        else:
            # Handle errors appropriately
            return HttpResponse("Failed to initiate payment request. Error: {}".format(response.text), status=response.status_code)
    else:
        return HttpResponse(status=405)  # Method not allowed


        