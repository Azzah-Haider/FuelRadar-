from django.shortcuts import render
from stations.models import Station, QueueStatus, FuelPrice

def home(request):
    # Get approved stations for everyone
    stations = Station.objects.filter(is_approved=True)
    
    # If user is a manager, also show their own station (even if pending)
    if request.user.is_authenticated and request.user.role == 'manager':
        try:
            manager_station = Station.objects.get(manager=request.user)
            if manager_station not in stations:
                stations = list(stations) + [manager_station]
        except Station.DoesNotExist:
            pass
    
    # Create station data list
    stations_with_details = []
    unique_cities = set()  # Use a set to track unique cities
    
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
        
        # Add city to unique cities set
        if station.city:
            unique_cities.add(station.city)
    
    # Sort cities alphabetically
    unique_cities = sorted(list(unique_cities))
    
    context = {
        'stations_with_details': stations_with_details,
        'total_stations': len(stations),
        'unique_cities': unique_cities,  # Pass unique cities to template
    }
    return render(request, 'home.html', context)