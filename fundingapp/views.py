import re
from django.forms import forms
from django.shortcuts import render
from .models import FundingBoard, User1, JoinFund, Post
from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy

from .saveData import DataContent
from django.contrib import messages

from django.shortcuts import render,redirect

def select(request):
    data = FundingBoard.objects.all()


    img = []
    for d in data:
        img.append("/static/" + str(d.board_id) + "jpg")

    return render(
        request,
        'fund_view/main.html',
        {
            "data" : data,
            "img" : img
        }
    )

def get_info(request):
    print("받음")
    return render(request, 'fundingapp/get_info.html')

def create(request):
    DT = DataContent()
    if request.method == 'POST':
        question_id =1
        title=request.POST['title'],
        category=request.POST['category'],
        language=request.POST['language'],
        print("title : ",title , " category : ", category)
        DT.set_1Page(title,category)
        # messages.success(request, DT.category)
        # HttpResponseRedirect(fundingapp:get_info)
        return render(request, 'fundingapp/get_info.html', {"DT" : DT})

    return render(request, 'fundingapp/create.html')


from django.views import View  
from django.shortcuts import redirect, render  
from django.core.exceptions import PermissionDenied


class Step1View(View):

    def get(self, request, *args, **kwargs):
        request.session['step1_complete'] = False
        request.session['step2_complete'] = False
        return render(request, 'step1.html')

    def post(self, request, *args, **kwargs):
        request.session['step1_complete'] = True
        return redirect(reverse('step2'))


class Step2View(View):

    def get(self, request, *args, **kwargs):
        if not request.session.get('step1_complete', False):
            raise PermissionDenied
        request.session['step1_complete'] = False
        return render(request, 'step2.html')

    def post(self, request, *args, **kwargs):
        request.session['step2_complete'] = True
        return redirect(reverse('step3'))


class Step3View(View):

    def get(self, request, *args, **kwargs):
        if not request.session.get('step2_complete', False):
            raise PermissionDenied
        request.session['step2_complete'] = False
        return render(request, 'step3.html')