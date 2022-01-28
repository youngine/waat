import re,os
from django.forms import forms
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import FundingBoard, User1, JoinFund, JoinProject, FundingBoardCrew, FundingBoardPrice
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
import time
# 펀딩 참여를 눌렀을 때 나오는 페이지
@csrf_exempt
def select(request, select_drop):

    # 페이징을 위한 내용
    now_page = int(request.GET.get('page', 1))
    data = FundingBoard.objects.all()

    if request.method =="POST":

        search_word = request.POST.get("search_word", 0)

        data = FundingBoard.objects.filter(title__contains = search_word)

    result = []
    for d in data:

        # 가격을 위해서는 FundingBoardPrice를 가져와야한다.

        price_data = FundingBoardPrice.objects.get(board_id = d.board_id)

        percent = int(price_data.fund_total_price / price_data.fund_goal_price * 100)
    
        # percent_n : 퍼센트 바 올라가는 갯수
        # percent_stan : 퍼센트 기준 값

        percent_n = 5
        percent_stan = 100
        percent_mark = int(percent / (percent_stan / (percent_n+1)))

        
        if percent_mark > percent_n:
            percent_mark = percent_n

        # 펀딩 남은 기간 확인, d_day가 끝난 경우(음수인 경우 0으로 표시)

        d_day = (d.end_date -  datetime.date.today()).days
        if d_day < 0:
            d_day = 0
        
        # 펀딩 참여 명수 구하기

        join_user = JoinFund.objects.filter(board_id = d.board_id)

        # 중복값 빼야함

        join_user_count = []
        for jo in join_user:
            join_user_count.append(jo.user_id)
        join_user_count = len(set(join_user_count))

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
            "language_text" : d.language_text,
            "func_a_price" : price_data.func_a_price,
            "func_b_price" : price_data.func_b_price,
            "func_c_price" : price_data.func_c_price,
            "fund_goal_price" : price_data.fund_goal_price,
            "fund_total_price" : price_data.fund_total_price,
            "percent" : percent,
            "regi_date" : d.regi_date,
            "start_date" : d.start_date,
            "end_date" : d.end_date,
            "percent_mark" : percent_mark,
            "d_day" : d_day,
            "join_user_count" : join_user_count
        })

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

# 펀딩 참여에서 게시물을 누른 경우
@csrf_exempt
def detail(request, board_id):

    data = FundingBoard.objects.get(board_id=board_id)
    current_user = request.session.get('user',0)
    filepath = data.file_name
    if request.method =="GET":
        
        price_data = FundingBoardPrice.objects.get(board_id = board_id)

        percent = int(price_data.fund_total_price / price_data.fund_goal_price * 100)
        
        # percent_n : 퍼센트 바 올라가는 갯수
        # percent_stan : 퍼센트 기준 값

        percent_n = 5
        percent_stan = 100
        percent_mark = int(percent / (percent_stan / (percent_n+1)))

        
        if percent_mark > percent_n:
            percent_mark = percent_n

        # 펀딩 남은 기간 확인, d_day가 끝난 경우(음수인 경우 0으로 표시)
        d_day = (data.end_date -  datetime.date.today()).days
        if d_day < 0:
            d_day = 0
        
        crew_data = FundingBoardCrew.objects.get(board_id = board_id)

        # crew_sum = 현재 남은 수
        crew_sum = crew_data.front_crew + crew_data.back_crew

        # 원래 남은 crew수를 구해야함.
        join_pro = JoinProject.objects.filter(board_id = board_id).count()

        all_crew_sum = crew_sum + join_pro
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
                "func_text" : data.func_text,
                "develop_content" : data.develop_content,
                "regi_date" : data.regi_date,
                "start_date" : data.start_date,
                "end_date" : data.end_date,

                "func_a_price" : price_data.func_a_price,
                "func_b_price" : price_data.func_b_price,
                "func_c_price" : price_data.func_c_price,
                "fund_goal_price" : price_data.fund_goal_price,
                "fund_total_price" : price_data.fund_total_price,

                "percent" : percent,
                "percent_mark" : percent_mark,
                "d_day" : d_day,

                "join_pro" : join_pro,
                "all_crew_sum" : all_crew_sum,
                "crew_sum" : crew_sum,

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


            price_data = FundingBoardPrice.objects.get(board_id=board_id)

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
                        total_price += price_data.func_a_price
                    elif i == "2":
                        result_list.append("2")
                        total_price += price_data.func_b_price
                    elif i == "3":
                        result_list.append("3")
                        total_price += price_data.func_c_price

            

            join_db = JoinFund()
            # 유저 이름
            join_db.user_id = user_name
            join_db.board_id = board_id
            join_db.fund_price = total_price
            join_db.fund_join_list = result_list
            
            join_db.save()

            # data : 현재 선택 된 게시물 정보
            price_data.fund_total_price += total_price
            price_data.save()
            return HttpResponseRedirect('/app/fund/select/1')

        if request.POST.get('btn_delete') == "btn_delete":
            # foreign key 삭제 해야함...
            data = FundingBoard.objects.get(board_id = board_id)
            
            # board데이터와 연관된 데이터들 삭제
            JoinProject.objects.filter(board_id=board_id).delete()
            FundingBoardCrew.objects.filter(board_id = board_id).delete()
            JoinFund.objects.filter(board_id = board_id).delete()
            FundingBoardPrice.objects.filter(board_id=board_id).delete()

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


            data = FundingBoard.objects.get(board_id = board_id)
            user = User1.objects.get(user_id = request.session['user'])
            return render(
                request,
                'fund_view/contact.html',
                {
                    "user_name" : user.user_name,
                    "user_email" : user.user_email,
                    "board_user_name" : data.user_id
                }

            )

