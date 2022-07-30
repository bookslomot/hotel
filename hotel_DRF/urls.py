from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # DJANGO
    path('admin/', admin.site.urls),
    # DJOSER
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # MY APPS
    path('hotel/', include('hotel.urls')),
    path('user/', include('user.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
