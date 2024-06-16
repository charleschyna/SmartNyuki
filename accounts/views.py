
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
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

def index(request):
    if request.method == 'POST':
        cl = MpesaClient() 
        phone_number = '0713881169' 
        amount = 1 
        account_reference = 'reference' 
        transaction_desc = 'Description'
        callback_url = 'https://api.darajambili.com/express-payment' 

        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        
        if response.get('ResponseCode') == '0':
            return HttpResponse('Payment request sent successfully. Check your phone for the prompt.')
        else:
            return HttpResponse('Failed to initiate payment. Please try again later.')

    return render(request, 'index.html')

def pay_subscription(request):
    if request.method == 'POST':
        cl = MpesaClient()
    
        phone_number = '0713881169'
        amount = 1
        account_reference = 'reference'
        transaction_desc = 'Description'
        callback_url = 'https://api.darajambili.com/express-payment'
    
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    
        if response.get('ResponseCode') == '0':
            return HttpResponse('Payment request sent successfully. Check your phone for the prompt.')
        else:
            return HttpResponse('Failed to initiate payment. Please try again later.')
    else:
        return HttpResponse('Invalid request method.')



        