# 팀원 모집
@csrf_exempt
def contact(request, board_id):

    if request.method == 'POST':
        # 데이터가 들어왔으니 저장해주자.

        # 만약 이미 신청한 사람이라면 안된다고 출력해주자.
        check_id = JoinProject.objects.filter(board_id = board_id)
        join_project_data = JoinProject()
        ck = -1
        for i in check_id:
            if i.user_id ==  request.session['user']:
                return HttpResponseRedirect(reverse('app:funding_main'))
        chk_dev_text = request.POST.get('chk_dev',0)

        if "radio_front" == chk_dev_text:
            join_project_data.check_crew = 0
        elif "radio_back" == chk_dev_text:
            join_project_data.check_crew = 1
        else:
            return HttpResponseRedirect(reverse('app:funding_main'))
        
        
        join_project_data.board_id = board_id
        join_project_data.user_id = request.session['user']
        join_project_data.user_name = request.POST['name']
        join_project_data.user_email = request.POST['email']
        join_project_data.subject = request.POST['subject']
        join_project_data.message = request.POST['message']

        join_project_data.save()


        fund_crew_data = FundingBoardCrew.objects.get(board_id = board_id)
        if join_project_data.check_crew == 0:
            fund_crew_data.front_crew -= 1

        if join_project_data.check_crew == 1:
            fund_crew_data.back_crew -= 1

        fund_crew_data.save()
        # 저장했으니 메인페이지로 보내주자.
        return HttpResponseRedirect(reverse('app:funding_main'))
    

    
    # 여기로 오는 경우 처음들어온 경우다.
    data = FundingBoard.objects.get(board_id=board_id)
    fund_crew_data = FundingBoardCrew.objects.get(board_id = board_id)

    user = User1.objects.get(user_id = request.session['user'])
    return render(
        request,
        'fund_view/contact.html',
        {
            "user_name" : user.user_name,
            "user_email" : user.user_email,
            "board_user_name" : data.user_id,
            "board_title" : data.title,
            "front_crew" : fund_crew_data.front_crew,
            "back_crew" : fund_crew_data.back_crew,
        }

    )


