from rest_framework import generics, permissions
from .serializers import RestaurantSerializer, ClientSerializer
from hotel_california_app.models import Restaurant, Client

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

