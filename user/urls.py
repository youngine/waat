from django.contrib import admin
from django.urls import path
from user import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signin/', views.signin,name='signin'),
    path('signout/', views.signout,name='signout'),
     path('signup/', views.signup,name='signup'),
]
