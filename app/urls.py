from django.contrib import admin
from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('main/', views.funding_challenge,name='funding_challenge'),
    path('contact/', views.assemble,name='assemble'),
    path('funding/', views.funding_join,name='funding_join'),


    path('shop/', views.shop,name='shop'),
    path('shop-single/', views.shop_single,name='shop_single'),
]
