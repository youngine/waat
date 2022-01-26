from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import (
    handler404, handler400, handler500
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('app/user/', include('user.urls')),
    path('app/fund/', include('fundingapp.urls')),
]+ static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)

handler404 = "app.views.page_not_found_page"