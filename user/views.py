from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,redirect
from .models import  User_info
from django.http import HttpResponse
from .forms import UserForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

def signin(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None: 
            login(request, user)
            request.session['user_id'] = username
            request.session['user_pw'] = password
            return HttpResponseRedirect(reverse('app:funding_main'))    
            # return redirect('/app/main/')
        else:
            return HttpResponseRedirect(reverse('user:signin'))    
            # render(request,'user/signin.html')  # 값 전달이 안된다는 오류를 리다이렉트로 해결함...
    else:
        return render(request,'user/signin.html')


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user_id = username
            user_pw = raw_password
            user_name = form.cleaned_data.get('last_name')
            user_email =form.cleaned_data.get('email')
            
            m = User_info(user_id=user_id, user_pw=user_pw, user_name=user_name,user_email=user_email)
            m.save()
            
            return HttpResponseRedirect(reverse('user:signin'))
            # return redirect('/user/signin/')
    else:
        form = UserForm()
    return render(request,'user/signup.html',{'form': form})




def signout(request):
    logout(request)
    return redirect('/app/main/')
