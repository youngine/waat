import re,os
from django.forms import forms
from django.shortcuts import render
from django.http import HttpResponse
from .models import FundingBoard, User1, JoinFund
from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from .saveData import DataContent
from django.contrib import messages
from django.shortcuts import render,redirect
from django.views import View  
from django.shortcuts import redirect, render  
from django.core.exceptions import PermissionDenied

import datetime


def select(request):
    data = FundingBoard.objects.all()
    result = []
    for d in data:
        result.append({
            "board_id" : d.board_id,
            "user_id" : d.user_id,
            "title" : d.title,
            "content" : d.intro	,
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
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def detail(request, board_id):

    # 현재는 root 아이디로 들어왔다고 가정하고 진행
    if request.method == 'POST':
        
        
        try:
            user_name = request.session['user']
        except KeyError as k:

            request.session['detail_funding'] = (True, board_id)
            return HttpResponseRedirect(reverse('user:signin'))

        # selected : 현재 선택 된 펀딩 목록 (1~3)
        selected = request.POST.getlist('func_check')

        data = FundingBoard.objects.get(board_id=board_id)

        total_price = 0
        result_list = []
        # 아무것도 선택을 안한상태
        if len(selected) == 0:

            # 첫 페이지 혹은 selelct 이거는 정해야할듯?
            return HttpResponseRedirect(reverse('fundingapp:select'))


        else:
            for i in selected:
                if i == "1":
                    result_list.append("1")
                    total_price += data.func_a_price
                elif i == "2":
                    result_list.append("2")
                    total_price += data.func_b_price
                elif i == "3":
                    result_list.append("3")
                    total_price += data.func_c_price

        # for i in fund_data:
        join_db = JoinFund()
        # 유저 이름
        join_db.user_id = user_name
        join_db.board_id = board_id
        join_db.fund_price = total_price
        join_db.fund_join_list = result_list
        
        join_db.save()

        # data : 현재 선택 된 게시물 정보
        # data = FundingBoard.objects.get(board_id=board_id)
        data.fund_total_price += total_price
        data.save()

        return HttpResponseRedirect(reverse('fundingapp:select'))
        
    data = FundingBoard.objects.filter(board_id=board_id)

    result = []      

    for d in data:
        result.append({
            "board_id" : d.board_id,
            "user_id" : d.user_id,
            "title" : d.title,
            "content" : d.intro,
            "fund_goal_price" : d.fund_goal_price,
            "fund_total_price" : d.fund_total_price,
             "percent" : int(d.fund_total_price / d.fund_goal_price * 100),
             "func_a_price" : d.func_a_price,
             "func_b_price" : d.func_b_price,
             "func_c_price" : d.func_c_price
             
        })

    return render(
        request,
        'fund_view/fund_detail.html',
        {
            "data" : result,
        }
    )

### 참고 소스 엄청 드러움.... 리팩토링 해야하는데.... DB부터 데이터 입력 가능한지 테스트 후 리팩토링 해야한다. 안쓰는 코드 다량 많음. 더미 코드 많다는 뜻임 -> 종원
class Create1(View):
    def get(self, request, *args, **kwargs):
        request.session['step1_complete'] = False
        request.session['step2_complete'] = False
        if len(request.session.get('user',"")) ==0:
            return HttpResponseRedirect(reverse('user:signin'))
        else:
            return render(request, 'fundingapp/create_step1.html') 

    def post(self, request, *args, **kwargs):
        request.session['step1_complete'] = True
        request.session['title'] = request.POST['title']
        request.session['category'] = request.POST['category']
        request.session['language'] = request.POST['language']
        request.session['target'] = request.POST['target']
        request.session['eqA'] = request.POST['eqA']
        request.session['eqB'] = request.POST['eqB']
        request.session['eqC'] = request.POST['eqC']
        
        upload_file = request.FILES.get('file',"")
        if len(upload_file) !=0: 
            path = os.path.join("media/img/",upload_file.name)        
            with open(path, 'wb') as file:
                file.write(upload_file.read())
                for chunk in upload_file.chunks():
                    file.write(chunk)
            print("저장위치 : ",path)
            request.session['imgefile'] = path
        else:
            request.session['imgefile'] = ""
        return HttpResponseRedirect(reverse('fundingapp:create2'))

class Create2(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('step1_complete', False):
            raise PermissionDenied
        request.session['step1_complete'] = False
        return render(request, 'fundingapp/create_step2.html')

    def post(self, request, *args, **kwargs):
        if request.POST.get("next",0) =="다음":
            request.session['step2_complete'] = True
            request.session['intro'] = request.POST['intro']
            request.session['background'] = request.POST['background']
            request.session['objects'] = request.POST['objects']

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
            # 세션에 다 저장이 됨. 그래서 삭제를 해야하는데 삭제는 del을 통해 삭제가 가능
            # 삭제전 세션에 저장된 데이터 DB에 저장하기.
            # 여기부터 DB 코드임.-> 종원

            FDB = FundingBoard()

            FDB.user_id = request.session['user']
            
            FDB.title = request.session['title']
            FDB.category = request.session['category']
            FDB.language_text = request.session['language']
            FDB.target = request.session['target']
            
            FDB.func_a_price = request.session['eqA']
            FDB.func_b_price = request.session['eqB']
            FDB.func_c_price = request.session['eqC']

            FDB.file_name = request.session['imgefile']
            FDB.intro = request.session['intro']
            FDB.background_text = request.session['background']
            FDB.object_text = request.session['objects']
            FDB.develop_content = request.POST['developContent']
            FDB.fund_goal_price = request.POST['goal_money']

            FDB.fund_total_price = 0
            FDB.regi_date = datetime.datetime.now().strftime ("%Y-%m-%d")
            FDB.save()

            # 세션에 저장된거 삭제
            # del request.session['intro']
            # del request.session['title']

            return HttpResponseRedirect(reverse('app:funding_main'))
        if request.POST.get("before",0) =="이전":
            request.session['step1_complete'] = True
            return HttpResponseRedirect(reverse('fundingapp:create2'))