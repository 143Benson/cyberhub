from django.contrib import admin
from .models import Service, ServiceRequest

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'status', 'requested_date')
    list_filter = ('status', 'requested_date')
    search_fields = ('user__username', 'service__name')
    readonly_fields = ('requested_date',)

admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)