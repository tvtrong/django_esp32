
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.urls import path, include
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path("", include("apps.home.urls")),  # add this
    path("", include("apps.authentication.urls")),  # add this
    path('admin/', admin.site.urls),
    path("dht11/", include('apps.dht11.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
