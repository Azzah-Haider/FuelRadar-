from django.shortcuts import render
from stations.models import Station, QueueStatus, FuelPrice

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
        
        stations_with_details.append({
            'station': station,
            'queue_status': queue_status,
            'fuel_prices': fuel_prices,
        })
    
    # Get unique cities for the filter
    unique_cities = sorted(set([s['station'].city for s in stations_with_details if s['station'].city]))
    
    context = {
        'stations_with_details': stations_with_details,
        'total_stations': len(stations),
        'unique_cities': unique_cities,
    }
    return render(request, 'home.html', context)