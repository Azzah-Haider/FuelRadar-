
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('driver', 'Driver'),
        ('manager', 'Station Manager'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='driver')
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def save(self, *args, **kwargs):
        """Auto-make admin users superusers"""
        if self.role == 'admin':
            self.is_superuser = True
            self.is_staff = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username
