from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, permissions
from django_filters import rest_framework as filters
from .serializers import RestaurantSerializer, ClientSerializer, ReservationSerializer, MealTypeSerializer, SpaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from hotel_california_app.models import Restaurant, Client, Reservation, MealType,Spa

class RestaurantListAPIView(generics.ListAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]    
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class ClientListAPIView(generics.ListAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientSerializer

    # Limit the results to the current user
    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

class MealTypeListAPIView(generics.ListAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    queryset = MealType.objects.all()
    serializer_class = MealTypeSerializer

class ReservationFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Reservation
        fields = ['restaurant', 'meal', 'date_from', 'date_to']

class ReservationListCreateView(generics.ListCreateAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer
    filterset_class = ReservationFilter

    def get_queryset(self):
        """Return reservations for the current user"""
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the reservation with the current user"""
        serializer.save(
            user=self.request.user,
            client=serializer.validated_data['client']  # Le client est déjà validé
        )

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        """Ensure users can only access their own reservations"""
        return Reservation.objects.filter(user=self.request.user)

class SpaListAPI(APIView):
    def get(self, request):
        spas = Spa.objects.all()
        serializer = SpaSerializer(spas, many=True)
        return Response(serializer.data)
