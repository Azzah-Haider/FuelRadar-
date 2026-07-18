from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from stations.models import Station, FuelPrice, QueueStatus

@login_required
def admin_dashboard(request):
    """Admin Dashboard - Shows all stations, users, and stats"""
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
    """Manager Dashboard - Shows their station details"""
    if request.user.role != 'manager':
        messages.error(request, 'You do not have access to the manager dashboard.')
        return redirect('home')
    
    try:
        station = Station.objects.get(manager=request.user)
        fuel_prices = FuelPrice.objects.filter(station=station)
        queue_status = QueueStatus.objects.filter(station=station).first()
        
        context = {
            'station': station,
            'fuel_prices': fuel_prices,
            'queue_status': queue_status,
        }
    except Station.DoesNotExist:
        context = {
            'station': None,
            'fuel_prices': [],
            'queue_status': None,
        }
    
    return render(request, 'dashboard/manager_dashboard.html', context)

@login_required
def driver_dashboard(request):
    """Driver Dashboard - Shows stations near them"""
    if request.user.role != 'driver':
        messages.error(request, 'You do not have access to the driver dashboard.')
        return redirect('home')
    
    stations = Station.objects.filter(is_approved=True)[:10]
    
    context = {
        'stations': stations,
    }
    return render(request, 'dashboard/driver_dashboard.html', context)
