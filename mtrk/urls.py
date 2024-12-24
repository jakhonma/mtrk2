from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/controller/', include('controller.urls')),
    path('api/v1/helper/', include('helper.urls')),
    path('api/v1/main/', include('main.urls')),
    path('api/v1/report/', include('report.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
