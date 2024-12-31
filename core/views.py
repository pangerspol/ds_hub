from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Request
from .serializer import RequestSerializer
from .onedrive import OneDriveManager

class RequestCreateView(APIView):
    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            saved_request = serializer.save()

            onedrive = OneDriveManager(
                client_id=os.environ.get("CLIENT_ID"),
                client_secret=os.environ.get("CLIENT_SECRET"),
                tenant_id=os.environ.get("TENANT_ID")
            )
            onedrive.authenticate()
            folder_name = f"request_{saved_request.case_number}_{saved_request.client_name}"
            folder_response = onedrive.create_folder("", folder_name)

            print(folder_response)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return HttpResponse("Hello, welcome to Dressler Strickland Hub!")

# Create your views here.
