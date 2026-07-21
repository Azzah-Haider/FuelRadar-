from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Station(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_stations'
    )
    is_approved = models.BooleanField(default=False)
    operating_hours = models.CharField(max_length=200, blank=True, null=True)
    services = models.TextField(blank=True, null=True, help_text="e.g., Car Wash, Restaurant, ATM")
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Gas Station'
        verbose_name_plural = 'Gas Stations'

class FuelPrice(models.Model):
    FUEL_TYPES = (
<<<<<<< HEAD
        ('banzen', 'Banzen'),
        ('gaz', 'Gaz'),
=======
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
>>>>>>> 4325fcac12587690b7aac25193aed142ef9c1976
    )

    
    station = models.ForeignKey(
        Station, 
        on_delete=models.CASCADE,
        related_name='fuel_prices'
    )
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.station.name} - {self.get_fuel_type_display()}: {self.price} SDG"
    
    class Meta:
        unique_together = ('station', 'fuel_type')
        ordering = ['station', 'fuel_type']
        verbose_name = 'Fuel Price'
        verbose_name_plural = 'Fuel Prices'


class QueueStatus(models.Model):
    STATUS_CHOICES = (
        ('green', '🟢 No Queue'),
        ('yellow', '🟡 Short Queue (5-10 min)'),
        ('red', '🔴 Long Queue (15+ min)'),
    )
    
    station = models.OneToOneField(
        Station, 
        on_delete=models.CASCADE,
        related_name='queue_status'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='green')
    queue_length = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        help_text="Estimated number of cars waiting"
    )
    updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='queue_updates'
    )
    
    def __str__(self):
        return f"{self.station.name} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = 'Queue Status'
        verbose_name_plural = 'Queue Statuses'