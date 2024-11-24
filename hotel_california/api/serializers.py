from rest_framework import serializers
from hotel_california_app.models import Restaurant, Client, Spa

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'capacity', 'opening_hours', 'location', 'is_active']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone_number', 'room_number', 'special_requests']

class SpaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spa
        fields = '__all__'