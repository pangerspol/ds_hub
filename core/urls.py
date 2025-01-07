from django.urls import path
from .views import RequestCreateView

urlpatterns = [
    path('add-request/', RequestCreateView.as_view(), name='add-request'),
]