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

class ReservationSerializer(serializers.ModelSerializer):
    date = serializers.DateField(
        format="%Y-%m-%d",
        input_formats=['%Y-%m-%d'],  # Liste des formats acceptés en entrée
        help_text="Format de date attendu : YYYY-MM-DD"
    )
    meal = serializers.SlugRelatedField(
        queryset=MealType.objects.all(),
        slug_field='name'    # Utilise le champ 'name' pour la création/mise à jour
    )
    restaurant = serializers.SlugRelatedField(
        queryset=Restaurant.objects.all(),
        slug_field='name'
    )
    
    # Remplacer le champ client existant par un CharField
    # En lecture on retourne uniquement client_name
    # En creation on attend `client` dans lequel on mettre le nom du client
    client = serializers.CharField(write_only=True, required=True)
    client_name = serializers.CharField(source='client.name', read_only=True)

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
        Valider que le client existe et appartient à l'utilisateur courant
        """
        request = self.context.get('request')
        try:
            client = Client.objects.get(name=value, user=request.user)
            return client
        except Client.DoesNotExist:
            raise serializers.ValidationError(
                "Client non trouvé (ou n'appartenant pas à l'utilisateur courant)"
            )
    
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
