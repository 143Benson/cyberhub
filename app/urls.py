from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('check-username/', views.check_username, name='check_username'),
    path('check-email/', views.check_email, name='check_email'),
    path('check-phone/', views.check_phone, name='check_phone'),

    path('api/dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('api/services/', views.service_list, name='service_list'),
    path('api/services/request/', views.request_service, name='request_service'),
]