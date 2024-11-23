from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    apikey = models.CharField(max_length=100, unique=True, blank=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    opening_hours = models.CharField(max_length=200)  # Could be JSON field for more complex schedules
    location = models.CharField(max_length=100)  # Location within the hotel
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MealType(models.Model):
    """Breakfast, Lunch, Dinner, etc."""
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    category = models.CharField(max_length=50)  # Appetizer, Main Course, Dessert, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DailyMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)
    date = models.DateField()
    items = models.ManyToManyField(MenuItem, through='DailyMenuItem')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['restaurant', 'meal_type', 'date']

    def __str__(self):
        return f"{self.restaurant} - {self.meal_type} - {self.date}"

class DailyMenuItem(models.Model):
    """Junction model for DailyMenu and MenuItem with additional fields"""
    daily_menu = models.ForeignKey(DailyMenu, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    special_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_special = models.BooleanField(default=False)

class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=10, null=True, blank=True)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (for {self.user})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reservations')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='client_id', related_name='reservations')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.restaurant} - {self.date} {self.time}"