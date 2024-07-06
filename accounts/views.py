from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from datetime import datetime
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Threshold
from .utils import send_push_notification
import json, base64
from django.urls import reverse
from django.views.generic import View
from firebase_admin import firestore
import requests
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth import logout
from .models import Hive
from .forms import LoginForm

@csrf_exempt
@login_required
def save_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        if token:
            profile = request.user.profile
            profile.fcm_token = token
            profile.save()
            return JsonResponse({'message': 'Token saved successfully'})
        return JsonResponse({'error': 'No token provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def sensor_data_view(request, hive_id):
    db = firestore.client()
    hive_ref = db.collection('hives').document(hive_id)
    hive_data = hive_ref.get().to_dict()
    
    hive = Hive.objects.get(id=hive_id)
    temperature = hive_data.get('temperature')
    humidity = hive_data.get('humidity')
    sound_level = hive_data.get('sound_level')

    notifications = []
    if temperature is not None:
        if temperature < hive.temperature_threshold_low:
            notifications.append(f"Temperature threshold exceeded: {temperature}°C")
        if temperature > hive.temperature_threshold_high:
            notifications.append(f"Temperature threshold exceeded: {temperature}°C")
    
    if humidity is not None:
        if humidity < hive.humidity_threshold_low:
            notifications.append(f"Humidity threshold exceeded: {humidity}%")
        if humidity > hive.humidity_threshold_high:
            notifications.append(f"Humidity threshold exceeded: {humidity}%")
    
    if sound_level is not None:
        if sound_level > hive.sound_threshold_high:
            notifications.append(f"Sound level threshold exceeded: {sound_level} dB")

    context = {
        'hive_id': hive_id,
        'temperature': temperature,
        'humidity': humidity,
        'sound_level': sound_level,
        'notifications': notifications,
    }
    return render(request, 'profile.html', context)

def send_push_notification(token, title, body):
    server_key = 'BPNsumvdyu5y1tjNslXq5iGDBC6AI_6DRN8EiZVn7UOFLxpp_npNfqNIMEReBIvmdmFBl2EnMJANLsU_LIELOsc'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'key={server_key}',
    }
    payload = {
        'notification': {
            'title': title,
            'body': body,
        },
        'to': token,
    }
    response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=json.dumps(payload))
    print('Notification sent:', response.json())

    
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
            Email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, Email=Email, password=password)
            if user:
                login(request, user)    
                return redirect('dashboard')
        return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'signin.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('reset-email')
        # Perform your logic to send reset email here
        # Example: send_mail(...) or use Firebase functionality

        message = 'Password reset email sent!'
        return render(request, 'password.html_reset', {'message': message})

    return render(request, 'password_reset.html')


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

@login_required
def sensor_data_view(request, hive_id):
    # Retrieve sensor data and check thresholds for a specific hive
    user_token = request.user.profile.fcm_token
    thresholds = Threshold.objects.filter(hive_id=hive_id)

    for threshold in thresholds:
        if sensor_data.exceeds_threshold(threshold):
            message = f"Threshold exceeded for {threshold.parameter}: {sensor_data.value}"
            send_push_notification(user_token, 'Threshold Exceeded', message)

    return render(request, 'sensor_data.html', context)

@login_required
@csrf_exempt  # Temporarily exempt from CSRF for simplicity, handle CSRF properly in production
def initiate_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')  # Assuming 'mpesa' for M-Pesa payment method
        
        # Replace with your actual M-Pesa API endpoint and credentials
        api_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        consumer_key = 'your_consumer_key'
        consumer_secret = 'your_consumer_secret'

        # Replace with your logic to fetch user's phone number
        user_phone_number = request.user.profile.Phone  # Replace with how you retrieve user's phone number

        # Construct your request to M-Pesa API
        headers = {
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # Replace with actual OAuth2 access token
            'Content-Type': 'application/json',
        }
        payload = {
            'BusinessShortCode': 'YOUR_BUSINESS_SHORTCODE',
            'Password': 'YOUR_PASSWORD',
            'Timestamp': 'YYYYMMDDHHMMSS',
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': '1000',  # Replace with actual subscription amount
            'PartyA': user_phone_number,
            'PartyB': 'YOUR_PAYBILL_NUMBER',
            'PhoneNumber': user_phone_number,
            'CallBackURL': 'YOUR_CALLBACK_URL',
            'AccountReference': 'YOUR_ACCOUNT_REFERENCE',
            'TransactionDesc': 'Subscription Payment',
        }

        try:
            response = requests.post(api_endpoint, headers=headers, json=payload)
            response_data = response.json()
            # Process the response from M-Pesa API, handle success or failure
            return JsonResponse({'success': True})  # Example response
        except Exception as e:
            print(f"Error initiating payment: {e}")
            return JsonResponse({'success': False, 'error': str(e)})  # Example error response

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
        