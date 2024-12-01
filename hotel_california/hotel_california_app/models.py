from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from watson import search as watson
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField(
        validators=[
            MinValueValidator(1, message="La capacité doit être d'au moins 1"),
            MaxValueValidator(250, message="La capacité ne peut pas dépasser 250")
        ]
    )
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=10, null=True, blank=True)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (for {self.user})"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='client_id', related_name='reservations')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    meal = models.ForeignKey(MealType, on_delete=models.CASCADE)
    number_of_guests = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Le nombre de convives doit être d'au moins 1"),
            MaxValueValidator(100, message="Le nombre de convives ne peut pas dépasser 100")
        ]
    )
    special_requests = models.TextField(blank=True)

    def __str__(self):
        return f"{self.client} - {self.restaurant} - {self.date} {self.meal}"
class Spa(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Enregistrer le modèle pour la recherche
watson.register(Client, fields=("name", "phone_number"))

# Déclaration des signaux automatiques pour la mise en oeuvre de la recherche floue
@receiver(post_save, sender=Client)
def update_search_index(sender, instance, **kwargs):
    watson.default_search_engine.update_obj_index(instance)

@receiver(post_delete, sender=Client)
def remove_from_search_index(sender, instance, **kwargs):
    watson.default_search_engine.remove_obj_index(instance)
