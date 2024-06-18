from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('testing/', include('apps.testing.urls')),
    path('', include('apps.lk.urls')),
    path('', include('apps.eisot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
