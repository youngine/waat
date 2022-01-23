from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [

    path('select/', views.select),
    path('detail/', views.detail),

]
