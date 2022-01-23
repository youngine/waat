from email import message_from_binary_file
from django.shortcuts import render
from .models import User_info

def login(request):
    return render(request, 'user/login.html') 

def user_list(request):
    user_list = User_info.objects.all()
    return render(
        request, 'user/user_list.html',
        { 'data': user_list}
    )
