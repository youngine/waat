from django.shortcuts import render
from fundingapp.saveData import DataContent
from .models import FundingBoard

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


def funding_main(request):
    
    data = FundingBoard.objects.all().order_by('-board_id')
    result = []
    for i, d in enumerate(data):
        if i == 4:
            break
        result.append({
            "board_id" : d.board_id,
            "file_name" : d.file_name,
            "title" : d.title,
            "percent" :  int(d.fund_total_price / d.fund_goal_price * 100),
            "intro" : d.intro,
            "total_funding" : d.fund_total_price,
        })


    return render(request, 
    'app/index.html',
        {
            "result" : result,
        }
    ) 
