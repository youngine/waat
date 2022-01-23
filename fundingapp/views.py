import re
from django.forms import forms
from django.shortcuts import render
from django.http import HttpResponse
from .models import FundingBoard, User1, JoinFund, Post
from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy

from .saveData import DataContent
from django.contrib import messages

from django.shortcuts import render,redirect
from django.views import View  
from django.shortcuts import redirect, render  
from django.core.exceptions import PermissionDenied

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
        'fund_view/fund_detail.html',
        {
            "data" : data,
        }
    )

### 참고 소스 엄청 드러움.... 리팩토링 해야하는데.... DB부터 데이터 입력 가능한지 테스트 후 리팩토링 해야한다. 안쓰는 코드 다량 많음. 더미 코드 많다는 뜻임 -> 종원
class Create1(View):
    def get(self, request, *args, **kwargs):
        request.session['step1_complete'] = False
        request.session['step2_complete'] = False
        # title =  request.session['title'] 
        # print("제목 : ",title)
        return render(request, 'fundingapp/create_step1.html')  # ,{"title":title}

    def post(self, request, *args, **kwargs):
        request.session['step1_complete'] = True
        # 이거 필요없는코드
        # title = request.POST['title']
        # category=request.POST['category']
        # language=request.POST['language']
        # target = request.POST['target']
        # eqA = request.POST['eqA']
        # eqB = request.POST['eqB']
        # eqC = request.POST['eqC']
        # imgefile = request.POST['imgefile']

        request.session['title'] = request.POST['title']
        request.session['category'] = request.POST['category']
        request.session['language'] = request.POST['language']
        request.session['target'] = request.POST['target']
        request.session['eqA'] = request.POST['eqA']
        request.session['eqB'] = request.POST['eqB']
        request.session['eqC'] = request.POST['eqC']
        request.session['imgefile'] = request.POST['imgefile']
        return HttpResponseRedirect(reverse('fundingapp:create2'))

class Create2(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('step1_complete', False):
            raise PermissionDenied
        request.session['step1_complete'] = False
        return render(request, 'fundingapp/create_step2.html')

    def post(self, request, *args, **kwargs):
        # print("이전 버튼 눌렀음 : ",request.POST.get("before",0))
        if request.POST.get("next",0) =="다음":
            request.session['step2_complete'] = True
            # 이것도 필요없는 코드
            # intro = request.POST['intro']
            # background=request.POST['background']
            # objects=request.POST['objects']

            request.session['intro'] = request.POST['intro']
            request.session['background'] = request.POST['background']
            request.session['objects'] = request.POST['objects']

            # request.session['title'] = request.session['title']
            # request.session['category'] = request.session['category']
            # request.session['language'] = request.session['language']
            # request.session['target'] = request.session['target'] 
            # request.session['eqA'] = request.session['eqA']
            # request.session['eqB'] = request.session['eqB']
            # request.session['eqC'] = request.session['eqC']
            # request.session['imgefile'] = request.session['imgefile']
        
            print(request.session['imgefile'])
            return HttpResponseRedirect(reverse('fundingapp:create3'))
        if request.POST.get("before",0) =="이전":
            print(request.session['title'])
            return HttpResponseRedirect(reverse('fundingapp:create1'))

class Create3(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('step2_complete', False):
            raise PermissionDenied
        request.session['step2_complete'] = False
        return render(request, 'fundingapp/create_step3.html')

    def post(self, request, *args, **kwargs):
        if request.POST.get("finsh",0) =="완료":
            developContent = request.POST['developContent']
            # p1 = request.POST['p1']
            # p2 = request.POST['p2']
            # p3 = request.POST['p3']
            # p4 = request.POST['p4']

            # 세션에 다 저장이 됨. 그래서 삭제를 해야하는데 삭제는 del을 통해 삭제가 가능
            # request.session['intro'] = request.session['intro'] 
            # request.session['background'] = request.session['background']
            # request.session['objects'] = request.session['objects']

            # request.session['title'] = request.session['title']
            # request.session['category'] = request.session['category']
            # request.session['language'] = request.session['language']
            # request.session['target'] = request.session['target'] 
            # request.session['eqA'] = request.session['eqA']
            # request.session['eqB'] = request.session['eqB']
            # request.session['eqC'] = request.session['eqC']
            # request.session['imgefile'] = request.session['imgefile']

            # 삭제전 세션에 저장된 데이터 DB에 저장하기.
            # 여기부터 DB 코드임.-> 종원

            del request.session['intro']
            del request.session['title']

            return HttpResponseRedirect(reverse('app:funding_main'))
        if request.POST.get("before",0) =="이전":
            request.session['step1_complete'] = True
            return HttpResponseRedirect(reverse('fundingapp:create2'))
"""
주석 파일. 테스트 해본다고 만든 소스코드 -> 종원
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
"""