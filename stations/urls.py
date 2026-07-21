from django.urls import path
from . import views

<<<<<<< HEAD
app_name = 'stations'  # Add this line for namespace


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
    
    #  AJAX ENDPOINTS
    path('api/search/', views.search_stations, name='search_stations'),
    path('api/update-queue/', views.update_queue_ajax, name='update_queue_ajax'),
    path('api/update-price/', views.update_price_ajax, name='update_price_ajax'),
=======
app_name = 'stations'

urlpatterns = [
    # Public / Driver
    path('', views.station_list, name='station_list'),
    path('<int:pk>/', views.station_detail, name='station_detail'),

    # Station Manager
    path('register/', views.register_station, name='register_station'),
    path('manage/', views.manage_station, name='manage_station'),
    path('delete/<int:pk>/', views.delete_station, name='delete_station'),

    # Fuel prices
    path('fuel-price/add/', views.add_fuel_price, name='add_fuel_price'),
    path('fuel-price/<int:pk>/edit/', views.update_fuel_price, name='update_fuel_price'),
    path('fuel-price/<int:pk>/delete/', views.delete_fuel_price, name='delete_fuel_price'),

    # Queue status
    path('queue-status/update/', views.update_queue_status, name='update_queue_status'),

    # Admin approval
    path('admin/pending/', views.pending_stations, name='pending_stations'),
    path('admin/approve/<int:pk>/', views.approve_station, name='approve_station'),
    path('admin/delete/<int:pk>/', views.admin_delete_station, name='admin_delete_station'),
>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976
]