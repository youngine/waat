from django.shortcuts import render
from .models import FundingBoard, User1, JoinFund

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
