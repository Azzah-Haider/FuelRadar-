from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .models import Station, FuelPrice, QueueStatus
from .forms import StationForm, FuelPriceForm, QueueStatusForm


# ========== STATION CRUD ==========

@login_required
def create_station(request):
    """Managers can create their station"""
    if request.user.role != 'manager':
        messages.error(request, 'Only station managers can create stations.')
        return redirect('home')
    
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.manager = request.user
            station.is_approved = False
            station.save()
            messages.success(request, 'Your station has been created! Waiting for admin approval.')
            return redirect('manager_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StationForm()
    
    return render(request, 'stations/create_station.html', {'form': form})


@login_required
def update_station(request):
    """Managers can edit their station"""
    if request.user.role != 'manager':
        messages.error(request, 'Only station managers can edit stations.')
        return redirect('home')
    
    stations = Station.objects.filter(manager=request.user)
    
    if not stations.exists():
        messages.error(request, 'You need to create a station first.')
        return redirect('stations:create_station')
    
    if stations.count() > 1:
        if request.method == 'POST' and 'station_id' in request.POST:
            station_id = request.POST.get('station_id')
            station = get_object_or_404(Station, id=station_id, manager=request.user)
        else:
            return render(request, 'stations/select_station.html', {'stations': stations, 'action': 'update'})
    else:
        station = stations.first()
    
    if request.method == 'POST':
        form = StationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            messages.success(request, f'{station.name} has been updated!')
            return redirect('manager_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StationForm(instance=station)
    
    return render(request, 'stations/update_station.html', {'form': form, 'station': station})

@login_required
def delete_station(request):
    """Managers can delete their station"""
    if request.user.role != 'manager':
        messages.error(request, 'Only station managers can delete stations.')
        return redirect('home')
    
    stations = Station.objects.filter(manager=request.user)
    
    if not stations.exists():
        messages.error(request, 'You need to create a station first.')
        return redirect('stations:create_station')
    
    if stations.count() > 1:
        if request.method == 'POST' and 'station_id' in request.POST:
            station_id = request.POST.get('station_id')
            station = get_object_or_404(Station, id=station_id, manager=request.user)
        else:
            return render(request, 'stations/select_station.html', {'stations': stations, 'action': 'delete'})
    else:
        station = stations.first()
    
    if request.method == 'POST':
        station_name = station.name
        station.delete()
        messages.success(request, f'"{station_name}" has been deleted.')
        return redirect('manager_dashboard')
    
    return render(request, 'stations/delete_station.html', {'station': station})


# ========== FUEL PRICE CRUD ==========

@login_required
def add_fuel_price(request):
    """Managers can add fuel prices to their station"""
    if request.user.role != 'manager':
        messages.error(request, 'Only station managers can add fuel prices.')
        return redirect('home')
    
    stations = Station.objects.filter(manager=request.user)
    
    if not stations.exists():
        messages.error(request, 'You need to create a station first.')
        return redirect('stations:create_station')
    
    # Get station_id from GET or POST
    station_id = request.GET.get('station_id') or request.POST.get('station_id')
    
    # If multiple stations and no station selected, show selection page
    if stations.count() > 1 and not station_id:
        return render(request, 'stations/select_station.html', {
            'stations': stations, 
            'action': 'add_price',
            'action_url': 'stations:add_fuel_price'
        })
    
    # Get the selected station
    if station_id:
        station = get_object_or_404(Station, id=station_id, manager=request.user)
    else:
        station = stations.first()

    if not station.is_approved:
        messages.warning(request, 'Your station must be approved by an admin before you can set fuel prices.')
        return redirect('manager_dashboard')
   
    if request.method == 'POST':
        form = FuelPriceForm(request.POST)
        if form.is_valid():
            fuel_price = form.save(commit=False)
            fuel_price.station = station
            fuel_price.save()
            messages.success(request, f'Fuel price added to {station.name}!')
            return redirect('manager_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FuelPriceForm()
    
    return render(request, 'stations/add_fuel_price.html', {
        'form': form, 
        'station': station,
        'station_id': station.id
    })

@login_required
def update_fuel_price(request, price_id):
    """Managers can update a fuel price"""
    if request.user.role != 'manager':
        messages.error(request, 'Only station managers can update fuel prices.')
        return redirect('home')
    
    try:
        station = Station.objects.get(manager=request.user)
    except Station.DoesNotExist:
        messages.error(request, 'You need to create a station first.')
        return redirect('stations:create_station')
    
    fuel_price = get_object_or_404(FuelPrice, id=price_id, station=station)

    if not station.is_approved:
        messages.warning(request, 'Your station must be approved by an admin before you can update fuel prices.')
        return redirect('manager_dashboard')

    if request.method == 'POST':
        form = FuelPriceForm(request.POST, instance=fuel_price)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fuel price updated successfully!')
            return redirect('manager_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FuelPriceForm(instance=fuel_price)
    
    return render(request, 'stations/update_fuel_price.html', {'form': form, 'fuel_price': fuel_price, 'station': station})


@login_required
def delete_fuel_price(request, price_id):
    """Managers can delete a fuel price"""
    if request.user.role != 'manager':
        messages.error(request, 'Only station managers can delete fuel prices.')
        return redirect('home')
    
    try:
        station = Station.objects.get(manager=request.user)
    except Station.DoesNotExist:
        messages.error(request, 'You need to create a station first.')
        return redirect('stations:create_station')
    
    fuel_price = get_object_or_404(FuelPrice, id=price_id, station=station)
    
    if request.method == 'POST':
        fuel_price.delete()
        messages.success(request, 'Fuel price deleted successfully!')
        return redirect('manager_dashboard')
    
    return render(request, 'stations/delete_fuel_price.html', {'fuel_price': fuel_price})


# ========== QUEUE STATUS CRUD ==========

@login_required
def update_queue_status(request):
    """Managers can update their station's queue status"""
    if request.user.role != 'manager':
        messages.error(request, 'Only station managers can update queue status.')
        return redirect('home')
    
    stations = Station.objects.filter(manager=request.user)
    
    if not stations.exists():
        messages.error(request, 'You need to create a station first.')
        return redirect('stations:create_station')
    
    # Get station_id from GET or POST
    station_id = request.GET.get('station_id') or request.POST.get('station_id')
    
    # If multiple stations and no station selected, show selection page
    if stations.count() > 1 and not station_id:
        return render(request, 'stations/select_station.html', {
            'stations': stations, 
            'action': 'update_queue'
        })
    
    # Get the selected station
    if station_id:
        station = get_object_or_404(Station, id=station_id, manager=request.user)
    else:
        station = stations.first()
    
    queue_status, created = QueueStatus.objects.get_or_create(station=station)

    if not station.is_approved:
        messages.warning(request, 'Your station must be approved by an admin before you can update queue status.')
        return redirect('manager_dashboard')

    if request.method == 'POST':
        form = QueueStatusForm(request.POST, instance=queue_status)
        if form.is_valid():
            queue = form.save(commit=False)
            queue.station = station
            queue.last_updated_by = request.user
            queue.save()
            messages.success(request, f'Queue status updated for {station.name}!')
            return redirect('manager_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QueueStatusForm(instance=queue_status)
    
    return render(request, 'stations/update_queue.html', {
        'form': form, 
        'station': station, 
        'queue_status': queue_status,
        'station_id': station.id
    })

# ========== AJAX VIEWS ==========

@require_http_methods(["GET"])
def search_stations(request):
    """AJAX: Search stations without page reload"""
    query = request.GET.get('q', '')
    city = request.GET.get('city', '')
    
    stations = Station.objects.filter(is_approved=True)
    
    if query:
        stations = stations.filter(name__icontains=query)
    
    if city:
        stations = stations.filter(city__icontains=city)
    
    station_data = []
    for station in stations:
        try:
            queue_status = QueueStatus.objects.get(station=station)
            queue_data = {
                'status': queue_status.status,
                'status_display': queue_status.get_status_display(),
                'queue_length': queue_status.queue_length
            }
        except QueueStatus.DoesNotExist:
            queue_data = None
        
        fuel_prices = FuelPrice.objects.filter(station=station)
        fuel_data = [{'fuel_type': p.get_fuel_type_display(), 'price': str(p.price)} for p in fuel_prices]
        
        station_data.append({
            'id': station.id,
            'name': station.name,
            'location': station.location,
            'city': station.city,
            'operating_hours': station.operating_hours,
            'queue_status': queue_data,
            'fuel_prices': fuel_data,
        })
    
    return JsonResponse({'stations': station_data, 'count': len(station_data)})


@login_required
@require_http_methods(["POST"])
def update_queue_ajax(request):
    """AJAX: Update queue status without page reload"""
    if request.user.role != 'manager':
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        station = Station.objects.get(manager=request.user)
    except Station.DoesNotExist:
        return JsonResponse({'error': 'No station found'}, status=404)
    
    try:
        data = json.loads(request.body)
        status = data.get('status')
        queue_length = data.get('queue_length')
        
        if not status:
            return JsonResponse({'error': 'Status is required'}, status=400)
        
        queue_status, created = QueueStatus.objects.get_or_create(station=station)
        queue_status.status = status
        if queue_length is not None:
            queue_status.queue_length = int(queue_length)
        queue_status.last_updated_by = request.user
        queue_status.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Queue status updated successfully!',
            'status': queue_status.status,
            'status_display': queue_status.get_status_display(),
            'queue_length': queue_status.queue_length,
            'updated_at': queue_status.updated_at.strftime('%Y-%m-%d %H:%M')
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def update_price_ajax(request):
    """AJAX: Update fuel price without page reload"""
    if request.user.role != 'manager':
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        station = Station.objects.get(manager=request.user)
    except Station.DoesNotExist:
        return JsonResponse({'error': 'No station found'}, status=404)
    
    try:
        data = json.loads(request.body)
        fuel_type = data.get('fuel_type')
        price = data.get('price')
        
        if not fuel_type or price is None:
            return JsonResponse({'error': 'Fuel type and price are required'}, status=400)
        
        fuel_price, created = FuelPrice.objects.get_or_create(
            station=station,
            fuel_type=fuel_type
        )
        fuel_price.price = price
        fuel_price.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Fuel price updated successfully!',
            'fuel_type': fuel_price.get_fuel_type_display(),
            'price': str(fuel_price.price),
            'updated_at': fuel_price.updated_at.strftime('%Y-%m-%d %H:%M')
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)