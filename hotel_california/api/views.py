from rest_framework import generics, permissions
from django_filters import rest_framework as filters
from .serializers import RestaurantSerializer, ClientSerializer, ReservationSerializer
from hotel_california_app.models import Restaurant, Client, Reservation

class RestaurantListAPIView(generics.ListAPIView):
    # Only a authenticated user can see the restaurants
    permission_classes = [permissions.IsAuthenticated]    
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class ClientListAPIView(generics.ListAPIView):
    # Only a authenticated user can see the clients list
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientSerializer

    # Limit the results to the current user
    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

class ReservationFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Reservation
        fields = ['restaurant', 'meal', 'date_from', 'date_to']

class ReservationListCreateView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ReservationFilter

    def get_queryset(self):
        """Return reservations for the current user"""
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the reservation with the current user"""
        serializer.save(user=self.request.user)

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Ensure users can only access their own reservations"""
        return Reservation.objects.filter(user=self.request.user)
