from django import forms
from .models import Station, FuelPrice, QueueStatus

<<<<<<< HEAD
class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'location', 'city', 'operating_hours', 'services', 'contact_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Station Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City Name'}),
            'operating_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 8:00 AM - 10:00 PM'}),
            'services': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g., Car Wash, Restaurant, ATM'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }
=======
SERVICE_CHOICES = [
    ('ATM', 'ATM'),
    ('Restaurant', 'Restaurant'),
    ('Car Wash', 'Car Wash'),
    ('Restroom', 'Restroom'),
    ('Store', 'Store'),
    ('Air & Tire Service', 'Air & Tire Service'),
]


class StationForm(forms.ModelForm):
    services = forms.MultipleChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Available Services',
    )

    class Meta:
        model = Station
        fields = ['name', 'location', 'city', 'operating_hours', 'services', 'contact_phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-check the boxes that match this station's existing saved services
        if self.instance and self.instance.pk and self.instance.services:
            self.initial['services'] = [s.strip() for s in self.instance.services.split(',') if s.strip()]

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected = self.cleaned_data.get('services', [])
        instance.services = ', '.join(selected)
        if commit:
            instance.save()
        return instance

>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976

class FuelPriceForm(forms.ModelForm):
    class Meta:
        model = FuelPrice
        fields = ['fuel_type', 'price']
<<<<<<< HEAD
        widgets = {
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in SDG', 'step': '0.01'}),
        }
=======

>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976

class QueueStatusForm(forms.ModelForm):
    class Meta:
        model = QueueStatus
<<<<<<< HEAD
        fields = ['status', 'queue_length']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'queue_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of cars waiting', 'min': '0'}),
        }
=======
        fields = ['status', 'queue_length']
>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976
