from django.urls import path
from . import views
from .views import RequestCreateView

urlpatterns = [
    path('', views.home, name='home'),
    path('add-request/', RequestCreateView.as_view(), name='add-request'),
]