def download(request,file_path):

    formating = file_path.split(".")[-1]
    with open(file_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={"다운로드 이미지."+formating}'

        return response


### 참고 소스 엄청 드러움.... 리팩토링 해야하는데.... DB부터 데이터 입력 가능한지 테스트 후 리팩토링 해야한다. 안쓰는 코드 다량 많음. 더미 코드 많다는 뜻임 -> 종원
class Create1(View):
    def get(self, request, *args, **kwargs):
        request.session['step1_complete'] = False
        request.session['step2_complete'] = False
        if len(request.session.get('user',"")) == 0:
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

            board = FundingBoard()
            price = FundingBoardPrice()
            crew = FundingBoardCrew()
            

            board.user_id = request.session['user']
            board.title = request.session['title']
            board.category = request.session['category']
            board.language_text = request.session['language']
            board.target = request.session['target']
            board.intro = request.session['intro']
            board.file_name = request.session['imgefile']
            board.background_text = request.session['background']
            board.object_text = request.session['objects']
            board.develop_content = request.POST['developContent']
            board.func_text = request.POST['func_text']

            request.session['regi_date'] = datetime.datetime.now().strftime ("%Y-%m-%d")
            board.regi_date = request.session['regi_date'] 
            board.start_date = request.POST['start_date']
            board.end_date = request.POST['end_date']
            board.save()
            request.session['start_date'] = request.POST['start_date']
            request.session['end_date'] = request.POST['end_date']

            

            # 생성된 board_id를 가져와야한다. user_id, title, start_date, end_date를 비교하자. 여기까지 같으면 어쩔수없긴하다..
            # 생성되기전에 진행되면 안보이므로.. sleep을 써서 1초정도는 스탑을 해주자. 계속 멈추게하면 무한 로딩이 걸릴수 있어서 이정도로 손봐야겠다..

            time.sleep(1)

            board_id = FundingBoard.objects.filter(
                user_id = request.session['user'], 
                title = request.session['title'],
                start_date = request.POST['start_date'],
                end_date = request.POST['end_date'])[0].board_id
            
            price.board_id = board_id
            price.func_a_price = request.POST.get('eqA',0)
            price.func_b_price = request.POST.get('eqB',0)
            price.func_c_price = request.POST.get('eqC',0)

            price.fund_goal_price = request.POST.get('goal_money',0)
            price.fund_total_price = 0

            price.save()

            crew.board_id = board_id
            crew.front_crew = 0
            crew.back_crew = 0

            crew.save()




            # 세션에 저장된거 삭제
            del request.session['intro']
            del request.session['background']
            del request.session['objects']
            
            # del request.session['title']
            del request.session['category']
            del request.session['language']
            del request.session['target']
            del request.session['imgefile']

            if request.POST.get("checkAddTeams",0) =="체크":
                return HttpResponseRedirect(reverse('fundingapp:ADDTeam'))

            return HttpResponseRedirect(reverse('app:funding_main'))
        if request.POST.get("before",0) =="이전":
            request.session['step1_complete'] = True
            return HttpResponseRedirect(reverse('fundingapp:create2'))


class AllViewPage(View):
    FDB = FundingBoard
    def get(self, request, *args, **kwargs):
        page_num = kwargs['page_num']
        board_id = kwargs['board_id']
        
        # 수정할 때 데이터이므로.. 여기다가 모든 데이터를 넣어주어야한다..
        DB_data = self.FDB.objects.get(board_id=board_id)

        # DB 데이터를 넘겨주어도 상관이 없다.
        if page_num == 1:
            file_name = DB_data.file_name.split("/img/")[-1]
            return render(request, 'fundingapp/view_All_modify.html',{"page_num": page_num,"board_id" : board_id, "DB_data":DB_data , "file_name" : file_name })
        elif page_num == 3:

            start_date = str(DB_data.start_date)
            end_date = str(DB_data.end_date)

            crew_data = FundingBoardCrew.objects.get(board_id = board_id)
            fc = crew_data.front_crew
            bc = crew_data.back_crew

            price_data = FundingBoardPrice.objects.get(board_id = board_id)


            result = {
                "board_id" : DB_data.board_id,
                "user_id" : DB_data.user_id,
                "title" : DB_data.title,
                "category" : DB_data.category,
                "target" : DB_data.target,
                "intro" : DB_data.intro,
                "file_name" : DB_data.file_name,
                "background_text" : DB_data.background_text,
                "object_text" : DB_data.object_text,
                "language_text" : DB_data.language_text,
                "func_text" : DB_data.func_text,
                "develop_content" : DB_data.develop_content,
                "regi_date" : DB_data.regi_date,
                "start_date" : DB_data.start_date,
                "end_date" : DB_data.end_date,

                "func_a_price" : price_data.func_a_price,
                "func_b_price" : price_data.func_b_price,
                "func_c_price" : price_data.func_c_price,
                "fund_goal_price" : price_data.fund_goal_price,
                "fund_total_price" : price_data.fund_total_price,

                "fc" : fc,
                "bc" : bc


            }



            if fc + bc >0:
                checkTeamsFlag = True
                return render(request, 'fundingapp/view_All_modify.html',{"page_num": page_num,"board_id" : board_id,"DB_data":result,"start_date": start_date,"end_date":end_date,"checkTeamsFlag":checkTeamsFlag})
            return render(request, 'fundingapp/view_All_modify.html',{"page_num": page_num,"board_id" : board_id,"DB_data":result,"start_date": start_date,"end_date":end_date}) 
        else:
            return render(request, 'fundingapp/view_All_modify.html',{"page_num": page_num,"board_id" : board_id,"DB_data":DB_data}) 


    def post(self, request, *args, **kwargs):
        board_id = kwargs['board_id']
        page_num = kwargs['page_num']

        DB_data = self.FDB.objects.get(board_id=board_id)
        price = FundingBoardPrice.objects.get(board_id = board_id)
        crew = FundingBoardCrew.objects.get(board_id = board_id)

        if page_num !=1:
            if request.POST.get("next",0) =="다음":
                DB_data.intro = request.POST.get('intro',DB_data.intro)
                DB_data.background_text = request.POST.get('background',DB_data.background_text)
                DB_data.object_text = request.POST.get('objects',DB_data.object_text)
                DB_data.save()
                page_num +=1
            if request.POST.get("before",0) =="이전":
                page_num -=1 
            if request.POST.get("finsh",0) =="완료":
                DB_data.fund_goal_price = request.POST.get('goal_money', price.fund_goal_price)
                DB_data.func_a_price = request.POST.get('eqA', price.func_a_price)
                DB_data.func_b_price = request.POST.get('eqB', price.func_b_price)
                DB_data.func_c_prce = request.POST.get('eqC', price.func_c_price)
                DB_data.develop_content = request.POST.get('developContent',DB_data.develop_content)
                DB_data.regi_date = datetime.datetime.now().strftime ("%Y-%m-%d")
                DB_data.start_date = request.POST.get('start_date', DB_data.start_date)
                DB_data.end_date = request.POST.get('end_date', DB_data.end_date)
                DB_data.save()
                if request.POST.get("checkAddTeams") =="체크":
                    request.session['board_id'] = board_id
                    fc = crew.front_crew
                    bc = crew.back_crew

                    return render(request,'fundingapp/addTeam.html',{'board_id':board_id,'fc':fc,'bc':bc})

                return HttpResponseRedirect(reverse('app:funding_main'))
        else:
            DB_data.title = request.POST.get('title',DB_data.title)
            DB_data.category = request.POST.get('category',DB_data.category)
            DB_data.language_text = request.POST.get('language',DB_data.language_text )
            DB_data.target = request.POST.get('target',DB_data.target)
            DB_data.save()
            page_num +=1
        return HttpResponseRedirect(reverse('fundingapp:allViewPage', 
                                        kwargs={'page_num': page_num,
                                                'board_id': board_id,
                                        }))



class ADDTeams(View):

    # board_id를 불러오자.

    def get(self, request, *args, **kwargs):
        if request.session.get('board_id',False):

            crew = FundingBoardCrew.objects.get(board_id = request.session.get('board_id'))

            fc = crew.front_crew
            bc = crew.back_crew
            return render(request,'fundingapp/addTeam.html',{'fc':fc,'bc':bc})

        regi = request.session['regi_date']
        title = request.session['title']
        user_id = request.session['user']
        return render(request,'fundingapp/addTeam.html',{'regi':regi,'title':title,'user_id':user_id})

    def post(self, request, *args, **kwargs):
        if request.POST.get("TeamFinsh",0) =="팀원모집":
            if request.session.get('board_id',False):
                crew = FundingBoardCrew.objects.get(board_id = request.session.get('board_id'))
                del request.session['board_id']
            else:
                regi = request.session['regi_date']
                title = request.session['title']
                user_id = request.session['user']
                start_date = request.session['start_date']
                end_date = request.session['end_date']

                sqlQ = FundingBoard.objects.filter(regi_date = regi, title = title, user_id = user_id, start_date = start_date, end_date = end_date)
                crew = FundingBoardCrew.objects.get(board_id = sqlQ[0].board_id)
                del request.session['title']
                del request.session['regi_date']

            crew.front_crew = request.POST.get("FrontEnd",0)
            crew.back_crew = request.POST.get("BackEnd",0)
            crew.save()

            return HttpResponseRedirect(reverse('app:funding_main'))

