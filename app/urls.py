from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('main/', views.index,name='index'),
    path('contact/', views.contact,name='contact'),
    path('funding/', views.funding,name='funding'),
    path('shop/', views.shop,name='shop'),
    path('shop-single/', views.shop_single,name='shop_single'),
]
