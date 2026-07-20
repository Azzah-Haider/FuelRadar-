from django import forms
from .models import Station, FuelPrice, QueueStatus

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


class FuelPriceForm(forms.ModelForm):
    class Meta:
        model = FuelPrice
        fields = ['fuel_type', 'price']


class QueueStatusForm(forms.ModelForm):
    class Meta:
        model = QueueStatus
        fields = ['status', 'queue_length']