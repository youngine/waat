from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('user/', include('user.urls')),
    path('fund/', include('fundingapp.urls')),
    
]
