from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from stations.models import Station, FuelPrice, QueueStatus, StationRating
from django.db import models

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('home')

    context = {
        'total_users': User.objects.count(),
        'total_stations': Station.objects.count(),
        'pending_stations': Station.objects.filter(is_approved=False).count(),
        'recent_stations': Station.objects.order_by('-created_at')[:5],
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'total_fuel_prices': FuelPrice.objects.count(),
        'stations_with_queue': QueueStatus.objects.count(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        messages.error(request, 'You do not have access to the manager dashboard.')
        return redirect('home')

    stations = Station.objects.filter(manager=request.user)
    
    # Add full_stars to each station
    for station in stations:
        ratings = station.ratings.all()  # Use the related_name
        avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
        station.full_stars = int(round(avg_rating)) if avg_rating > 0 else 0
        station.total_ratings = ratings.count()

    context = {
        'stations': stations,
    }
    return render(request, 'dashboard/manager_dashboard.html', context)


@login_required
def driver_dashboard(request):
    """Driver Dashboard - Shows stations with ratings"""
    if request.user.role != 'driver':
        messages.error(request, 'You do not have access to the driver dashboard.')
        return redirect('home')
    
    # Get all approved stations
    stations = Station.objects.filter(is_approved=True)
    
    stations_with_details = []
    green_stations_count = 0
    
    for station in stations:
        try:
            queue_status = QueueStatus.objects.get(station=station)
        except QueueStatus.DoesNotExist:
            queue_status = None
        
        fuel_prices = FuelPrice.objects.filter(station=station)
        
        # Count green stations
        if queue_status and queue_status.status == 'green':
            green_stations_count += 1
        
        # Get average rating
        ratings = StationRating.objects.filter(station=station)
        avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
        
        # Convert to integer for star display (round to nearest integer)
        full_stars = int(round(avg_rating)) if avg_rating > 0 else 0
        
        total_ratings = ratings.count()
        
        # Get user's rating
        user_rating = None
        try:
            user_rating_obj = StationRating.objects.get(station=station, user=request.user)
            user_rating = user_rating_obj.rating
        except StationRating.DoesNotExist:
            pass
        
        stations_with_details.append({
            'station': station,
            'queue_status': queue_status,
            'fuel_prices': fuel_prices,
            'avg_rating': round(avg_rating, 1),
            'full_stars': full_stars,
            'total_ratings': total_ratings,
            'user_rating': user_rating,
        })
    
    context = {
        'stations_with_details': stations_with_details,
        'total_stations': len(stations),
        'green_stations_count': green_stations_count,
    }
    
    
    return render(request, 'dashboard/driver_dashboard.html', context)