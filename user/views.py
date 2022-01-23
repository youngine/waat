from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,redirect
from .models import  User_info
from django.http import HttpResponse
from django.contrib import messages

def signin(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None: 
            login(request, user)
            request.session['user_id'] = username
            request.session['user_pw'] = password    
            return redirect('/app/main/')
        else:
            render(request,'user/signin.html')
    else:
        return render(request,'user/signin.html')


def signout(request):
    logout(request)
    return redirect('/app/main/')
