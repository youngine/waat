from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

app_name = 'fundingapp'

urlpatterns = [

    path('detail/<int:board_id>', views.detail, name='detail'),
    path('select/', views.select,name='select'),
    path('create/', views.create,name='create'),

    path('get_info/', views.get_info,name='get_info'),
    path('step1/', Step1View.as_view(), name='step1'),
    path('step2/', Step2View.as_view(), name='step2'),
    path('step3/', Step3View.as_view(), name='step3'),
]
