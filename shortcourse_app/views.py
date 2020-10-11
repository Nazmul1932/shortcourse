from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from shortcourse_app.EmailBackend import EmailBackend
from django.contrib import messages
from .models import *


def login_user(request):
    return render(request, 'login.html')


def do_login(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Method not allowed</h1>')
    else:
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            if user.user_type == '1':
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == '2':
                return HttpResponseRedirect(reverse('instructor_home'))
            else:
                return HttpResponseRedirect(reverse('student_home'))

        else:
            messages.error(request, 'Invalid login details')
            return HttpResponseRedirect('login_user')


def get_user_details(request):
    if request.user is not None:
        return HttpResponse('User : '+request.user.email+ 'User_Type : '+request.user.user_type)
    else:
        return HttpResponse('Please Login First')


def logout_user(request):
    logout(request)
    return redirect('login_user')


def signup_admin(request):
    return render(request, 'signup_admin_page.html')


def signup_student(request):
    return None


def signup_instructor(request):
    return None