from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
import secrets
import string

class Tour(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('service_provider', 'Service Provider'),
        ('admin', 'Admin'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)  # Changed to BooleanField
    company = models.CharField(max_length=20)
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='user'
    )
    date_created = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password on initial creation
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash."""
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

class TourToken(models.Model):
    """Custom token model for Tour users"""
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(Tour, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)
    
    @classmethod
    def generate_key(cls):
        """Generate a random token key"""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40))
    
    def __str__(self):
        return self.key
    

class SafariPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    group_size_min = models.IntegerField()
    group_size_max = models.IntegerField()
    picture = models.ImageField(upload_to='safari_packages/')


class Booking(models.Model):
    safari_package = models.ForeignKey(SafariPackage, on_delete=models.CASCADE)
    start_date = models.DateField()
    participants = models.IntegerField()
    special_requirements = models.TextField(blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    