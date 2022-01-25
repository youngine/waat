from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

app_name = 'fundingapp'

urlpatterns = [

    path('detail/<int:board_id>', views.detail, name='detail'),
    path('select/', views.select,name='select'),
    path('create1/', Create1.as_view(),name='create1'),
    path('create2/', Create2.as_view(),name='create2'),
    path('create3/', Create3.as_view(),name='create3'),
    path('download/<str:file_path>', views.download, name='download'),
    path('allViewPage/<int:page_num>/<int:board_id>',AllViewPage.as_view(), name="allViewPage"),

    # path('AllViewPage/<int:board_id>/<int:page_num>/',AllViewPage.as_view(),name="modify")
    # path('AllViewPage/',AllViewPage.as_view(),name="AllViewPage")

]
