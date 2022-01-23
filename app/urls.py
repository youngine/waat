from django.contrib import admin
from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('main/', views.funding_main,name='funding_main'),
    path('contact/', views.assemble,name='assemble'),
    path('funding/', views.funding_join,name='funding_join'),

    # path('tb/', views.tb,name='tb'), # 테스트 한다고 만든것. ->종원
    
    path('shop/', views.shop,name='shop'),
    path('shop-single/', views.shop_single,name='shop_single'),
]
