from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from .models import  User_info
from django.http import HttpResponse

def login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            u = User_info.objects.get(user_id=username, user_pw=password)
            user = authenticate(username=username, password=password)
            login(request, user)

        except User_info.DoesNotExist as e:
            return HttpResponse('로그인 실패')
    else:
        return redirect('/app/main/')


def user_list(request):
    data = User_info.objects.all()
    return render(
        request, 'user/user_list.html',
        { 'data': data}
    )
