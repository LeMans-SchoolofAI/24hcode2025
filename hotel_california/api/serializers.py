from rest_framework import serializers
from hotel_california_app.models import Restaurant, Client, Reservation, MealType

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'capacity', 'opening_hours', 'location', 'is_active']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone_number', 'room_number', 'special_requests']

class ReservationSerializer(serializers.ModelSerializer):
    meal = serializers.SlugRelatedField(
        queryset=MealType.objects.all(),
        slug_field='name'    # Utilise le champ 'name' pour la création/mise à jour
    )
    restaurant = serializers.SlugRelatedField(
        queryset=Restaurant.objects.all(),
        slug_field='name'
    )
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.none())
    meal = serializers.PrimaryKeyRelatedField(queryset=MealType.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['client'].queryset = Client.objects.filter(user=user)

    class Meta:
        model = Reservation
        fields = ['id', 'client', 'client_name', 'restaurant', 'date',
                  'meal', 'number_of_guests', 'special_requests']
    
    def validate_client(self, value):
        """
        Check that the client belongs to the current user
        """
        request = self.context.get('request')
        if value.user != request.user:
            raise serializers.ValidationError(
                "You can only make reservations for your own clients"
            )
        return value
    
    def validate_restaurant(self, value):
        if not Restaurant.objects.filter(name=value, is_active=True).exists():
            raise serializers.ValidationError(
                "Ce restaurant n'existe pas ou n'est pas actif"
            )
        return value
    
    def validate(self, data):
        # Add custom validation here
        if data['number_of_guests'] <= 0:
            raise serializers.ValidationError("Number of guests must be positive")
        return data
