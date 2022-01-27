from django.shortcuts import render
from django.template import RequestContext
from fundingapp.saveData import DataContent
from .models import FundingBoard, User1, JoinFund, JoinProject, FundingBoardCrew, FundingBoardPrice

def index(request):
    return render(request, 'app/index.html') 

def shop_single(request):
    return render(request, 'app/shop-single.html') 

def shop(request):
    return render(request, 'app/shop.html') 
    
def contact(request):
    return render(request, 'app/contact.html') 

def funding(request):
    return render(request, 'app/funding.html') 

def funding_join(request):
    return render(request, 'app/funding.html') 

def assemble(request):
    return render(request, 'app/contact.html') 

# 메인 페이지에 보이는 카드에 보여줄 데이터 가져오기
def funding_main(request):

    # 최신 순서대로 게시물 id 가져오기
    funding_board_data = FundingBoard.objects.all().order_by('board_id')
    
    # 결과값 저장할 공간
    result = []

    # 순서대로 진행을 하며 4개까지만 보여주기
    for i, d in enumerate(funding_board_data):
        if i == 4:
            break
        print(i, d.board_id)
        # 값도 가져와야 하므로 FundingBoardPrice의 값도 가져오자.
        price_data = FundingBoardPrice.objects.get(board_id = d.board_id)

        result.append({
            "board_id" : d.board_id,
            "file_name" : d.file_name,
            "title" : d.title,
            "percent" :  int(price_data.fund_total_price / price_data.fund_goal_price * 100),
            "intro" : d.intro,
            "total_funding" : price_data.fund_total_price,
        })
        
    return render(request, 
    'app/index.html',
        {
            "result" : result,
        }
    ) 
