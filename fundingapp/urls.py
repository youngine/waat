from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'fundingapp'

urlpatterns = [

    path('select/', views.select,name='select'),
    path('create/', views.create,name='create'),

    path('get_info/', views.get_info,name='get_info'),
]
