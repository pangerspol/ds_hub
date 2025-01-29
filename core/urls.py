from django.urls import path
from .views import (
    ClientListCreateView, ClientDetailView,
    EntryTypeListCreateView, EntryTypeDetailView,
    StatusListCreateView, StatusDetailView,
    MedicalRecordListCreateView, MedicalRecordDetailView,
    CustomUserListCreateView, CustomUserDetailView,
    LocationListCreateView, LocationDetailView,
    CustomGroupListCreateView, CustomGroupDetailView
)

urlpatterns = [

    # Client URLs
    path('clients/', ClientListCreateView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),

    # EntryType URLs
    path('entry-types/', EntryTypeListCreateView.as_view(), name='entry_type_list'),
    path('entry-types/<int:pk>/', EntryTypeDetailView.as_view(), name='entry_type_detail'),

    # Status URLs
    path('statuses/', StatusListCreateView.as_view(), name='status_list'),
    path('statuses/<int:pk>/', StatusDetailView.as_view(), name='status_detail'),

    # MedicalRecord URLs
    path('medical-records/', MedicalRecordListCreateView.as_view(), name='medical_record_list'),
    path('medical-records/<int:pk>/', MedicalRecordDetailView.as_view(), name='medical_record_detail'),

    # CustomUser URLs
    path('users/', CustomUserListCreateView.as_view(), name='user_list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user_detail'),

    # CustomGroup URLs
    path('groups/', CustomGroupListCreateView.as_view(), name='group_list'),
    path('groups/<int:pk>/', CustomGroupDetailView.as_view(), name='group_detail'),

    # Location URLs
    path('locations/', LocationListCreateView.as_view(), name='location_list'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location_detail'),
    
]