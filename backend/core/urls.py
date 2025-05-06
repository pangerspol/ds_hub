from django.urls import path
from . import views
from .views import (
    ClientListCreateView, ClientDetailView,
    CustomUserListCreateView, CustomUserDetailView,
    LocationListCreateView, LocationDetailView,
    CustomGroupListCreateView, CustomGroupDetailView,
    ProviderListCreateView, ProviderDetailView,
)

urlpatterns = [

    # Client URLs
    path('clients/', ClientListCreateView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),

    # CustomUser URLs
    path('users/', CustomUserListCreateView.as_view(), name='user_list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user_detail'),

    # CustomGroup URLs
    path('groups/', CustomGroupListCreateView.as_view(), name='group_list'),
    path('groups/<int:pk>/', CustomGroupDetailView.as_view(), name='group_detail'),

    # Location URLs
    path('locations/', LocationListCreateView.as_view(), name='location_list'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location_detail'),

    # Provider URLs
    path('provider/', ProviderListCreateView.as_view(), name='provider_list'),
    path('provider/<int:pk>/', ProviderDetailView.as_view(), name='provider_detail'),

    
]