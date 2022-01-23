from django.shortcuts import render
from .models import FundingBoard, User1, JoinFund
from django.http import HttpResponse

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

def detail(request):
    data = FundingBoard.objects.filter(board_id=1)

    img = []
    for d in data:
        img.append("/static/" + str(d.board_id) + "jpg")

    return render(
        request,
        'fund_view/fund_detail.html',
        {
            "data" : data,
            "img" : img
        }
    )