from rest_framework import serializers
from hotel_california_app.models import Restaurant, Client, Reservation, MealType, Spa

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'capacity', 'opening_hours', 'location', 'is_active']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone_number', 'room_number', 'special_requests']

class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = ['id', 'name']

class SpaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spa
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    number_of_guests = serializers.IntegerField(
        min_value=1,
        max_value=100,
        help_text="Nombre de convives (entre 1 et 100)"
    )
    date = serializers.DateField(
        format="%Y-%m-%d",
        input_formats=['%Y-%m-%d'],  # Liste des formats acceptés en entrée
        help_text="Format de date attendu : YYYY-MM-DD"
    )

    class Meta:
        model = Reservation
        fields = ['id', 'client', 'restaurant', 'date',
                  'meal', 'number_of_guests', 'special_requests']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Vérification de l'existence du contexte et de la requête
        if self.context and 'request' in self.context and self.context['request']:
            user = self.context['request'].user
            self.fields['client'].queryset = Client.objects.filter(user=user)
        else:
            # Fallback pour la génération du schéma
            self.fields['client'].queryset = Client.objects.all()

    def validate(self, data):
        # Add custom validation here
        # 'number_of_guests' is not always present because of partial updates
        if 'number_of_guests' in data and data['number_of_guests'] <= 0:
            raise serializers.ValidationError("Number of guests must be positive")
        return data
