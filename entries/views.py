from rest_framework import generics
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from integrations.services import SharePointManager

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

# MedicalRecord Views
class MedicalRecordListCreateView(generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

# Upload Document View
class UploadDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Allows file uploads

    # Define allowed document types per entry type
    DOCUMENT_TYPES = {
        "medicalrecord": {
            "invoice": "invoice_path",
            "approval": "approval_path",
            "receipt": "receipt_path",
            "record": "record_path",
            "expense": "expense_path",
            "package": "package_path"
        },
    }

    def post(self, request, *args, **kwargs):
        # Validate request data
        if 'file' not in request.FILES or 'entry_id' not in request.data or 'entry_type' not in request.data or 'document_type' not in request.data:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        entry_id = request.data['entry_id']
        entry_type = request.data['entry_type'].lower()
        document_type = request.data['document_type'].lower()

        # Get the model dynamically
        entry_model_map = {
            "medicalrecord": MedicalRecord,
        }

        if entry_type not in entry_model_map:
            return Response({"error": "Invalid entry type"}, status=status.HTTP_400_BAD_REQUEST)

        entry_model = entry_model_map[entry_type]

        # Validate entry instance
        try:
            entry_instance = entry_model.objects.get(id=entry_id)
        except entry_model.DoesNotExist:
            return Response({"error": f"{entry_type} not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate document type
        if entry_type not in self.DOCUMENT_TYPES or document_type not in self.DOCUMENT_TYPES[entry_type]:
            return Response({"error": f"Invalid document type '{document_type}' for entry type '{entry_type}'"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get the correct field name for the document type
        document_field = self.DOCUMENT_TYPES[entry_type][document_type]

        # Ensure the entry has a SharePoint temp folder ID
        if not entry_instance.temp_folder_id:
            return Response({"error": "Entry does not have a SharePoint temporary folder ID"}, status=status.HTTP_400_BAD_REQUEST)

        manager = SharePointManager()
        manager.authenticate()

        # Upload the file to SharePoint
        sharepoint_folder_id = entry_instance.temp_folder_id
        sharepoint_file_url = manager.upload_file_to_sharepoint(file, sharepoint_folder_id, document_type)

        if not sharepoint_file_url:
            return Response({"error": "Failed to upload file to SharePoint"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Store the SharePoint file path in the correct model field
        setattr(entry_instance, document_field, sharepoint_file_url)
        entry_instance.save()

        return Response({
            "message": f"{document_type.replace('_', ' ').title()} uploaded successfully",
            "file_url": sharepoint_file_url
        }, status=status.HTTP_201_CREATED)



