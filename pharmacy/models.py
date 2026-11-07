from django.db import models
from django.contrib.auth.models import User

class Pharmacy(models.Model):
    HIGHWAY_CHOICES = [
        ('NH-65', 'NH-65'),
        ('NH-16', 'NH-16'),
        ('NH-44', 'NH-44'),
    ]
    name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200)
    address = models.TextField(default="Main Road")
    highway = models.CharField(max_length=20, choices=HIGHWAY_CHOICES, default='NH-65')
    distance = models.CharField(max_length=20, default="500m")
    phone = models.CharField(max_length=15, blank=True, default='')
    email = models.EmailField(blank=True)
    is_open_24 = models.BooleanField(default=True, verbose_name="24/7 Open")
    opening_time = models.CharField(max_length=20, default="9:00 AM")
    closing_time = models.CharField(max_length=20, default="10:00 PM")
    rating = models.FloatField(default=4.5)
    latitude = models.CharField(max_length=20, blank=True)
    longitude = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.name} - {self.highway}"

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('Tablet', 'Tablet'),
        ('Syrup', 'Syrup'),
        ('Injection', 'Injection'),
        ('Capsule', 'Capsule'),
    ]
    name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Tablet')
    price = models.IntegerField()
    stock = models.IntegerField(default=10)
    expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    pharmacies = models.ManyToManyField(Pharmacy, related_name='medicines')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    medicine_name = models.CharField(max_length=100)
    highway = models.CharField(max_length=20, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine_name} - {self.highway}"