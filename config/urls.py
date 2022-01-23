from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('user/', include('user.urls')),
    path('fund/', include('fundingapp.urls')),
    # path('tb/', include('app.urls')), # 테스트 한다고 만든 것. ->종원
]
