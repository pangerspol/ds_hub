from django.urls import path
from .views import (
    MedicalRecordListCreateView, MedicalRecordDetailView,
    UploadDocumentView
)

urlpatterns = [
# MedicalRecord URLs
    path('medical-records/', MedicalRecordListCreateView.as_view(), name='medical_record_list'),
    path('medical-records/<int:pk>/', MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('upload-document/', UploadDocumentView.as_view(), name='upload-document'),
]