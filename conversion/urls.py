from django.urls import path
from . import views

app_name = 'conversion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('convert/', views.convert_file, name='convert_file'),
]
