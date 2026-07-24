from django.urls import path
from . import views

app_name = 'stations'

urlpatterns = [
    # Station CRUD
    path('create/', views.create_station, name='create_station'),
    path('update/', views.update_station, name='update_station'),
    path('delete/', views.delete_station, name='delete_station'),
    
    # Fuel Price CRUD
    path('add-price/', views.add_fuel_price, name='add_fuel_price'),
    path('update-price/<int:price_id>/', views.update_fuel_price, name='update_fuel_price'),
    path('delete-price/<int:price_id>/', views.delete_fuel_price, name='delete_fuel_price'),
    
    # Queue Status
    path('update-queue/', views.update_queue_status, name='update_queue_status'),
    
    # AJAX Endpoints
    path('api/search/', views.search_stations, name='search_stations'),
    path('api/update-queue/', views.update_queue_ajax, name='update_queue_ajax'),
    path('api/update-price/', views.update_price_ajax, name='update_price_ajax'),

     # Rating URLs
    path('api/rate/', views.rate_station_ajax, name='rate_station_ajax'),
    path('api/get-rating/<int:station_id>/', views.get_station_rating, name='get_station_rating'),
]
