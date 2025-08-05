from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model() 

def index(request):
    return render(request, 'index.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.", extra_tags='signup')
            return redirect('signin')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created. Please log in.", extra_tags='login')
        return redirect('signin')

    return redirect('signin')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.", extra_tags='login')
            return redirect('signin')
        
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! Welcome back.", extra_tags='login')
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password.", extra_tags='login')
            return redirect('signin')

    return redirect('signin')


def redirect_to_signin(request):
    return redirect('signin')

