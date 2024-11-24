from rest_framework import serializers
from hotel_california_app.models import Restaurant, Client, Reservation

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'capacity', 'opening_hours', 'location', 'is_active']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone_number', 'room_number', 'special_requests']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'client', 'restaurant', 'date', 'meal', 
                 'number_of_guests', 'special_requests']
        
    def validate(self, data):
        # Add custom validation here
        if data['number_of_guests'] <= 0:
            raise serializers.ValidationError("Number of guests must be positive")
        return data
