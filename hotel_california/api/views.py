from rest_framework import generics, permissions
from .serializers import RestaurantSerializer, ClientSerializer, SpaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from hotel_california_app.models import Restaurant, Client,Spa

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

class SpaListAPI(APIView):
    def get(self, request):
        spas = Spa.objects.all()
        serializer = SpaSerializer(spas, many=True)
        return Response(serializer.data)