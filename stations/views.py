from django.shortcuts import render, redirect, get_object_or_404
<<<<<<< HEAD
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
    
=======
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Station, FuelPrice, QueueStatus
from .forms import StationForm, FuelPriceForm, QueueStatusForm


# ---------- DRIVER / PUBLIC VIEWS (Read) ----------

def station_list(request):
    """Public list of approved stations. Anyone can view, including guests."""
    stations = Station.objects.filter(is_approved=True)
    return render(request, 'stations/list.html', {'stations': stations})


def station_detail(request, pk):
    """Public detail page for one station, showing prices and queue status."""
    station = get_object_or_404(Station, pk=pk, is_approved=True)
    fuel_prices = station.fuel_prices.all()
    queue_status = getattr(station, 'queue_status', None)
    return render(request, 'stations/detail.html', {
    'station': station,
    'fuel_prices': fuel_prices,
    'queue_status': queue_status,
})


# ---------- STATION MANAGER VIEWS (Create/Update/Delete own station) ----------

@role_required('manager')
def register_station(request):
    """Station Manager registers a NEW station. Only allowed if they don't already have one."""
    if Station.objects.filter(manager=request.user).exists():
        messages.info(request, 'You already have a registered station.')
        return redirect('stations:manage_station')

>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.manager = request.user
<<<<<<< HEAD
            station.is_approved = False  # Needs admin approval
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
    
    station = get_object_or_404(Station, manager=request.user)
    
=======
            station.is_approved = False  # must be approved by an admin
            station.save()
            messages.success(request, 'Station submitted for admin approval!')
            return redirect('stations:manage_station')
    else:
        form = StationForm()
    return render(request, 'stations/register.html', {'form': form})


@role_required('manager')
def manage_station(request):
    """Station Manager updates their EXISTING station's info."""
    station = get_object_or_404(Station, manager=request.user)

>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976
    if request.method == 'POST':
        form = StationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            messages.success(request, 'Your station has been updated!')
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
    
    station = get_object_or_404(Station, manager=request.user)
    
    if request.method == 'POST':
        station_name = station.name
        station.delete()
        messages.success(request, f'"{station_name}" has been deleted.')
        return redirect('home')
    
    return render(request, 'stations/delete_station.html', {'station': station})

# ========== FUEL PRICE CRUD ==========

@login_required
def add_fuel_price(request):
    """Managers can add fuel prices to their station"""
    if request.user.role != 'manager':
        messages.error(request, 'Only station managers can add fuel prices.')
        return redirect('home')
    
    try:
        station = Station.objects.get(manager=request.user)
    except Station.DoesNotExist:
        messages.error(request, 'You need to create a station first.')
        return redirect('stations:create_station')
    
=======
            messages.success(request, 'Station updated!')
            return redirect('stations:manage_station')
    else:
        form = StationForm(instance=station)

    fuel_prices = station.fuel_prices.all()
    queue_status = getattr(station, 'queue_status', None)
    return render(request, 'stations/manage.html', {
        'form': form,
        'station': station,
        'fuel_prices': fuel_prices,
        'queue_status': queue_status,
    })


@role_required('manager')
def delete_station(request, pk):
    """Station Manager permanently removes their own station (e.g. it closed)."""
    station = get_object_or_404(Station, pk=pk, manager=request.user)
    if request.method == 'POST':
        station.delete()
        messages.success(request, 'Station removed.')
        return redirect('manager_dashboard')
    return render(request, 'stations/confirm_delete.html', {'station': station})


# ---------- FUEL PRICE MANAGEMENT (Manager) ----------

@role_required('manager')
def add_fuel_price(request):
    """Add a new fuel type/price entry for the manager's own station."""
    station = get_object_or_404(Station, manager=request.user)
    if not station.is_approved:
        messages.warning(request, 'Your station must be approved by an admin before you can set this.')
        return redirect('stations:manage_station')
>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976
    if request.method == 'POST':
        form = FuelPriceForm(request.POST)
        if form.is_valid():
            fuel_price = form.save(commit=False)
            fuel_price.station = station
            fuel_price.save()
