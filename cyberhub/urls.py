from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('conversion/', include('conversion.urls', namespace='conversion')),
    path('i18n/', include('django.conf.urls.i18n')),  # <-- Add this line
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)