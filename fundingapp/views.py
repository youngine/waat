from django.shortcuts import render
from .models import FundingBoard, User1, JoinFund
from django.http import HttpResponse

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