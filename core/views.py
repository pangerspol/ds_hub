from rest_framework import generics
from .models import Client, CustomUser, Location, CustomGroup, Provider
from .serializers import ClientSerializer, CustomUserSerializer, LocationSerializer, CustomGroupSerializer, ProviderSerializer

# Client Views
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# CustomUser Views
class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# CustomGroup Views
class CustomGroupListCreateView(generics.ListCreateAPIView):
    queryset = CustomGroup.objects.all()
    serializer_class = CustomGroupSerializer

class CustomGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomGroup.objects.all()
    serializer_class = CustomGroupSerializer

# Location Views
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# Provider Views
class ProviderListCreateView(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ProviderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    
    