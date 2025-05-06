from rest_framework import serializers
from .models.medical_record import MedicalRecord
from core.serializers import ClientSerializer, CustomUserSerializer, LocationSerializer, CustomGroupSerializer, ProviderSerializer

class MedicalRecordSerializer(serializers.ModelSerializer):

    client = ClientSerializer(read_only=True)
    provider = ProviderSerializer(read_only=True)
    #location = LocationSerializer(read_only=True)
    custom_user = CustomUserSerializer(read_only=True)
    #custom_group = CustomGroupSerializer(read_only=True)

    class Meta:
        model = MedicalRecord
        fields = '__all__'