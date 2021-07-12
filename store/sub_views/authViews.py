from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from admin_panel.models import *


def register(request):
    return render(request, "register.html")

def login(request):
    return render(request, "login.html")

def save_register(request):
    if request.method == "POST":
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(email=email, name=full_name)
                user.set_password(password1)
                profile = Profile(user=user, full_name=full_name)
                user.save()
                profile.save()
                return redirect('login')
        else:
            messages.info(request, 'Password do not match')
            return redirect('register')
    else:
        messages.info(request, 'Invalid Credentail')
        return redirect('register')


def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_staff:
                return redirect('dash_user_board')
            else:
                redirect('/')
        else:
            messages.info(request, 'Invalid Credentail')
            return redirect('login')
    return render(request, "login.html") 



def logout(request):
    auth.logout(request)
    return redirect("/")