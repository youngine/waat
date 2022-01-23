from django.shortcuts import render
from fundingapp.saveData import DataContent

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



def funding_main(request):
    return render(request, 'app/index.html') 

def funding_join(request):
    return render(request, 'app/funding.html') 

def assemble(request):
    return render(request, 'app/contact.html') 

# def tb(request):  # 테스트 한다고 만든 것 ->종원
#     return render(request, 'app/dasd.html') 