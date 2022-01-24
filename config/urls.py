from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('app/user/', include('user.urls')),
    path('app/fund/', include('fundingapp.urls')),
]
