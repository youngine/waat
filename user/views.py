from django.shortcuts import render,redirect
from .models import  User_info
from django.contrib import messages
from django.http import  HttpResponseRedirect
from django.urls import reverse

def signin(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User_info.objects.get(user_id = username)
            if password != user.user_pw:
                messages.info(request, '비밀번호를 확인해주세요.')
                return HttpResponseRedirect(reverse('user:signin'))   
            else:
                username = user.user_id
        except User_info.DoesNotExist as e:
                messages.info(request, '확인되지 않는 아이디입니다.')
                return HttpResponseRedirect(reverse('user:signin'))   
        else:
            request.session['user'] = username
            return HttpResponseRedirect(reverse('app:funding_main'))    
    else:
        return render(request,'user/signin.html')


def signup(request):
    if request.method == 'POST':

        user_id = request.POST.get('username')
        user_pw =  request.POST.get('password1')
        user_pw_check =request.POST.get('password2')
        user_name = request.POST.get('last_name')
        user_email = request.POST.get('email')

        if user_pw_check != user_pw:
            messages.info(request, '비밀번호가 일치하지 않습니다.')
            return HttpResponseRedirect(reverse('user:signup'))   
        try:
            user = User_info.objects.get(user_id = user_id)
            messages.info(request, '존재하는 아이디입니다.')
            return HttpResponseRedirect(reverse('user:signup'))   
        except User_info.DoesNotExist as e:
            m = User_info(user_id=user_id, user_pw=user_pw, user_name=user_name,user_email=user_email)
            m.save()
            return HttpResponseRedirect(reverse('user:signin'))   
    else:
        return render(request,'user/signup.html')



def signout(request):
    del request.session['user']
    return redirect('/app/main/')


def usercheck(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        login_user =  request.session.get('user')

        try:
            user = User_info.objects.get(user_id = username, user_email=email)
            if user.user_id != login_user:
                messages.info(request, '현재 사용자와 아이디가 일치하지 않습니다.')
                return HttpResponseRedirect(reverse('user:usercheck'))
            else:
                messages.info(request, '변경할 비밀번호를 입력해주세요.')
                return HttpResponseRedirect(reverse('user:pwchange'))
        except User_info.DoesNotExist as e:
            messages.info(request, '아이디와 이메일을 확인해주세요.')
            return HttpResponseRedirect(reverse('user:usercheck'))  
    else:
         messages.info(request, '아이디와 이메일을 입력하시면 　비밀번호 변경이 가능합니다.')
         return render(request,'user/usercheck.html')


def pwchange(request):
    if request.method == 'POST':
        username = request.session.get('user')
        user_pw =  request.POST.get('password1')
        user_pw_check =request.POST.get('password2')

        if user_pw_check != user_pw:
            messages.info(request, '비밀번호가 일치하지 않습니다.')
            return HttpResponseRedirect(reverse('user:pwchange'))   
        else:
            user = User_info.objects.get(user_id = username)
            user.user_pw = user_pw
            user.save()
            del request.session['user']
            messages.info(request, '　비밀번호가 변경되었습니다.　　다시 로그인 해주세요.')
            return HttpResponseRedirect(reverse('user:signin'))   

    return render(request,'user/pwchange.html')
