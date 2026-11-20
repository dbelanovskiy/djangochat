from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('core.urls')),
    path('rooms/', include('room.urls')),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
] + static(settings.STATIC_URL, documnet_root=settings.STATIC_ROOT)
