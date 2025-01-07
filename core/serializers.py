from rest_framework import serializers
from .models import Request

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'case_number', 'client_name', 'paralegal', 'office', 'created_at'] #could have used '__all__' instead of listing all fields