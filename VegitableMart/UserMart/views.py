from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user
from GreenApp.models import Customer
from django.core.mail import send_mail
from .models import UserOTP
from django.conf import settings
# Create your views here.

import random
def signup(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        if get_otp:
            get_usr = request.POST.get('user')
            usr = User.objects.get(username=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.success(request, f'Account is verified for {usr.email}, Now Login {usr.username}!!')
                return redirect('login')
            else:
                messages.warning(request, f'You entered wrong OTP')
                return render(request, 'UserMart/signup.html', {'otp': True, 'user': usr})

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        if request.POST['password1'] == request.POST['password2']:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('signup')
            else:

                user = User.objects.create_user(username=username, password=password1, first_name=first_name,
                                              last_name=last_name, email=email)
                usr = User.objects.get(username=username)
                user.is_active = False
                user.save()
                usr_otp=random.randint(100000,999999)
                UserOTP.objects.create(user=user, otp=usr_otp)
                mess = f"Hello {user.first_name.upper()},\nYour OTP is {usr_otp}\n"
                send_mail(
                     "Welcome to Mukesh E-Mart - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
                username = request.POST.get('username')
                messages.info(request, username.capitalize() + ' ' + 'registered successfully !')
                return render(request, 'UserMart/signup.html',{'otp':True,'user':user})
        else:
            messages.error(request, 'Invalid Password')
            return render(request, 'UserMart/signup.html')

    else:
        return render(request, 'UserMart/signup.html')

# @unauthenticated_user
def MartLogin(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == "GET":
        return render(request, 'UserMart/login.html', {'form': AuthenticationForm()})
    else:
        get_otp = request.POST.get('otp')
        if get_otp:
            get_usr = request.POST.get('user')
            usr = User.objects.get(username=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.success(request, f'Account is verified for {usr.email}, Now Login {usr.username}!!')
                return redirect('login')
            else:
                messages.warning(request, f'You entered wrong OTP')
                return render(request, 'UserMart/signup.html', {'otp': True, 'user': usr})

        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        username = request.POST.get('username')
        if user is not None:
            login(request, user)
            messages.success(request, username.capitalize() + ' ' + 'successfully logged in !')
            return redirect('home')
        elif not User.objects.filter(username=username).exists():
            messages.warning(request,f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login')
        elif not User.objects.get(username=username).is_active:
            user = User.objects.get(username=username)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=usr_otp)
            mess = f"Hello {user.first_name.upper()},\nYour OTP is {usr_otp}\n"

            send_mail(
                "Welcome to Mukesh E-Mart - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            return render(request, 'UserMart/login.html', {'otp': True, 'user': user})
        # else:
        #     messages.warning(request,
        #                      f'Please enter a correct username and password')
        #     return redirect('login')

        messages.error(request, 'Invalid Username and Password ')
    return render(request, 'UserMart/login.html', {'form': AuthenticationForm()})


def MartLogout(request):
    username = request.user.customer
    logout(request)
    messages.success(request, f'{username} successfully logged Out !')
    return redirect('login')





def resend_otp(request):
    if request.method == "GET":
        get_usr = request.GET.get('user')
        print(get_usr)
        if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
            user = User.objects.get(username=get_usr)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user = user, otp = usr_otp)
            mess = f"Hello {user.first_name.upper()},\nYour OTP is {usr_otp}\n"
            send_mail(
                "Welcome to Mukesh E-Mart - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently = False
            )
            return HttpResponse("Resend")

    return HttpResponse("Can't Send ")