<<<<<<< HEAD
            messages.success(request, 'Fuel price added successfully!')
            return redirect('manager_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FuelPriceForm()
    
    return render(request, 'stations/add_fuel_price.html', {'form': form, 'station': station})

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
    
=======
            messages.success(request, 'Fuel price added!')
            return redirect('stations:manage_station')
    else:
        form = FuelPriceForm()
    return render(request, 'stations/fuel_price_form.html', {'form': form})


@role_required('manager')
def update_fuel_price(request, pk):
    """Edit an existing fuel price. Ownership check prevents editing another station's prices."""
    fuel_price = get_object_or_404(FuelPrice, pk=pk, station__manager=request.user)
    if not fuel_price.station.is_approved:
        messages.warning(request, 'Your station must be approved by an admin before you can set this.')
        return redirect('stations:manage_station')
>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976
    if request.method == 'POST':
        form = FuelPriceForm(request.POST, instance=fuel_price)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
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
    
    try:
        station = Station.objects.get(manager=request.user)
    except Station.DoesNotExist:
        messages.error(request, 'You need to create a station first.')
        return redirect('stations:create_station')
    
    # Get or create queue status
    queue_status, created = QueueStatus.objects.get_or_create(station=station)
    
    if request.method == 'POST':
        form = QueueStatusForm(request.POST, instance=queue_status)
        if form.is_valid():
            queue = form.save(commit=False)
            queue.station = station
            queue.last_updated_by = request.user
            queue.save()
            messages.success(request, 'Queue status updated successfully!')
            return redirect('manager_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QueueStatusForm(instance=queue_status)
    
    return render(request, 'stations/update_queue.html', {'form': form, 'station': station, 'queue_status': queue_status})

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
    
    # Get queue status and fuel prices for each station
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
=======
            messages.success(request, 'Fuel price updated!')
            return redirect('stations:manage_station')
    else:
        form = FuelPriceForm(instance=fuel_price)
    return render(request, 'stations/fuel_price_form.html', {'form': form})


@role_required('manager')
def delete_fuel_price(request, pk):
    fuel_price = get_object_or_404(FuelPrice, pk=pk, station__manager=request.user)
    if request.method == 'POST':
        fuel_price.delete()
        messages.success(request, 'Fuel price removed.')
        return redirect('stations:manage_station')
    return render(request, 'stations/confirm_delete.html', {'fuel_price': fuel_price})


# ---------- QUEUE STATUS UPDATES (Manager) ----------

@role_required('manager')
def update_queue_status(request):
    """Manager updates the live green/yellow/red queue indicator for their station."""
    station = get_object_or_404(Station, manager=request.user)
    if not station.is_approved:
        messages.warning(request, 'Your station must be approved by an admin before you can set this.')
        return redirect('stations:manage_station')
    queue_status, created = QueueStatus.objects.get_or_create(station=station)

    if request.method == 'POST':
        form = QueueStatusForm(request.POST, instance=queue_status)
        if form.is_valid():
         updated = form.save(commit=False)
         updated.last_updated_by = request.user
         updated.save()
         messages.success(request, 'Queue status updated!')
         return redirect('stations:manage_station')
    else:
        form = QueueStatusForm(instance=queue_status)
    return render(request, 'stations/queue_status_form.html', {'form': form})


# ---------- ADMIN APPROVAL SYSTEM ----------

@role_required('admin')
def pending_stations(request):
    """Admin sees all stations awaiting approval."""
    stations = Station.objects.filter(is_approved=False)
    return render(request, 'stations/pending.html', {'stations': stations})


@role_required('admin')
def approve_station(request, pk):
    station = get_object_or_404(Station, pk=pk)
    if request.method == 'POST':
        station.is_approved = True
        station.save()
        messages.success(request, f'{station.name} approved!')
        return redirect('stations:pending_stations')
    return render(request, 'stations/confirm_approve.html', {'station': station})


@role_required('admin')
def admin_delete_station(request, pk):
    """Admin removes an inappropriate or duplicate station registration."""
    station = get_object_or_404(Station, pk=pk)
    if request.method == 'POST':
        station.delete()
        messages.success(request, 'Station removed by admin.')
        return redirect('stations:pending_stations')
    return render(request, 'stations/confirm_delete.html', {'station': station})
>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976
