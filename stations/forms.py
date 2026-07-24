from django import forms
from .models import Station, FuelPrice, QueueStatus
from .models import StationRating

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'location', 'city', 'operating_hours', 'services', 'contact_phone', 'map_link']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Station Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City Name'}),
            'operating_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 8:00 AM - 10:00 PM'}),
            'services': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g., Car Wash, Restaurant, ATM'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

class FuelPriceForm(forms.ModelForm):
    class Meta:
        model = FuelPrice
        fields = ['fuel_type', 'price']
        widgets = {
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in SDG', 'step': '0.01'}),
        }

class QueueStatusForm(forms.ModelForm):
    class Meta:
        model = QueueStatus
        fields = ['status', 'queue_length']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'queue_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of cars waiting', 'min': '0'}),
        }

class StationRatingForm(forms.ModelForm):
    class Meta:
        model = StationRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience...'}),
        }