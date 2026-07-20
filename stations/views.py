from django.shortcuts import render, redirect, get_object_or_404
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

    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.manager = request.user
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

    if request.method == 'POST':
        form = StationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
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
    if request.method == 'POST':
        form = FuelPriceForm(request.POST)
        if form.is_valid():
            fuel_price = form.save(commit=False)
            fuel_price.station = station
            fuel_price.save()
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
    if request.method == 'POST':
        form = FuelPriceForm(request.POST, instance=fuel_price)
        if form.is_valid():
            form.save()
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