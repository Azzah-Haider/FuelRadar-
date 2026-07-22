from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from stations.models import Station, FuelPrice, QueueStatus


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

    context = {
        'stations': stations,
    }
    return render(request, 'dashboard/manager_dashboard.html', context)


@login_required
def driver_dashboard(request):
    if request.user.role != 'driver':
        messages.error(request, 'You do not have access to the driver dashboard.')
        return redirect('home')

    total_stations = Station.objects.filter(is_approved=True).count()
    green_stations_count = QueueStatus.objects.filter(status='green', station__is_approved=True).count()

    stations = Station.objects.filter(is_approved=True)
    stations_with_details = []

    for station in stations:
        queue_status = QueueStatus.objects.filter(station=station).first()
        fuel_prices = FuelPrice.objects.filter(station=station)

        stations_with_details.append({
            'station': station,
            'queue_status': queue_status,
            'fuel_prices': fuel_prices,
        })

    context = {
        'total_stations': total_stations,
        'green_stations_count': green_stations_count,
        'stations_with_details': stations_with_details,
    }
    return render(request, 'dashboard/driver_dashboard.html', context)