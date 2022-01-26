import re,os
from django.forms import forms
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import FundingBoard, User1, JoinFund,JoinProject
from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from .saveData import DataContent
from django.contrib import messages
from django.shortcuts import render,redirect
from django.views import View  
from django.core.exceptions import PermissionDenied
import datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from config import settings
@csrf_exempt
def select(request, select_drop):

    now_page = int(request.GET.get('page', 1))
    data = FundingBoard.objects.all()

    if request.method =="POST":

        search_word = request.POST.get("search_word", 0)

        data = FundingBoard.objects.filter(title__contains = search_word)


    result = []
    for d in data:
        result.append({

            "board_id" : d.board_id,
            "user_id" : d.user_id,
            "title" : d.title,
            "category" : d.category,
            "target" : d.target,
            "intro" : d.intro,
            "file_name" : d.file_name,
            "background_text" : d.background_text,
            "object_text" : d.object_text,
            "develop_content" : d.develop_content,
            "func_a_price" : d.func_a_price,
            "language_text" : d.language_text,
            "func_b_price" : d.func_b_price,
            "func_c_price" : d.func_c_price,
            "fund_goal_price" : d.fund_goal_price,
            "fund_total_price" : d.fund_total_price,
            "percent" : int(d.fund_total_price / d.fund_goal_price * 100),
            "regi_date" : d.regi_date,
            "start_date" : d.start_date,
            "end_date" : d.end_date
            
        })
    print(result)
    # 최신순
    if select_drop == 1:
        result = sorted(result, key = lambda x: -x["board_id"])

    # 인기순
    elif select_drop == 2:
        result = sorted(result, key = lambda x: -x["percent"])

    # 오래된 순
    else:
        result = sorted(result, key = lambda x: x["board_id"])
    
    page_num = 5
    p = Paginator(result, page_num)

    info = p.page(now_page)

    start_page = (now_page - 1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages



    return render(
        request,
        'fund_view/main.html',
        {
            "data" : result,
            "select_drop" : select_drop,
            "info" : info,
            'page_range' : range(start_page, end_page + 1)
            
        }
    )


@csrf_exempt
def detail(request, board_id):
    data = FundingBoard.objects.get(board_id=board_id)
    current_user = request.session.get('user',0)
    filepath = data.file_name
    if request.method =="GET":
        percent = int(data.fund_total_price / data.fund_goal_price * 100)
        
        # percent_n : 퍼센트 바 올라가는 갯수
        # percent_stan : 퍼센트 기준 값

        percent_n = 5
        percent_stan = 100
        percent_mark = int(percent / (percent_stan / (percent_n+1)))

        
        if percent_mark > percent_n:
            percent_mark = percent_n

        # 펀딩 남은 기간 확인, d_day가 끝난 경우(음수인 경우 0으로 표시)
        d_day = (data.end_date - data.start_date).days
        if d_day < 0:
            d_day = 0
            

        result = [{
                "board_id" : data.board_id,
                "user_id" : data.user_id,
                "title" : data.title,
                "category" : data.category,
                "target" : data.target,
                "intro" : data.intro,
                "file_name" : data.file_name,
                "background_text" : data.background_text,
                "object_text" : data.object_text,
                "language_text" : data.language_text,
                "develop_content" : data.develop_content,
                "func_a_price" : data.func_a_price,
                "func_b_price" : data.func_b_price,
                "func_c_price" : data.func_c_price,
                "fund_goal_price" : data.fund_goal_price,
                "fund_total_price" : data.fund_total_price,
                "percent" : percent,
                "regi_date" : data.regi_date,
                "start_date" : data.start_date,
                "end_date" : data.end_date,
                "percent_mark" : percent_mark,
                "d_day" : d_day

            }]
 

        return render(request,
        'fund_view/fund_detail.html', 
        {
            "data" : result,
            "current_user" : current_user
        })
    if request.method == 'POST':
        try:
            # 현재는 root 아이디로 들어왔다고 가정하고 진행
            user_name = request.session['user']
        except KeyError as k:
            request.session['detail_funding'] = (True, board_id)
            return HttpResponseRedirect(reverse('user:signin'))
        if request.POST.get('btn_funding') == "btn_funding":
            selected = request.POST.getlist('func_check')
            data = FundingBoard.objects.get(board_id=board_id)

            total_price = 0
            result_list = []
            # 아무것도 선택을 안한상태
            if len(selected) == 0:
                # 첫 페이지 혹은 selelct 이거는 정해야할듯?
                return HttpResponseRedirect('/app/fund/select/1')
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

            join_db = JoinFund()
            # 유저 이름
            join_db.user_id = user_name
            join_db.board_id = board_id
            join_db.fund_price = total_price
            join_db.fund_join_list = result_list
            
            join_db.save()

            # data : 현재 선택 된 게시물 정보
            data.fund_total_price += total_price
            data.save()
            return HttpResponseRedirect('/app/fund/select/1')

        if request.POST.get('btn_delete') == "btn_delete":
            # foreign key 삭제 해야함...
            join_db = JoinFund.objects.filter(board_id = board_id).delete()
            join_project_db = JoinProject.objects.filter(board_id=board_id).delete()
            data.delete()
            return HttpResponseRedirect(reverse('app:funding_main'))

        # 이거 펀딩 기능별 가격이 바뀌면,,,, 이전 가격으로 진행이된다. 이벤트라 생각하자
        if request.POST.get('btn_modify') == "btn_modify":
            page_num=1
            return HttpResponseRedirect(reverse('fundingapp:allViewPage', 
                                        kwargs={'page_num': page_num,
                                                'board_id': board_id,
                                        }))

        if request.POST.get('btn_concat') == "btn_concat":

            user = User1.objects.get(user_id = request.session['user'])
            return render(
                request,
                'fund_view/contact.html',
                {
                    "user_name" : user.user_name,
                    "user_email" : user.user_email
                }

            )

@csrf_exempt
def contact(request, board_id):

    
    if request.method == 'POST':
        # 데이터가 들어왔으니 저장해주자.

        # 만약 이미 신청한 사람이라면 안된다고 출력해주자.
        check_id = JoinProject.objects.filter(board_id = board_id)

        for i in check_id:
            if i.user_id ==  request.session['user']:
                print("이미 했음")
                return HttpResponseRedirect(reverse('app:funding_main'))

        data = JoinProject()
        data.board_id = board_id
        data.user_id = request.session['user']
        data.user_name = request.POST['name']
        data.user_email = request.POST['email']
        data.subject = request.POST['subject']
        data.message = request.POST['message']

        data.save()

        # 저장했으니 메인페이지로 보내주자.
        return HttpResponseRedirect(reverse('app:funding_main'))
    
    # 여기로 오는 경우 처음들어온 경우다.

    user = User1.objects.get(user_id = request.session['user'])
    return render(
        request,
        'fund_view/contact.html',
        {
            "user_name" : user.user_name,
            "user_email" : user.user_email
        }

    )



def download(request,file_path):
    print(file_path)
    formating = file_path.split(".")[-1]
    with open(file_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={"다운로드 이미지."+formating}'
        print(response['Content-Disposition'])
        return response


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

        upload_file = request.FILES.get('file',"")
        if len(upload_file) !=0: 
            path = os.path.join("media/img/",upload_file.name)        
            with open(path, 'wb') as file:
                file.write(upload_file.read())
                for chunk in upload_file.chunks():
                    file.write(chunk)
            # print("저장위치 : ",path)
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
            
            FDB.func_a_price = request.POST['eqA']
            FDB.func_b_price = request.POST['eqB']
            FDB.func_c_price = request.POST['eqC']

            FDB.file_name = request.session['imgefile']
            FDB.intro = request.session['intro']
            FDB.background_text = request.session['background']
            FDB.object_text = request.session['objects']
            FDB.develop_content = request.POST['developContent']
            FDB.fund_goal_price = request.POST['goal_money']

            FDB.fund_total_price = 0
            FDB.regi_date = datetime.datetime.now().strftime ("%Y-%m-%d")

            # FDB.start_date = datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d")
            FDB.start_date =request.POST['start_date']
            FDB.end_date =request.POST['end_date']

            # FDB.end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d")
            
            FDB.save()

            # 세션에 저장된거 삭제
            # del request.session['intro']
            # del request.session['title']

            return HttpResponseRedirect(reverse('app:funding_main'))
        if request.POST.get("before",0) =="이전":
            request.session['step1_complete'] = True
            return HttpResponseRedirect(reverse('fundingapp:create2'))


class AllViewPage(View):
    FDB = FundingBoard
    def get(self, request, *args, **kwargs):
        page_num = kwargs['page_num']
        board_id = kwargs['board_id']
        
        DB_data = self.FDB.objects.get(board_id=board_id)
        print(DB_data.end_date)
        if page_num ==1:
            file_name = DB_data.file_name.split("/img/")[-1]
            return render(request, 'fundingapp/view_All_modify.html',{"page_num": page_num,"board_id" : board_id, "DB_data":DB_data , "file_name" : file_name})
        elif page_num ==3:
            start_date = str(DB_data.start_date)
            end_date = str(DB_data.end_date)
            return render(request, 'fundingapp/view_All_modify.html',{"page_num": page_num,"board_id" : board_id,"DB_data":DB_data,"start_date": start_date,"end_date":end_date}) 
        else:
            return render(request, 'fundingapp/view_All_modify.html',{"page_num": page_num,"board_id" : board_id,"DB_data":DB_data}) 


    def post(self, request, *args, **kwargs):
        board_id = kwargs['board_id']
        page_num = kwargs['page_num']

        DB_data = self.FDB.objects.get(board_id=board_id)
        if page_num !=1:
            if request.POST.get("next",0) =="다음":
                DB_data.intro = request.POST['intro']
                DB_data.background_text = request.POST['background']
                DB_data.object_text = request.POST['objects']
                DB_data.save()
                page_num +=1
            if request.POST.get("before",0) =="이전":
                page_num -=1 
            if request.POST.get("finsh",0) =="완료":
                DB_data.fund_goal_price = request.POST['goal_money'] 
                DB_data.func_a_price = request.POST['eqA']
                DB_data.func_b_price = request.POST['eqB']
                DB_data.func_c_price = request.POST['eqC']
                DB_data.develop_content = request.POST['developContent']
                DB_data.regi_date = datetime.datetime.now().strftime ("%Y-%m-%d")
                DB_data.save()
                return HttpResponseRedirect(reverse('app:funding_main'))
        else:
            DB_data.title = request.POST['title']
            DB_data.category = request.POST['category']
            DB_data.language_text =  request.POST['language']
            DB_data.target = request.POST['target']
            DB_data.save()
            page_num +=1
        return HttpResponseRedirect(reverse('fundingapp:allViewPage', 
                                        kwargs={'page_num': page_num,
                                                'board_id': board_id,
                                        }))

