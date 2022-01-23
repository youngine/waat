import re
from django.forms import forms
from django.shortcuts import render
from django.http import HttpResponse
from .models import FundingBoard, User1, JoinFund, Post, FundingFunc
from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy

from .saveData import DataContent
from django.contrib import messages

from django.shortcuts import render,redirect


def select(request):
    data = FundingBoard.objects.all()

    result = []

    for d in data:
        
        result.append({
            "board_id" : d.board_id,
            "user_id" : d.user_id,
            "title" : d.title,
            "content" : d.content,
            "fund_goal_price" : d.fund_goal_price,
            "fund_total_price" : d.fund_total_price,
            "percent" : int(d.fund_total_price / d.fund_goal_price * 100)

        })


    

    return render(
        request,
        'fund_view/main.html',
        {
            "data" : result,

        }
    )

def detail(request, board_id):
    data = FundingBoard.objects.filter(board_id=board_id)
    join_data = FundingFunc.objects.filter(board_id =board_id)
    result = []

    for j in join_data:
        func_a_expl = j.func_a_expl
        func_b_expl = j.func_b_expl
        func_c_expl = j.func_c_expl
        func_a_price = j.func_a_price
        func_b_price = j.func_b_price
        func_c_price = j.func_c_price
        

    for d in data:
        
        result.append({
            "board_id" : d.board_id,
            "user_id" : d.user_id,
            "title" : d.title,
            "content" : d.content,
            "fund_goal_price" : d.fund_goal_price,
            "fund_total_price" : d.fund_total_price,
             "percent" : int(d.fund_total_price / d.fund_goal_price * 100),
             "func_a_price" : func_a_price,
             "func_b_price" : func_b_price,
             "func_c_price" : func_c_price,
             "func_a_expl" : func_a_expl,
             "func_b_expl" : func_b_expl,
             "func_c_expl" : func_c_expl,
             
             
             

        })
    print(result)
    return render(
        request,
        'fund_view/fund_detail.html',
        {
            "data" : result,
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
        return render(request, 'fundingapp/step1.html')

    def post(self, request, *args, **kwargs):
        request.session['step1_complete'] = True
        print(request.session['step1_complete'])
        return HttpResponseRedirect(reverse('fundingapp:step2'))


class Step2View(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('step1_complete', False):
            raise PermissionDenied
        request.session['step1_complete'] = False
        return render(request, 'fundingapp/step2.html')

    def post(self, request, *args, **kwargs):
        request.session['step2_complete'] = True
        return HttpResponseRedirect(reverse('fundingapp:step3'))


class Step3View(View):

    def get(self, request, *args, **kwargs):
        if not request.session.get('step2_complete', False):
            raise PermissionDenied
        request.session['step2_complete'] = False
        return render(request, 'fundingapp/step3.html')
