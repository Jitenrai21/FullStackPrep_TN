from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model() 

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('signin')


def signin(request):
    return render(request, 'signin.html')


def demo(request):
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

from django.template.context_processors import csrf

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST['email']
        password = request.POST['password']

        user = None
        try:
            user_obj = User.objects.get(email=identifier)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username/email or password')
            context = {}
            context.update(csrf(request))
            return render(request, 'signin.html', context)

    return redirect('signin')

def redirect_to_signin(request):
    return redirect('signin')



otp_store = {}

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            otp_store[email] = otp

            # Send OTP
            send_mail(
                'Your Password Reset OTP',
                f'Your OTP is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            request.session['reset_email'] = email
            messages.success(request, 'OTP sent to your email.')
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'Email is not registered.')
            return redirect('password/forgot_password')
    return render(request, 'password/forgot_password.html')


def verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        entered_otp = request.POST.get('otp')

        if email and otp_store.get(email) == int(entered_otp):
            messages.success(request, 'OTP verified. Please reset your password.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP.')
            return redirect('verify_otp')
    return render(request, 'password/verify_otp.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        new_password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            otp_store.pop(email, None)
            request.session.pop('reset_email', None)
            messages.success(request, 'Password reset successful.')
            return redirect('signin')
        except User.DoesNotExist:
            messages.error(request, 'Something went wrong.')
            return redirect('forgot_password')
    return render(request, 'password/reset_password.html')