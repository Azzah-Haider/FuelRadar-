from django.shortcuts import render
from stations.models import Station, QueueStatus, FuelPrice, StationRating
from django.db import models

def home(request):
    # Get ONLY approved stations for everyone
    stations = Station.objects.filter(is_approved=True)
    
    # Create station data list
    stations_with_details = []
    
    for station in stations:
        try:
            queue_status = QueueStatus.objects.get(station=station)
        except QueueStatus.DoesNotExist:
            queue_status = None
        
        fuel_prices = FuelPrice.objects.filter(station=station)
        
        # Get average rating
        ratings = StationRating.objects.filter(station=station)
        avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
        full_stars = int(round(avg_rating)) if avg_rating > 0 else 0
        total_ratings = ratings.count()
        
        stations_with_details.append({
            'station': station,
            'queue_status': queue_status,
            'fuel_prices': fuel_prices,
            'avg_rating': round(avg_rating, 1),
            'full_stars': full_stars,
            'total_ratings': total_ratings,
        })
    
    # Get unique cities for the filter
    unique_cities = sorted(set([s['station'].city for s in stations_with_details if s['station'].city]))
    
    context = {
        'stations_with_details': stations_with_details,
        'total_stations': len(stations),
        'unique_cities': unique_cities,
    }
    return render(request, 'home.html', context)