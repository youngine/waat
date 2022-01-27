from django.contrib import admin
from django.urls import path
from user import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('signin/', views.signin,name='signin'),
    path('signout/', views.signout,name='signout'),
    path('signup/', views.signup,name='signup'),
    path('usercheck/', views.usercheck,name='usercheck'),
    path('pwchange/', views.pwchange,name='pwchange'),
    path('myfunding/', views.myfunding, name='myfunding'),
    path('myboarding/', views.myboarding, name='myboarding'),

]
