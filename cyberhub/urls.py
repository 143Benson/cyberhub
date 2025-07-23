from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  # <-- Add this line
]