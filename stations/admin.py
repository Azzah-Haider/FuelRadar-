from django.contrib import admin
from .models import Station, FuelPrice, QueueStatus

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'manager', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'city', 'created_at']
    search_fields = ['name', 'location', 'city', 'manager__username']
    actions = ['approve_stations']
    
    def approve_stations(self, request, queryset):
        queryset.update(is_approved=True)
    approve_stations.short_description = "Approve selected stations"

@admin.register(FuelPrice)
class FuelPriceAdmin(admin.ModelAdmin):
    list_display = ['station', 'fuel_type', 'price', 'updated_at']
    list_filter = ['fuel_type', 'updated_at']
    search_fields = ['station__name']
    ordering = ['-updated_at']

@admin.register(QueueStatus)
class QueueStatusAdmin(admin.ModelAdmin):
    list_display = ['station', 'status', 'queue_length', 'updated_at']
    list_filter = ['status', 'updated_at']
    search_fields = ['station__name']
    ordering = ['-updated_at']