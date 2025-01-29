from rest_framework import generics
from .models import Client, EntryType, Status, MedicalRecord, CustomUser, Location, CustomGroup
from .serializers import ClientSerializer, EntryTypeSerializer, StatusSerializer, MedicalRecordSerializer, CustomUserSerializer, LocationSerializer, CustomGroupSerializer
from decouple import config

# Create your views here.

# Client Views
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# EntryType Views
class EntryTypeListCreateView(generics.ListCreateAPIView):
    queryset = EntryType.objects.all()
    serializer_class = EntryTypeSerializer

class EntryTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntryType.objects.all()
    serializer_class = EntryTypeSerializer

# Status Views
class StatusListCreateView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class StatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

# MedicalRecord Views
class MedicalRecordListCreateView(generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

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

    
    